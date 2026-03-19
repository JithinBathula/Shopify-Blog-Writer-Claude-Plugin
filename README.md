# Shopify Blog Writer

An end-to-end Shopify blog pipeline plugin — draft posts from an Excel tracker with detailed content briefs, generate AI featured images, and upload everything to your store.

## What It Does

- **Draft** blog posts from an Excel tracker with full content briefs (target keywords, hidden intent, key arguments, recommended structure)
- **Generate** photorealistic featured images using AI (Nano Banana 2 via OpenRouter)
- **Upload** articles with images to your Shopify store via the Admin API
- **Track** progress in an Excel spreadsheet with automatic status updates

## Architecture

This plugin uses the right component type for each job:

| Component | Type | Purpose |
|-----------|------|---------|
| **company-info** | Skill | Brand knowledge — product catalog, website URL, brand voice guidelines |
| **blog-drafting** | Skill | Writing expertise — SEO rules, format templates, content brief interpretation |
| **blog-pipeline** | Command | Orchestrator — reads tracker, coordinates drafting/image/upload, updates status |
| **image-generator** | Agent | Autonomous image creation — analyzes blog, crafts prompt, calls API |
| **shopify-uploader** | Agent | Autonomous upload — assembles payload, pushes to Shopify API |

Three Python scripts handle all deterministic work (API calls, Excel read/write):

| Script | What It Does |
|--------|-------------|
| `scripts/read_tracker.py` | Read next eligible row, update status, mark done |
| `scripts/generate_image.py` | Call OpenRouter API, extract base64 PNG, save to disk |
| `scripts/upload_to_shopify.py` | Authenticate with Shopify, upload article with image and SEO metadata |

## Usage

### Run the Blog Pipeline

The main way to use this plugin. Add rows to your Excel tracker, then run:

- `/blog-pipeline` — process the next pending blog
- `/blog-pipeline all` — process all pending blogs sequentially
- `/blog-pipeline 3` — process 3 blogs from the queue

The pipeline reads from `Blog Articles/blog-tracker.xlsx`, picks the next row by Publishing Priority, drafts the post, generates a featured image, uploads to Shopify, and marks the row as done.

### Write a Blog Post (standalone)

Ask Claude to write a blog post and it will load the company-info and blog-drafting skills automatically:

- "Write a blog post about collagen for joint health"
- "Draft a Shopify blog about recovery supplements for athletes"

### Generate a Featured Image (standalone)

Ask Claude to generate a featured image and the image-generator agent handles it:

- "Generate a featured image for this blog post"
- "Create a hero image for the wellness article"

### Upload to Shopify (standalone)

Ask Claude to upload and the shopify-uploader agent handles it:

- "Upload this blog post to Shopify"
- "Push this article to the store"

## The Excel Tracker

The pipeline is driven by `Blog Articles/blog-tracker.xlsx`. Each row is a blog post.

### Core Columns

| Column | Description |
|--------|-------------|
| **#** | Row number |
| **Title** | Blog post title |
| **Author** | Author name |
| **Length** | short / standard / medium-form / long-form |
| **Status** | planned / pending / in-progress / done |
| **Shopify ID** | Article ID (filled by pipeline) |
| **Shopify URL** | URL handle (filled by pipeline) |
| **Completed Date** | Date processed (filled by pipeline) |

### Content Brief Columns (optional)

| Column | Description |
|--------|-------------|
| **Format** | Comparison, Ranked list, How-to guide, Topic guide |
| **Target Keyword** | Primary and secondary SEO keywords (separated by " / ") |
| **Gap Type** | Content gap: Competitive, Audience, Depth, Timing |
| **Strategic Rationale** | Why this article matters for the brand |
| **Hidden Intent** | The emotional undercurrent driving the searcher |
| **Key Arguments** | Mandatory talking points (must all appear in the article) |
| **Product Tie-In** | Which products and protocol bundles to feature |
| **Recommended Word Count** | Target word count (overrides Length if both present) |
| **Recommended Structure** | Structural blueprint for the article |
| **Publishing Priority** | Numeric priority (1 = publish first) |

### Adding New Blog Ideas

Add a row with at minimum: **Title**, **Author**, and **Status** = `pending` or `planned`. The content brief columns are optional but produce much better results when filled in.

## Setup

### Credentials

Add these to a `.env` file in your working folder:

```
# Shopify (for uploading posts)
SHOPIFY_STORE_URL=yourstore.myshopify.com
SHOPIFY_CLIENT_ID=your-client-id
SHOPIFY_CLIENT_SECRET=your-client-secret

# OpenRouter (for image generation)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Where to get these:**
- Shopify credentials: partners.shopify.com → your app → Settings (app must have `write_content` scope)
- OpenRouter API key: openrouter.ai → Settings → API Keys

### Product Dossiers

Place your product dossier documents (`.docx`, `.pdf`) in your workspace folder. The blog-drafting skill will automatically discover and read them when writing content related to those products.

### Dependencies

The scripts use only Python standard library modules (`urllib.request`, `json`, `base64`, `pathlib`, `argparse`). The only external dependency is `openpyxl` for Excel file handling:

```bash
pip install openpyxl
```
