"""Compatibility entry point; canonical source lives in decks/postgres-metal."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parent / "decks/postgres-metal/build_content.py"), run_name="__main__")
