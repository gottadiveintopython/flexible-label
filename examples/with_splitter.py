KV_CODE = '''
<MyLabel@FontsizeAdjustmentBehavior+Label>:

BoxLayout:
    BoxLayout:
        orientation: 'vertical'
        Splitter:
            sizable_from: 'bottom'
            Widget:
        MyLabel:
            text: 'Kivy'
            color: 0, 0, 0, 1
            outline_width: 2
            outline_color: 0, 1, 0, 1
    Splitter:
        sizable_from: 'left'
        Widget:
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