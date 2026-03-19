---
name: blog-pipeline
description: >
  Orchestrates the full blog creation pipeline — from idea to published Shopify post —
  driven by an Excel tracker file. Use when the user asks to "run the blog pipeline",
  "process the next blog", "create the next blog post from the tracker",
  "run the blog queue", or "process pending blogs".
---

# Blog Pipeline Orchestrator

Automates the entire blog creation workflow by reading from an Excel tracker spreadsheet. Each run picks up the next pending blog idea, drafts it, generates a featured image, uploads it to Shopify, and marks it done in the tracker.

## The Excel Tracker

The pipeline is driven by an Excel file located in the user's workspace at:

```
Blog Articles/blog-tracker.xlsx
```

### Tracker Columns

#### Core Columns (original)

| Column | Description | Filled By |
|--------|-------------|-----------|
| **#** | Row number | Pre-filled |
| **Title** | Blog post title or topic idea | User |
| **Author** | Author name for the post | User |
| **Length** | "short" (400-600), "standard" (800-1200), "medium-form" (1000-1500), or "long-form" (1500-2500) | User |
| **Status** | `planned` / `pending` / `in-progress` / `done` | Pipeline |
| **Shopify ID** | Article ID after upload | Pipeline |
| **Shopify URL** | Full URL handle after upload | Pipeline |
| **Completed Date** | Date the pipeline finished processing | Pipeline |

#### Content Brief Columns (optional but powerful)

These columns provide a detailed content brief for each article. When populated, they give the blog-drafting skill precise creative direction — the target keywords to optimize for, the emotional angle to take, the specific arguments to make, and the structure to follow. When blank, the pipeline falls back to inferring these from the title and company-info skill.

| Column | Description | How It's Used |
|--------|-------------|---------------|
| **Format** | Article format — e.g. "Comparison", "Ranked list", "How-to guide", "Topic guide", "Topic guide / Comparison (Pillar)" | Determines the writing template and structural approach. A "Comparison" gets a decision table up front; a "Ranked list" gets numbered items with H3s; a "How-to guide" gets step-by-step protocol sections. |
| **Target Keyword** | Primary SEO keyword(s) — may include multiple separated by " / " | Passed directly to the blog-drafting skill as the primary and secondary keywords. The first keyword before the slash is the primary; the rest are secondary. These drive title optimization, H2 placement, and keyword density. |
| **Gap Type** | Content gap this article fills — e.g. "Competitive gap", "Audience gap", "Depth gap + Timing gap" | Provides strategic context so the draft understands *why* this article exists. A "Competitive gap" means competitors own this topic and the article needs to outperform them. An "Audience gap" means this is an underserved reader segment. |
| **Strategic Rationale** | Why this article matters for the brand — business context that informs tone and angle | Read by the drafting skill to understand the strategic stakes. This shapes how aggressively the article positions the brand, whether it should be defensive or offensive, and what the core narrative tension is. |
| **Hidden Intent** | The emotional undercurrent or unspoken question the searcher really has | This is arguably the most important brief column. It tells the drafting skill what the reader is *actually* feeling when they search this topic — skepticism, fear, decision fatigue, frustration. The introduction and framing should directly address this emotional state. |
| **Key Arguments** | Numbered list of core arguments, claims, or talking points to cover | These are the mandatory content beats. Every argument listed here should appear in the article body. The drafting skill should treat these as a checklist — if an argument is listed, it must be covered. |
| **Product Tie-In** | Which BeMe products and protocol bundles to feature and link | Tells the drafting skill which products to hyperlink and where to place CTAs. "Full range" means mention all four products; specific products (e.g. "BUILD, Bulletproof Protocol") mean focus the product mentions on those. |
| **Recommended Word Count** | Target word count — overrides the Length column if both are present | When present, this is the target length. If this says 1400 and Length says "long-form" (1500-2500), use 1400. |
| **Recommended Structure** | Suggested article structure — e.g. "Comparison table early, then 3-4 H2 sections with evidence, FAQ block at end" | A direct instruction to the drafting skill about how to organize the article. Follow this structure unless it conflicts with the content. |
| **Publishing Priority** | Numeric priority (1 = publish first) | Used to determine queue order when multiple rows are pending/planned. |

### How Users Add New Blog Ideas

Users simply add a new row to the tracker with at minimum:
- **Title** — the blog topic or title
- **Author** — who the post should be attributed to
- **Status** — set to `pending` or `planned`

All other fields are optional — the pipeline will use sensible defaults:
- **Length**: If blank, defaults to "long-form"
- **Recommended Word Count**: If present, takes precedence over the Length column

When the content brief columns (Format through Recommended Structure) are populated, the pipeline passes them directly to the blog-drafting skill as a structured creative brief. This means the drafting skill doesn't need to infer keywords, tone, structure, or product focus — it's all spelled out. When these columns are blank, the pipeline falls back to determining keywords, target audience, and tone automatically from the blog title and the company-info skill.

## Pipeline Workflow

When this skill is triggered, follow these steps exactly:

### Step 1: Read the Tracker

1. Open `Blog Articles/blog-tracker.xlsx` from the user's workspace folder using openpyxl
2. Find all rows where the Status column = `pending` or `planned`
3. If no eligible rows exist, inform the user that the queue is empty and stop
4. **Select the next row to process:** If a Publishing Priority column exists and has values, pick the row with the lowest priority number. Otherwise, pick the first eligible row by row order.
5. Extract **all** column values for that row — including the content brief columns (Format, Target Keyword, Gap Type, Strategic Rationale, Hidden Intent, Key Arguments, Product Tie-In, Recommended Word Count, Recommended Structure) if they exist and are populated
6. Update the Status to `in-progress` and save the file immediately (so it reflects current state)

### Step 2: Draft the Blog Post

Follow the **blog-drafting** skill workflow, passing along the content brief from the tracker:

1. **Load company context** — Read the `company-info` skill to get website URL, product catalog, and brand voice
2. **Read product dossiers** — List the workspace folder and read all `.docx` and `.pdf` files relevant to the blog topic
3. **Fetch the website** — Get current product URLs, pricing, and availability from the company website
4. **Build the creative brief** — Assemble the drafting inputs from the tracker row:
   - **Title and length** from the core columns (Recommended Word Count overrides Length if present)
   - **Target keywords** from the Target Keyword column (first keyword = primary, rest = secondary). If blank, derive from the title.
   - **Format** from the Format column — this determines the article template (see blog-drafting skill for format-specific structures)
   - **Hidden Intent** — pass this to the drafting skill so the introduction directly addresses the reader's emotional state
   - **Key Arguments** — these are mandatory content beats that must all appear in the article body
   - **Strategic Rationale and Gap Type** — provide these as context so the drafting skill understands the strategic angle
   - **Product Tie-In** — which products to feature and hyperlink
   - **Recommended Structure** — the specific structural blueprint to follow
   - If any of these columns are blank, the drafting skill infers them from the title and company-info skill as before
5. **Draft the post** — Write the full blog post as HTML:
   - Follow the Recommended Structure if provided; otherwise use the blog-drafting default: Title → Introduction → Body Sections → Conclusion + CTA → SEO Metadata
   - Hyperlink every product mention to real product URLs
   - Do NOT include placeholder image tags
   - Ground claims in product dossier data
   - Cover every Key Argument listed in the tracker
6. **Generate SEO metadata** — meta title, meta description, URL slug, and tags
7. **Save the HTML** to the working directory for the next steps

### Step 3: Generate the Featured Image

Follow the **blog-image-gen** skill workflow:

1. Analyze the blog post content to determine an appropriate image concept
2. Craft a detailed photorealistic image prompt (include subject, style directive, anti-style directive, composition, mood, color palette)
3. Load the OpenRouter API key from the `.env` file in `Blog Articles/`
4. Call the OpenRouter API with model `google/gemini-3.1-flash-image-preview`, aspect ratio `3:2`, size `2K`
5. Extract the base64 image from the response and save as PNG
6. Generate alt text (under 125 characters, includes primary keyword)

### Step 4: Upload to Shopify

Follow the **shopify-upload** skill workflow:

1. Load Shopify credentials from the `.env` file in `Blog Articles/`
2. Authenticate via Client Credentials Grant to get an access token
3. Fetch the blog ID (use the first/default blog)
4. Build the article payload:
   - `title`: From the tracker row
   - `author`: From the tracker row
   - `body_html`: The drafted HTML (strip any leading `<h1>` — Shopify renders the title separately)
   - `handle`: The URL slug from SEO metadata
   - `tags`: From SEO metadata
   - `summary_html`: A short excerpt for the blog listing page
   - `image`: The generated image as base64 with alt text
   - `metafields`: SEO title and meta description
   - **Visibility:** Always set `published: true` so the post is immediately visible on the store
5. Upload via POST to the Shopify Admin API
6. Capture the returned article ID and handle

### Step 5: Update the Tracker

1. Open `Blog Articles/blog-tracker.xlsx` again with openpyxl
2. Find the row that was being processed (match by title or row number)
3. Update the following columns:
   - **Status** → `done`
   - **Shopify ID** → the article ID returned from the API
   - **Shopify URL** → the full handle/URL path
   - **Completed Date** → today's date
4. Save the Excel file

### Step 6: Report Results

Provide a summary to the user:
- Blog title that was processed
- The Shopify article ID and URL
- How many pending items remain in the tracker queue

## Error Handling

- If any step fails (drafting, image generation, or upload), set the tracker Status back to `pending` and report the error to the user
- Do NOT leave a row stuck in `in-progress` — always reset to `pending` on failure so it can be retried
- If the `.env` file is missing or credentials are invalid, stop immediately and ask the user to set up credentials

## Processing Multiple Posts

By default, the pipeline processes **one post per run**. If the user asks to "process all pending blogs" or "run the full queue", process each pending row sequentially — completing the full pipeline for one post before starting the next. Report progress after each post.

## Dependencies

This skill orchestrates the following skills (read their SKILL.md files for detailed instructions):

- `company-info` — Company context, product catalog, brand voice
- `blog-drafting` — Blog post writing with SEO optimization
- `blog-image-gen` — Photorealistic featured image generation
- `shopify-upload` — Shopify Admin API article upload
