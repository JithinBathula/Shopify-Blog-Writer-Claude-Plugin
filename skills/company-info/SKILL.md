---
name: company-info
description: >
  This skill provides company context, product catalog details, and brand information
  used by other skills in this plugin. It should be loaded automatically by blog-drafting,
  blog-image-gen, and shopify-upload when they need company-specific context. It can also
  be triggered directly when the user asks "what products do we have", "show me company info",
  "list our product catalog", or needs a refresher on brand details.
---

# Company Information & Product Research

This skill is the central source of truth for company-specific context within the shopify-blog-writer plugin. Other skills (blog-drafting, blog-image-gen, shopify-upload) should load this skill first to gather the information they need about the company, its products, and its brand.

## Website

The company website is the primary source for up-to-date product information, pricing, and URLs.

- **Website URL:** `https://bemewellness.com`
- Use `WebFetch` on the website homepage to discover the current product catalog, pricing, and any active promotions or bundles.
- Every product mention in blog content **must** be hyperlinked to its product page on the website. Fetch the website to get the correct product URLs — do not guess or hardcode them.

## Product Research

### Product Dossiers (Local Files)

The user's workspace folder contains detailed product dossier documents (`.docx` files) that include scientific references, clinical study data, ingredient breakdowns, usage protocols, and brand-approved messaging.

**Before writing any blog content, always:**

1. List the files in the user's workspace folder to discover available product dossiers and reference documents.
2. Read all dossier files relevant to the blog topic — these contain the science, claims, and product details that should inform the content.
3. Look for files with names like `*Dossier*`, `*Product*`, `*Collagen*`, or any `.docx` / `.pdf` files that may contain product or brand information.

### Website Product Pages

After reading local dossiers, also fetch the relevant product pages from the website to get:

- Current pricing
- Product availability (in stock vs. sold out)
- Exact product page URLs for hyperlinking
- Any updated product descriptions or claims

### Cross-Referencing

Always cross-reference local dossier information with the live website to ensure:

- Prices are current
- Products mentioned are still available
- URLs are correct and active
- No discontinued products are featured prominently

## Product Catalog

The current BeMe Wellness product lineup (verify against the website for updates):

| Product | Target | Technology | Key Claim |
|---------|--------|-----------|-----------|
| **BUILD** — Lean Muscle Collagen | Muscle, body composition | BODYBALANCE® (GELITA) | Lean muscle gain + fat loss |
| **MOVE** — Bone + Joint Collagen | Bones, joints, cartilage | FORTIGEL® + FORTIBONE® (GELITA) | Joint comfort + bone density |
| **PROTECT** — Ligaments + Tendons Collagen | Tendons, ligaments, fascia | TENDOFORTE® (GELITA) | Connective tissue resilience |
| **GLOW** — Hair, Skin, Nail Collagen | Skin, hair, nails | VERISOL® (GELITA) | Wrinkle reduction + skin elasticity |

The store also offers **Protocol Bundles** that combine multiple products for specific goals (e.g., The Longevity Protocol, The Mobility Protocol). Check the website for current bundle availability and pricing.

## Brand Voice

BeMe Wellness positions itself as a science-backed, premium wellness brand. When creating content:

- Lead with science and clinical evidence — this brand earns trust through published research, not hype
- Speak to an active, health-conscious audience (skewing toward adults 35+, with strong appeal to women 40+)
- Use benefit-driven language grounded in study outcomes (e.g., "clinically studied to support lean muscle" not "amazing muscle builder")
- Mention the specific GELITA peptide technologies by name — they are a key differentiator
- Products are liquid sachets with high bioavailability — this is a practical advantage worth highlighting
- Tone: knowledgeable, empowering, warm — never clinical or cold, never overly salesy

## How Other Skills Should Use This

### blog-drafting
Before writing any blog post, load this skill to:
1. Identify which products are relevant to the blog topic
2. Read the corresponding product dossiers for scientific claims and details
3. Fetch the website for current product URLs and pricing
4. Hyperlink every product mention to its product page

### blog-image-gen
Reference the brand voice and product positioning when crafting image prompts to ensure visual consistency with the brand.

### shopify-upload
Use the brand context for author name, tags, and summary generation.
