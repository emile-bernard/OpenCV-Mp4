import tkinter as tk
from videoCapture import VideoCapture

class VideoListBox:
    def __init__(self, parent, videoCapture, videoFiles):
        self.parent = parent
        self.videoCapture = videoCapture
        self.videoFiles = videoFiles
        self.draw()

    def draw(self):
        self.videoListBox = tk.Listbox(self.parent)
        self.videoListBox.config(width = 30, height = 40)

        for videoFile in self.videoFiles:
            self.videoListBox.insert(tk.END, videoFile[0])

        self.videoListBox.bind('<<ListboxSelect>>', self.videoListBoxSelectionChanged)
        self.videoListBox.select_set(0) #Sets focus on the first item.
        self.videoListBox.event_generate("<<ListboxSelect>>")
        self.videoListBox.pack(side = "left")

    def videoListBoxSelectionChanged(self, *args):
        isSelectedPath, selectedVideoPath = self.getSelectedVideoPath()
        if(isSelectedPath):
            self.videoCapture = VideoCapture(selectedVideoPath)

    def getSelectedVideoPath(self):
        try:
            curentSelection = self.videoListBox.curselection()[0]
            return (True, self.videoFiles[curentSelection][1])
        except:
            return (False, None)
