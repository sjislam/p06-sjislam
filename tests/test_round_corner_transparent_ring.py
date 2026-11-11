from PIL import Image

from thumbor.ext.filters import _round_corner


def test_transparent_round_corner_edge_has_no_dark_ring():
    size = 60
    source = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    data = source.tobytes()

    result = _round_corner.apply(
        1,
        "RGBA",
        20,
        20,
        255,
        255,
        255,
        size,
        size,
        data,
        True,
    )
    out = Image.frombytes("RGBA", (size, size), bytes(result))

    darkened = []
    for y in range(size):
        for x in range(size):
            r, g, b, a = out.getpixel((x, y))
            if a > 0 and (r, g, b) != (255, 255, 255):
                darkened.append((x, y, (r, g, b, a)))

    assert darkened == [], (
        "visible corner pixels were darkened (dark ring): "
        f"{darkened[:5]}"
    )
