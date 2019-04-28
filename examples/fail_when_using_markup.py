KV_CODE = '''
<MyLabel@FontsizeAdjustmentBehavior+Label>:

FloatLayout:
    MyLabel:
        size_hint: .5, .5
        pos_hint: {'center': (.5, .5)}
        text: 'ABCDE[size=30]abcde[/size]'
        markup: True
        canvas.before:
            Color:
                rgb: 0, .3, 0
            Rectangle:
                pos: self.pos
                size: self.size
'''

def _test():
    from kivy.app import runTouchApp
    from kivy.lang import Builder
    from fontsizeadjustmentbehavior import FontsizeAdjustmentBehavior

    runTouchApp(Builder.load_string(KV_CODE))

if __name__ == "__main__":
    import sys
    from pathlib import PurePath

    sys.path.append(str(PurePath(__file__).parents[1]))


_test()