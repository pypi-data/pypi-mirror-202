import time
from bar_styles import BAR_STYLES, BarColors, BarStyles


class ProgressBar:
    def __init__(self, color=BarColors.GREEN, style=BarStyles.DEFAULT, show_fractions=True, show_time=True):
        self.color = color.value
        self.style = BAR_STYLES.get(style.value)
        self.show_fractions = show_fractions
        self.show_time = show_time
        self.start_time = None
        self.end_time = None

    def __call__(self, width=50, index=0, iterable=None, current=None):
        self.progress(color=self.color,
                      style=self.style,
                      width=width,
                      index=index,
                      iterable=iterable,
                      current=current)

    def progress(self, color, style, width, index, iterable, current):
        total = len(iterable)
        total -= 1
        pp = int((index / total) * 100)
        left = int(width * pp // 100)
        right = int(width - left)
        print(color +
              '\r[', style["left"] * left,
              style["right"] * right, ']',
              f' {pp: .1f}%',
              self._get_fractions(index, total)
              + self._get_current(current)
              + '\033[92m',
              sep='',
              end='',
              flush=True)
        if self.show_time:
            self._show_total_time(index, iterable)

    def _get_fractions(self, i, t):
        if self.show_fractions:
            return f' - {i}/{t}'
        return ''

    def _show_total_time(self, index, iterable):
        if index == 0:
            self.start_time = time.time()
        elif index+1 == len(iterable):
            self.end_time = time.time()
            print(f"\n Process Completed in {self.end_time - self.start_time: .2f} seconds")

    @staticmethod
    def _get_current(current):
        if current:
            return f' > {current}'
        return ''

    @staticmethod
    def _get_style(key):
        return BAR_STYLES.get(key, BAR_STYLES["default"])
