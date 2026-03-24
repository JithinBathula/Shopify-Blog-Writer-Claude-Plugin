#!/usr/bin/env python3
"""
Generate a photorealistic blog featured image using Nano Banana 2
(Google Gemini 3.1 Flash Image Preview) via the OpenRouter API.

Usage:
    python generate_image.py \
        --prompt "A photorealistic image of..." \
        --output /path/to/output.png \
        --env-file /path/to/.env \
        --aspect-ratio 3:2 \
        --size 2K

Returns JSON to stdout:
    {
        "success": true,
        "image_path": "/path/to/output.png",
        "base64_data": "iVBORw0KGgo...",
        "model": "google/gemini-3.1-flash-image-preview"
    }

API Reference (OpenRouter + Nano Banana 2):
    Endpoint:   POST https://openrouter.ai/api/v1/chat/completions
    Model:      google/gemini-3.1-flash-image-preview
    Modalities: ["image", "text"]

    image_config options:
        aspect_ratio: 1:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16, 21:9, 5:4, 4:5
        image_size:   0.5K, 1K, 2K, 4K

    Response contains base64 PNG in:
        choices[0].message.images[0].image_url.url
        (prefixed with "data:image/png;base64,")

    Pricing: Input $0.25/M tokens, Output $1.50/M tokens, Image $60/M tokens

    Error codes:
        400 = bad request (check payload)
        401 = invalid API key (must start with sk-or-v1-)
        402 = insufficient credits
        429 = rate limited (wait and retry)
        500 = server error (retry once)

    Timeout: Image generation takes 15-60 seconds. Use 120s timeout.
"""

import argparse
import base64
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


MODEL = "google/gemini-3.1-flash-image-preview"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_ASPECT_RATIO = "3:2"
DEFAULT_SIZE = "2K"
TIMEOUT_SECONDS = 120
MAX_RETRIES = 2


def load_env(env_path):
    """Load environment variables from a .env file."""
    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars


def generate_image(api_key, prompt, aspect_ratio=DEFAULT_ASPECT_RATIO, image_size=DEFAULT_SIZE):
    """
    Call the OpenRouter API to generate a photorealistic image.

    Returns the raw base64 image data (without the data URL prefix).
    Raises on failure after retries.
    """
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": aspect_ratio,
            "image_size": image_size,
        },
        "stream": False,
    }

    json_data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(ENDPOINT, data=json_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                result = json.loads(response.read().decode("utf-8"))

            # Extract base64 image from response
            images = result.get("choices", [{}])[0].get("message", {}).get("images", [])
            if not images:
                raise ValueError(
                    "No image returned in API response. "
                    "The prompt may not have clearly requested a visual scene."
                )

            data_url = images[0]["image_url"]["url"]
            # Strip the "data:image/png;base64," prefix
            if "," in data_url:
                b64_data = data_url.split(",", 1)[1]
            else:
                b64_data = data_url

            return b64_data

        except urllib.error.HTTPError as e:
            last_error = e
            status = e.code
            if status == 429 and attempt < MAX_RETRIES:
                # Rate limited — wait and retry
                time.sleep(2 ** (attempt + 1))
                continue
            elif status == 500 and attempt < MAX_RETRIES:
                # Server error — retry once
                time.sleep(1)
                continue
            else:
                error_body = ""
                try:
                    error_body = e.read().decode("utf-8", errors="replace")
                except Exception:
                    pass
                raise RuntimeError(
                    f"OpenRouter API error {status}: {error_body}"
                ) from e

        except urllib.error.URLError as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            raise RuntimeError(f"Network error: {e.reason}") from e

    raise RuntimeError(f"Failed after {MAX_RETRIES + 1} attempts. Last error: {last_error}")


def main():
    parser = argparse.ArgumentParser(description="Generate a blog featured image via OpenRouter API.")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output PNG file path")
    parser.add_argument("--env-file", required=True, help="Path to .env file with OPENROUTER_API_KEY")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO, help="Image aspect ratio (default: 3:2)")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Image size: 0.5K, 1K, 2K, 4K (default: 2K)")

    args = parser.parse_args()

    # Load API key
    env_path = Path(args.env_file)
    if not env_path.exists():
        print(json.dumps({"success": False, "error": f".env file not found: {env_path}"}))
        sys.exit(1)

    env_vars = load_env(env_path)
    api_key = env_vars.get("OPENROUTER_API_KEY")
    if not api_key:
        print(json.dumps({"success": False, "error": "OPENROUTER_API_KEY not found in .env file"}))
        sys.exit(1)

    # Generate
    try:
        b64_data = generate_image(api_key, args.prompt, args.aspect_ratio, args.size)
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img_bytes = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    result = {
        "success": True,
        "image_path": str(output_path.resolve()),
        "base64_data": b64_data,
        "model": MODEL,
        "file_size_bytes": len(img_bytes),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
