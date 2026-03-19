# Shopify Blog Writer

An end-to-end Shopify blog pipeline plugin for Claude — draft posts from an Excel tracker with detailed content briefs, generate AI featured images, and upload everything to your store.

## What It Does

- **Draft** blog posts from an Excel tracker with full content briefs (target keywords, hidden intent, key arguments, recommended structure)
- **Generate** photorealistic featured images using AI (Nano Banana 2 via OpenRouter)
- **Upload** articles with images to your Shopify store via the Admin API
- **Track** progress in an Excel spreadsheet with automatic status updates

## Install

### In Claude Desktop (Cowork)

1. Open **Settings** > **Customize** > **Browse plugins**
2. Go to the **Personal** tab
3. Click **Add marketplace**
4. Enter: `JithinBathula/Shopify-Blog-Writer-Claude-Plugin`
5. Click **Sync**
6. Find **Shopify Blog Writer** in the marketplace and click **Install**

### In Claude Code (CLI)

```bash
# Add the marketplace
/plugin marketplace add JithinBathula/Shopify-Blog-Writer-Claude-Plugin

# Install the plugin
/plugin install shopify-blog-writer@jithinbathula-shopify-blog-writer-claude-plugin
```

## Setup

After installing, tell Claude:

> "Set up my brand" or "Configure the plugin" or "Initialize the blog writer"

This walks you through everything in one conversation:

1. **Company & Products** — your brand name, website URL, and product catalog
2. **Brand Voice** — tone, audience, language style, differentiators
3. **Credentials** — Shopify API keys and OpenRouter API key (saved to `.env`)
4. **Blog Tracker** — creates your `blog-tracker.xlsx` with all 18 columns
5. **Product Documents** — identifies dossiers, spec sheets, or reference files in your workspace

After setup, you're ready to run `/blog-pipeline` immediately.

To update settings later, just say "update my brand setup" — you can change individual fields without redoing everything.

### Credentials You'll Need

- **Shopify:** Go to partners.shopify.com > your app > Settings. The app needs `write_content` scope. Copy the Client ID and Client Secret.
- **OpenRouter:** Go to openrouter.ai > Settings > API Keys. Create a key (starts with `sk-or-v1-`). Used for AI image generation.

The setup skill will ask for these and save them to a `.env` file in your workspace.

## Usage

### Run the Blog Pipeline

The main way to use this plugin. Add rows to your Excel tracker, then run:

- `/blog-pipeline` — process the next pending blog
- `/blog-pipeline all` — process all pending blogs sequentially
- `/blog-pipeline 3` — process 3 blogs from the queue

The pipeline reads your tracker, picks the next row by Publishing Priority, drafts the post, generates a featured image, uploads to Shopify, and marks the row as done.

### Write a Blog Post (standalone)

- "Write a blog post about our new product launch"
- "Draft a Shopify blog about choosing the right product for beginners"

### Generate a Featured Image (standalone)

- "Generate a featured image for this blog post"
- "Create a hero image for the latest article"

### Upload to Shopify (standalone)

- "Upload this blog post to Shopify"
- "Push this article to the store"

## Architecture

| Component | Type | Purpose |
|-----------|------|---------|
| **brand-setup** | Skill | Complete plugin setup — company info, credentials, tracker, product docs |
| **company-info** | Skill | Brand knowledge — product catalog, website URL, brand voice guidelines |
| **blog-drafting** | Skill | Writing expertise — SEO rules, format templates, content brief interpretation |
| **blog-pipeline** | Command | Orchestrator — reads tracker, coordinates drafting/image/upload, updates status |
| **image-generator** | Agent | Autonomous image creation — analyzes blog, crafts prompt, calls API |
| **shopify-uploader** | Agent | Autonomous upload — assembles payload, pushes to Shopify API |

Three Python scripts handle deterministic work (API calls, Excel read/write):

| Script | What It Does |
|--------|-------------|
| `scripts/read_tracker.py` | Read next eligible row, update status, mark done |
| `scripts/generate_image.py` | Call OpenRouter API, extract base64 PNG, save to disk |
| `scripts/upload_to_shopify.py` | Authenticate with Shopify, upload article with image and SEO metadata |

## The Excel Tracker

The pipeline is driven by a `blog-tracker.xlsx` file. Each row is a blog post.

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
| **Product Tie-In** | Which products and bundles to feature |
| **Recommended Word Count** | Target word count (overrides Length if both present) |
| **Recommended Structure** | Structural blueprint for the article |
| **Publishing Priority** | Numeric priority (1 = publish first) |

The content brief columns are optional but produce much better results when filled in. Add a row with at minimum **Title**, **Author**, and **Status** = `pending` or `planned`.

## License

MIT
