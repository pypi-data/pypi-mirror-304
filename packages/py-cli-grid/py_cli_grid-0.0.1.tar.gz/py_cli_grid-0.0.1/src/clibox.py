import re

class CommandLineBox():
    """This class represents a box inside a terminal (TODO just vertical boxes currently)"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height

    def _fill_box(self, string: str):
        self.height_margin = self.height - string.count("\n")
        marging = "\n"*int(self.height_margin/2) 
        return "%s%s%s" % (marging, string, marging)

    def render(self, string: str, vertically_filled=True):
        if vertically_filled:
            return self._fill_box(string)
        else:
            return string

    def render_cols(self, col_list_str: list, vertically_filled = True):
        n_cols = len(col_list_str)
        col_width = int(self.width/n_cols)
        col_max_height = max(l.count("\n") for l in col_list_str)

        frame_str = ""
        line_remaining = list()
        for line in range(col_max_height+1):
            line_str = ""
            for col in col_list_str:
                line_remaining.append(str())
                col_str = ""
                lines = col.split("\n")
                if len(lines) > line:
                    if len(lines[line]) - self._non_printable_len(lines[line]) > col_width - 1:
                        line_size = col_width-1 + \
                            self._non_printable_len(lines[line][0:col_width])
                        col_str += lines[line][0:line_size]
                        line_remaining[-1] = lines[line][line_size:len(
                            lines[line])]
                    else:
                        col_str += lines[line]
                col_fill_size = (col_width - len(col_str) +
                                 self._non_printable_len(col_str))
                line_str += col_str + " " * \
                    (col_fill_size if col_fill_size > 0 else 0)

            if any(line_remaining):
                for lr in line_remaining:
                    col_str = lr
                    col_fill_size = (col_width - len(col_str) +
                                     self._non_printable_len(col_str))
                    line_str += col_str + " " * \
                        (col_fill_size if col_fill_size > 0 else 0)
            line_remaining.clear()

            frame_str += line_str + "\n"
        if vertically_filled:
            return self._fill_box(frame_str)
        else:
            return frame_str

    def _non_printable_len(self, string: str):
        matches = re.findall("\x1b.[0-9]*m", string)
        return sum([len(m) for m in matches])
