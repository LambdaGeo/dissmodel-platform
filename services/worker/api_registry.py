# services/worker/api_registry.py
from __future__ import annotations

import subprocess
import tomllib
from functools import lru_cache
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

CONFIGS_PATH = Path("/configs")
MODELS_DIR   = CONFIGS_PATH / "models"


# ── Git sync ──────────────────────────────────────────────────────────────────

def sync_configs() -> None:
    """
    Pull latest changes from the configs repo.
    Called by APScheduler every 15 minutes and by POST /admin/sync.
    Clears the spec cache after a successful pull.
    """
    if not CONFIGS_PATH.exists():
        raise RuntimeError(
            f"Configs path '{CONFIGS_PATH}' does not exist. "
            f"Is the configs-sync container running?"
        )

    result = subprocess.run(
        ["git", "-C", str(CONFIGS_PATH), "pull", "--ff-only"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"git pull failed: {result.stderr.strip()}")

    # Invalidate cache only if something actually changed
    if "Already up to date." not in result.stdout:
        load_model_spec.cache_clear()

    return result.stdout.strip()


def start_sync_scheduler(interval_seconds: int = 900) -> BackgroundScheduler:
    """
    Start the background scheduler for periodic config sync.
    Called once at API startup.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        sync_configs,
        trigger   = "interval",
        seconds   = interval_seconds,
        id        = "config_sync",
        misfire_grace_time = 60,
    )
    scheduler.start()
    return scheduler


# ── Spec loading ──────────────────────────────────────────────────────────────

@lru_cache(maxsize=64)
def load_model_spec(model_name: str) -> dict:
    """
    Load and cache a model spec from TOML.

    Cache is invalidated by sync_configs() after a successful git pull.
    Raises FileNotFoundError if the model is not registered.
    """
    path = MODELS_DIR / f"{model_name}.toml"

    if not path.exists():
        available = [p.stem for p in MODELS_DIR.glob("*.toml")]
        raise FileNotFoundError(
            f"Model '{model_name}' not found in registry. "
            f"Available: {available or 'none — is dissmodel-configs mounted?'}"
        )

    with open(path, "rb") as f:
        return tomllib.load(f)


def list_models() -> list[dict]:
    """
    Return metadata for all registered models.
    Used by GET /models.
    """
    if not MODELS_DIR.exists():
        return []

    models = []
    for path in sorted(MODELS_DIR.glob("*.toml")):
        try:
            spec = load_model_spec(path.stem)
            models.append({
                "name":        path.stem,
                "class":       spec.get("model", {}).get("class", ""),
                "description": spec.get("model", {}).get("description", ""),
            })
        except Exception:
            pass   # skip malformed TOMLs silently

    return models


# ── Catalog ───────────────────────────────────────────────────────────────────

def load_catalog():
    """
    Open the Intake catalog from the configs repo.
    Returns None if catalog.yaml is not present (optional in MVP).
    """
    import intake

    catalog_path = CONFIGS_PATH / "catalog.yaml"
    if not catalog_path.exists():
        return None

    return intake.open_catalog(str(catalog_path))