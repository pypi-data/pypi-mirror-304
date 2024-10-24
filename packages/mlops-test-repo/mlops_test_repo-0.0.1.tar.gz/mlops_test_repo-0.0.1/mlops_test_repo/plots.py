from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from mlops_test_repo.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(input_path: Path, output_path: Path):
    """
    Function for plot any data
    """
    pass


if __name__ == "__main__":
    app()
