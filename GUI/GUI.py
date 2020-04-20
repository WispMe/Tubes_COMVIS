import tkinter as tki
import cv2
from PIL import Image
from PIL import ImageTk

root = tki.Tk()

file = "hasil.PNG"

canvas = tki.Canvas(root, width = 300, height = 300)
canvas.pack()
img = tki.PhotoImage(file=file)
canvas.create_image(20,20, image=img)

frame2 = tki.LabelFrame(root)
current_row = 0

#create a label for databases entry
jb_label = tki.Label(frame2, text="Jenis Buku: ", font=18)
jb_label.grid(row=current_row, column=0)
jb_text = tki.StringVar()
jb_entry = tki.Entry(frame2, textvariable=jb_text, font=18)
jb_entry.grid(row=current_row, column=1)
current_row += 1

k_label = tki.Label(frame2, text="Kode: ", font=18)
k_label.grid(row=current_row, column=0)
k_text = tki.StringVar()
k_entry = tki.Entry(frame2, textvariable=k_text, font=18)
k_entry.grid(row=current_row, column=1)
current_row += 1

n_label = tki.Label(frame2, text="Nama Pengarang: ", font=18)
n_label.grid(row=current_row, column=0)
n_text = tki.StringVar()
n_entry = tki.Entry(frame2, textvariable=n_text, font=18)
n_entry.grid(row=current_row, column=1)
current_row += 1

p_label = tki.Label(frame2, text="Penerbit: ", font=18)
p_label.grid(row=current_row, column=0)
p_text = tki.StringVar()
p_entry = tki.Entry(frame2, textvariable=p_text, font=18)
p_entry.grid(row=current_row, column=1)
current_row += 1

ko_label = tki.Label(frame2, text="Kota: ", font=18)
ko_label.grid(row=current_row, column=0)
ko_text = tki.StringVar()
ko_entry = tki.Entry(frame2, textvariable=ko_text, font=18)
ko_entry.grid(row=current_row, column=1)
current_row += 1

t_label = tki.Label(frame2, text="Tahun: ", font=18)
t_label.grid(row=current_row, column=0)
t_text = tki.StringVar()
t_entry = tki.Entry(frame2, textvariable=t_text, font=18)
t_entry.grid(row=current_row, column=1)
current_row += 1

kol_text = tki.StringVar()
gab_label = tki.Message(frame2, textvariable=kol_text, font=18, width=500)
gab_label.grid(row=current_row)
current_row += 1
current_row += 1

frame2.pack(side="right", fill='y')
root.mainloop()