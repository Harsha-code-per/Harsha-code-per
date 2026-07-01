# Harsha Studio // Repository Design System

This design system establishes the visual guidelines, documentation standards, and structural templates for all repositories in the Harshavardhan K ecosystem (e.g., `Billytics`, `DeV`, `SecureChat`, `Spectravein`). 

The goal is to maintain a unified, premium engineering aesthetic—ensuring every project reads like a chapter of the same long-term story.

---

## 1. Visual Language & Style Guide

### Color Architecture
Every visual asset, diagram, or highlight must adhere to these meanings:
*   **Clarity / Body Text**: `#ffffff` (White) and `#e2e8f0` (Slate-200) on a pitch-black `#050508` or `#0a0a0f` base.
*   **System Intelligence**: `#00f2fe` (Neon Cyan) represents machine learning, execution pathways, and active agents.
*   **Technical Engineering**: `#5e6ad2` (Electric Indigo) and `#71717a` (Muted Gray) represent data layers, interfaces, and architecture scaffolding.
*   **Alerts & Statuses**: `#10b981` (Emerald Green) represents normal execution or verified state; `#ef4444` (Rose Red) represents critical failures or bounds.

### Typography
*   **Headings**: Use strong, sentence-case headings. Avoid overly decorative symbols.
*   **Monospace Elements**: Use monospace font (`SFMono-Regular`, `Consolas`, `Menlo`, or `ui-monospace`) for metadata, logs, ports, and configuration tags to maintain a technical ledger aesthetic.
*   **Spacing**: Ensure "aggressive whitespace" by leaving ample margins between sections. Use `<br />` tags to enforce space on GitHub markdown rendering.

---

## 2. Repository README Template

All future projects should structure their main documentation as follows:

```markdown
# [Project Name]

> A concise, one-sentence description explaining how this system works and what user behavior it enables.

---

## Current Status
- **Active Focus**: What is being engineered right now.
- **Constraints**: System bounds (e.g., Latency, Cost, Memory).

## Architecture Map
[Include a clean, minimal vector diagram mapping the system layout. Avoid glossy boxes; use wireframe block diagrams in Indigo and Cyan.]

## Engineering Decisions
- **Decision 001**: Why [Stack X] was selected over [Stack Y].
- **Decision 002**: How we solve [Memory / Scalability Challenge Z].

## Capabilities
- **Domain A**: Core execution engine.
- **Domain B**: Interaction layer.

## Setup & Observability
- Details on running tests and checking system telemetry.
```

---

## 3. Architecture Diagrams

*   **Format**: Prefer clean, transparent SVGs or high-resolution PNGs with transparent backgrounds.
*   **Lines**: Thin 1px vector lines (`stroke-width="1"`) with sharp grid boundaries.
*   **Aesthetic**: Keep diagrams looking like engineering blueprints drawn on technical paper rather than round, glossy PowerPoint blocks.

---

## 4. Documentation Tone

*   **Voice**: Confident, technical, and objective.
*   **Phrasing**: Use active engineering terms (*"engineered"*, *"profiled"*, *"instrumented"*, *"architected"*) rather than marketing-hype words (*"revolutionary"*, *"game-changing"*, *"cutting-edge"*).
*   **Focus**: Prioritize explaining *why* decisions were made, *how* constraints are handled, and *what* was measured, rather than lists of basic dependencies.
