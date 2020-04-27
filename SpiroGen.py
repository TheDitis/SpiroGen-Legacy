# from interface.SpiroGenPlayground import SpiroGenPlayground
from spirogen.interface import Application
import cProfile


def main():
    cProfile.run('Application()', sort='time')


if __name__ == "__main__":
    main()
