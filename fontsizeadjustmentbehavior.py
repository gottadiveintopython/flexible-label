__all__ = ('FontsizeAdjustmentBehavior', )

from kivy.properties import NumericProperty
from kivy.factory import Factory


class FontsizeAdjustmentBehavior:

    font_size_max = NumericProperty(9999)
    font_size_min = NumericProperty(1)
    _font_size_scaling = NumericProperty(.96)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _trigger_texture_update = self._trigger_texture_update
        fbind = self.fbind
        self.funbind('font_size', _trigger_texture_update, 'font_size')
        fbind('size', _trigger_texture_update)
        fbind('font_size_max', _trigger_texture_update)
        fbind('font_size_min', _trigger_texture_update)

    def texture_update(self, *largs):
        self._label.resolve_font_name()
        self._adjust_font_size()
        return super().texture_update(*largs)

    def _adjust_font_size(self):
        if self.text == '':
            return

        # --------------------------------------------------------------------
        # 現在のfont_sizeで描画した時にどれぐらいの大きさの領域が要るのか予測
        # (正確な計算はできていない)
        # --------------------------------------------------------------------
        get_extents = self._label.get_extents

        # get_extents()は複数行文字列の計算ができないので一行毎に行う
        lines = self.text.split('\n')

        # get_extents()はstripオプションを考慮しないので、有効な場合はこちら側
        # でstrip
        if self.strip:
            lines = (line.strip() for line in lines)

        # 算出
        line_size_list = [get_extents(line) for line in lines]
        pred_content_width = max(width for (width, height) in line_size_list)
        pred_content_height = sum(height for (width, height) in line_size_list)

        if pred_content_width <= 0 or pred_content_height <= 0:
            return

        # --------------------------------------------------------------------
        # 実際に利用可能な領域の大きさ
        # --------------------------------------------------------------------
        dst_width = (self.text_size[0] or self.width) - 2 * self.padding_x
        dst_height = (self.text_size[1] or self.height) - 2 * self.padding_y

        if dst_width <= 0 or dst_height <= 0:
            return

        # --------------------------------------------------------------------
        # [予測した大きさ]と[実際に利用可能な領域の大きさ]の縦横比を求め、そこ
        # からfont_sizeを何倍にすればいいのか算出
        # --------------------------------------------------------------------
        pred_aspect_ratio = pred_content_width / pred_content_height
        dst_aspect_ratio = dst_width / dst_height
        if pred_aspect_ratio < dst_aspect_ratio:
            scaling = dst_height / pred_content_height
        else:
            scaling = dst_width / pred_content_width
        scaling *= self._font_size_scaling

        # --------------------------------------------------------------------
        # font_size_minからfont_size_maxまでの範囲内でfont_sizeを設定
        # --------------------------------------------------------------------
        new_font_size = max(self.font_size_min,
                            min(self._label.options['font_size'] * scaling,
                                self.font_size_max))
        self.font_size = new_font_size
        self._label.options['font_size'] = new_font_size


Factory.register('FontsizeAdjustmentBehavior', cls=FontsizeAdjustmentBehavior)