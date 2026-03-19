---
name: blog-drafting
description: >
  This skill should be used when the user asks to "write a blog post",
  "draft a Shopify blog", "create blog content", "write an article for our store",
  "help with blog copywriting", or needs guidance on Shopify blog structure,
  SEO for e-commerce blogs, or product-focused content writing.
---

# Shopify Blog Post Drafting

Draft blog posts optimized for Shopify stores — structured for readability, SEO, and conversion.

## Before Writing

### Step 1: Load Company Context

**Before doing anything else**, read the `company-info` skill (`skills/company-info/SKILL.md` in this plugin) to get:

- The company website URL
- Where to find product dossiers and reference documents in the workspace
- The current product catalog and positioning
- Brand voice guidelines

Follow the research steps outlined in the company-info skill:

1. **Read product dossiers** — List the user's workspace folder and read all `.docx` and `.pdf` files relevant to the blog topic. These contain clinical data, ingredient details, and brand-approved claims that should inform the content.
2. **Fetch the website** — Use the website URL from the company-info skill to get current product pages, pricing, availability, and exact product URLs.
3. **Hyperlink products** — Every product mentioned in the blog must link to its product page on the website. Never use placeholder links — always fetch real URLs.

### Step 2: Gather Blog Details

After loading company context, gather these details. **When called from the blog-pipeline**, most or all of these will already be provided via the tracker's content brief columns — use them directly instead of asking the user. When called standalone (user asks to draft a blog directly), ask the user for anything not provided.

#### Core details (always needed):

- **Topic or product focus** — what the post is about (from Title column or user input)
- **Target audience** — who is reading this (infer from Gap Type and Hidden Intent if available, otherwise ask)
- **Goal** — inform, drive traffic, promote a product, build authority (infer from Strategic Rationale if available)
- **Target keyword(s)** — primary SEO keyword and 2-3 secondary keywords (from **Target Keyword** column — first keyword before " / " is primary, rest are secondary)
- **Tone** — casual, professional, playful, authoritative (default: friendly and knowledgeable)
- **Desired length** — short (400-600 words), standard (800-1200 words), medium-form (1000-1500 words), or long-form (1500-2500 words). **Recommended Word Count** from the tracker overrides this if present.

#### Content brief details (from tracker columns, when available):

- **Format** — the article format shapes the entire structure (see "Format-Specific Structures" below)
- **Hidden Intent** — the emotional undercurrent driving the searcher. This is critical for the introduction: don't open with a generic hook, open by directly addressing what the reader is feeling (skepticism, fear, frustration, decision fatigue, etc.)
- **Key Arguments** — mandatory content beats. Every argument listed must appear in the article body. Treat this as a checklist.
- **Strategic Rationale** — why this article exists for the brand. Informs how aggressively to position BeMe (defensive vs offensive) and the narrative tension.
- **Gap Type** — what content gap this fills. "Competitive gap" means competitors own this topic; "Audience gap" means an underserved reader segment.
- **Product Tie-In** — which specific products and protocol bundles to feature and hyperlink. "Full range" = mention all products; specific names = focus on those.
- **Recommended Structure** — a structural blueprint that overrides the default blog structure below. Follow it directly.

## Blog Post Structure

If a **Recommended Structure** was provided in the content brief, follow that structure directly — it was designed for the specific article. The sections below serve as the default when no custom structure is given, and as general guidance for quality within any structure.

### Format-Specific Structures

When a **Format** is specified in the content brief, use these templates as a starting point (the Recommended Structure column may refine further):

- **Comparison** — Lead with a comparison table or decision matrix early in the article (within the first 300 words). Follow with H2 sections that expand on each comparison dimension with evidence. End with a clear "which one is right for you" decision framework and FAQ block.
- **Ranked list** — Short intro (under 100 words), then numbered items each as an H3. Each item gets 2-3 sentences of explanation plus a product callout where relevant. Close with a summary CTA.
- **How-to guide** — Opening hook that identifies the problem, then step-by-step protocol sections as H2s. Include dosage tables, timing protocols, or practical checklists where relevant. End with FAQ block.
- **Topic guide** — Educational and authoritative. Deeper science sections with mechanisms explained in accessible language. Use H2 sections for major themes. Can be a pillar piece that other articles link to.
- **Topic guide / Comparison (Pillar)** — Combine the depth of a topic guide with a comparison table. This is a hub piece — structure it so other articles can link to specific sections.

### Default Structure

Follow this structure when no custom Recommended Structure is provided:

### 1. Title
- Include the primary keyword naturally
- Keep under 60 characters for SEO
- Use a hook: number, question, "how to", or bold claim
- Examples: "5 Ways to Style [Product] This Season", "The Complete Guide to [Topic]"

### 2. Introduction (2-3 paragraphs)
- If a **Hidden Intent** was provided, open by directly addressing that emotional state — don't use a generic hook, speak to what the reader is actually feeling when they search this topic
- Open with a relatable problem, question, or scenario
- Establish why the reader should care
- Preview what the post covers
- Keep it under 150 words

### 3. Body Sections
- Use H2 headings for main sections, H3 for subsections
- Each section should deliver a clear takeaway
- If **Key Arguments** were provided, ensure every single one appears in the body — treat them as a mandatory checklist, not suggestions
- Weave in product mentions naturally — never force a sales pitch. Use the **Product Tie-In** to know which products to feature.
- Use short paragraphs (2-4 sentences max)
- Include bullet points or numbered lists for scannable content
- **Do NOT include placeholder image tags** like `[IMAGE: ...]` — the featured image is handled separately by the blog-image-gen skill, and inline images are not used in Shopify blog posts
- **Hyperlink every product mention** to the real product URL on the website

### 4. Conclusion
- Summarize the key points in 2-3 sentences
- End with a clear call-to-action (CTA): shop a collection, try a product, read a related post
- Keep the CTA conversational, not pushy

### 5. SEO Metadata
After the post body, provide:
- **Meta title** (under 60 characters, includes primary keyword)
- **Meta description** (under 155 characters, compelling and keyword-rich)
- **URL slug** (short, lowercase, hyphenated, keyword-focused)
- **Suggested tags** (3-5 relevant Shopify blog tags)

## Writing Guidelines

### Tone and Voice
- Write like a knowledgeable friend, not a salesperson
- Use "you" and "your" to speak directly to the reader
- Avoid jargon unless the audience expects it
- Be specific — replace vague claims with concrete details
- Match the brand voice from the company-info skill

### Using Product Dossier Data
- Ground claims in the clinical studies and scientific references found in the product dossiers
- Cite specific outcomes (e.g., percentages, study populations, durations) to build credibility
- Reference the branded collagen peptide technologies by name when relevant — they differentiate the products
- Never fabricate or exaggerate study results — use only what the dossiers and published research support

### SEO Best Practices
- Place the primary keyword in the title, first paragraph, one H2, and the conclusion
- Use secondary keywords in H2/H3 headings and naturally throughout the body
- Keep keyword density natural (1-2% of total word count)
- Write for humans first, search engines second
- Use internal linking placeholders: `[LINK: related post or collection URL]`

### E-commerce Focus
- Connect content to products without being salesy
- Use benefit-driven language ("keeps you warm" not "made of wool")
- Include social proof placeholders where relevant: `[SOCIAL PROOF: customer quote or review]`
- Think about the buyer's journey — awareness, consideration, decision

### Formatting for Shopify
- Shopify blogs support basic HTML and Markdown
- Structure with proper heading hierarchy (H1 for title, H2 for sections, H3 for subsections)
- Keep paragraphs short for mobile readability

## Output Format

Deliver the blog post as a complete, ready-to-paste HTML draft with clear section headings. After the post, include the SEO metadata block. Flag any placeholders that the user needs to fill in (images, links, social proof).

## Reference Materials

For detailed SEO keyword research strategies and advanced formatting patterns, see `references/seo-guide.md`.
