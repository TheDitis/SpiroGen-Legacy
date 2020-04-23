from spirogen.spirogen import setup, Colors, ColorScheme, LVL2, wait

rainbow1 = Colors.rainbow(200)
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

    # Do stuff here:

    # example1
    # LVL2.layered_flowers(60, 8, innerdepth=1, rotate=1, colors=rainbow1)

    # example2
    # CL1 = CascadeLines(nlines=200, lengthrange=(2, 1000), distrange=(10, 600), pensizerange=(1, 10), rotation=3, color='white', position=(0, 0))
    # DrawPath(CL1, colors=rainbow1, pensize=(1, 1))

    # example 3
    # ss = LVL2.sin_spiral(50, 1, rotate=2, rotaterate=20, cosine=True)
    # DrawPath(ss, colors=rainbow1)

    # example 4
    # LVL2.sin_avg_point_rotation(strands=100, xshift=2, yshift=2, rotate=4, rotaterate=30, individualrotation=1, wlshift=2, ampshift=2, length=10, webends=2)

    # example 5
    LVL2.spiral_spiral(curve=5, centerdist=0, poly=400, diameter=10, scale=10)

    wait()


if __name__ == "__main__":
    main()
