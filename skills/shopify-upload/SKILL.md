---
name: shopify-upload
description: >
  This skill should be used when the user asks to "upload to Shopify",
  "publish a blog post to Shopify", "push articles to the store",
  "upload blog to Shopify", "post to Shopify", or needs to send
  drafted blog content to their Shopify store via the Admin API.
---

# Upload Blog Posts to Shopify

Upload blog articles to a Shopify store as **hidden (unpublished) drafts** via the Shopify Admin REST API, with full SEO metadata.

## Prerequisites

Before uploading, confirm the user has:

1. **Shopify credentials** — via a `.env` file (see Credentials section below)
2. **Blog post content** — HTML file(s) ready to upload
3. **SEO metadata** — title, SEO title, meta description, tags, handle, author, and optionally a scheduled publish date

If any of these are missing, ask the user to provide them before proceeding.

## Credentials

Load Shopify credentials from a `.env` file in the user's working folder. Look for a file named `.env` in the same directory as the blog articles or in the workspace root.

The `.env` file should contain:

```
SHOPIFY_STORE_URL=yourstore.myshopify.com
SHOPIFY_CLIENT_ID=your-client-id
SHOPIFY_CLIENT_SECRET=your-client-secret
```

**Loading order:**
1. First, check for a `.env` file in the same directory as the blog HTML files / metadata
2. If not found, check the workspace root folder
3. If still not found, ask the user to provide credentials or create a `.env` file

**Reading the `.env` file in Python:**

```python
from pathlib import Path

def load_env(env_path):
    """Load environment variables from a .env file."""
    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars
```

**Security rules:**
- Never hardcode credentials in scripts
- Never print the full Client Secret — mask it in any output (e.g., show only last 4 characters)
- Never commit `.env` files to version control
- Credentials loaded from `.env` are used only for the current upload session

## Important Rules

- **Do NOT include the post title in the HTML body.** Shopify renders the title separately on the page, so including it in `body_html` causes a duplicate heading. Strip any leading `<h1>` tag from the HTML before uploading.
- **All posts are uploaded as hidden (unpublished) by default.** Set `"published": false` in every API call. The user can publish manually from Shopify Admin when ready.
- **Never hardcode or log credentials.** Use environment variables or ask the user to provide them at runtime. Mask secrets in any output.

## Upload Workflow

### Step 1: Authenticate

Use the Shopify Client Credentials Grant flow to get a temporary access token.

```
POST https://{store_url}/admin/oauth/access_token
Content-Type: application/json

{
  "client_id": "{client_id}",
  "client_secret": "{client_secret}",
  "grant_type": "client_credentials"
}
```

The response contains an `access_token` valid for approximately 24 hours.

### Step 2: Discover the Blog ID

Fetch the list of blogs on the store and select the appropriate one (usually the first/default blog).

```
GET https://{store_url}/admin/api/2024-01/blogs.json
X-Shopify-Access-Token: {access_token}
```

If the store has multiple blogs, ask the user which one to target.

### Step 3: Prepare Each Article

For each article to upload, build the payload:

```json
{
  "article": {
    "title": "The article title",
    "author": "Author Name",
    "body_html": "<p>Article HTML content — no <h1> title</p>",
    "tags": "tag1, tag2, tag3",
    "handle": "url-slug-for-the-post",
    "summary_html": "<p>Short summary for blog listing page</p>",
    "published": false,
    "image": {
      "attachment": "RAW_BASE64_IMAGE_DATA",
      "alt": "Descriptive alt text with primary keyword"
    },
    "metafields": [
      {
        "namespace": "global",
        "key": "title_tag",
        "value": "SEO Title Under 60 Characters",
        "type": "single_line_text_field"
      },
      {
        "namespace": "global",
        "key": "description_tag",
        "value": "Meta description under 155 characters with target keyword.",
        "type": "single_line_text_field"
      }
    ]
  }
}
```

**Key fields:**

| Field | Purpose | Notes |
|-------|---------|-------|
| `title` | Article title displayed on the page | Do NOT repeat in body_html |
| `body_html` | Full article content | Strip any leading `<h1>` tag |
| `published` | Visibility | Always `false` — hidden by default |
| `published_at` | Optional scheduled date | ISO 8601 format with timezone |
| `handle` | URL slug | Lowercase, hyphenated, keyword-focused |
| `tags` | Comma-separated tags | Used for filtering and organization |
| `summary_html` | Excerpt for blog listing | Keep under 200 words |
| `image` | Featured image | Object with `attachment` (raw base64, no prefix) and `alt` (descriptive text with keyword) |
| `metafields` | SEO title and meta description | Use `global` namespace with `title_tag` and `description_tag` keys |

### Featured Image

If a featured image is available (generated via the **blog-image-gen** skill or provided by the user), include it in the article payload using the `image` field:

```json
"image": {
  "attachment": "RAW_BASE64_WITHOUT_DATA_URL_PREFIX",
  "alt": "Descriptive alt text including the primary keyword"
}
```

**Important rules for images:**
- The `attachment` field takes **raw base64 data only** — strip the `data:image/png;base64,` prefix before sending
- Always include an `alt` field with a descriptive text that includes the blog's primary keyword naturally
- Alt text should be under 125 characters and describe what's visible in the image
- If no image is available, omit the `image` field entirely — don't send an empty object

### Step 4: Upload via API

```
POST https://{store_url}/admin/api/2024-01/blogs/{blog_id}/articles.json
Content-Type: application/json
X-Shopify-Access-Token: {access_token}
```

Send each article payload to this endpoint. Add a 0.5-second delay between requests to respect rate limits.

### Step 5: Report Results

After all uploads, provide a summary:

- Number of successful uploads vs failures
- Article ID and handle for each success
- Error details for any failures
- Remind the user to review drafts in Shopify Admin → Online Store → Blog posts

## Writing the Upload Script

When creating the upload script, use Python with only standard library modules (`urllib.request`, `json`, `os`, `sys`, `time`, `pathlib`). No pip installs required.

Load credentials from a `.env` file in the user's working directory (see the Credentials section above). Fall back to environment variables if no `.env` file is found.

See `references/api-reference.md` for the full Shopify Admin API details and error handling patterns.

## Metadata Format

When working with a batch of articles, use a JSON metadata file structured like this:

```json
{
  "blog_articles": [
    {
      "file": "blog1-article-slug.html",
      "title": "Article Title Here",
      "seo_title": "SEO Title Under 60 Chars",
      "handle": "article-url-slug",
      "meta_description": "Meta description under 155 characters.",
      "summary": "Short summary for the blog listing page.",
      "tags": "tag1, tag2, tag3",
      "author": "Author Name",
      "scheduled_date": "2026-03-03T09:00:00+08:00"
    }
  ]
}
```

Each entry maps to one article. The `file` field points to the HTML content file relative to the metadata JSON.
