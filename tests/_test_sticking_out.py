__all__ = ('StickingOutTestCase', )

import sys
import unittest
import itertools

from kivy.config import Config
Config.set('graphics', 'resizable', 0)
WINDOW_WIDTH = Config.getint('graphics', 'width')
WINDOW_HEIGHT = Config.getint('graphics', 'height')
from kivy.app import runTouchApp, stopTouchApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
IS_PROVIDER_SDL2 = CoreLabel.__name__ == 'LabelSDL2'

import _before_test
from flexiblelabel import FlexibleLabel


class StickingOutTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import os
        from pathlib import Path
        cls.screenshot_dir = \
            Path(__file__).parent / 'screenshot' / os.environ['KIVY_TEXT']
        cls.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        label = self.label
        Window.screenshot(str(
            self.screenshot_dir / 'sticking_out_{}..png'.format(self.methodname)))
        Window.remove_widget(label)

    def run_for_a_while(self, *, duration=1.5):
        Clock.schedule_once(lambda __: stopTouchApp(), duration)
        runTouchApp(self.label)

    def assert_content_is_not_sticking_out(self):
        '''assert the content is not sticking out from the label'''
        content_size = self.label._label.content_size
        label_size = self.label.size
        self.assertGreaterEqual(label_size[0], content_size[0])
        self.assertGreaterEqual(label_size[1], content_size[1])

    # def assert_texture_is_not_sticking_out(self):
    #     '''assert the texture is not sticking out from the label'''
    #     label = self.label
    #     self.assertGreaterEqual(label.size[0], label.texture_size[0])
    #     self.assertGreaterEqual(label.size[1], label.texture_size[1])

    def test_short_text(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(text='short text')
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_short_text_with_padding(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(text='short text with padding',
                                   padding=(40, 40))
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_long_text(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(text='long text ' * 10)
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_multiline_text(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(
            text='\n'.join(itertools.repeat('20 lines', 20)),
        )
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_multiline_text_with_padding(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(
            text='\n'.join(itertools.repeat('20 lines with padding', 20)),
            padding=(40, 40),
        )
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_text_wrap(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(
            font_size_min='40sp',
            text_size=(WINDOW_WIDTH, None),
            text='text wrap ' * 10,
        )
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_text_wrap_with_padding(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(
            font_size_min='40sp',
            text_size=(WINDOW_WIDTH, None),
            text='text wrap with padding ' * 5,
            padding=(40, 40),
        )
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    @unittest.skipUnless(IS_PROVIDER_SDL2,
                         "'outline' feature is available on sdl2 only")
    def test_outline(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(
            markup=True,
            outline_width=4,
            outline_color=(1, 1, 1, 1, ),
            color=(0, 0, 0, 1, ),
            text='outlined text',
        )
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_shorten(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = FlexibleLabel(
            text='shortened text ' * 10,
            shorten=True,
            font_size_min='60sp',
            text_size=(WINDOW_WIDTH, None),
        )
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()

    def test_setting_font_size_affects_nothing(self):
        self.methodname = sys._getframe().f_code.co_name
        self.label = label = FlexibleLabel(text='Hello Kivy')
        label.texture_update()
        label.font_size = 100
        self.run_for_a_while()
        self.assert_content_is_not_sticking_out()
