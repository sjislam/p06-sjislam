from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.engines.pil import Engine
from thumbor.transformer import Transformer


def _png_bytes(size):
    buf = BytesIO()
    Image.new("RGBA", size, (255, 0, 0, 255)).save(buf, "PNG")
    return buf.getvalue()


def test_fit_in_1x1_returns_1x1_image():
    config = Config()
    context = Context(config=config)
    context.request = RequestParameters(fit_in=True, width=1, height=1)
    engine = Engine(context)
    context.request.engine = engine
    engine.load(_png_bytes((940, 2)), ".png")

    transformer = Transformer(context)
    transformer._calculate_target_dimensions()
    transformer.fit_in_resize()

    assert engine.size == (1, 1), engine.size
