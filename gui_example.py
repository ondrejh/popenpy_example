from tkinter import *

root = Tk()

def callback():
    print('click!')

b = Button(root, text="OK", command=callback)
b.pack()

listbox = Listbox(root)
listbox.pack(fill=BOTH, expand=1)

for i in range(20):
    listbox.insert(END, str(i))

mainloop()
