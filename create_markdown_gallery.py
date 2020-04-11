import os


def main():
    directory = './example_images'
    with open('gallery.md', 'w') as outputfile:
        for filename in os.listdir(directory):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                imageline = f"![example]({os.path.join(directory, filename)})"
                outputfile.writelines([imageline, '\n\n'])


if __name__ == "__main__":
    main()
