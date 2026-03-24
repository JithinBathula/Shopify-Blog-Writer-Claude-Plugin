---
name: brand-setup
description: >
  Complete first-time setup for the shopify-blog-writer plugin. Walks the user through
  configuring everything: company info, brand voice, product catalog, Shopify credentials,
  OpenRouter API key, blog tracker spreadsheet, and product dossier locations. Use this
  skill when the user says "set up my brand", "configure my store", "set up the blog writer",
  "configure the plugin", "initialize the plugin", or when the company-info skill still
  contains [TODO] markers. Also trigger if the user tries to run the blog pipeline or draft
  a blog post and the plugin has not been configured yet — prompt them to run setup first.
---

# Plugin Setup

Walk the user through the complete first-time configuration of the shopify-blog-writer plugin. By the end, every component of the plugin should be ready to use — the user should be able to run `/blog-pipeline` immediately after setup finishes.

## When to Trigger

- The user explicitly asks to set up or configure the plugin
- The `company-info/SKILL.md` file still contains `[TODO]` markers
- Another skill or command detects the plugin is not configured
- The `.env` file is missing when the pipeline or upload runs

## Setup Overview

The setup covers five areas, handled in phases. Use AskUserQuestion to keep the conversation structured. Don't dump everything at once — move through the phases naturally, and let the user skip phases they've already handled.

| Phase | What It Configures | Output |
|-------|-------------------|--------|
| 1. Company & Products | Brand identity, product catalog | `company-info/SKILL.md` |
| 2. Brand Voice & Tone | Writing personality, audience, differentiators | `company-info/SKILL.md` |
| 3. Credentials | Shopify API keys, OpenRouter API key | `.env` file |
| 4. Blog Tracker | Excel spreadsheet with the right columns | `blog-tracker.xlsx` |
| 5. Product Documents | Location and type of dossiers/reference files | `company-info/SKILL.md` |

## Before Starting

Check the current state so you know what's already done:

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/company-info/SKILL.md` — does it still contain `[TODO]` markers?
2. Check if a `.env` file exists in the user's workspace folder — does it have Shopify and OpenRouter credentials?
3. Check if `blog-tracker.xlsx` exists in the workspace folder — does it have the expected columns?

Tell the user what's already configured and what still needs to be set up. If everything is done, show the current settings and ask if they want to update anything.

---

## Phase 1: Company & Products

### Company Basics

Collect:
1. **Company name** — the brand name as it should appear in content
2. **Website URL** — the full Shopify store URL (e.g., `https://yourstore.com`)
3. **Industry / niche** — what the company sells and in what space

### Product Catalog

Ask the user to describe their products. For each product, collect:
1. **Product name** — as it appears on the store
2. **Target / category** — who or what it's for
3. **Key feature** — the main differentiator (branded ingredient, technology, material, etc.)
4. **Key claim** — the primary benefit message

Also ask:
- Do you offer bundles, kits, or subscription options?
- Are there any proprietary technologies, branded ingredients, or certifications that should always be mentioned?

**Shortcut:** Offer to save the user time by fetching their website directly with WebFetch to discover products, descriptions, and prices. Also offer to read any product documents in their workspace. If the user says yes, do the research and present what you found for confirmation rather than making them type everything.

---

## Phase 2: Brand Voice & Tone

Collect the brand personality:

1. **Brand positioning** — how do they describe themselves? (e.g., "science-backed premium", "fun and affordable", "luxury artisan")
2. **Content approach** — what should content lead with? (science, storytelling, value, lifestyle)
3. **Target audience** — who are they writing for? (demographics, interests, expertise level)
4. **Language style** — how should the writing feel? (benefit-driven, casual, technical, conversational)
5. **Tone** — specific tone words (e.g., "knowledgeable, warm, empowering" or "playful, irreverent, bold")
6. **What to avoid** — any tone or language that's off-brand (e.g., "never clinical or cold", "never use jargon", "never overly salesy")
7. **Must-mention differentiators** — anything that should always be highlighted

**Shortcut:** If you fetched their website in Phase 1, you can propose brand voice suggestions based on the tone of their existing website copy and product descriptions. Present these as suggestions for the user to confirm or adjust.

### Write company-info/SKILL.md

Once Phases 1 and 2 are complete, generate and write the company-info file. The file is at:
```
${CLAUDE_PLUGIN_ROOT}/skills/company-info/SKILL.md
```

Use the template in the "Company Info Template" section below. Replace all `{placeholders}` with the user's data. Make sure there are **zero** `[TODO]` markers left in the final file.

---

## Phase 3: Credentials

The plugin needs two sets of API credentials to function. Ask the user for each one. **Never store credentials anywhere except the `.env` file. Never echo secrets back to the user in full.**

### Shopify Credentials

Ask the user:
1. Do you already have a Shopify app set up with `write_content` scope?
2. If yes, do you have your Client ID and Client Secret ready?
3. What is your Shopify store URL? (e.g., `yourstore.myshopify.com`)

If they don't have an app yet, explain:
- Go to partners.shopify.com → create an app → Settings
- The app needs `write_content` scope
- Copy the Client ID and Client Secret

### OpenRouter API Key

Ask the user:
1. Do you have an OpenRouter account and API key?
2. If yes, is it ready to provide?

If they don't have one, explain:
- Go to openrouter.ai → Settings → API Keys
- Create a new key (it starts with `sk-or-v1-`)
- The image generation model costs approximately $60 per million output tokens

### Write the .env File

Create a `.env` file in the user's workspace folder (the same folder where `blog-tracker.xlsx` lives or will live). The file should contain:

```
# Shopify credentials (for uploading blog posts)
SHOPIFY_STORE_URL={store_url}
SHOPIFY_CLIENT_ID={client_id}
SHOPIFY_CLIENT_SECRET={client_secret}

# OpenRouter API key (for AI image generation)
OPENROUTER_API_KEY={api_key}
```

If the user doesn't have credentials ready, write the `.env` file with placeholder values and tell them which lines to fill in later. Mark those as `your-key-here` so it's obvious they're placeholders.

If a `.env` file already exists, read it first and only update the missing values — don't overwrite credentials the user already has.

**Security:** After writing the file, remind the user that `.env` files contain secrets and should never be committed to git. The plugin's `.gitignore` already excludes `.env` files.

---

## Phase 4: Blog Tracker

The pipeline reads from an Excel tracker file. Check if one already exists.

### If the tracker already exists

Look for `blog-tracker.xlsx` in the user's workspace. If found:
1. Read it and check what columns it has
2. If it has the expected columns (#, Title, Author, Length, Status, Shopify ID, Shopify URL, Completed Date), confirm it's good
3. If the content brief columns are missing (Format, Target Keyword, Gap Type, Strategic Rationale, Hidden Intent, Key Arguments, Product Tie-In, Recommended Word Count, Recommended Structure, Publishing Priority), offer to add them
4. Report how many rows exist and how many are pending/planned

### If no tracker exists

Create one using openpyxl with all 18 columns:

**Core columns:** #, Title, Author, Length, Status, Shopify ID, Shopify URL, Completed Date

**Content brief columns:** Format, Target Keyword, Gap Type, Strategic Rationale, Hidden Intent, Key Arguments, Product Tie-In, Recommended Word Count, Recommended Structure, Publishing Priority

Format the header row with bold text and a colored background. Set reasonable column widths. Save it to the user's workspace folder as `blog-tracker.xlsx`.

### Ask about initial content

After the tracker is ready, ask:
- Do you have any blog ideas you'd like to add to the tracker now?
- If yes, collect titles and any brief details, and add them as pending rows

---

## Phase 5: Product Documents

Ask the user about reference materials:

1. Do you have product dossiers, spec sheets, data sheets, or reference documents in your workspace?
2. If yes, what are they called? (so the company-info skill knows what file patterns to search for)
3. What kind of information do they contain? (e.g., clinical data, ingredients, brand-approved claims, specs, manufacturing details)

If the user has documents, list the files in their workspace to confirm which ones are relevant. Then update the Product Research section of `company-info/SKILL.md` with:
- A description of what the documents contain
- The file name patterns to look for (e.g., `*Dossier*`, `*Product*`, `*Spec*`)

If the user doesn't have documents, that's fine — the blog-drafting skill will rely on the website and the product catalog in company-info instead. Update the Product Research section to reflect this.

---

## Company Info Template

When writing `${CLAUDE_PLUGIN_ROOT}/skills/company-info/SKILL.md`, use this exact structure:

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

{product_documents_section}

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

### Filling the Placeholders

- **{product_catalog_table}** — Markdown table with columns: Product, Target / Category, Key Feature, Key Claim
- **{brand_voice_section}** — Natural paragraph + bullet points: "{company_name} positions itself as {positioning}. When creating content:" followed by the user's guidelines. End with "**Tone:** {tone_description}"
- **{product_documents_section}** — If the user has docs: describe what they contain and list the file patterns. If not: write "No local product documents are available. Rely on the website and the product catalog below for all product information."
- **{bundles_description}** — If bundles exist, describe them. If not, omit entirely.

---

## After Setup is Complete

Present a summary:

1. **Company:** {name} — {website}
2. **Products:** {count} products configured
3. **Brand voice:** {tone summary}
4. **Credentials:** Shopify {status}, OpenRouter {status}
5. **Tracker:** {path} with {row_count} rows ({pending_count} pending)
6. **Documents:** {count} reference files found

Then tell the user:
- "Your plugin is ready. You can now run `/blog-pipeline` to process your first blog post."
- "To add blog ideas, add rows to your tracker spreadsheet."
- "To update your brand settings later, just say 'update my brand setup'."

---

## Reconfiguration

If the user runs setup again and everything is already configured (no TODO markers, .env exists, tracker exists), show the current state and ask what they want to update. Support:

- **Partial update** — "I want to update my brand voice" → only re-do Phase 2, rewrite just that section of company-info
- **Add products** — "I have a new product" → add to the catalog table
- **Update credentials** — "I have a new API key" → update just that line in .env
- **Full reconfiguration** — "Start from scratch" → re-do all phases
