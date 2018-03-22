from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pygame
import numpy as np
import os
import gtransform
from orient import orient
from drawlines import draw_lines


'''
STL Viewer Application

Application designed to open and display ASCII STL files for ME8720 at Clemson University
Allows viewing of wireframe and filled STL models and rotation and panning of the object

Evan Chodora, 2018
echodor@clemson.edu
'''


# Class to draw an STL object from an ASCII STL file
class DrawObject:
        pxarray = []  # Initialize the pixel array for the class

        def __init__(self):
                # Initiate new Loader class and run load_stl with the selected file
                self.model = Loader()
                self.model.load_stl(window.filename)

        # Function to plot the initial object after loading (runs the orient function)
        def initial_plot(self, loc):

                # Copy original geometry to new variable to be used for transformations
                self.model.coordinates, self.model.normals = self.model.geometry, self.model.normal
                # Apply perspective
                plot_geometry, camera = gtransform.perspective(persp.get(), self.model.coordinates, fz.get(), phi.get(),
                                                               theta.get())
                # Draw lines between points
                plot_geometry = draw_lines(plot_geometry, self.model.normals, camera, view.get(), embed_w, embed_h)

                # Clear pixel array to white and then change each pixel color based on the XY pixel map
                self.pxarray = pygame.PixelArray(loc)
                self.pxarray[:][:] = (255, 255, 255)
                for point in range(0, plot_geometry.shape[0]):
                        x = int(450 + plot_geometry[point, 0])
                        y = int(350 + plot_geometry[point, 1])
                        self.pxarray[x][y] = (0, 0, 0)
                # Plot pixel array to screen and refresh window/GUI
                pygame.surfarray.blit_array(loc, self.pxarray)
                pygame.display.flip()
                window.update()

        # Function to replot the object with a specified transformation/perspective
        def plot_transform(self, loc, transtype, perspective, data):

                if transtype == 'ortho':
                        # Transform original geometry according to the selected orthographic view
                        new_geometry, new_normals = gtransform.transform(self.model.geometry,
                                                                         self.model.normal, transtype,
                                                                         data)
                        # Draw lines between points
                        new_geometry = draw_lines(new_geometry, new_normals, [0, 0, 1], view.get(), embed_w,
                                                  embed_h)
                else:
                        # Transform geometry based on the selected transformation
                        self.model.coordinates, self.model.normals = gtransform.transform(self.model.coordinates,
                                                                                          self.model.normals, transtype,
                                                                                          data)
                        # Apply perspective
                        new_geometry, camera = gtransform.perspective(perspective, self.model.coordinates,
                                                                      fz.get(), phi.get(), theta.get())
                        # Draw lines between points
                        new_geometry = draw_lines(new_geometry, self.model.normals, camera,
                                                  view.get(), embed_w, embed_h)

                # Clear pixel array to white and then change each pixel color based on the XY pixel map
                self.pxarray[:][:] = (255, 255, 255)
                for point in range(0, new_geometry.shape[0]):
                        x = int(450 + new_geometry[point, 0])
                        y = int(350 + new_geometry[point, 1])
                        self.pxarray[x][y] = (0, 0, 0)
                # Plot pixel array to screen and refresh window/GUI
                pygame.surfarray.blit_array(loc, self.pxarray)
                pygame.display.flip()
                window.update()


# STL file loader class
class Loader:
        # Initialize class variables
        geometry = []
        normal = []
        name = []
        normal_face = []

        # Load ASCII STL File (no Binary STLs - based on project requirements)
        def load_stl(self, filename):
                self.geometry = []  # Clear previous geometry data
                self.name = []  # Clear previous STL model name
                self.normal = []  # Clear previous STL normal data
                fp = open(filename, 'r')  # Open selected file into memory

                # Loop over each line in the STL file
                for line in fp.readlines():
                        parts = line.split()
                        if len(parts) > 0:
                                # Start of filename, store filename
                                if parts[0] == 'solid':
                                        self.name = line[6:-1]
                                # Beginning of a new face - store normals and begin new triangle variable
                                if parts[0] == 'facet':
                                        triangle = []
                                        # Select face normal components (provided STLs had Y and Z reversed)
                                        self.normal_face = (float(parts[2]), -1*float(parts[4]), float(parts[3]), 1)
                                # Store all the vertex points in 'triangle'
                                if parts[0] == 'vertex':
                                        triangle.append((float(parts[1]), float(parts[2]), float(parts[3]), 1))
                                # End of face append new face to the model data
                                if parts[0] == 'endloop':
                                        self.geometry.append([triangle[0], triangle[1], triangle[2]])
                                        self.normal.append(self.normal_face)
                fp.close()
                # Convert lists to numpy arrays of the correct dimensions (Nx4 matrices)
                self.normal = np.asarray(self.normal).reshape((-1, 4))
                self.geometry = np.asarray(self.geometry).reshape((-1, 4))
                self.geometry = orient(self.geometry, embed_w, embed_h)  # Orient object geometry in screen space
                window.title("STL Viewer Application - " + self.name)  # Put filename in the GUI header


# Class to create a perspective settings popup dialog box for user input
class SettingsDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)  # Use Tkinter top for a separate popup GUI
        top.geometry("240x200")  # Window dimensions
        top.resizable(0, 0)  # Un-resizable
        top.title('Perspective settings')  # Window title
        self.DiLabel = Label(top, text='Dimetric Settings').place(x=50, rely=.05, anchor="c")
        self.fzLabel = Label(top, text='Fz').place(x=45, rely=.2, anchor="c")
        self.phiLabel = Label(top, text='Phi').place(x=45, rely=.5, anchor="c")
        self.thetaLabel = Label(top, text='Theta').place(x=45, rely=.65, anchor="c")
        self.TriLabel = Label(top, text='Trimetric Settings').place(x=50, rely=.35, anchor="c")
        self.fzBox = Entry(top)  # Fz entry box
        self.fzBox.place(x=140, rely=.2, anchor="c")
        self.fzBox.insert(0, fz.get())  # Prefill with Fz variable value
        self.phiBox = Entry(top)  # Phi entry box
        self.phiBox.place(x=140, rely=.5, anchor="c")
        self.phiBox.insert(0, phi.get())  # Prefill with Phi variable value
        self.thetaBox = Entry(top)  # Theta entry box
        self.thetaBox.place(x=140, rely=.65, anchor="c")
        self.thetaBox.insert(0, theta.get())  # Prefill with Theta variable value
        # Save button, runs command to store/send variables back to the main window space
        self.mySubmitButton = Button(top, text='Save', command=self.send).place(relx=.5, rely=.85, anchor="c")

    def send(self):
        # Update main window variables with those filled in the entry boxes
        fz.set(self.fzBox.get())
        phi.set(self.phiBox.get())
        theta.set(self.thetaBox.get())
        self.top.destroy()  # Destroy popup window and return to main window loop


def save_click():
        SettingsDialog(window)  # Create a new iteration of the popup window class


def file_select():
        # Function to select an STL file and store the path as "filename"
        window.filename = filedialog.askopenfilename(initialdir="C:\\", title="Select STL File",
                                                     filetypes=(("STL files", "*.STL"), ("All files", "*.*")))
        status_text = "Opened: " + window.filename  # Add file name to bottom status bar
        status.configure(text=status_text)
        file_select.stlobject = DrawObject()  # Create new stlobject class for the selected file
        DrawObject.initial_plot(file_select.stlobject, screen)  # Run initial object plot function for the class


def about_popup():
        # Info box about the software from the Help menu
        messagebox.showinfo('About STL Viewer',
                            'Created by Evan Chodora, 2018\n\n Designed to open and manipulate STL files')


# ****** Initialize Main Window ******	

window = Tk()
window.title('STL Viewer Application')  # Main window title
window.geometry("1200x800")  # Main overall window size
window.resizable(0, 0)  # Scaling disallowed in X and Y

# ****** Embed PyGame Window (Pixel Map Display) ******

embed_w = 900  # Width
embed_h = 700  # Height
embed = Frame(window, width=embed_w, height=embed_h)
embed.place(x=50, y=40)
# Set appropriate environment variables for embedding PyGame window in Tkinter GUI
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((embed_w, embed_h))
# Set embed screen to white and refresh the screen object and the GUI
screen.fill((255, 255, 255))
pygame.display.init()
pygame.display.flip()

# ****** Define Default Perspective Settings/View Type ******
persp = StringVar()
persp.set('iso')
view = StringVar()
view.set('hide')
phi = DoubleVar()
phi.set(45)
theta = DoubleVar()
theta.set(35)
fz = DoubleVar()
fz.set(0.375)

# ****** Toolbar ******

# Create main menu bar
menu = Menu(window, tearoff=False)
window.config(menu=menu)

# Create "File" submenu
subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open File", command=file_select)
subMenu.add_command(label="Exit", command=window.destroy)

# Create "Edit" submenu
subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=subMenu)
perspMenu = Menu(subMenu, tearoff=False)
subMenu.add_cascade(label="Change Perspective", menu=perspMenu)
perspMenu.add_radiobutton(label='Isometric', variable=persp, value='iso')  # Isometric projection
perspMenu.add_radiobutton(label='Dimetric', variable=persp, value='di')  # Dimetric projection
perspMenu.add_radiobutton(label='Trimetric', variable=persp, value='tri')  # Trimetric projection
viewMenu = Menu(subMenu, tearoff=False)
subMenu.add_cascade(label="View Type", menu=viewMenu)
viewMenu.add_radiobutton(label='Wireframe', variable=view, value='wire')  # Full wireframe
viewMenu.add_radiobutton(label='Hide Faces', variable=view, value='hide')  # Hide non-visible faces
viewMenu.add_radiobutton(label='Partial Hidden', variable=view, value='grey')  # Grey hidden lines
subMenu.add_command(label="Recenter Object", command=lambda: DrawObject.initial_plot(file_select.stlobject, screen))
subMenu.add_command(label="Perspective Settings", command=save_click)

# Create "View" submenu
subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="View", menu=subMenu)
subMenu.add_command(label="Top", command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                           'ortho', persp.get(), 'top'))
subMenu.add_command(label="Bottom", command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                              'ortho', persp.get(), 'bottom'))
subMenu.add_command(label="Left", command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                            'ortho', persp.get(), 'left'))
subMenu.add_command(label="Right", command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                             'ortho', persp.get(), 'right'))
subMenu.add_command(label="Front", command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                             'ortho', persp.get(), 'front'))
subMenu.add_command(label="Back", command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                            'ortho', persp.get(), 'back'))

# Create "Help" submenu
subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command=about_popup)

# ****** Control Panel ******

# Control text labels
rotate = Label(window, text="Rotate", font=("Helvetica", 16))
rotate.place(x=1075, rely=0.15, anchor="c")
zoom = Label(window, text="Zoom", font=("Helvetica", 16))
zoom.place(x=1075, rely=0.45, anchor="c")
pan = Label(window, text="Pan", font=("Helvetica", 16))
pan.place(x=1075, rely=0.65, anchor="c")

# Rotation buttons layout
rot_l = Button(window, text="<-", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                     'rotation', persp.get(), [2, -15]))
rot_l.place(x=1025, rely=.25, anchor="c")
rot_r = Button(window, text="->", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                     'rotation', persp.get(), [2, 15]))
rot_r.place(x=1125, rely=.25, anchor="c")
rot_u = Button(window, text="/\\", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                      'rotation', persp.get(),
                                                                                      [1, -15]))
rot_u.place(x=1075, rely=.2, anchor="c")
rot_d = Button(window, text="\\/", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                      'rotation', persp.get(), [1, 15]))
rot_d.place(x=1075, rely=.3, anchor="c")

# Zoom buttons layout
zoom_in = Button(window, text="+", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                      'zoom', persp.get(), [0.8]))
zoom_in.place(x=1025, rely=.5, anchor="c")
zoom_out = Button(window, text="-", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                       'zoom', persp.get(), [1.2]))
zoom_out.place(x=1125, rely=.5, anchor="c")

# Panning buttons layout
pan_l = Button(window, text="<-", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                     'translate', persp.get(),
                                                                                     [-20, 0, 0]))
pan_l.place(x=1025, rely=.75, anchor="c")
pan_r = Button(window, text="->", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                     'translate', persp.get(),
                                                                                     [20, 0, 0]))
pan_r.place(x=1125, rely=.75, anchor="c")
pan_u = Button(window, text="/\\", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                      'translate', persp.get(),
                                                                                      [0, -20, 0]))
pan_u.place(x=1075, rely=.7, anchor="c")
pan_d = Button(window, text="\\/", width=5, command=lambda: DrawObject.plot_transform(file_select.stlobject, screen,
                                                                                      'translate', persp.get(),
                                                                                      [0, 20, 0]))
pan_d.place(x=1075, rely=.8, anchor="c")

# ****** Keyboard Control Bindings ******

window.bind("<Left>", lambda event: DrawObject.plot_transform(file_select.stlobject, screen,
                                                              'rotation', persp.get(), [2, -15]))
window.bind("<Right>", lambda event: DrawObject.plot_transform(file_select.stlobject, screen,
                                                               'rotation', persp.get(), [2, 15]))
window.bind("<Up>", lambda event: DrawObject.plot_transform(file_select.stlobject, screen,
                                                            'rotation', persp.get(), [1, -15]))
window.bind("<Down>", lambda event: DrawObject.plot_transform(file_select.stlobject, screen,
                                                              'rotation', persp.get(), [1, 15]))

# ****** Status Bar ******

status = Label(window, text="Waiting...", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# ****** Run Main GUI Loop ******

window.mainloop()  # Main loop to run the GUI, waits for button input
