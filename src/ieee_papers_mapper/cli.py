#!/usr/bin/env python3

import click
from ieee_papers_mapper.config.logging_config import setup_logging

setup_logging()


@click.group()
def cli():
    """IEEE Papers Mapper -- fetch, classify, and visualize IEEE research papers."""


@cli.command()
@click.option("--weeks", default=0, help="Repeat every N weeks.")
@click.option("--days", default=0, help="Repeat every N days.")
@click.option("--hours", default=0, help="Repeat every N hours.")
@click.option("--minutes", default=0, help="Repeat every N minutes.")
@click.option("--seconds", default=0, help="Repeat every N seconds.")
def run(weeks, days, hours, minutes, seconds):
    """Run the pipeline. One-shot by default, add interval flags to schedule."""
    import time
    from ieee_papers_mapper.data.pipeline import run_pipeline

    has_schedule = any([weeks, days, hours, minutes, seconds])

    if not has_schedule:
        click.echo("Running pipeline (one-shot)...")
        result = run_pipeline()
        click.echo("Done. New papers processed." if result else "No new papers found.")
        return

    from ieee_papers_mapper.config.scheduler import Scheduler

    scheduler = Scheduler(
        job=run_pipeline,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
    try:
        scheduler.start()
        click.echo("Scheduler running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
        click.echo("Scheduler stopped.")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to.")
@click.option("--port", default=8050, help="Port to serve on.")
@click.option("--debug/--no-debug", default=True, help="Enable debug mode.")
def dashboard(host, port, debug):
    """Launch the Dash dashboard."""
    from ieee_papers_mapper.app.dash_webapp import app

    click.echo(f"Starting dashboard at http://{host}:{port}")
    app.run_server(debug=debug, host=host, port=port)


@cli.command()
def verify():
    """Check system health: API key, database, model availability."""
    import os
    import duckdb
    from ieee_papers_mapper.config import config as cfg

    click.echo("=== IEEE Papers Mapper — System Verify ===\n")

    # API key
    if cfg.IEEE_API_KEY:
        click.echo(f"API key:    set ({cfg.IEEE_API_KEY[:4]}...)")
    else:
        click.secho("API key:    MISSING — set IEEE_API_KEY in .env", fg="red")

    # Database
    if os.path.exists(cfg.DB_PATH):
        conn = duckdb.connect(cfg.DB_PATH, read_only=True)
        click.echo(f"Database:   {cfg.DB_PATH}\n")
        for table in cfg.DB_TABLES:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                click.echo(f"  {table:20s} {count:>6} rows")
            except Exception:
                click.secho(f"  {table:20s} MISSING", fg="red")
        conn.close()
    else:
        click.secho(f"Database:   NOT FOUND at {cfg.DB_PATH}", fg="yellow")
        click.echo("  Run: ieee-papers db-reset")

    # Classifier
    click.echo()
    try:
        from ieee_papers_mapper.data.classify_papers import _get_classifier

        click.echo("Classifier: available (lazy-load, not yet loaded)")
    except ImportError:
        click.secho("Classifier: transformers not installed", fg="red")

    click.echo()


@cli.command("db-reset")
@click.confirmation_option(prompt="This will delete all data. Continue?")
def db_reset():
    """Delete and recreate the database from scratch."""
    import os
    from ieee_papers_mapper.config import config as cfg
    from ieee_papers_mapper.data.database import Database

    if os.path.exists(cfg.DB_PATH):
        os.remove(cfg.DB_PATH)
        click.echo(f"Deleted {cfg.DB_PATH}")

    wal_path = cfg.DB_PATH + ".wal"
    if os.path.exists(wal_path):
        os.remove(wal_path)

    db = Database(name="ieee_papers", filepath=cfg.SRC_DIR)
    db.initialise()
    db.close()
    click.echo("Database recreated with all tables.")
