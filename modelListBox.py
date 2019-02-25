import tkinter as tk

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
        self.model = Model(self.getSelectedModelPath())

    def getSelectedModelPath(self):
        curentSelection = self.modelListBox.curselection()[0]
        return self.modelFiles[curentSelection][1]
