---
name: blog-image-gen
description: >
  This skill should be used when the user asks to "generate a blog image",
  "create a featured image for a blog post", "make a hero image",
  "generate an image for Shopify blog", "create blog visuals", or needs
  a realistic, professional featured image for a blog article. Uses
  Nano Banana 2 via OpenRouter to generate photorealistic images.
---

# Blog Image Generation

Generate realistic, professional featured images for Shopify blog posts using Nano Banana 2 (Gemini 3.1 Flash Image Preview) via the OpenRouter API.

## Credentials

Load the OpenRouter API key from a `.env` file in the user's working folder.

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Loading order:**
1. Check for `.env` in the same directory as blog content
2. Check the workspace root folder
3. If not found, ask the user for their API key

## Image Requirements

All blog images must meet these standards:

- **Aspect ratio:** Always 3:2 (landscape orientation, ideal for blog headers)
- **Style:** Photorealistic — never cartoon, illustration, anime, or stylized. The image should look like a professional photograph or a high-end stock photo.
- **Resolution:** Request 2K or 4K from the API for crisp display on retina screens
- **Content:** Relevant to the blog topic, visually appealing, suitable for a health/wellness brand

## Workflow

### Step 1: Analyse the Blog Post

Read the blog post content (title, topic, key themes) and determine what kind of image would work best as the featured hero image. Consider:

- The main subject of the article (e.g., supplements, wellness, collagen, fitness)
- The tone (educational, aspirational, clinical, lifestyle)
- What would make someone click when they see it on the blog listing page

### Step 2: Craft the Image Prompt

Write a detailed prompt for Nano Banana 2 that produces a **photorealistic** result. Every prompt must include these elements:

1. **Subject description** — what's in the image
2. **Style directive** — always include: "photorealistic, professional photography, high resolution, natural lighting"
3. **Anti-style directive** — always include: "Do not create cartoon, illustrated, animated, or stylized images. The image must look like a real photograph."
4. **Composition** — describe framing, depth of field, angle
5. **Mood/atmosphere** — warm, clean, clinical, energetic, serene, etc.
6. **Colour palette** — should align with the brand or topic

**Example prompt for a wellness supplement blog:**
```
A clean, modern flat lay photograph of various wellness supplement sachets arranged on a white marble countertop, with fresh fruits (mango, apple, strawberry) and a glass of water nearby. Soft natural morning light from a window, shallow depth of field. Photorealistic, professional product photography, high resolution, natural lighting. Do not create cartoon, illustrated, animated, or stylized images. The image must look like a real photograph. Warm, inviting colour tones with clean white and natural accents.
```

**Example prompt for a bone and joint health blog:**
```
A photorealistic image of an active woman in her 50s stretching outdoors in a park during golden hour, looking healthy and energetic. She is wearing tasteful athletic wear and smiling naturally. The background shows soft green trees and warm sunlight. Professional lifestyle photography, high resolution, natural lighting, shallow depth of field. Do not create cartoon, illustrated, animated, or stylized images. The image must look like a real photograph.
```

### Step 3: Call the OpenRouter API

**Endpoint:** `POST https://openrouter.ai/api/v1/chat/completions`

**Request body:**
```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": "YOUR_IMAGE_PROMPT_HERE"
    }
  ],
  "modalities": ["image", "text"],
  "image_config": {
    "aspect_ratio": "3:2",
    "image_size": "2K"
  },
  "stream": false
}
```

**Key parameters:**
- `model` — always `google/gemini-3.1-flash-image-preview` (Nano Banana 2)
- `modalities` — always `["image", "text"]`
- `image_config.aspect_ratio` — always `"3:2"`
- `image_config.image_size` — `"2K"` for standard, `"4K"` for high quality

**Response format:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Description text...",
        "images": [
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,iVBORw0KGgoAAAANSUh..."
            }
          }
        ]
      }
    }
  ]
}
```

The image is returned as a **base64-encoded PNG data URL** in `choices[0].message.images[0].image_url.url`.

### Step 4: Extract and Save the Image

1. Parse the base64 data from the response (strip the `data:image/png;base64,` prefix)
2. Decode the base64 string to binary
3. Save as a PNG file alongside the blog HTML file
4. Name the file to match the blog: e.g., `blog6-wellness-supplements-worth-it-2026.png`

### Step 5: Generate Alt Text

Create descriptive alt text for the image that:
- Describes what's visible in the image
- Includes the primary keyword from the blog post naturally
- Is under 125 characters
- Is useful for screen readers and SEO

**Example:** `"Wellness supplements and fresh fruits arranged on a marble countertop in natural light"`

## Connecting to Shopify Upload

Once the image is generated and saved, pass this information to the **shopify-upload** skill:

- **Image file path** — the saved PNG file
- **Alt text** — the generated description
- **Base64 data** — the raw base64 string (Shopify accepts base64 directly via the `image.attachment` field)

The Shopify article API accepts images as base64 in the `image` field:
```json
{
  "article": {
    "title": "...",
    "body_html": "...",
    "image": {
      "attachment": "BASE64_IMAGE_DATA_WITHOUT_PREFIX",
      "alt": "Descriptive alt text with keyword"
    }
  }
}
```

## Writing the Image Generation Script

Use Python with only standard library modules (`urllib.request`, `json`, `os`, `base64`, `pathlib`). No pip installs required.

```python
import urllib.request
import json
import base64
from pathlib import Path

def generate_blog_image(api_key, prompt, output_path):
    """Generate a blog image using Nano Banana 2 via OpenRouter."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "google/gemini-3.1-flash-image-preview",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": "3:2",
            "image_size": "2K"
        },
        "stream": False
    }
    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    # Extract base64 image
    images = result["choices"][0]["message"].get("images", [])
    if not images:
        raise ValueError("No image returned in response")

    data_url = images[0]["image_url"]["url"]
    # Strip prefix: "data:image/png;base64,"
    b64_data = data_url.split(",", 1)[1]

    # Save to file
    img_bytes = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    return b64_data  # Return base64 for Shopify upload
```

See `references/openrouter-api.md` for full API details and error handling.

## Prompt Tips for Photorealism

- Always lead with a concrete scene description, not abstract concepts
- Mention specific lighting: "soft natural window light", "golden hour sunlight", "studio lighting"
- Include camera-like terms: "shallow depth of field", "85mm lens", "wide-angle shot"
- Mention textures and materials: "marble countertop", "wooden table", "linen backdrop"
- For people: describe age range, activity, and expression rather than specific individuals
- Never use brand names or logos in the prompt — the image should be generic enough for any blog
- End every prompt with the anti-style directive to prevent stylized outputs
