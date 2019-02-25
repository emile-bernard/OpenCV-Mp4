import tkinter as tk

class ParamsForm:
    ENTER_BTN_X_PADDING = 5
    ENTER_BTN_Y_PADDING = 5

    ENTRY_FIELD_X_PADDING = 5
    ENTRY_FIELD_Y_PADDING = 5

    LABEL_WIDTH = 15

    def __init__(self, parent, model):
        self.parent = parent
        self.model = model
        self.draw()

    def draw(self):
        fields = 'Image scale factor', 'Min neighbors'
        entries = self.makeform(self.parent, fields)
        self.parent.bind('<Return>', (lambda event, e=entries: fetch(e)))
        enterButton = tk.Button(self.parent, text='Enter', command=(lambda e=entries: self.enterParams(e)))
        enterButton.pack(side=tk.LEFT, padx=self.ENTER_BTN_X_PADDING, pady=self.ENTER_BTN_Y_PADDING)

    def enterParams(self, entries):
        self.model.setImageScaleFactor(float(entries[0][1].get()))
        self.model.setCanditateRectangleMinNeighbors(int(entries[1][1].get()))

    def makeform(self, root, fields):
        entries = []
        for field in fields:
            row = tk.Frame(root)
            label = tk.Label(row, width=self.LABEL_WIDTH, text=field, anchor='w')
            entry = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=self.ENTRY_FIELD_X_PADDING, pady=self.ENTRY_FIELD_Y_PADDING)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, entry))
        return entries
