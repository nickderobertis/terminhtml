import typer
from terminhtml.cli import app

if __name__ == "__main__":
    # For some reason this is the required setup for docs generation to work.
    # main() is the actual CLI entrypoint. Access it through the cli module.
    typer.run(app)
