def _test():
    from kivy.app import runTouchApp
    from kivy.uix.label import Label
    from fontsizeadjustmentbehavior import FontsizeAdjustmentBehavior

    class MyLabel(FontsizeAdjustmentBehavior, Label):
        pass

    runTouchApp(MyLabel(text='Hello Kivy'))


if __name__ == "__main__":
    import sys
    from pathlib import PurePath

    sys.path.append(str(PurePath(__file__).parents[1]))


_test()