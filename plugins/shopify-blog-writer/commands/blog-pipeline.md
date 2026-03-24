---
description: Run the blog creation pipeline — draft, image, upload to Shopify
allowed-tools: Read, Write, Edit, Bash, Agent, Glob, Grep, WebFetch
argument-hint: [all|next|<number>]
---

Run the blog creation pipeline. This orchestrates the full workflow: read the Excel tracker → draft the blog post → generate a featured image → upload to Shopify → update the tracker.

## Arguments

- No argument or `next` → process the **next** pending blog (one post)
- `all` → process **all** pending/planned blogs sequentially
- A number (e.g., `3`) → process that many blogs from the queue

## Step 1: Read the Tracker

Run the tracker script to find the next eligible row:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/read_tracker.py \
  --tracker "Blog Articles/blog-tracker.xlsx" \
  --action next
```

The script returns JSON with all row data including the content brief columns (format, target_keyword, hidden_intent, key_arguments, strategic_rationale, gap_type, product_tie_in, recommended_word_count, recommended_structure, publishing_priority).

If `"found": false`, inform the user the queue is empty and stop.

If a row is found, immediately mark it as in-progress:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/read_tracker.py \
  --tracker "Blog Articles/blog-tracker.xlsx" \
  --action set-status \
  --row <row_index> \
  --status in-progress
```

## Step 2: Draft the Blog Post

Load the **company-info** and **blog-drafting** skills, then draft the article:

1. Read the company-info skill for website URL, product catalog, and brand voice
2. Read product dossiers from the workspace folder (`.docx` and `.pdf` files relevant to the topic)
3. Fetch the website for current product URLs, pricing, and availability
4. Use the content brief from the tracker row to draft the post:
   - **Title and length** from the core columns (recommended_word_count overrides length if present)
   - **Target keywords** from target_keyword (first keyword before " / " is primary, rest are secondary). If blank, derive from the title.
   - **Format** determines the article template (Comparison, Ranked list, How-to guide, Topic guide)
   - **Hidden Intent** — the introduction must directly address this emotional state
   - **Key Arguments** — mandatory content beats, every one must appear in the article body
   - **Strategic Rationale and Gap Type** — context for how aggressively to position the brand
   - **Product Tie-In** — which products to feature and hyperlink
   - **Recommended Structure** — follow this structural blueprint directly
   - If any brief columns are blank, infer from the title and company-info skill
5. Write the full blog post as HTML following the blog-drafting skill guidelines
6. Generate SEO metadata: meta title, meta description, URL slug, and tags
7. Save the HTML to the working directory

## Step 3: Generate the Featured Image

Spawn the **image-generator** agent to handle this autonomously. Pass it:
- The blog title
- The blog HTML content (or a summary of the key themes)
- The primary keyword
- The path to the `.env` file in the workspace

The agent will craft a photorealistic prompt, call `scripts/generate_image.py`, generate alt text, and return the image file path, base64 data, and alt text.

## Step 4: Upload to Shopify

Once the draft and image are ready, spawn the **shopify-uploader** agent. Pass it:
- The blog title, author, and HTML content
- SEO metadata (seo_title, meta_description, handle, tags)
- A short summary_html for the blog listing page
- The image base64 data and alt text from Step 3
- The path to the `.env` file
- Whether to publish immediately (the pipeline default is `published: true`)

The agent will assemble the payload, call `scripts/upload_to_shopify.py`, and return the Shopify article ID and handle.

## Step 5: Update the Tracker

Once the upload succeeds, update the tracker row:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/read_tracker.py \
  --tracker "Blog Articles/blog-tracker.xlsx" \
  --action update \
  --row <row_index> \
  --status done \
  --shopify-id <article_id> \
  --shopify-url <handle>
```

## Step 6: Report Results

Tell the user:
- Blog title that was processed
- The Shopify article ID and URL
- How many pending items remain (from the tracker script's `remaining` count)

## Error Handling

If any step fails (drafting, image generation, or upload), reset the tracker row to its previous status:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/read_tracker.py \
  --tracker "Blog Articles/blog-tracker.xlsx" \
  --action set-status \
  --row <row_index> \
  --status pending
```

Then report the error to the user. Never leave a row stuck in `in-progress`.

If the `.env` file is missing or credentials are invalid, stop immediately and ask the user to set up credentials.

## Processing Multiple Posts

If the user passed `all` or a number:
1. Process each post sequentially — complete the full pipeline for one post before starting the next
2. Report progress after each post
3. If one post fails, report the error and continue to the next
4. At the end, give a summary of all posts processed (successes and failures)
