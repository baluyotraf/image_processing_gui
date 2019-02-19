from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk


root = Tk()
root.title("Image Processor")
root.option_add('*tearOff', FALSE)

content = ttk.Frame(root, width=600, height=300)
image_info = ttk.Frame(content, width=300, height=300,
                       borderwidth=1, relief='solid')
image_display = ttk.Frame(content, width=300, height=300,
                          borderwidth=1, relief='solid')
lbl_image = ttk.Label(image_display)
lbl_filename_l = ttk.Label(image_info, text='Filename:')
lbl_filename_v = ttk.Label(image_info, text='N/A')
lbl_format_l = ttk.Label(image_info, text='Format:')
lbl_format_v = ttk.Label(image_info, text='N/A')
lbl_mode_l = ttk.Label(image_info, text='Mode:')
lbl_mode_v = ttk.Label(image_info, text='N/A')
lbl_size_l = ttk.Label(image_info, text='Size:')
lbl_size_v = ttk.Label(image_info, text='N/A')


def process_image(*args, **kwargs):
    fn = filedialog.askopenfilename()
    try:
        img = Image.open(fn)
    except OSError:
        messagebox.showerror('Invalid Image File',
                             'Please Specify a valid image file')
        return

    lbl_filename_v['text'] = img.filename
    lbl_format_v['text'] = img.format
    lbl_mode_v['text'] = img.mode
    lbl_size_v['text'] = f'{img.width}x{img.height}'

    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    lbl_image['image'] = img
    lbl_image.image = img


menubar = Menu(root)
root['menu'] = menubar

menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menu_file.add_command(label='Open', command=process_image)


content.grid(row=0, column=0)
content.grid_propagate(0)
image_info.grid(row=0, column=0)
image_info.grid_propagate(0)

lbl_filename_l.grid(row=0, column=0, sticky=(N, W))
lbl_filename_v.grid(row=0, column=1, sticky=(N, W))

lbl_format_l.grid(row=1, column=0, sticky=(N, W))
lbl_format_v.grid(row=1, column=1, sticky=(N, W))

lbl_mode_l.grid(row=2, column=0, sticky=(N, W))
lbl_mode_v.grid(row=2, column=1, sticky=(N, W))

lbl_size_l.grid(row=3, column=0, sticky=(N, W))
lbl_size_v.grid(row=3, column=1, sticky=(N, W))

image_display.grid(row=0, column=1)
image_display.grid_propagate(0)
lbl_image.place(relx=0.5, rely=0.5, anchor='center')


root.mainloop()
