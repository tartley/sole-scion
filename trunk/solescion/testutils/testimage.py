from solescion.utils.screenshot import _create_tempfile


def save_to_tempfile(image):
    tempfile, fname = _create_tempfile()
    image.save(tempfile, format='PNG')
    return fname


def assert_entirely(image, rgb, message=None):
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            actual = image.getpixel((x, y))[:3]
            if actual != rgb:
                if message is None:
                    message = ''
                msg = '%s != %s\n  pixel %d,%d wrong color\n  %s' % \
                    (actual, rgb, x, y, message)
                raise AssertionError(msg)


def assert_contains(image, rgb, message=None):
    found = set()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            actual = image.getpixel((x, y))[:3]
            if actual == rgb:
                return
            found.add(actual)
    if message is None:
        message = ''
    msg = 'does not contain %s. does contain:\n  %s\n%s' % \
        (rgb, found, message)
    raise AssertionError(msg)


def _assert_rectangle_at_verifyargs(size, rect, rect_rgb, back_rgb):
    left, bottom, right, top = rect

    is_degenerate = left >= (right-1) or bottom >= (top-1)
    if is_degenerate:
        msg = 'degenerate rect %d,%d %d,%d. Broken test?' % \
            (left, bottom, right, top)
        raise AssertionError(msg)

    touches_edge = (
        left <= 0 or bottom <= 0 or
        right+1 >= size[0] or
        top+1 >= size[1]
    )
    if touches_edge:
        msg = 'rect %d,%d %d,%d touches edge of %s. Broken test?' % \
            (left, bottom, right, top, size)
        raise AssertionError(msg)

    if rect_rgb == back_rgb:
        msg = 'colors are same %s. Broken test?' % (rect_rgb,)
        raise AssertionError(msg)


def assert_rectangle_at(image, rect, rect_rgb, back_rgb):
    _assert_rectangle_at_verifyargs(image.size, rect, rect_rgb, back_rgb)
    left, bottom, right, top = rect

    def assert_pixel(x, y, color):
        actual = image.getpixel((x, y))[:3]
        if actual != color:
            fname = save_to_tempfile(image)
            msg = 'rectangle %d,%d %d,%d bad, eg at %d,%d:\n' \
                '%s != %s\n' \
                'image saved to %s' % \
                (left, bottom, right, top, x, y, actual, color, fname)
            raise AssertionError(msg)

    for y in range(bottom, top+1):
        assert_pixel(left, y, rect_rgb)
        assert_pixel(left-1, y, back_rgb)
        assert_pixel(right, y, rect_rgb)
        assert_pixel(right+1, y, back_rgb)

    for x in range(left, right+1):
        assert_pixel(x, bottom, rect_rgb)
        assert_pixel(x, bottom-1, back_rgb)
        assert_pixel(x, top, rect_rgb)
        assert_pixel(x, top+1, back_rgb)

