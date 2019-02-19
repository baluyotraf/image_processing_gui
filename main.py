import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk


class ImageFrame(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._image = None

        self.lbl_image = tk.Label(self)
        self.lbl_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

        # img = value.copy()
        # img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(value)
        self.lbl_image['image'] = img
        self.lbl_image.image = img


class ImageInfo(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._image = None

        self.lbl_labels = [
            tk.Label(self, text='Filename:'),
            tk.Label(self, text='Format:'),
            tk.Label(self, text='Mode:'),
            tk.Label(self, text='Size:'),
        ]

        self.lbl_values = [
            tk.Label(self, text='N/A'),
            tk.Label(self, text='N/A'),
            tk.Label(self, text='N/A'),
            tk.Label(self, text='N/A')
        ]

        for idx, lbl in enumerate(self.lbl_labels):
            lbl.grid(row=idx, column=0, sticky=(tk.N, tk.W))

        for idx, lbl in enumerate(self.lbl_values):
            lbl.grid(row=idx, column=1, sticky=(tk.N, tk.W))

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

        fn, fmt, md, sz = self.lbl_values
        fn['text'] = value.filename
        fmt['text'] = value.format
        md['text'] = value.mode
        sz['text'] = f'{value.width}x{value.height}'


class ImageProcessingApp(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.menubar = tk.Menu(master)
        master.configure(menu=self.menubar)

        self.menu_file = tk.Menu(self.menubar)
        self.menu_file.add_command(label='Open', command=self.process_image)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.image_info = ImageInfo(self, borderwidth=5, relief=tk.SOLID)
        self.image_info.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.W, tk.S))

        self.image_frame = ImageFrame(self, borderwidth=5, relief=tk.SOLID)
        self.image_frame.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.W, tk.S))

        ugrp = 'a'
        self.columnconfigure(0, weight=1, uniform=ugrp)
        self.columnconfigure(1, weight=1, uniform=ugrp)
        self.rowconfigure(0, weight=1)

    def process_image(self, *args, **kwargs):
        fn = filedialog.askopenfilename()
        try:
            img = Image.open(fn)
        except OSError:
            messagebox.showerror('Invalid Image File',
                                 'Please Specify a valid image file')
            return

        self.image_info.image = img
        self.image_frame.image = img


root = tk.Tk()
root.title('Image Processor')
root.option_add('*tearOff', tk.FALSE)
ipa = ImageProcessingApp(root, borderwidth=5, relief=tk.SOLID)
ipa.pack(fill=tk.BOTH, expand=tk.TRUE)

root.mainloop()
