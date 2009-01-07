from solescion.utils.screenshot import _create_tempfile


def save_to_tempfile(image):
    tempfile, fname = _create_tempfile()
    image.save(tempfile, format='PNG')
    return fname


def assert_entirely(image, expectedRgb, assertMsg=None):
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = image.getpixel((x, y))[:3]
            if rgb != expectedRgb:
                if assertMsg is None:
                    assertMsg = ''
                msg = '%s != %s\n  pixel %d,%d wrong color\n  %s' % \
                    (rgb, expectedRgb, x, y, assertMsg)
                raise AssertionError(msg)


def assert_contains(image, expectedRgb, assertMsg=None):
    found = set()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = image.getpixel((x, y))[:3]
            if rgb == expectedRgb:
                return
            found.add(rgb)
    if assertMsg is None:
        assertMsg = ''
    msg = 'does not contain %s. does contain:\n  %s\n%s' % \
        (expectedRgb, found, assertMsg)
    raise AssertionError(msg)


def _assert_rectangle_at_verifyargs(imageSize, rect, rectCol, backCol):
    left, bottom, right, top = rect

    rectIsDegenerate = left >= (right-1) or bottom >= (top-1)
    if rectIsDegenerate:
        msg = 'degenerate rect %d,%d %d,%d. Broken test?' % \
            (left, bottom, right, top)
        raise AssertionError(msg)

    rectTouchesEdges = (
        left <= 0 or bottom <= 0 or
        right+1 >= imageSize[0] or
        top+1 >= imageSize[1]
    )
    if rectTouchesEdges:
        msg = 'rect %d,%d %d,%d touches edge of %s. Broken test?' % \
            (left, bottom, right, top, imageSize)
        raise AssertionError(msg)

    if rectCol == backCol:
        msg = 'colors are same %s. Broken test?' % (rectCol,)
        raise AssertionError(msg)


def assert_rectangle_at(image, rect, rectCol, backCol):
    _assert_rectangle_at_verifyargs(image.size, rect, rectCol, backCol)
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
        assert_pixel(left, y, rectCol)
        assert_pixel(left-1, y, backCol)
        assert_pixel(right, y, rectCol)
        assert_pixel(right+1, y, backCol)

    for x in range(left, right+1):
        assert_pixel(x, bottom, rectCol)
        assert_pixel(x, bottom-1, backCol)
        assert_pixel(x, top, rectCol)
        assert_pixel(x, top+1, backCol)

