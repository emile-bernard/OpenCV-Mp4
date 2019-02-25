import os
import cv2
import sys
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

from model import Model
from videoCapture import VideoCapture
from modelListBox import ModelListBox
from videoListBox import VideoListBox
from canvas import Canvas
from paramsForm import ParamsForm

class App(tk.Frame):
    UPDATE_DELAY = 15

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.modelFiles = self.getFiles("./assets/models")
        self.model = Model(self.modelFiles[0][1])
        self.videoFiles = self.getFiles("./assets/videos")
        self.videoCapture = VideoCapture(self.videoFiles[0][1])

        self.modelListBox = ModelListBox(self.parent, self.model, self.modelFiles)
        self.videoListBox = VideoListBox(self.parent, self.videoCapture, self.videoFiles)
        self.canvas = Canvas(self.parent, self.videoCapture)
        self.paramsForm = ParamsForm(self.parent, self.model)

        self.update()

    def getFiles(self, path):
        modelFiles = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                modelFileName = filename
                modelFilePath = os.path.join(root, filename)
                modelFile = (modelFileName, modelFilePath)
                modelFiles.append(modelFile)

        return modelFiles

    def getSelectedModelName(self):
        curentSelection = self.modelListBox.curselection()[0]
        return self.modelFiles[curentSelection][0]

    def getSelectedVideoName(self):
        curentSelection = self.videoListBox.curselection()[0]
        return self.videoFiles[curentSelection][0]

    def update(self):
        isFrameRead, frame = self.videoCapture.getFrame()
        if isFrameRead:
            self.model.detectFaces(frame)
            photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.createImage(0, 0, photo, tk.NW)
        self.parent.after(self.UPDATE_DELAY, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenCV mp4")
    root.resizable(0, 0)
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
