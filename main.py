import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk


class ImageFrame(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._image = None
        self.bind('<Configure>', self.on_resize)

        self.lbl_image = tk.Label(self)
        self.lbl_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _resize_image(self, img):
        size = (
            self.winfo_width(),
            self.winfo_height(),
        )

        img = img.copy()
        img.thumbnail(size)

        return img

    def _set_display_image(self, img):
        img = self._resize_image(img)
        img = ImageTk.PhotoImage(img)
        self.lbl_image['image'] = img
        self.lbl_image.image = img

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self._set_display_image(value)

    def on_resize(self, *args, **kwargs):
        if self._image is not None:
            self._set_display_image(self._image)


class ImageInfo(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._image = None
        self.bind('<Configure>', self.on_resize)

        self.lbl_labels = [
            ttk.Label(self, text='Filename:'),
            ttk.Label(self, text='Format:'),
            ttk.Label(self, text='Mode:'),
            ttk.Label(self, text='Size:'),
        ]

        self.lbl_values = [
            ttk.Label(self),
            ttk.Label(self),
            ttk.Label(self),
            ttk.Label(self),
        ]

        for idx, lbl in enumerate(self.lbl_labels):
            lbl.grid(row=idx, column=0, sticky=(tk.N, tk.W))

        for idx, lbl in enumerate(self.lbl_values):
            lbl.configure(text='N/A', justify=tk.LEFT)
            lbl.grid(row=idx, column=1, sticky=(tk.N, tk.W, tk.E))

        self.columnconfigure(1, weight=1)

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

    def on_resize(self, *args, **kwargs):
        for lbl in self.lbl_values:
            length = lbl.winfo_width()
            lbl['wraplength'] = length - 10


class ImageProcessingApp(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.menubar = tk.Menu(master)
        master.configure(menu=self.menubar)

        self.menu_file = tk.Menu(self.menubar)
        self.menu_file.add_command(label='Open', command=self.process_image)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.image_info = ImageInfo(self)
        self.image_info.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.W, tk.S))

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.W, tk.S))

        self.columnconfigure(0, minsize=200)
        self.columnconfigure(1, weight=1)
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
root.minsize(width=900, height=450)
ipa = ImageProcessingApp(root)
ipa.pack(fill=tk.BOTH, expand=tk.TRUE)

root.mainloop()
