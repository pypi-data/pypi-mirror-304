# coding=utf-8
import os.path
from typing import Iterable, Any

from .color import _Color, Color


class ConsoleTable:

    def __init__(self, data: Iterable[dict[str, Any]], max_width=100, caption='',
                 caption_color=Color.yellow, title_color=Color.thin_cyan, colorize=True):
        def init_value(val):
            if isinstance(val, str | _Color):
                return val
            if val is None:
                return ''
            return str(val)

        self.colorize = colorize
        self.caption = caption
        self.caption_color = caption_color
        self.title_color = title_color
        self.data = [{str(k): init_value(v) for k, v in row.items()} for row in data]
        self.header = list(self.data[0].keys()) if data else []
        self.max_width = max_width
        self.col_width = []
        self._table_str = ""
        self.col_width = self._get_widths()
        self._table_str = self.make_table_str() if self.colorize else self.make_table_str_without_color()

    @staticmethod
    def _get_string_width(val: str):
        w = 0
        for v in val:
            if u'\u4e00' <= v <= u'\u9fff' or v in '【】（）—…￥！·、？。，《》：；‘“':
                w += 2
            else:
                w += 1
        return w

    def _get_widths(self):
        """获取列宽度，列宽度为整列数据中的最大数据宽度"""

        col_width = [self._get_string_width(key) for key in self.header]
        for row in self.data:
            for i, key in enumerate(self.header):
                value = row.get(key, '')
                width = min(self._get_string_width(value), self.max_width)
                col_width[i] = max(col_width[i], width)
        return col_width

    def make_table_str(self):
        def format_str(val, width):
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        header = ' | '.join(str(self.title_color(format_str(key, w))) for w, key in zip(self.col_width, self.header))
        if self.caption:
            caption = self.caption_color(format_str(self.caption, sum(self.col_width) + (len(self.col_width) - 1) * 3))
            header = caption + '\n' + header
        rows = [' | '.join(format_str(row.get(key, ""), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * (sum(self.col_width) + (len(self.col_width) - 1) * 3)] + rows)

    def make_table_str_without_color(self):
        def format_str(val, width):
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        def get_value(row, key):
            val = row.get(key, "")
            if isinstance(val, _Color):
                return val.raw
            return val

        header = ' | '.join(str(format_str(key, w)) for w, key in zip(self.col_width, self.header))
        if self.caption:
            caption = format_str(self.caption, sum(self.col_width) + (len(self.col_width) - 1) * 3)
            header = caption + '\n' + header
        rows = [' | '.join(format_str(get_value(row, key), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * (sum(self.col_width) + (len(self.col_width) - 1) * 3)] + rows)

    def __str__(self):
        return self._table_str

    __repr__ = __str__

    def to_image(
            self,
            *,
            odd_row_color='#f8f9fa', even_row_color='white', header_color='#B4DCFF',
            cell_char_size=40,
            font_path: str = r'C:\Windows\Fonts\simhei.ttf', title_font_path: str = r'C:\Windows\Fonts\msyhbd.ttc',
            font_size=12, title_font_size: int = None
    ):
        """
        将表格转换为图片
        :param odd_row_color: 偶数行颜色，默认为 #f8f9fa
        :param even_row_color: 奇数行颜色，默认为 white
        :param header_color: 表头颜色，默认为 #B4DCFF
        :param cell_char_size: 单元格中的单行文本字符数，默认为40，超过这个长度的文本将会被换行显示
        :param font_path: 字体文件路径，一般采用
        :param title_font_path: 表头字体文件路径，一般采用加粗字体
        :param font_size: 字体大小，默认为12
        :param title_font_size: 表头字体大小，默认为font_size + 2
        :return:
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ModuleNotFoundError:
            raise ModuleNotFoundError('请先安装pillow（pip install pillow -U）')

        def split(value, size):
            v = str(value)
            return '\n'.join(('\n'.join(j[i:i + size] for i in range(0, len(j), size))) for j in v.split('\n'))

        data = self.data
        baseImg = Image.new('RGB', (1920, 1080))
        baseDraw = ImageDraw.Draw(baseImg)
        title_font_path = title_font_path or font_path
        if not os.path.exists(font_path) or not os.path.exists(title_font_path):
            raise FileNotFoundError('字体文件不存在！')
        font = ImageFont.truetype(font_path, size=font_size)
        bFont = ImageFont.truetype(title_font_path, size=title_font_size or (font_size + 2))
        header = [split(k, cell_char_size) for k in data[0].keys()]
        values = [[split(str(row[k]) if row[k] is not None else '', cell_char_size) for k in header] for row in data]
        width = [10] * len(header)
        height = []
        for j, row in enumerate([header, *values]):
            height.append(1)
            for i, val in enumerate(row):
                _, _, w, h = baseDraw.textbbox((0, 0), val, font=font if j > 0 else bFont)
                width[i] = max(width[i], int(w))
                height[-1] = max(height[-1], int(h) + 2)

        totalWidth = sum(width) + (len(width) + 1) * 10
        totalHeight = sum(height) + (len(height) + 1) * 12
        img = Image.new('RGB', (totalWidth, totalHeight), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        for i, row in enumerate([header, *values], start=1):
            curHeight = i * 12 + sum(height[:i - 1])
            if i > 1:
                draw.rectangle(
                    [(5, curHeight - 5), (totalWidth - 5, curHeight + height[i - 1] + 5)],
                    fill=odd_row_color if i % 2 == 1 else even_row_color
                )
            else:
                draw.rectangle(
                    [(5, curHeight - 5), (totalWidth - 5, curHeight + height[i - 1] + 5)],
                    fill=header_color
                )
            for j, val in enumerate(row, start=1):
                curWidth = j * 10 + sum(width[:j - 1])
                draw.text((curWidth, curHeight), val, font=font if i > 1 else bFont, fill=(0, 0, 0))

            draw.line(
                [(5, curHeight + height[i - 1] + 5), (totalWidth - 5, curHeight + height[i - 1] + 5)]
                , fill=(0, 0, 0) if i == 1 else (202, 202, 202),
                width=2)
        return img


if __name__ == '__main__':
    table = ConsoleTable(
        [{'server_name': 'intelligent-platform-product', 'status': Color.green('成功'), 'message': '构建成功'}],
        caption='构建结果',
    )
    print(table)
