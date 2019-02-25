import tkinter as tk
from model import Model

class ModelListBox:
    def __init__(self, parent, model, modelFiles):
        self.parent = parent
        self.model = model
        self.modelFiles = modelFiles
        self.draw()

    def draw(self):
        self.modelListBox = tk.Listbox(self.parent)
        self.modelListBox.config(width = 40, height = 40)

        for modelFile in self.modelFiles:
            self.modelListBox.insert(tk.END, modelFile[0])

        self.modelListBox.bind('<<ListboxSelect>>', self.modelListBoxSelectionChanged)
        self.modelListBox.select_set(0) #Sets focus on the first item.
        self.modelListBox.event_generate("<<ListboxSelect>>")
        self.modelListBox.pack(side = "left")

    def modelListBoxSelectionChanged(self, *args):
        isSelectedPath, selectedModelPath = self.getSelectedModelPath()
        if(isSelectedPath):
            self.model = Model(selectedModelPath)

    def getSelectedModelPath(self):
        try:
            curentSelection = self.modelListBox.curselection()[0]
            return (True, self.modelFiles[curentSelection][1])
        except:
            return (False, None)
