# Shopify Blog Writer

A plugin that covers the full Shopify blog workflow — drafting posts, generating featured images, and uploading everything to your store.

## What It Does

- **Draft** blog posts optimized for SEO and conversions, informed by product dossiers and live website data
- **Generate** photorealistic featured images using AI (Nano Banana 2 via OpenRouter)
- **Upload** articles with images to your Shopify store as hidden drafts via the Admin API

## Components

### Skills

| Skill | What It Does | Trigger Phrases |
|-------|-------------|----------------|
| **company-info** | Central source of company context — website URL, product catalog, dossier locations, and brand voice | "what products do we have", "show me company info", "list our product catalog" |
| **blog-drafting** | Draft blog posts with SEO metadata, informed by product dossiers and website | "write a blog post", "draft a Shopify blog", "create blog content" |
| **blog-image-gen** | Generate realistic 3:2 featured images for blog posts | "generate a blog image", "create a featured image", "make a hero image" |
| **shopify-upload** | Upload articles with images to Shopify as hidden drafts | "upload to Shopify", "publish blog to Shopify", "push articles to the store" |
| **blog-pipeline** | Full orchestrator — reads Excel tracker, drafts, generates image, uploads, marks done | "run the blog pipeline", "process the next blog", "run the blog queue" |

### How Skills Work Together

The **company-info** skill acts as the shared knowledge base. When **blog-drafting** is triggered, it first loads company-info to discover product dossiers in the workspace, fetch the website for current product URLs and pricing, and apply brand voice guidelines. This means blog content is always grounded in real product data and links to live product pages.

The **blog-pipeline** skill ties everything together. It reads from an Excel tracker spreadsheet (`Blog Articles/blog-tracker.xlsx`), picks the next pending blog idea, and runs the full pipeline automatically: drafting → image generation → Shopify upload → update tracker. Add new rows to the spreadsheet, run the pipeline, and your blog posts are created end-to-end.

## Usage

### Writing a Blog Post

Ask Claude to write a blog post and it will automatically:
1. Load company context (website, product catalog, brand voice)
2. Read relevant product dossiers from your workspace for scientific claims and details
3. Fetch the live website for current product URLs and pricing
4. Guide you through providing the right details (topic, audience, keywords, tone)
5. Draft a complete post with SEO metadata and real product hyperlinks

**Example prompts:**
- "Write a blog post about summer skincare routines for our beauty store"
- "Draft a buying guide for standing desks"

### Generating a Featured Image

Ask Claude to generate a featured image for your blog post. It will analyse the blog content and create a photorealistic 3:2 image using Nano Banana 2 via OpenRouter.

**Example prompts:**
- "Generate a featured image for this blog post"
- "Create a hero image for the wellness supplements article"

### Uploading to Shopify

Ask Claude to upload your blog posts to Shopify. It will push articles as hidden (unpublished) drafts with full SEO metadata, and attach featured images with alt text if available.

**Example prompts:**
- "Upload these blog posts to my Shopify store"
- "Push the articles with images to Shopify as drafts"

**Important notes:**
- All posts are uploaded as **hidden by default** — you publish them manually from Shopify Admin
- The title is NOT duplicated in the article body (Shopify renders it separately)
- Featured images include descriptive alt text for SEO and accessibility

### Running the Blog Pipeline

The easiest way to create blog posts end-to-end. Add rows to the Excel tracker and let the pipeline handle everything.

**Setup:**
1. Open `Blog Articles/blog-tracker.xlsx` in your workspace
2. Add a new row with at minimum: Title, Author, and Status = `pending`
3. Optionally fill in: Length (short, standard, or long-form)
4. Ask Claude to run the pipeline

**Example prompts:**
- "Run the blog pipeline" — processes the next pending blog
- "Process all pending blogs" — runs the full queue sequentially

The pipeline will draft the post, generate a featured image, upload to Shopify as a visible post, and mark the row as done in the tracker.

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
