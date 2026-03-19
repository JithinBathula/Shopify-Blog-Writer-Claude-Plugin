# OpenRouter Image Generation API Reference

Complete reference for generating images via the OpenRouter API using Nano Banana 2.

## Model

**Model ID:** `google/gemini-3.1-flash-image-preview`
**Name:** Nano Banana 2 (Gemini 3.1 Flash Image Preview)
**Provider:** Google AI Studio via OpenRouter
**Context length:** 65,536 tokens
**Input:** Text and image
**Output:** Text and image

### Pricing
- Input tokens: $0.25/M tokens
- Output tokens: $1.50/M tokens
- Image output: $60/M tokens

## Endpoint

```
POST https://openrouter.ai/api/v1/chat/completions
```

## Authentication

```
Authorization: Bearer sk-or-v1-your-key-here
Content-Type: application/json
```

API keys are obtained from openrouter.ai → Settings → API Keys.

## Request Body

```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [
    {
      "role": "user",
      "content": "Your image generation prompt here"
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

### Parameters

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `model` | Yes | `google/gemini-3.1-flash-image-preview` | Nano Banana 2 model ID |
| `messages` | Yes | Array | Standard chat messages format |
| `modalities` | Yes | `["image", "text"]` | Must include "image" for generation |
| `image_config` | No | Object | Image generation settings |
| `stream` | No | `false` | Set false for complete response |

### image_config Options

| Field | Values | Default | Description |
|-------|--------|---------|-------------|
| `aspect_ratio` | `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`, `5:4`, `4:5` | `1:1` | Image aspect ratio |
| `image_size` | `0.5K`, `1K`, `2K`, `4K` | `1K` | Output resolution |

**For blog images, always use:**
- `aspect_ratio`: `"3:2"` — landscape format ideal for blog headers
- `image_size`: `"2K"` — good balance of quality and generation speed

## Response Format

```json
{
  "id": "gen-xxx",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's the image I generated...",
        "images": [
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
            }
          }
        ]
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 1200,
    "total_tokens": 1250
  }
}
```

### Extracting the Image

1. Access `choices[0].message.images[0].image_url.url`
2. This is a data URL: `data:image/png;base64,{BASE64_DATA}`
3. Split on `,` and take the second part to get raw base64
4. Decode base64 to get binary PNG data

```python
import base64

data_url = result["choices"][0]["message"]["images"][0]["image_url"]["url"]
b64_data = data_url.split(",", 1)[1]
img_bytes = base64.b64decode(b64_data)
```

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Success | Parse response |
| 400 | Bad request | Check payload format |
| 401 | Invalid API key | Verify key starts with `sk-or-v1-` |
| 402 | Insufficient credits | Top up OpenRouter account |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry once |

### Common Issues

- **No images in response:** The model may return text-only if the prompt doesn't clearly request an image. Make sure the prompt describes a visual scene.
- **Timeout:** Image generation can take 15-60 seconds. Set timeout to at least 120 seconds.
- **Stylized output:** If the image looks like a cartoon or illustration, strengthen the anti-style directive in the prompt.

## Connecting to Shopify

The base64 image data can be passed directly to Shopify's article API:

```json
{
  "article": {
    "title": "Blog Post Title",
    "body_html": "<p>Content...</p>",
    "image": {
      "attachment": "RAW_BASE64_WITHOUT_DATA_URL_PREFIX",
      "alt": "Descriptive alt text for SEO and accessibility"
    }
  }
}
```

**Important:** The `attachment` field takes raw base64 data (without the `data:image/png;base64,` prefix). Strip the prefix before sending to Shopify.
