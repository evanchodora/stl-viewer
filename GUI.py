from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def test():
	print("Button Clicked")

def file_select():
        # Function to select an STL file and store the path as "filename"
        window.filename = filedialog.askopenfilename(initialdir = "C:\\", title = "Select STL File", filetypes = (("STL files","*.STL"),("All files","*.*")))
        print(window.filename)
        status_text = "Opened: " + window.filename
        status.configure(text=status_text)
	
def about_popup():
        # Info box about the software from Help menu
	messagebox.showinfo('About STL Viewer',
		'Created by Evan Chodora, 2018\n\n Designed to open and manipulate STL files')

# ****** Initialize Main Window ******	

window = Tk()
window.title('STL Viewer Application')
window.geometry("1200x800") #Main overall window size
window.resizable(0, 0) #Scaling disallowed in X and Y

# ****** Toolbar ******

# Create main menu bar
menu = Menu(window, tearoff = False)
window.config(menu=menu)

# Create "File" submenu
subMenu = Menu(menu, tearoff = False)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open File", command = file_select)
subMenu.add_command(label="Exit", command = window.destroy)

# Create "Edit" submenu
subMenu = Menu(menu, tearoff = False)
menu.add_cascade(label="Edit", menu=subMenu)
subMenu.add_command(label="Change Perspective", command = test)

# Create "Help" submenu
subMenu = Menu(menu, tearoff = False)
menu.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command = about_popup)

# ****** Control Panel ******

# Control labels
rotate = Label(window, text="Rotate", font=("Helvetica", 16))
rotate.place(x=1100, rely=0.15, anchor="c")
zoom = Label(window, text="Zoom", font=("Helvetica", 16))
zoom.place(x=1100, rely=0.45, anchor="c")
pan = Label(window, text="Pan", font=("Helvetica", 16))
pan.place(x=1100, rely=0.65, anchor="c")

# Rotation buttons layout
rot_l = Button(window, text="<-", width=5, command=test)
rot_l.place(x=1050, rely=.25, anchor="c")
rot_r = Button(window, text="->", width=5, command=test)
rot_r.place(x=1150, rely=.25, anchor="c")
rot_u = Button(window, text="/\\", width=5, command=test)
rot_u.place(x=1100, rely=.2, anchor="c")
rot_d = Button(window, text="\\/", width=5, command=test)
rot_d.place(x=1100, rely=.3, anchor="c")

# Zoom buttons layout
zoom_in = Button(window, text="+", width=5, command=test)
zoom_in.place(x=1050, rely=.5, anchor="c")
zoom_out = Button(window, text="-", width=5, command=test)
zoom_out.place(x=1150, rely=.5, anchor="c")

# Panning buttons layout
pan_l = Button(window, text="<-", width=5, command=test)
pan_l.place(x=1050, rely=.75, anchor="c")
pan_r = Button(window, text="->", width=5, command=test)
pan_r.place(x=1150, rely=.75, anchor="c")
pan_u = Button(window, text="/\\", width=5, command=test)
pan_u.place(x=1100, rely=.7, anchor="c")
pan_d = Button(window, text="\\/", width=5, command=test)
pan_d.place(x=1100, rely=.8, anchor="c")

# ****** Status Bar ******

status = Label(window, text="Waiting...", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# ****** Run Main GUI Loop ******

window.mainloop()
