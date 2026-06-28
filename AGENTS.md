# AGENTS.md

## Quick Start
- Run the pipeline with `python main.py` after installing deps manually (no requirements file): `pip install openai pydantic requests edge-tts genanki python-dotenv`.
- Required env vars: `OPENAI_API_KEY` and `PEXELS_API_KEY`. `.env` is loaded in `modulos/llm_agent.py`, so `main.py` picks up `PEXELS_API_KEY` via that import side-effect.

## Behavior + Outputs
- The input list is hardcoded in `main.py` (`lista_teste`); edit it to run. The LLM hard limit is `max_palavras = 50` and each term must be <= 30 chars or it raises.
- Assets are written to `media_temp/` (created at runtime). The deck output is `Meus_Flashcards_Mandarim.apkg` in the repo root.

## External Services
- The pipeline calls OpenAI (LLM), Pexels (images), and Edge-TTS (audio) once per card (word + example sentence), so runs are network-dependent and can be slow/costly.

## Agent skills

### Issue tracker

GitHub Issues for this repo; external PRs are not a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use default canonical label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout (root `CONTEXT.md` + `docs/adr/`). See `docs/agents/domain.md`.
