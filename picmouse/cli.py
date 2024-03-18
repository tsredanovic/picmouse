from time import sleep
import click
import pyautogui
from PIL import Image

from utils import load_image, save_image, convert

# SHARED COMMAND OPTIONS

_base_convert_command_options = [
    click.option(
        "--in-path", type=click.Path(), required=True, help="Input image path."
    ),
    click.option(
        "--width",
        type=click.INT,
        help="Output image width. Defaults to input image width.",
    ),
    click.option(
        "--height",
        type=click.INT,
        help="Output image height. Defaults to input image height.",
    ),
    click.option(
        "--resample",
        type=click.Choice(
            ["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"],
            case_sensitive=False,
        ),
        default="nearest",
        help="Resampling used when resizing image. Only used if width and/or height is provided. Defaults to nearest.",
    ),
    click.option(
        "--resolution",
        type=click.IntRange(min=0, max=100),
        default=100,
        help="Output image resolution. Defaults to 100.",
    ),
    click.option(
        "--threshold",
        type=click.IntRange(min=0, max=255),
        default=125,
        help="Threshold used when converting to monochrome. Defaults to 125.",
    ),
    click.option(
        "--invert", is_flag=True, show_default=True, default=False, help="Invert image."
    ),
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


# COMMAND ARGS MAPPINGS


def get_resample(resample):
    resample_map = {
        "nearest": Image.Resampling.NEAREST,
        "box": Image.Resampling.BOX,
        "bilinear": Image.Resampling.BILINEAR,
        "hamming": Image.Resampling.HAMMING,
        "bicubic": Image.Resampling.BICUBIC,
        "lanczos": Image.Resampling.LANCZOS,
    }
    return resample_map[resample]


# COMMANDS


@click.group()
def cli():
    pass


# Convert iamge command


@cli.command(name="convert")
@click.option("--out-path", type=click.Path(), required=True, help="Output image path.")
@add_options(_base_convert_command_options)
def convert_command(
    in_path, out_path, width, height, resample, resolution, threshold, invert
):
    resample = get_resample(resample)
    click.echo(f"in_path: {in_path}")
    click.echo(f"out_path: {out_path}")
    click.echo(f"width: {width}")
    click.echo(f"height: {height}")
    click.echo(f"resample: {resample}")
    click.echo(f"resolution: {resolution}")
    click.echo(f"threshold: {threshold}")
    click.echo(f"invert: {invert}")

    img = load_image(in_path)
    img = convert(img, width, height, resolution, threshold, resample, invert)
    save_image(img, out_path)


# Draw image command


@cli.command(name="draw")
@click.option(
    "--pos",
    nargs=2,
    type=click.INT,
    required=True,
    help="Starts drawing at this position.",
)
@add_options(_base_convert_command_options)
def draw_command(pos, in_path, width, height, resample, resolution, threshold, invert):
    resample = get_resample(resample)
    click.echo(f"pos: {pos}")
    click.echo(f"in_path: {in_path}")
    click.echo(f"width: {width}")
    click.echo(f"height: {height}")
    click.echo(f"resample: {resample}")
    click.echo(f"resolution: {resolution}")
    click.echo(f"threshold: {threshold}")
    click.echo(f"invert: {invert}")

    img = load_image(in_path)
    img = convert(img, width, height, resolution, threshold, resample, invert)

    pyautogui.moveTo(pos[0], pos[1])


# Move mouse to possition command


@cli.command(name="mouse-to-pos")
@click.option(
    "--pos",
    nargs=2,
    type=click.INT,
    required=True,
    help="Moves mouse to this position.",
)
def mouse_to_pos_command(pos):
    click.echo(f"pos: {pos}")
    pyautogui.moveTo(pos[0], pos[1])


# Move mouse from start to finish position command


@cli.command(name="mouse-start-to-finish")
@click.option(
    "--start",
    nargs=2,
    type=click.INT,
    required=True,
    help="Moves mouse from this position.",
)
@click.option(
    "--finish",
    nargs=2,
    type=click.INT,
    required=True,
    help="Moves mouse to this position.",
)
@click.option(
    "--seconds",
    type=click.INT,
    default=3,
    help="Time for movement and waiting between movements.",
)
def mouse_to_pos_command(start, finish, seconds):
    click.echo(f"start: {start}")
    click.echo(f"finish: {finish}")
    click.echo(f"seconds: {seconds}")
    pyautogui.moveTo(start[0], start[1], seconds)
    sleep(seconds)
    pyautogui.moveTo(finish[0], finish[1], seconds)


if __name__ == "__main__":
    cli()
