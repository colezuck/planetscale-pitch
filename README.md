# PlanetScale sales preparation

Durable product context, presentations, and preparation for Cole's PlanetScale interviews.

## Start here

| Task | Entry point |
| --- | --- |
| Understand the final-round assignment | [Interview requirements](interview/brief/README.md) |
| Explain the product accurately | [Product and evidence index](context/README.md) |
| Prepare the five-minute teach-back | [Teach-back](interview/teach-back/README.md) |
| Prepare the cold call | [Cold call](interview/cold-call/README.md) |
| Prepare the first discovery meeting | [Discovery](interview/discovery/README.md) |
| Research the shared account | [Honeycomb](accounts/honeycomb/README.md) |
| Work on the existing pitch | [Postgres on Metal deck](decks/postgres-metal/README.md) |
| Build smooth system diagrams | [Diagram framework and lab](shared/presentation/README.md) |
| Match the PlanetScale visual style | [Design guidance](shared/design/README.md) |
| Check what is included | [Repository inventory](docs/repository-inventory.md) |
| Maintain this repository | [Agent instructions](AGENTS.md) |

## Local commands

Run from the repository root. Requires Python 3 and Node.js; `npm ci` installs the deployment CLI.

```sh
npm run build             # Audience HTML and deployment folder
npm run build:presenter   # Local presenter HTML from the existing private script
npm run check             # Repository paths, JavaScript syntax, Git whitespace
npm run build:diagrams    # Build the reusable diagram lab
npm run test:diagrams     # Scene compiler and motion geometry tests
npm run serve             # Local preview on http://127.0.0.1:8765
```

Open `/decks/postgres-metal/index.html` on the local server for development, or the deck's `Meridian-PlanetScale.html` for the portable audience presentation. `Present-PlanetScale.command` launches the local presenter.

`npm run deploy` publishes the existing Cloudflare Pages site when deployment is requested. Published `/planetscale/` routes remain unchanged. Root `build_content.py` and `package_deck.py` remain compatibility entry points.

## Ownership and status

- `context/`: shared product research and source evidence, with original review dates.
- `accounts/`: reusable account research; label facts, hypotheses, and open questions.
- `interview/`: assignment requirements and preparation for each exercise.
- `decks/`: presentation implementations and exports. The existing pitch works; the teach-back deck has not been authored.
- `shared/`: guidance used across decks. The existing deck retains its runtime/artwork; reusable diagram primitives and motion now live in `shared/presentation/`.
- `.agents/skills/`: repository-specific skills.
- `scripts/`: repository maintenance checks.
- `dist/`: ignored deployment output; never a source of truth.

Notion can hold brainstorming and working drafts. Record a page link and last reconciliation date when incorporating it; preserve settled decisions and scripts here. Do not maintain competing final scripts in both places.

This repository is public by Cole's choice. Interview preparation can be committed; credentials and existing local presenter files remain ignored. The research is dated context, not a live product specification.
