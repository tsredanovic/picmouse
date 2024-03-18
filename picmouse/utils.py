from PIL import Image, ImageOps
import pyautogui


def load_image(path):
    with Image.open(path) as in_img:
        return in_img.convert("RGB")


def save_image(img, path):
    img.save(path)


def resize(img, width, height, resample):
    return img.resize((width, height), resample)


def apply_resolution(img, resolution, resample):
    width, height = img.size
    img = img.resize(
        (width * resolution // 100, height * resolution // 100)
    )  # TODO add resample here
    return img.resize((width, height), resample)


def apply_threshold(img, threshold):
    img = img.convert("L")
    img = img.point(lambda p: 255 if p > threshold else 0)
    return img.convert("1")


def invert(img):
    return ImageOps.invert(img)


def convert(
    img,
    width=None,
    height=None,
    resolution=None,
    threshold=None,
    resample=None,
    invert=False,
):
    # Resize only if width and/or height are provided
    width = width if width else img.width
    height = height if height else img.height
    if width != img.width or height != img.height:
        img = resize(img, width, height, resample)

    # Apply resolution if less than 100
    if resolution < 100:
        img = apply_resolution(img, resolution, resample)

    # Apply threshold
    img = apply_threshold(img, threshold)

    # Invert if needed
    if invert:
        img = invert(img)

    return img


def draw(
    pos,
    img,
):
    current_row = 0
    for i, pixel in enumerate(img.getdata(), 1):
        if pixel > 127:
            current_col = (i - 1) % img.width
            pyautogui.click(pos[0] + current_col, pos[1] + current_row)
            print(f"Clicked at {pos[0] + current_col}, {pos[1] + current_row}")
            
        if i != 0 and i % img.width == 0:
            current_row += 1

