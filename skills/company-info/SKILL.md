---
name: company-info
description: >
  This skill provides company context, product catalog details, and brand information
  used by other skills in this plugin. It should be loaded automatically by blog-drafting,
  the image-generator agent, and the shopify-uploader agent when they need company-specific
  context. It can also be triggered directly when the user asks "what products do we have",
  "show me company info", "list our product catalog", or needs a refresher on brand details.
  If the TODO markers below have not been filled in, tell the user to run the brand-setup
  skill first ("set up my brand") before proceeding.
---

# Company Information & Product Research

This skill is the central source of truth for company-specific context within the shopify-blog-writer plugin. Other skills and agents should load this skill first to gather the information they need about the company, its products, and its brand.

> **SETUP REQUIRED:** If the sections below still contain `[TODO]` markers, the plugin has not been configured yet. Tell the user to run the **brand-setup** skill by saying "set up my brand" or "configure my store". Alternatively, they can edit this file directly. See `examples/beme-company-info.md` for a fully filled-out example.

## Website

The company website is the primary source for up-to-date product information, pricing, and URLs.

- **Company Name:** [TODO: Your company name]
- **Website URL:** [TODO: https://yourstore.com]
- Use `WebFetch` on the website homepage to discover the current product catalog, pricing, and any active promotions or bundles.
- Every product mention in blog content **must** be hyperlinked to its product page on the website. Fetch the website to get the correct product URLs — do not guess or hardcode them.

## Product Research

### Product Dossiers (Local Files)

The user's workspace folder may contain detailed product documents (`.docx`, `.pdf` files) that include product details, specifications, ingredients, scientific references, or brand-approved messaging.

**Before writing any blog content, always:**

1. List the files in the user's workspace folder to discover available product documents and reference materials.
2. Read all files relevant to the blog topic — these contain the details and claims that should inform the content.
3. Look for files with names like `*Product*`, `*Dossier*`, `*Spec*`, `*Guide*`, or any `.docx` / `.pdf` files that may contain product or brand information.

### Website Product Pages

After reading local documents, also fetch the relevant product pages from the website to get:

- Current pricing
- Product availability (in stock vs. sold out)
- Exact product page URLs for hyperlinking
- Any updated product descriptions or claims

### Cross-Referencing

Always cross-reference local document information with the live website to ensure:

- Prices are current
- Products mentioned are still available
- URLs are correct and active
- No discontinued products are featured prominently

## Product Catalog

[TODO: Fill in your product catalog. Add one row per product. Delete the example rows below.]

| Product | Target / Category | Key Feature | Key Claim |
|---------|-------------------|-------------|-----------|
| [TODO: Product Name 1] | [TODO: Who/what it's for] | [TODO: Key ingredient, technology, or differentiator] | [TODO: Main benefit claim] |
| [TODO: Product Name 2] | [TODO: Who/what it's for] | [TODO: Key ingredient, technology, or differentiator] | [TODO: Main benefit claim] |

[TODO: If your store offers bundles, kits, or subscription options, describe them here.]

## Brand Voice

[TODO: Fill in your brand voice guidelines. Delete the example prompts below and write your own.]

[TODO: Your Company Name] positions itself as [TODO: describe your brand positioning — e.g., "a science-backed premium wellness brand", "a playful affordable fashion brand", "a luxury artisan coffee roaster"]. When creating content:

- [TODO: What should the content lead with? e.g., "Lead with science and clinical evidence", "Lead with storytelling and lifestyle imagery", "Lead with value and practical tips"]
- [TODO: Who is the target audience? e.g., "Speak to health-conscious adults 35+", "Speak to budget-savvy millennials", "Speak to professional developers"]
- [TODO: What language style? e.g., "Use benefit-driven language grounded in study outcomes", "Use casual, meme-friendly language", "Use precise technical terminology"]
- [TODO: Any proprietary terms or differentiators to always mention? e.g., "Mention our patented X technology by name", "Always reference our 100% organic certification"]
- [TODO: Product format or delivery advantage? e.g., "Products are liquid sachets with high bioavailability", "All products ship same-day with free returns"]
- **Tone:** [TODO: Describe your tone — e.g., "knowledgeable, empowering, warm — never clinical or cold, never overly salesy", "fun, irreverent, conversational — never corporate or stiff"]

## How Other Skills Should Use This

### blog-drafting
Before writing any blog post, load this skill to:
1. Identify which products are relevant to the blog topic
2. Read the corresponding product documents for details and claims
3. Fetch the website for current product URLs and pricing
4. Hyperlink every product mention to its product page

### image-generator agent
Reference the brand voice and product positioning when crafting image prompts to ensure visual consistency with the brand.

### shopify-uploader agent
Use the brand context for author name, tags, and summary generation.
