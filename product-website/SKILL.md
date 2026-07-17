---
name: product-website
description: Build, audit, or rewrite product marketing websites so the offer is clear, credible, memorable, demonstrable, easy to buy, and worth sharing. Use when working on a SaaS or indie-product homepage, landing page, pricing page, launch site, hero section, headline, CTA, testimonials, comparison table, product demo, paywall presentation, OG/social image, or conversion-focused website review.
---

# Product Website

Optimize the website for the right visitor's next decision. Use strong patterns as hypotheses, not universal laws, and never trade truth, accessibility, or product economics for punchier marketing.

## Load the pattern catalog

Read [patterns.md](references/patterns.md) before auditing or changing positioning, page structure, pricing presentation, proof, comparisons, or social previews. It groups the patterns by job, adds evidence standards, and identifies the business-model decisions that must not be treated as cosmetic website edits.

## Establish the job

Inspect the repository and existing site before recommending changes. Find the current routes, content sources, design system, responsive behavior, analytics hooks, product screenshots or demos, metadata, tests, and deployment constraints.

Recover or state:

- The primary audience and the painful or desirable moment that brought them here.
- The product's single most important job, outcome, and credible differentiator.
- The primary conversion event: buy, start a trial, run an analysis, book a call, join a waitlist, or another concrete action.
- The traffic source and visitor awareness level when known.
- The pricing model, marginal delivery cost, ongoing value, and support burden when monetization is in scope.
- Available proof: product behavior, customer language, testimonials, measured outcomes, founder experience, and fair competitor data.

Separate repository-observed facts, user-provided facts, and unverified hypotheses. Ask only for missing information that would materially change the direction. Never invent product capabilities, customer quotes, metrics, prices, or competitive claims.

## Write the message spine

Draft an internal positioning sentence before polishing page copy:

`For [specific audience] facing [recognizable problem], [product] delivers [desired outcome] through [credible mechanism or difference].`

Use it to choose one dominant promise and one primary call to action. The published copy does not need to follow the template, but a visitor should be able to answer quickly:

1. What is this?
2. Is it for me?
3. What outcome can I expect?
4. Why should I believe it?
5. What happens when I click?

Prefer plain, specific language drawn from real customers and founder experience. Replace vague adjectives with verifiable details. A memorable line may be emotional or surprising, but it must remain comprehensible and supportable.

## Shape the page

Make the hero sufficient to understand and act on the offer. Give it a clear headline, a useful explanation, the primary CTA, and visible product or proof when assets allow. Do not force every possible element into the first viewport.

Build a narrative in which each section has one dominant job. A common sequence is:

1. Recognize the visitor's problem or desire.
2. Show the product producing the promised outcome.
3. Prove the result with authentic evidence.
4. Explain the meaningful difference or answer objections.
5. Present pricing or the decision path without unnecessary choices.
6. End on a distinctive, useful, or shareable final impression and repeat the primary action.

Adapt or omit sections based on visitor awareness and sales motion. Keep one dominant CTA path while preserving necessary utilities such as sign-in, documentation, accessibility controls, and legal links.

## Audit and prioritize

Evaluate the page through the six lenses in the pattern catalog:

- Positioning and recall
- Attention and hierarchy
- Demonstration and proof
- Action and pricing
- Trust and distinctiveness
- Distribution and sharing

Score each lens `0` (missing or harmful), `1` (present but weak), or `2` (clear and credible). Do not average the score into false precision.

Classify findings:

- `P0` — Visitors cannot understand, trust, use, or act on the offer.
- `P1` — The page creates avoidable doubt or conversion friction.
- `P2` — The page works but could become more memorable or shareable.

Write each finding as `observation → consequence → recommendation → verification`. Do not promise a conversion lift. Express uncertain improvements as experiments with a target signal and guardrail.

## Implement in the repository

When the user asks for changes, implement the highest-priority coherent slice rather than scattering disconnected tweaks across the page.

- Follow the repository's framework, components, content model, and design tokens.
- Preserve semantic heading order, keyboard access, readable contrast, useful alternative text, reduced-motion preferences, and responsive behavior.
- Use real product UI or an honest representation. Do not create a screenshot or testimonial that implies nonexistent functionality or customers.
- Keep image and video payloads proportionate; a demo that ruins page performance weakens the pitch.
- Set accurate title, description, canonical, and social-preview metadata using the framework's supported mechanism.
- Add analytics events only when analytics already exists or the user authorizes the privacy and dependency change.
- Keep competitor comparisons factual, scoped, dated, and sourced.

Treat changes to price, packaging, subscriptions, free access, trials, and paywall timing as product decisions. Recommend or prototype them when requested, but do not silently enact them as copy cleanup.

## Verify the actual experience

Run the repository's checks, then verify proportionately:

1. Inspect the rendered page at representative narrow and wide viewports.
2. Follow the primary CTA through its real destination and confirm its label matches what happens.
3. Check navigation, forms, pricing states, keyboard flow, contrast, and media fallbacks.
4. Inspect emitted metadata and the social-preview asset rather than trusting source code alone.
5. Audit every number, quote, badge, customer logo, comparison, and superlative for support.
6. Confirm there are no placeholder assets, dead links, clipped sections, or layout shifts hiding the product.

For an audit, return the message spine, lens scorecard, prioritized findings, and proposed experiments. For an implementation, lead with the changed customer experience, then report verification and remaining hypotheses.

## Credit

This skill adapts and generalizes Marc Lou's *32 Principles of a Viral Product*. See the liner notes and source links in [patterns.md](references/patterns.md).
