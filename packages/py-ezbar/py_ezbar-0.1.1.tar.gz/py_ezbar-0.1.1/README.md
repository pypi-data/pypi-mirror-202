
# Ez-Bar

Very simple customizable progress bar.

## Installation
```bash
pip install py-ezbar
```

## Usage and Examples

import, configure and use it's easy
```bash
from py_ezbar import ProgressBar, BarStyles, BarColors
    
progress_bar = ProgressBar(color=BarColors.YELLOW, style=BarStyles.DEFAULT, show_fractions=True)
t = range(327)
x = [fake.bs() for _ in range(5)]
y = {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
}

for i in t:
    progress_bar(index=i, iterable=t, current=i)
    sleep(0.01)

for i, v in enumerate(x):
    progress_bar(index=i, iterable=x, current=v)
    sleep(0.01)

for i, (k, v) in enumerate(y.items()):
    progress_bar(index=i, iterable=x, current=v)
    sleep(0.01)
```

![example](https://raw.githubusercontent.com/kdrkrgz/ez-bar/master/docs/gifs/example.gif)