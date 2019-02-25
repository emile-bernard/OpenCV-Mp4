import tkinter as tk

class ParamsForm:
    def __init__(self, parent, model):
        self.parent = parent
        self.model = model
        self.draw()

    def draw(self):
        fields = 'Image scale factor', 'Min neighbors'
        entries = self.makeform(self.parent, fields)
        self.parent.bind('<Return>', (lambda event, e=entries: fetch(e)))
        enterButton = tk.Button(self.parent, text='Enter', command=(lambda e=entries: self.enterParams(e)))
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
