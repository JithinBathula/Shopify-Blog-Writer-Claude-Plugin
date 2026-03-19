# Shopify Admin API Reference for Blog Articles

Detailed API patterns for uploading and managing blog articles via the Shopify Admin REST API.

## Authentication: Client Credentials Grant

This is the authentication method for apps created through the Shopify Partners Dev Dashboard.

### Request

```
POST https://{store}.myshopify.com/admin/oauth/access_token
Content-Type: application/json

{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "grant_type": "client_credentials"
}
```

### Response

```json
{
  "access_token": "shpca_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "scope": "write_content,read_content"
}
```

The token is temporary (valid ~24 hours). Request a new one for each upload session.

### Required Scopes

The app must have `write_content` (and ideally `read_content`) scope configured in the Shopify Partners dashboard.

### Troubleshooting Auth Failures

| HTTP Code | Cause | Fix |
|-----------|-------|-----|
| 401 | Invalid credentials | Double-check Client ID and Secret |
| 403 | Missing scope | Add `write_content` in Partners dashboard, reinstall app |
| 404 | Wrong store URL | Verify the `.myshopify.com` domain |

## Blog Discovery

### List All Blogs

```
GET https://{store}.myshopify.com/admin/api/2024-01/blogs.json
X-Shopify-Access-Token: {token}
```

Response contains an array of blog objects with `id`, `title`, and `handle`.

Most stores have a single blog (commonly titled "News" or "All"). Use the first blog ID unless the user specifies otherwise.

## Article Creation

### Create a Hidden Article

```
POST https://{store}.myshopify.com/admin/api/2024-01/blogs/{blog_id}/articles.json
Content-Type: application/json
X-Shopify-Access-Token: {token}
```

### Full Payload

```json
{
  "article": {
    "title": "Article Title",
    "author": "Author Name",
    "body_html": "<p>Article content here. Do NOT include an h1 title.</p>",
    "tags": "tag1, tag2, tag3",
    "handle": "url-slug-lowercase-hyphenated",
    "summary_html": "<p>Short excerpt for blog listing.</p>",
    "published": false,
    "published_at": "2026-03-03T09:00:00+08:00",
    "metafields": [
      {
        "namespace": "global",
        "key": "title_tag",
        "value": "SEO Title Tag",
        "type": "single_line_text_field"
      },
      {
        "namespace": "global",
        "key": "description_tag",
        "value": "SEO meta description for search results.",
        "type": "single_line_text_field"
      }
    ]
  }
}
```

### Key Behaviors

- **`published: false`** — creates a hidden draft. The article won't be visible on the storefront.
- **`published_at`** — sets a scheduled publish date but does NOT auto-publish. The user must manually publish or use Shopify's scheduling feature.
- **`handle`** — becomes the URL slug at `/blogs/{blog-handle}/{article-handle}`. Keep it short, keyword-focused, and lowercase with hyphens.
- **`metafields`** with `global` namespace and `title_tag`/`description_tag` keys — these set the SEO title and meta description visible in search results.

### Successful Response

```json
{
  "article": {
    "id": 1234567890,
    "title": "Article Title",
    "handle": "url-slug",
    "created_at": "2026-03-03T09:00:00+08:00",
    "published_at": null,
    "body_html": "...",
    "blog_id": 9876543210,
    "author": "Author Name",
    "tags": "tag1, tag2, tag3"
  }
}
```

## Error Handling

### Common API Errors

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200/201 | Success | Article created |
| 401 | Token expired or invalid | Re-authenticate |
| 403 | Insufficient scope | Check app permissions |
| 404 | Blog not found | Verify blog ID |
| 422 | Validation error | Check payload (duplicate handle, missing title) |
| 429 | Rate limited | Wait and retry after `Retry-After` header |

### Rate Limiting

Shopify allows approximately 2 requests per second for REST API calls. Add a 0.5-second delay between article uploads to stay well within limits.

If you receive a 429 response, read the `Retry-After` header and wait that many seconds before retrying.

## Removing the Title from body_html

Since Shopify renders the article title as an `<h1>` on the page automatically, the HTML body must NOT contain the title again. Before uploading, strip any leading `<h1>` element:

### Python Pattern

```python
import re

def strip_leading_h1(html):
    """Remove the first <h1>...</h1> tag if it appears at the start of the content."""
    return re.sub(r'^\s*<h1[^>]*>.*?</h1>\s*', '', html, count=1, flags=re.IGNORECASE | re.DOTALL)
```

Apply this to every `body_html` before sending it to the API.

## API Version

Use `2024-01` or later. Shopify maintains backward compatibility within a version for 12 months. Check the Shopify changelog for the latest stable version.
