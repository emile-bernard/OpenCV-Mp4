import os
import cv2
import sys
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

from model import Model
from videoCapture import VideoCapture

class App:
    UPDATE_DELAY = 15

    def __init__(self):
        self.modelFiles = self.getModelFiles()
        self.model = Model(self.modelFiles[0][1])
        self.videoCapture = VideoCapture("./assets/videos/fair_960x540.mp4")

        self.window = tk.Tk()
        self.window.title("OpenCV mp4")
        self.window.resizable(0, 0)

        self.drawModelList()
        self.drawCanvas()
        self.drawSnapshotButton()

        self.update()
        self.window.mainloop()

    def getModelFiles(self):
        modelFiles = []
        for root, dirs, files in os.walk("./assets/models"):
            for filename in files:
                modelFileName = filename
                modelFilePath = os.path.join(root, filename)
                modelFile = (modelFileName, modelFilePath)
                modelFiles.append(modelFile)

        return modelFiles

    def drawModelList(self):
        self.listBox = tk.Listbox(self.window)
        self.listBox.config(width = 40)

        for modelFile in self.modelFiles:
            self.listBox.insert(tk.END, modelFile[0])

        self.listBox.bind('<<ListboxSelect>>', self.listBoxSelectionChanged)

        self.listBox.select_set(0) #Sets focus on the first item.
        self.listBox.event_generate("<<ListboxSelect>>")

        self.listBox.pack(side = "left", fill = tk.Y)

    def getSelectedModelName(self):
        curentSelection = self.listBox.curselection()[0]
        return self.modelFiles[curentSelection][0]

    def getSelectedModelPath(self):
        curentSelection = self.listBox.curselection()[0]
        return self.modelFiles[curentSelection][1]

    def listBoxSelectionChanged(self, *args):
        self.model = Model(self.getSelectedModelPath())

    def drawCanvas(self):
        self.canvas = tk.Canvas(self.window, width = self.videoCapture.width, height = self.videoCapture.height)
        self.canvas.pack()

    def drawSnapshotButton(self):
        self.snapshotButton = tk.Button(self.window, text="Take a snapshot", width=50, command=self.snapshot)
        self.snapshotButton.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        isFrameRead, frame = self.videoCapture.getFrame()
        if isFrameRead:
            self.model.detectFaces(frame)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.UPDATE_DELAY, self.update)

    def snapshot(self):
        isFrameRead, frame = self.videoCapture.getFrame()
        if isFrameRead:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

App()
