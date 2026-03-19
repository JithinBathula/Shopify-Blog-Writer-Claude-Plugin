---
name: brand-setup
description: >
  Configure the shopify-blog-writer plugin for a specific company by collecting brand
  information and writing the company-info skill file. Use this skill when the user says
  "set up my brand", "configure my store", "set up the blog writer", "configure company info",
  "initialize the plugin", or when the company-info skill still contains [TODO] markers.
  Also trigger if the user tries to run the blog pipeline or draft a blog post and the
  company-info skill has not been configured yet — prompt them to run brand setup first.
---

# Brand Setup

Walk the user through configuring the shopify-blog-writer plugin for their specific company. This skill collects all the information needed to write a complete `company-info/SKILL.md` file, then generates and saves it.

## When to Trigger

- The user explicitly asks to set up or configure the plugin
- The `company-info/SKILL.md` file still contains `[TODO]` markers
- Another skill (blog-drafting, blog-pipeline) detects the company-info is not configured

## The Interview

Collect the following information from the user. Use AskUserQuestion where appropriate to keep the conversation structured. Don't ask everything at once — group into natural phases.

### Phase 1: Company Basics

1. **Company name** — the brand name as it should appear in content
2. **Website URL** — the full Shopify store URL (e.g., `https://yourstore.com`)
3. **Industry / niche** — what the company sells and in what space (e.g., "wellness supplements", "artisan coffee", "sustainable fashion")

### Phase 2: Product Catalog

Ask the user to describe their products. For each product, collect:

1. **Product name** — as it appears on the store
2. **Target / category** — who or what it's for
3. **Key feature** — the main differentiator (branded ingredient, technology, material, etc.)
4. **Key claim** — the primary benefit message

Also ask:
- Do you offer bundles, kits, or subscription options?
- Are there any proprietary technologies, branded ingredients, or certifications that should always be mentioned?

**Tip:** If the user has product dossiers or documents in their workspace folder, offer to read them to extract product information automatically. Also offer to fetch their website to discover products directly. This can save the user a lot of typing.

### Phase 3: Brand Voice & Tone

Collect the brand personality:

1. **Brand positioning** — how do they describe themselves? (e.g., "science-backed premium", "fun and affordable", "luxury artisan")
2. **Content approach** — what should content lead with? (science, storytelling, value, lifestyle)
3. **Target audience** — who are they writing for? (demographics, interests, expertise level)
4. **Language style** — how should the writing feel? (benefit-driven, casual, technical, conversational)
5. **Tone** — specific tone words (e.g., "knowledgeable, warm, empowering" or "playful, irreverent, bold")
6. **What to avoid** — any tone or language that's off-brand (e.g., "never clinical or cold", "never use jargon", "never overly salesy")
7. **Must-mention differentiators** — anything that should always be highlighted (certifications, technologies, sourcing, format advantages)

### Phase 4: Product Documents

Ask if they have product dossiers, spec sheets, or reference documents in their workspace:
- What are they called? (so the skill knows what file patterns to look for)
- What kind of information do they contain? (clinical data, ingredients, brand-approved claims, etc.)

## Writing the Company Info File

Once all information is collected, generate the complete `company-info/SKILL.md` file. Use the template structure from the existing file but replace all `[TODO]` markers with the user's actual data.

The file to write is located at:
```
${CLAUDE_PLUGIN_ROOT}/skills/company-info/SKILL.md
```

### Template

Use this exact structure — keep the frontmatter, section headings, and "How Other Skills Should Use This" section intact. Only fill in the company-specific content:

```markdown
---
name: company-info
description: >
  This skill provides company context, product catalog details, and brand information
  used by other skills in this plugin. It should be loaded automatically by blog-drafting,
  the image-generator agent, and the shopify-uploader agent when they need company-specific
  context. It can also be triggered directly when the user asks "what products do we have",
  "show me company info", "list our product catalog", or needs a refresher on brand details.
---

# Company Information & Product Research

This skill is the central source of truth for company-specific context within the shopify-blog-writer plugin. Other skills and agents should load this skill first to gather the information they need about the company, its products, and its brand.

## Website

The company website is the primary source for up-to-date product information, pricing, and URLs.

- **Company Name:** {company_name}
- **Website URL:** {website_url}
- Use `WebFetch` on the website homepage to discover the current product catalog, pricing, and any active promotions or bundles.
- Every product mention in blog content **must** be hyperlinked to its product page on the website. Fetch the website to get the correct product URLs — do not guess or hardcode them.

## Product Research

### Product Dossiers (Local Files)

The user's workspace folder may contain detailed product documents (`.docx`, `.pdf` files) that include {document_description}.

**Before writing any blog content, always:**

1. List the files in the user's workspace folder to discover available product documents and reference materials.
2. Read all files relevant to the blog topic — these contain the details and claims that should inform the content.
3. Look for files with names like {file_patterns}.

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

{product_catalog_table}

{bundles_description}

## Brand Voice

{brand_voice_section}

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
```

### Filling the Template

When generating the file content:

- **{product_catalog_table}** — Build a markdown table with columns: Product, Target / Category, Key Feature, Key Claim. One row per product.
- **{brand_voice_section}** — Write this as a natural paragraph followed by bullet points, similar to the example in `examples/beme-company-info.md`. Start with "{company_name} positions itself as {positioning}. When creating content:" followed by bullet points for each guideline the user provided.
- **{document_description}** — Describe what the user's documents contain (e.g., "scientific references, clinical study data, ingredient breakdowns, and brand-approved messaging")
- **{file_patterns}** — List glob patterns for finding relevant files (e.g., `*Dossier*`, `*Product*`, `*Spec*`)
- **{bundles_description}** — If the user offers bundles, describe them. Otherwise omit this section.

## After Writing

1. Confirm to the user that the company-info has been configured
2. Show them a summary of what was saved (company name, number of products, brand tone)
3. Tell them they can now run the blog pipeline or draft posts
4. Mention they can re-run brand setup anytime to update their info, or edit the file directly

## Reconfiguration

If the user runs brand setup again and the file already has content (no TODO markers), tell them the plugin is already configured and show the current settings. Ask if they want to:
- Update specific fields (partial update)
- Start from scratch (full reconfiguration)
