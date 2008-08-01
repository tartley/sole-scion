from os import fdopen
from tempfile import mkstemp

from pyglet.image import get_buffer_manager

from PIL import Image


def _create_tempfile():
    fd, fname = mkstemp(prefix='testimage-', suffix='.png')
    tempfile = fdopen(fd, "w+b")
    return tempfile, fname


def image_from_window(window):
    tempfile, fname = _create_tempfile()
    window.switch_to()
    colorBuffer = get_buffer_manager().get_color_buffer()
    colorBuffer.save(filename=fname, file=tempfile)
    tempfile.seek(0)
    image = Image.open(tempfile)
    return image


def save_to_tempfile(image):
    tempfile, fname = _create_tempfile()
    image.save(tempfile, format='PNG')
    return fname


def assert_entirely(image, expectedRgb, assertMsg=None):
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = image.getpixel((x,y))[:3]
            if rgb != expectedRgb:
                if assertMsg is None:
                    assertMsg=''
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


def _assert_rectangle_at_verifyargs(
    imageSize,
    left, bottom, right, top,
    rectCol, backCol):

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


def assert_rectangle_at(
    image,
    left, bottom, right, top,
    rectCol, backCol):

    _assert_rectangle_at_verifyargs(
        image.size, left, bottom, right, top, rectCol, backCol)

    width, height = image.size[0], image.size[1]

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
        assert_pixel(right, y, rectCol)
        assert_pixel(left-1, y, backCol)
        assert_pixel(right+1, y, backCol)

    for x in range(left, right+1):
        assert_pixel(x, bottom, rectCol)
        assert_pixel(x, top, rectCol)
        assert_pixel(x, bottom-1, backCol)
        assert_pixel(x, top+1, backCol)

