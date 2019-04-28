'''
outline_widthが0ではない時、markupの真偽値によって作られるtextureの大きさが変
わる事を検証するcode。
'''

from kivy.config import Config
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 600)
from kivy.uix.label import Label
from kivy.app import runTouchApp
from kivy.lang import Builder
from kivy.core.text import Label as CoreLabel

assert CoreLabel.__name__ == 'LabelSDL2', "Make sure the text-provider is sdl2!"


root = Builder.load_string('''
<TestLabel@Label>:
    font_size: 100
    text: 'Kivy'
    outline_width: 4
    canvas.before:
        Color:
            rgba: .2, .2, .2, 1
        Rectangle:
            size: self.texture_size
            pos:
                (
                int(self.center_x - self.texture_size[0] / 2.),
                int(self.center_y - self.texture_size[1] / 2.),
                )

BoxLayout:
    orientation: 'vertical'
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            points: 308, 0, 308, 600
        Line:
            points: 491, 0, 491, 600
    TestLabel:
        id: not_markup
        markup: False
    TestLabel:
        id: markup
        markup: True
''')
runTouchApp(root)

for id, l in root.ids.items():
    print(f'{id}: {l.texture_size} {l._label.get_extents(l.text)}')
