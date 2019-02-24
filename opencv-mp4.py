import os
import cv2
import sys
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

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

class VideoCapture:
    def __init__(self, videoPath):
        self.videoCapture = cv2.VideoCapture(videoPath)
        self.width = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.videoCapture.isOpened():
            self.videoCapture.release()

    def getFrame(self):
        if self.videoCapture.isOpened():
            isFrameRead, frame = self.videoCapture.read()
            if isFrameRead:
                 return (isFrameRead, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (isFrameRead, None)
        else:
            return (isFrameRead, None)

class Model:
    IMAGE_SCALE_FACTOR = 1.1
    CANDIDATE_RECTANGLE_MIN_NEIGHBORS = 5
    OBJECT_MIN_HORIZONTAL_SIZE = 20
    OBJECT_MIN_VERTICAL_SIZE = 20

    def __init__(self, classifierPath):
        self.classifier = cv2.CascadeClassifier(classifierPath)

    def detectFaces(self, frame):
        colorSpace = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detectedObjects = self.classifier.detectMultiScale(
            colorSpace,
            scaleFactor = self.IMAGE_SCALE_FACTOR,
            minNeighbors = self.CANDIDATE_RECTANGLE_MIN_NEIGHBORS,
            minSize = (self.OBJECT_MIN_HORIZONTAL_SIZE, self.OBJECT_MIN_VERTICAL_SIZE),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        self.drawDetectedObjects(frame, detectedObjects)

    def drawDetectedObjects(self, frame, objects):
        for (x, y, w, h) in objects:
            rectangle = Rectangle(frame, (x, y), (x+w, y+h))
            rectangle.draw()

            text = Text(frame, "Object", (x, y))
            text.draw()

class Rectangle:
    RECTANGLE_COLOR = (0, 255, 0)
    RECTANGLE_THICKNESS = 1

    def __init__(self, frame, rectangleVertex, rectangleOppositeVertex):
        self.frame = frame
        self.rectangleVertex = rectangleVertex
        self.rectangleOppositeVertex = rectangleOppositeVertex
        self.draw()

    def draw(self):
        cv2.rectangle(self.frame, self.rectangleVertex, self.rectangleOppositeVertex, self.RECTANGLE_COLOR, self.RECTANGLE_THICKNESS)

class Text:
    TEXT_FONT = cv2.FONT_HERSHEY_DUPLEX
    TEXT_COLOR = (255, 255, 255)
    TEXT_SCALE = 0.5
    TEXT_THICKNESS = 1

    def __init__(self, frame, text, position):
        self.frame = frame
        self.position = position
        self.text = text
        self.draw()

    def draw(self):
        cv2.putText(self.frame, self.text, self.position, self.TEXT_FONT, self.TEXT_SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)

App()
