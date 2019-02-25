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
        self.modelFiles = self.getFiles("./assets/models")
        self.model = Model(self.modelFiles[0][1])
        self.videoFiles = self.getFiles("./assets/videos")
        self.videoCapture = VideoCapture(self.videoFiles[0][1])

        self.window = tk.Tk()
        self.window.title("OpenCV mp4")
        self.window.resizable(0, 0)

        self.drawModelList()
        self.drawVideoList()
        self.drawCanvas()
        self.drawParams()

        self.update()
        self.window.mainloop()

    def getFiles(self, path):
        modelFiles = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                modelFileName = filename
                modelFilePath = os.path.join(root, filename)
                modelFile = (modelFileName, modelFilePath)
                modelFiles.append(modelFile)

        return modelFiles

    def drawModelList(self):
        self.modelListBox = tk.Listbox(self.window)
        self.modelListBox.config(width = 40, height = 40)
        for modelFile in self.modelFiles:
            self.modelListBox.insert(tk.END, modelFile[0])

        self.modelListBox.bind('<<ListboxSelect>>', self.modelListBoxSelectionChanged)
        self.modelListBox.select_set(0) #Sets focus on the first item.
        self.modelListBox.event_generate("<<ListboxSelect>>")
        self.modelListBox.pack(side = "left")

    def drawVideoList(self):
        self.videoListBox = tk.Listbox(self.window)
        self.videoListBox.config(width = 30, height = 40)
        for videoFile in self.videoFiles:
            self.videoListBox.insert(tk.END, videoFile[0])

        self.videoListBox.bind('<<ListboxSelect>>', self.videoListBoxSelectionChanged)
        self.videoListBox.select_set(0) #Sets focus on the first item.
        self.videoListBox.event_generate("<<ListboxSelect>>")
        self.videoListBox.pack(side = "left")

    def videoListBoxSelectionChanged(self, *args):
        self.videoCapture = VideoCapture(self.getSelectedVideoPath())

    def getSelectedModelName(self):
        curentSelection = self.modelListBox.curselection()[0]
        return self.modelFiles[curentSelection][0]

    def getSelectedModelPath(self):
        curentSelection = self.modelListBox.curselection()[0]
        return self.modelFiles[curentSelection][1]

    def getSelectedVideoName(self):
        curentSelection = self.videoListBox.curselection()[0]
        return self.videoFiles[curentSelection][0]

    def getSelectedVideoPath(self):
        curentSelection = self.videoListBox.curselection()[0]
        return self.videoFiles[curentSelection][1]

    def modelListBoxSelectionChanged(self, *args):
        self.model = Model(self.getSelectedModelPath())

    def drawCanvas(self):
        self.canvas = tk.Canvas(self.window, width = self.videoCapture.width, height = self.videoCapture.height)
        self.canvas.pack()

    def drawParams(self):
        fields = 'Image scale factor', 'Min neighbors'
        entries = self.makeform(self.window, fields)
        self.window.bind('<Return>', (lambda event, e=entries: fetch(e)))
        enterButton = tk.Button(self.window, text='Enter', command=(lambda e=entries: self.enterParams(e)))
        enterButton.pack(side=tk.LEFT, padx=5, pady=5)

    def enterParams(self, entries):
        self.model.setImageScaleFactor(float(entries[0][1].get()))
        self.model.setCanditateRectangleMinNeighbors(int(entries[1][1].get()))

    def makeform(self, root, fields):
        entries = []
        for field in fields:
            row = tk.Frame(root)
            label = tk.Label(row, width=15, text=field, anchor='w')
            entry = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, entry))
        return entries

    def update(self):
        isFrameRead, frame = self.videoCapture.getFrame()
        if isFrameRead:
            self.model.detectFaces(frame)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.UPDATE_DELAY, self.update)

App()
