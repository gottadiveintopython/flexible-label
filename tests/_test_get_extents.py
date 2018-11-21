__all__ = ('NoMarkupTestCase', 'MarkupTestCase', )

import unittest
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel

IS_PROVIDER_SDL2 = CoreLabel.__name__ == 'LabelSDL2'


class NoMarkupTestCase(unittest.TestCase):

    def setUp(self):
        self.label = Label()

    @unittest.expectedFailure
    def test_can_handle_linebreak(self):
        get_extents = self.label._label.get_extents

        size1 = get_extents('Hello Kivy')
        size2 = get_extents('Hello Kivy\nHello Kivy')
        self.assertEqual(size1[0], size2[0])
        self.assertLess(size1[1], size2[1])

    def test_not_affected_by_padding(self):
        label = self.label
        get_extents = label._label.get_extents

        size1 = get_extents('Hello Kivy')
        label.padding_x = 20
        size2 = get_extents('Hello Kivy')
        self.assertEqual(size1, size2)
        label.padding_y = 20
        size3 = get_extents('Hello Kivy')
        self.assertEqual(size1, size3)

    def test_affected_by_leading_and_trailing_white_space(self):
        label = self.label
        get_extents = label._label.get_extents

        size1 = get_extents('Hello Kivy')
        size2 = get_extents('Hello Kivy    ')
        self.assertLess(size1[0], size2[0])
        self.assertEqual(size1[1], size2[1])
        size3 = get_extents('    Hello Kivy')
        self.assertLess(size1[0], size3[0])
        self.assertEqual(size1[1], size3[1])

    def test_not_affected_by_text_size(self):
        label = self.label
        get_extents = label._label.get_extents

        text = 'Hello Kivy' * 100
        size1 = get_extents(text)
        label.text_size = (400, None)
        size2 = get_extents(text)
        self.assertEqual(size1, size2)
        label.text_size = (400, 1)
        size3 = get_extents(text)
        self.assertEqual(size1, size3)

    def test_not_affected_by_shorten(self):
        label = self.label
        get_extents = label._label.get_extents

        text = 'Hello Kivy' * 100
        size1 = get_extents(text)
        label.text_size = (400, None)
        label.shorten = True
        size2 = get_extents(text)
        self.assertEqual(size1, size2)
        label.text_size = (400, 1)
        size3 = get_extents(text)
        self.assertEqual(size1, size3)

    @unittest.expectedFailure
    def test_affected_by_strip(self):
        label = self.label
        get_extents = label._label.get_extents

        size1 = get_extents('Hello Kivy')
        label.stip = True
        size2 = get_extents('    Hello Kivy    ')
        self.assertEqual(size1, size2)

    @unittest.expectedFailure
    def test_affected_by_bold(self):
        label = self.label
        get_extents = label._label.get_extents

        text = 'Hello Kivy'
        size1 = get_extents(text)
        label.bold = True
        size2 = get_extents(text)
        self.assertLess(size1, size2)

    @unittest.expectedFailure
    def test_affected_by_italic(self):
        label = self.label
        get_extents = label._label.get_extents

        text = 'Hello Kivy'
        size1 = get_extents(text)
        label.italic = True
        size2 = get_extents(text)
        self.assertLess(size1, size2)

    @unittest.expectedFailure
    def test_affected_by_font_name(self):
        label = self.label
        get_extents = label._label.get_extents

        text = 'Hello Kivy'
        size1 = get_extents(text)
        label.font_name = 'Garuda.ttf'  # can be replaced with any font
        size2 = get_extents(text)
        self.assertNotEqual(size1, size2)
        label.font_name = 'Dyuthi.ttf'  # can be replaced with any font
        size3 = get_extents(text)
        self.assertNotEqual(size1, size3)

    def test_affected_by_font_size(self):
        label = self.label
        get_extents = label._label.get_extents

        text = 'Hello Kivy'
        size1 = get_extents(text)
        label.font_size = 40
        size2 = get_extents(text)
        self.assertNotEqual(size1, size2)


class MarkupTestCase(NoMarkupTestCase):

    def setUp(self):
        self.label = Label(markup=True)

    @unittest.skipUnless(IS_PROVIDER_SDL2,
                         "'outline' feature is available on sdl2 only")
    def test_affected_by_outline(self):
        label = self.label
        get_extents = label._label.get_extents

        size1 = get_extents('Hello Kivy')
        label.outline_width = 5
        size2 = get_extents('Hello Kivy')
        self.assertLess(size1, size2)
