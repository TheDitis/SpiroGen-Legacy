from tkinter import Tk, Frame, Scale, Canvas, NW, Button
import PIL as pil
from PIL import Image, ImageTk



class Application(Frame):
    def __init__(self):
        super().__init__(Tk())
        self.master.geometry("200x300")
        self.pack()
        self.canvas = Canvas(self, width=200, height=200)
        self.canvas.pack()

        pil_img = Image.open('./huetest.png')

        img = ImageTk.PhotoImage(pil_img.resize((200, 200), Image.ANTIALIAS))
        self.canvas.background = img
        bg = self.canvas.create_image(0, 0, anchor=NW, image=img)

        self.scale = Scale(self, orient='horizontal', from_=-127, to=127, command=lambda *x: self.shift_hue(pil_img, self.canvas))
        self.scale.pack()

        self.master.mainloop()

    def shift_hue(self, img, canvas):
        huetarget = img.convert('HSV').load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                huetarget[i, j] = ((self.scale.get() + huetarget[i, j][0]) % 255, huetarget[i, j][1], huetarget[i, j][2])
        img = huetarget
        self.canvas.pack_forget()
        self.canvas = Canvas(self, width=200, height=200)
        self.canvas.pack()
        canvas.background = img
        bg = canvas.create_image(0, 0, anchor=NW, image=img)



def main():
    Application()


if __name__ == "__main__":
    main()


# from PIL import Image, ImageTk
# import tkinter as tk
#
#
# class BkgrFrame(tk.Frame):
#     def __init__(self, parent, file_path, width, height):
#         super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)
#
#         self.canvas = tk.Canvas(self, width=width, height=height)
#         self.canvas.pack()
#
#         pil_img = Image.open(file_path)
#         self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
#         self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
#
#     def add(self, widget, x, y):
#         canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
#         return widget
#
#
# if __name__ == '__main__':
#
#     IMAGE_PATH = './testimg.png'
#     WIDTH, HEIGTH = 350, 200
#
#     root = tk.Tk()
#     root.geometry('{}x{}'.format(WIDTH, HEIGTH))
#
#     bkrgframe = BkgrFrame(root, IMAGE_PATH, WIDTH, HEIGTH)
#     bkrgframe.pack()
#
#     # Put some tkinter widgets in the BkgrFrame.
#     button1 = bkrgframe.add(tk.Button(root, text="Start"), 10, 10)
#     button2 = bkrgframe.add(tk.Button(root, text="Continue"), 50, 10)
#
#     root.mainloop()