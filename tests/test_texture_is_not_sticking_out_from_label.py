'''
(WARNING): This test is extreamly heavy.

Labelのpropertyであるboldやitalic等を網羅的に組み合わせて、どの場合においても
label.textureがlabel.sizeを超えることがないか確かめるtest。もし超えてしまった
場合は、その時の状態が`failure_screenshot`folderに保存される。
'''

import shutil
import pytest
import random
from functools import partial
from conftest import PROVIDER, ALL_FONTS
from kivy.core.text import DEFAULT_FONT
from kivy.uix.label import Label

from fontsizeadjustmentbehavior import FontsizeAdjustmentBehavior


class MyLabel(FontsizeAdjustmentBehavior, Label):
    pass


@pytest.fixture(scope='session')
def screenshot_dir():
    from pathlib import Path

    SS_DIR = Path(__file__).parent / 'failure_screenshot' / PROVIDER
    if SS_DIR.is_dir():
        shutil.rmtree(SS_DIR)
    SS_DIR.mkdir(parents=True)
    return SS_DIR


p = pytest.mark.parametrize
sdl2_exclusive = lambda v: pytest.param(
    v, marks=pytest.mark.skipif(
        PROVIDER != 'sdl2',
        reason="sdl2 exclusive"))

@p('markup', [False, True])
@p('italic', [False, True])
@p('bold', [False, True])
@p('strip', [False, True])
@p('shorten', [False, True])
@p('underline', [False, sdl2_exclusive(True)])
@p('strikethrough', [False, sdl2_exclusive(True)])
@p('outline_width', [0, sdl2_exclusive(2)])
@p('text', ['normal', 'long text ' * 10, '  leading white space', 'multi\nline'])
@p('font_name', [DEFAULT_FONT])
# @p('font_name', [random.choice(ALL_FONTS)])
@p('padding', [(0, 0), (10, 0), (0, 10), (10, 10), ])
@p('text_size', [(None, None), (200, None), (None, 220), (300, 220)])
def test_texture_is_not_sticking_out_from_label(
    screenshot_dir,
    underline, strikethrough,
    outline_width,
    markup, italic, bold, strip, shorten, text, font_name, padding, text_size,
):
    l = MyLabel()
    l.size = (320, 240)
    # l.valign = 'center'
    # l.halign = 'center'
    l.markup = markup
    l.italic = italic
    l.bold = bold
    l.underline = underline
    l.strikethrough = strikethrough
    l.outline_color = (1, 0, 1, 1)
    l.outline_width = outline_width
    l.strip = strip
    l.shorten = shorten
    l.text = text
    l.font_name = font_name
    l.padding = padding
    l.text_size = text_size

    l.texture_update()
    l_size = l.size
    t_size = l.texture_size
    try:
        assert l_size[1] >= t_size[1]
        assert l_size[0] >= t_size[0]
    except AssertionError:
        fn = '-'.join(item for item in (
            font_name,
            'markup' if markup else None,
            'italic' if italic else None,
            'bold' if bold else None,
            'underline' if underline else None,
            'strikethrough' if strikethrough else None,
            'outline' if outline_width != 0 else None,
            'strip' if strip else None,
            'shorten' if shorten else None,
            None if (padding[0] + padding[1]) == 0 else f"padding{padding}",
            None if (text_size[0] is None and text_size[1] is None) else f"text_size{text_size}",
            make_text_suit_to_filename(text),
        ) if item is not None) + '.png'
        take_a_screenshot(label=l, filepath=screenshot_dir / fn)
        raise


def make_text_suit_to_filename(text):
    from itertools import compress
    tags = ','.join(compress(
        (
         'lws',  # stands for 'leading white space'
         'tws',  # stands for 'trailing white space'
         'lb',  # stands for 'line break'
        ),
        (
            text.startswith(' '),
            text.endswith(' '),
            '\n' in text
        ),
    )) or 'normal'
    return f'text({tags})'


def take_a_screenshot(*, label, filepath):
    from kivy.graphics import Color, Rectangle, Line
    from kivy.uix.widget import Widget

    PADDING = (20, 20)
    root = Widget(
        size=(label.width + 2 * PADDING[0], label.height + 2 * PADDING[1]))
    with root.canvas:
        Color(0, .6, 0, 1)
        Rectangle(pos=(0, 0), size=root.size)
        Color(0, 0, 0, 1)
        Rectangle(pos=PADDING, size=label.size)
        Color(1, 1, 1, 1)
        t_size = label.texture_size
        t_pos = (int(root.center_x - t_size[0] / 2.),
                 int(root.center_y - t_size[1] / 2.), )
        Rectangle(texture=label.texture, size=t_size, pos=t_pos)
        Line(
            dash_offset=4, dash_length=2,
            rectangle=[*t_pos, *t_size, ]
        )
    root.export_to_png(str(filepath))
