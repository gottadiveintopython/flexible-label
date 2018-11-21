__all__ = ('FlexibleLabel', )

from kivy.uix.label import Label
from kivy.properties import NumericProperty


class FlexibleLabel(Label):

    font_size_max = NumericProperty(None, allownone=True)
    font_size_min = NumericProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.funbind('font_size', self._trigger_texture_update, 'font_size')
        self.fbind('size', self._trigger_texture_update)

    def texture_update(self, *largs):
        self._adjust_font_size()
        return super().texture_update(*largs)

    def _adjust_font_size(self):
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

        # --------------------------------------------------------------------
        # 実際に利用可能な領域の大きさ
        # --------------------------------------------------------------------
        dst_width = self.width - 2 * self.padding_x
        dst_height = self.height - 2 * self.padding_y

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

        # --------------------------------------------------------------------
        # font_size_minからfont_size_maxまでの範囲内でfont_sizeを設定
        # --------------------------------------------------------------------
        new_font_size = max(self.font_size_min or 1,
                            min(self.font_size * scaling,
                                self.font_size_max or 99999))
        self.font_size = new_font_size
        self._label.options['font_size'] = new_font_size
