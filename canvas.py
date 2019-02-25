import tkinter as tk

class Canvas:
    def __init__(self, parent, videoCapture):
        self.parent = parent
        self.videoCapture = videoCapture
        self.draw()

    def draw(self):
        self.canvas = tk.Canvas(self.parent, width = self.videoCapture.width, height = self.videoCapture.height)
        self.canvas.pack()

    def createImage(self, x, y, image, anchor):
        self.canvas.create_image(x, y, image = image, anchor = anchor)
