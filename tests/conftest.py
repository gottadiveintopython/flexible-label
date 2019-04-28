__all__ = ('PROVIDER', 'ALL_FONTS', )

from pathlib import Path
import random
import pytest
from kivy.uix.label import Label
from kivy.core.text import LabelBase, Label as CoreLabel


PROVIDER = {
    'LabelSDL2': 'sdl2', 'LabelPIL': 'pil', 'LabelPango': 'pango',
}[CoreLabel.__name__]


def _get_fontfiles(*, fullpath=False):
    for dir_ in LabelBase.get_system_fonts_dir():
        for item in Path(dir_).iterdir():
            if item.is_file() and item.suffix in ('.ttc', '.ttf', ):
                yield item.absolute() if fullpath else item.name
ALL_FONTS = tuple(_get_fontfiles())


# BOOLEAN_PROPS_SDL2 = {
#     'font_blended', 'font_hinting', 'font_kerning', 'strikethrough',
#     'underline',
# }
# BOOLEAN_PROPS = {
#     'bold', 'markup', 'strip', 'italic', 'shorten', 'mipmap',
#     *BOOLEAN_PROPS_SDL2
# }

# def pytest_generate_tests(metafunc):
#     boolean_props = BOOLEAN_PROPS.intersection(metafunc.fixturenames)
#     for prop in boolean_props:
#         metafunc.parametrize(
#             prop, [False, True, ], ids=lambda value: prop if value else '')
#     if 'font_name' in metafunc.fixturenames:
#         metafunc.parametrize(
#             'font_name',
#             [DEFAULT_FONT, *metafunc.config.getoption('fontname')])


# @pytest.fixture(scope='function')
# def random_font():
#     return random.choice(all_font)


# @pytest.fixture(scope='session')
# def all_fontfiles():
#     return list(get_fontfiles())


# def pytest_addoption(parser):
#     parser.addoption(
#         '--fontname',
#         action='append',
#         default=[],
#         help='add a font to be used for tests',
#     )