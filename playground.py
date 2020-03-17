from spirogen import setup, Transform, Analyze, Colors, ColorScheme, Pattern, PolarPattern, Wave, Rectangle, Circle, RadialAngularPattern, FlowerPattern, FlowerPattern2, DrawPath, TimesTable, CascadeLines, LVL2, wait

rainbow1 = Colors.rainbow(50)
rainbow2 = Colors.rainbow(30)
hot1 = Colors.hot1(20)
grayscale1 = Colors.grayscale1(1000)

darkgrays = ColorScheme({'r': [0, 60], 'g': [0, 60], 'b': [0, 60]}, 20)
whiteish = ColorScheme({'r': [50, 220], 'g': [50, 220], 'b': [50, 220]}, 30)
# darkgrays.shiftlightness(0)


def main():
    speed = 10
    drawspeed = 1000
    setup(drawspeed, speed, 'black', hide=True)

    # Do stuff here
    LVL2.layered_flowers(60, 8, innerdepth=1, rotate=1, colors=rainbow1)

    wait()


if __name__ == "__main__":
    main()
