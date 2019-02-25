import tkinter as tk
from videoCapture import VideoCapture

class VideoListBox:
    LISTBOX_WIDTH = 30
    LISTBOX_HEIGHT = 40

    def __init__(self, parent, videoCapture, videoFiles):
        self.videoListBox = tk.Listbox(parent)
        self.videoCapture = videoCapture
        self.videoFiles = videoFiles
        self.draw()

    def draw(self):
        self.videoListBox.config(width = self.LISTBOX_WIDTH, height = self.LISTBOX_HEIGHT)

        for videoFile in self.videoFiles:
            self.videoListBox.insert(tk.END, videoFile[0])

        self.videoListBox.bind('<<ListboxSelect>>', self.videoListBoxSelectionChanged)
        self.videoListBox.select_set(0) #Sets focus on the first item.
        self.videoListBox.event_generate("<<ListboxSelect>>")
        self.videoListBox.pack(side = "left")

    def videoListBoxSelectionChanged(self, *args):
        isSelectedPath, selectedVideoPath = self.getSelectedVideoPath()
        if(isSelectedPath):
            self.videoCapture.setVideoPath(selectedVideoPath)

    def getSelectedVideoPath(self):
        try:
            curentSelection = self.videoListBox.curselection()[0]
            return (True, self.videoFiles[curentSelection][1])
        except:
            return (False, None)

    def getSelectedVideoName(self):
        curentSelection = self.videoListBox.curselection()[0]
        return self.videoFiles[curentSelection][0]
