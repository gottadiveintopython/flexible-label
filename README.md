# FontsizeAdjustmentBehavior : Automatically adjust font_size of Label

## Examples

### short text

```python
from kivy.app import runTouchApp
from kivy.lang import Builder

import fontsizeadjustmentbehavior

root = Builder.load_string('''
<MyLabel@FontsizeAdjustmentBehavior+Label>:

MyLabel:
    text: 'Hello Kivy'
''')

runTouchApp(root)
```

![](screenshot/short_text.png)

### long text

```yaml
MyLabel:
    text: ('Hello Kivy ' * 5)[:-1]
```

![](screenshot/long_text.png)

### multi line

```yaml
MyLabel:
    text: ('Hello Kivy\\n' * 5)[:-1]
```

![](screenshot/multiline.png)

### font_size_max

```yaml
MyLabel:
    text: 'Hello Kivy'
    font_size_max: '60sp'
```

![](screenshot/font_size_max.png)

### font_size_min

```yaml
MyLabel:
    text: 'Hello Kivy ' * 5
    font_size_min: '30sp'
```

![](screenshot/font_size_min.png)

## Things not allowed

### markup

Setting `markup` to True is OK, but setting `text` to an actual markup-text hinders the adjustment.

```yaml
MyLabel:
    markup: True
    text: 'ABCDE[size=40]abcde[/size]'
```

![](screenshot/failure_markup.png)

### line\_height & max\_lines

These properties need to be default-value.


## How to test

**WARNING: Test is extreamly heavy**

```
$ make test
```

## Environment

- Python 3.7.1
- Kivy 1.10.1
- SDL2 2.0.4
- SDL2-ttf 2.0.14

## TODO

- providerが対応していないpropertyを設定した場合の`get_extents()`の振るまいを確認
- `markup=False, outline_width=2`のような情況での`get_extents()`の振るまいを確認
