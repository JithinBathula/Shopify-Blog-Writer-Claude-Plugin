#!/usr/bin/env python3
"""
Upload a blog article to Shopify via the Admin REST API.

Usage:
    python upload_to_shopify.py \
        --env-file /path/to/.env \
        --payload /path/to/article-payload.json

    python upload_to_shopify.py \
        --env-file /path/to/.env \
        --payload /path/to/article-payload.json \
        --published

The payload JSON file should have this structure:
    {
        "title": "Article Title",
        "author": "Author Name",
        "body_html": "<p>HTML content — no leading <h1></p>",
        "handle": "url-slug",
        "tags": "tag1, tag2, tag3",
        "summary_html": "<p>Short excerpt</p>",
        "seo_title": "SEO Title Under 60 Characters",
        "meta_description": "Meta description under 155 characters.",
        "image_base64": "RAW_BASE64_DATA_WITHOUT_PREFIX",
        "image_alt": "Descriptive alt text"
    }

Returns JSON to stdout:
    {
        "success": true,
        "article_id": 662924853496,
        "handle": "collagen-for-bone-health",
        "url": "https://store.myshopify.com/blogs/news/collagen-for-bone-health"
    }

Shopify Admin API Reference:
    Auth:       POST https://{store}/admin/oauth/access_token (Client Credentials Grant)
    List blogs: GET  https://{store}/admin/api/2024-01/blogs.json
    Create art: POST https://{store}/admin/api/2024-01/blogs/{blog_id}/articles.json

    The access_token from Client Credentials Grant is valid ~24 hours.
    Rate limit: 0.5s delay between requests recommended.

    Article payload fields:
        title, author, body_html, tags, handle, summary_html, published, image, metafields
    Image format:
        {"attachment": "RAW_BASE64_NO_PREFIX", "alt": "description"}
    Metafields for SEO:
        namespace=global, key=title_tag or description_tag, type=single_line_text_field

    Important:
        - Do NOT include <h1> in body_html — Shopify renders the title separately
        - image.attachment is raw base64 (strip "data:image/png;base64," prefix)
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


API_VERSION = "2024-01"


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


def api_request(url, headers, data=None, method="GET"):
    """Make an HTTP request and return parsed JSON response."""
    json_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def authenticate(store_url, client_id, client_secret):
    """Get an access token via Shopify Client Credentials Grant."""
    url = f"https://{store_url}/admin/oauth/access_token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/json"}

    try:
        result = api_request(url, headers, payload, method="POST")
        token = result.get("access_token")
        if not token:
            raise ValueError(f"No access_token in response: {json.dumps(result)[:200]}")
        return token
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise RuntimeError(f"Authentication failed (HTTP {e.code}): {error_body}") from e


def get_blog_id(store_url, access_token):
    """Fetch the first/default blog ID from the store."""
    url = f"https://{store_url}/admin/api/{API_VERSION}/blogs.json"
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json",
    }

    result = api_request(url, headers)
    blogs = result.get("blogs", [])
    if not blogs:
        raise RuntimeError("No blogs found on the store. Create one in Shopify Admin first.")
    return blogs[0]["id"]


def upload_article(store_url, access_token, blog_id, payload_data, published=False):
    """Upload a single article to Shopify."""
    url = f"https://{store_url}/admin/api/{API_VERSION}/blogs/{blog_id}/articles.json"
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json",
    }

    # Build the article payload
    article = {
        "title": payload_data["title"],
        "author": payload_data.get("author", ""),
        "body_html": payload_data["body_html"],
        "published": published,
    }

    # Optional fields
    if payload_data.get("handle"):
        article["handle"] = payload_data["handle"]
    if payload_data.get("tags"):
        article["tags"] = payload_data["tags"]
    if payload_data.get("summary_html"):
        article["summary_html"] = payload_data["summary_html"]

    # Featured image
    if payload_data.get("image_base64"):
        b64 = payload_data["image_base64"]
        # Strip data URL prefix if present
        if "," in b64 and b64.startswith("data:"):
            b64 = b64.split(",", 1)[1]
        article["image"] = {
            "attachment": b64,
            "alt": payload_data.get("image_alt", ""),
        }

    # SEO metafields
    metafields = []
    if payload_data.get("seo_title"):
        metafields.append({
            "namespace": "global",
            "key": "title_tag",
            "value": payload_data["seo_title"],
            "type": "single_line_text_field",
        })
    if payload_data.get("meta_description"):
        metafields.append({
            "namespace": "global",
            "key": "description_tag",
            "value": payload_data["meta_description"],
            "type": "single_line_text_field",
        })
    if metafields:
        article["metafields"] = metafields

    try:
        result = api_request(url, headers, {"article": article}, method="POST")
        art = result.get("article", {})
        return {
            "success": True,
            "article_id": art.get("id"),
            "handle": art.get("handle"),
            "url": f"https://{store_url}/blogs/{blog_id}/{art.get('handle', '')}",
        }
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body[:500]}",
        }


def main():
    parser = argparse.ArgumentParser(description="Upload a blog article to Shopify.")
    parser.add_argument("--env-file", required=True, help="Path to .env file with Shopify credentials")
    parser.add_argument("--payload", required=True, help="Path to article payload JSON file")
    parser.add_argument("--published", action="store_true", default=False,
                        help="Publish immediately (default: hidden draft)")
    parser.add_argument("--blog-id", type=int, help="Specific blog ID (auto-discovers first blog if omitted)")

    args = parser.parse_args()

    # Load credentials
    env_path = Path(args.env_file)
    if not env_path.exists():
        print(json.dumps({"success": False, "error": f".env file not found: {env_path}"}))
        sys.exit(1)

    env_vars = load_env(env_path)
    store_url = env_vars.get("SHOPIFY_STORE_URL")
    client_id = env_vars.get("SHOPIFY_CLIENT_ID")
    client_secret = env_vars.get("SHOPIFY_CLIENT_SECRET")

    if not all([store_url, client_id, client_secret]):
        missing = [k for k, v in {"SHOPIFY_STORE_URL": store_url, "SHOPIFY_CLIENT_ID": client_id,
                                    "SHOPIFY_CLIENT_SECRET": client_secret}.items() if not v]
        print(json.dumps({"success": False, "error": f"Missing in .env: {', '.join(missing)}"}))
        sys.exit(1)

    # Load payload
    payload_path = Path(args.payload)
    if not payload_path.exists():
        print(json.dumps({"success": False, "error": f"Payload file not found: {payload_path}"}))
        sys.exit(1)

    with open(payload_path) as f:
        payload_data = json.load(f)

    # Authenticate
    try:
        access_token = authenticate(store_url, client_id, client_secret)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Authentication failed: {e}"}))
        sys.exit(1)

    # Get blog ID
    try:
        blog_id = args.blog_id or get_blog_id(store_url, access_token)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Failed to get blog ID: {e}"}))
        sys.exit(1)

    # Upload
    result = upload_article(store_url, access_token, blog_id, payload_data, published=args.published)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
