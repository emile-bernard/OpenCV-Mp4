import cv2
import sys
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title = 'Counting Seconds'
        self.pretrainedFaceClassifier = cv2.CascadeClassifier("./assets/model/haarcascade_frontalface_alt.xml")
        self.videoCapture = VideoCapture("./assets/video/cumbia_960x540.mp4")

        self.drawMenu()
        self.drawCanvas()
        self.drawButton()

        self.updateDelay = 15
        self.update()

        self.window.mainloop()

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

    def drawCanvas(self):
        self.canvas = tk.Canvas(self.window, width = self.videoCapture.width, height = self.videoCapture.height)
        self.canvas.pack()

    def drawButton(self):
        self.btn = tk.Button(self.window, text="Take a snapshot", width=50, command=self.snapshot)
        self.btn.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        ret, frame = self.videoCapture.get_frame()
        if ret:
            self.detectFaces(frame)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.updateDelay, self.update)

    def detectFaces(self, frame):
        colorSpace = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detectedObjects = self.pretrainedFaceClassifier.detectMultiScale(
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

    def snapshot(self):
        ret, frame = self.videoCapture.get_frame()
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

    def get_frame(self):
        if self.videoCapture.isOpened():
            ret, frame = self.videoCapture.read()
            if ret:
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

App()
