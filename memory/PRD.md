# PRD — SAURABH: Master Astrological Chart (1-Page PDF Document)

## Original Problem Statement
A single, print-ready, self-contained HTML document styled as a modern-executive dark-mode report, exporting cleanly to a 1-page A4 PDF via browser "Print to PDF". Not an app — a static document deliverable.

## User Choices
- Faint geometric chart-wheel watermark behind the hero (premium feel)
- Mars & Jupiter kept as stylized placeholders ("Focused Placement / Strategic House", "Expansive / Growth House")
- Agent-written copy in confident, executive-strategic tone

## Locked Design System
- Canvas #0B0E14 · Cards #161B22 · Borders #232A34 · Blue #3B82F6 · Gold #F59E0B · Off-white #E2E8F0
- Inter via @import + system-ui fallback · @page A4 margin 12mm · print-color-adjust: exact
- Hero name ~28px, section labels 11px uppercase tracked, body 9–10px

## What's Been Implemented (June 2026)
- `/app/saurabh-master-chart.html` — canonical self-contained deliverable (inlined CSS, no build step)
- `/app/frontend/public/master-chart.html` — served copy for live preview; root `/` redirects to it (App.js)
- Layout: Hero (name + subtitle + 4 identity chips + rotating SVG chart-wheel watermark) → 9×5 planetary table (zebra, gold Exalted/Swakshetra tags, 2-line text clamp) → 4 house cards (Vessel/Engine/Arena/Treasury) → gold-bordered executive callout (THE PRECISION SOVEREIGN + Operational Directive) → footer with placeholder flags
- Screen-only entrance animations (staggered reveals, wheel rotation), fully disabled in @media print
- Verified via headless Chrome print-to-PDF: exactly 1 A4 page. Testing agent iteration_1: 100% pass.

## Architecture Notes
- Backend untouched (template FastAPI, no features). MongoDB unused.
- Ascendant reconciliation: Pisces rising → Virgo=7H, Leo=6H, Capricorn=11H, Rahu 5H (Cancer), Ketu 11H

## Backlog / Next
- P1: Swap in exact Mars & Jupiter signs/houses when provided (30-second edit in the table)
- P2: Render and deliver an actual .pdf file artifact
- P2: Letter-size variant, light-mode variant
