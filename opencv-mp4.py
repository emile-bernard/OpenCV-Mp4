import cv2
import sys
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

class App:
    def __init__(self):
        self.model = Model("./assets/model/haarcascade_frontalface_alt.xml")
        self.videoCapture = VideoCapture("./assets/video/cumbia_960x540.mp4")

        self.window = tk.Tk()
        self.window.title = "OpenCV mp4"

        self.drawClassifierInput()
        # self.drawMenu()
        self.drawModelList()
        self.drawCanvas()
        self.drawButton()

        self.updateDelay = 15
        self.update()

        self.window.mainloop()

    def drawClassifierInput(self):
        tk.Label(self.window, text = "Scale Factor").pack(fill = tk.X)
        tk.Label(self.window, text = "Min Neighbors").pack(fill = tk.X)

        scaleFactorEntry = tk.Entry(self.window).pack(fill = tk.X)
        minNeighborsEntry = tk.Entry(self.window).pack(fill = tk.X)

    def drawMenu(self):
        self.menuButton = tk.Menubutton(self.window, text = "Menu Button")
        self.menuButton.grid()
        self.menuButton.menu = tk.Menu(self.menuButton, tearoff = 0)
        self.menuButton["menu"] = self.menuButton.menu
        cVar  = 0
        aVar = 0
        self.menuButton.menu.add_checkbutton(label = 'Contact', variable = cVar)
        self.menuButton.menu.add_checkbutton(label = 'About', variable = aVar)
        self.menuButton.pack()

    def drawModelList(self):
        self.listBox = tk.Listbox(self.window)
        self.listBox.insert(1, "Smile")

        self.listBox.insert(2, "Eye Tree Eye Glasses")
        self.listBox.insert(3, "Eye")
        self.listBox.insert(4, "Left Eye 2 Splits")
        self.listBox.insert(5, "Right Eye 2 Splits")

        self.listBox.insert(6, "Frontal Cat Face Extended")
        self.listBox.insert(7, "Frontal Cat Face")

        self.listBox.insert(8, "Frontal Face Alt Tree")
        self.listBox.insert(9, "Frontal Face Alt")
        self.listBox.insert(10, "Frontal Face Alt 2")
        self.listBox.insert(11, "Frontal Face Default")
        self.listBox.insert(12, "Profile Face")

        self.listBox.insert(13, "Full Body")
        self.listBox.insert(14, "Lower Body")
        self.listBox.insert(15, "Upper Body")

        self.listBox.insert(16, "Licence Plate Rus 16 Stages")
        self.listBox.insert(17, "Russian Plate Number")

        # self.listBox.pack(fill = tk.X)
        self.listBox.pack(side = "left", fill = tk.Y)

    def drawCanvas(self):
        self.canvas = tk.Canvas(self.window, width = self.videoCapture.width, height = self.videoCapture.height)
        self.canvas.pack()

    def drawButton(self):
        self.btn = tk.Button(self.window, text="Take a snapshot", width=50, command=self.snapshot)
        self.btn.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        ret, frame = self.videoCapture.getFrame()
        if ret:
            self.model.detectFaces(frame)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.updateDelay, self.update)

    def snapshot(self):
        ret, frame = self.videoCapture.getFrame()
        if ret:
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
            ret, frame = self.videoCapture.read()
            if ret:
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

class Model:
    def __init__(self, classifierPath):
        self.classifier = cv2.CascadeClassifier(classifierPath)

    def detectFaces(self, frame):
        colorSpace = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detectedObjects = self.classifier.detectMultiScale(
            colorSpace,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        self.drawRectagle(frame, detectedObjects)

    def drawRectagle(self, frame, objects):
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

App()
