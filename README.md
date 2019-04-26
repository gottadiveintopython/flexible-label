# FlexibleLabel : Automatically adjust font_size

## Test

```
make test
```

### 環境(Environment)

- Python 3.7.1
- Kivy 1.10.1
- SDL2 2.0.4
- SDL2-ttf 2.0.14

## TODO

- behaviour classにする
- providerが対応していないpropertyを設定した場合の`get_extents()`の振るまいを確認
- `markup=False, outline_width=2`のような情況での`get_extents()`の振るまいを確認
- `line_height`, `max_lines`を既定値のままにして欲しい事を説明
- `ABC[size=30]DEF[/size]`のようなmarkupが使えない事を説明