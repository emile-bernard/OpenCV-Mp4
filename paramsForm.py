import tkinter as tk

class LabeledEntry(tk.Entry):
    def __init__(self, master=None, label="Search", **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.label = label
        self.on_exit()
        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)

    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, tk.END)

    def on_exit(self, event=None):
        if not self.get():
            self.insert(0, self.label)

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
        entries = self.makeform(self.parent)
        self.parent.bind('<Return>', (lambda event, e=entries: fetch(e)))
        enterButton = tk.Button(self.parent, text='Enter', command=(lambda e=entries: self.enterParams(e)))
        enterButton.pack(side=tk.LEFT, padx=self.ENTER_BTN_X_PADDING, pady=self.ENTER_BTN_Y_PADDING)

    def enterParams(self, entries):
        self.model.setImageScaleFactor(round(float(entries[0][1].get()), 2))
        self.model.setCanditateRectangleMinNeighbors(round(int(entries[1][1].get())))

    def makeform(self, root):
        entries = []
        scaleFactorRow = tk.Frame(root)
        scaleFactorLabel = tk.Label(scaleFactorRow, width=self.LABEL_WIDTH, text="Image scale factor", anchor='w')
        scaleFactorEntry = tk.Entry(scaleFactorRow)
        scaleFactorEntry = LabeledEntry(scaleFactorRow, label=self.model.getImageScaleFactor())
        scaleFactorEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        scaleFactorRow.pack(side=tk.TOP, fill=tk.X, padx=self.ENTRY_FIELD_X_PADDING, pady=self.ENTRY_FIELD_Y_PADDING)
        scaleFactorLabel.pack(side=tk.LEFT, expand=tk.NO, fill=tk.X)
        entries.append(("Image scale factor", scaleFactorEntry))

        minNeighborsRow = tk.Frame(root)
        minNeighborsLabel = tk.Label(minNeighborsRow, width=self.LABEL_WIDTH, text="Min neighbors", anchor='w')
        minNeighborsEntry = tk.Entry(minNeighborsRow)
        minNeighborsEntry = LabeledEntry(minNeighborsRow, label=self.model.getCanditateRectangleMinNeighbors())
        minNeighborsEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        minNeighborsRow.pack(side=tk.TOP, fill=tk.X, padx=self.ENTRY_FIELD_X_PADDING, pady=self.ENTRY_FIELD_Y_PADDING)
        minNeighborsLabel.pack(side=tk.LEFT)
        minNeighborsEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append(("Min neighbors", minNeighborsEntry))

        return entries
