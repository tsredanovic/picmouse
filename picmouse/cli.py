import click
import pyautogui
from PIL import Image

from utils import convert


@click.group()
def cli():
    pass


@cli.command()
@click.option("--in-path", type=click.Path(), required=True, help="Input image path.")
@click.option("--out-path", type=click.Path(), required=True, help="Output image path.")
@click.option(
    "--width",
    type=click.INT,
    help="Output image width. Defaults to input image width.",
)
@click.option(
    "--height",
    type=click.INT,
    help="Output image height. Defaults to input image height.",
)
@click.option(
    "--resample",
    type=click.Choice(
        ["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"],
        case_sensitive=False,
    ),
    default="nearest",
    help="Resampling used when resizing image. Only used if width and/or height is provided. Defaults to nearest.",
)
@click.option(
    "--resolution",
    type=click.IntRange(min=0, max=100),
    default=100,
    help="Output image resolution. Defaults to 100.",
)
@click.option(
    "--threshold",
    type=click.IntRange(min=0, max=255),
    default=125,
    help="Threshold used when converting to monochrome. Defaults to 125.",
)
@click.option(
    "--invert", is_flag=True, show_default=True, default=False, help="Invert image."
)
def convert(in_path, out_path, width, height, resample, resolution, threshold, invert):
    resample_map = {
        "nearest": Image.Resampling.NEAREST,
        "box": Image.Resampling.BOX,
        "bilinear": Image.Resampling.BILINEAR,
        "hamming": Image.Resampling.HAMMING,
        "bicubic": Image.Resampling.BICUBIC,
    }
    resample = resample_map[resample]
    click.echo(f"in_path: {in_path}")
    click.echo(f"out_path: {out_path}")
    click.echo(f"width: {width}")
    click.echo(f"height: {height}")
    click.echo(f"resample: {resample}")
    click.echo(f"resolution: {resolution}")
    click.echo(f"threshold: {threshold}")
    click.echo(f"invert: {invert}")

    convert(in_path, out_path, width, height, resolution, threshold, resample, invert)


@cli.command()
@click.option("--pos", nargs=2, type=click.INT, required=True, help="Moves mouse to this position.")
def mouse_to_pos(pos):
    x, y = pos
    pyautogui.moveTo(x, y)

if __name__ == "__main__":
    cli()
