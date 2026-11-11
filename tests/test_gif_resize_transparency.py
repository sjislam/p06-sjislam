from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def _palette_gif_with_transparent_left_half():
    img = Image.new("P", (40, 40), 0)
    palette = [0, 0, 0] + [255, 0, 0] + [0] * (256 * 3 - 6)
    img.putpalette(palette)
    for x in range(20, 40):
        for y in range(40):
            img.putpixel((x, y), 1)
    buffer = BytesIO()
    img.save(buffer, "GIF", transparency=0)
    return buffer.getvalue()


def test_resized_gif_keeps_transparent_background():
    config = Config()
    config.PILLOW_PRESERVE_INDEXED_MODE = True
    context = Context(config=config)
    engine = Engine(context)
    engine.load(_palette_gif_with_transparent_left_half(), ".gif")

    engine.resize(80, 80)
    result = engine.read(".gif")

    out = Image.open(BytesIO(result)).convert("RGBA")
    left_alpha = out.getpixel((5, 40))[3]
    right_alpha = out.getpixel((75, 40))[3]

    assert left_alpha == 0, (
        "transparent area became opaque after resize: alpha=%d" % left_alpha
    )
    assert right_alpha == 255
