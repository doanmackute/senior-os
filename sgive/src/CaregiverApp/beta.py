from screeninfo import get_monitors

for monitor in get_monitors():
    width = monitor.width
    height = monitor.height
firstWidth = get_monitors()[0].width
firstHeight = get_monitors()[0].height
print(f"res je: {firstWidth}x{firstHeight}")
