import os
os.environ['KIVY_TEXT'] = 'sdl2'
import unittest

from _visual_test import *


class IsProviderSDL2TestCase(unittest.TestCase):

    def test_provider_actually_is_sdl2(self):
        from kivy.core.text import Label as CoreLabel
        self.assertEqual(CoreLabel.__name__, 'LabelSDL2')


if __name__ == '__main__':
    unittest.main()
