def _test():
    from kivy.app import runTouchApp
    from kivy.uix.label import Label
    from fontsize_adjustment_behavior import FontsizeAdjustmentBehavior

    class MyLabel(FontsizeAdjustmentBehavior, Label):
        pass

    runTouchApp(MyLabel(text='Hello Kivy'))


_test()
