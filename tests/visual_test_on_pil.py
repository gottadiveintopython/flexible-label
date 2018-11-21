import os
os.environ['KIVY_TEXT'] = 'pil'
import unittest

from _visual_test import *


class IsProviderPILTestCase(unittest.TestCase):

    def test_provider_actually_is_pil(self):
        from kivy.core.text import Label as CoreLabel
        self.assertEqual(CoreLabel.__name__, 'LabelPIL')


if __name__ == '__main__':
    unittest.main()
