from tkinter import *
from tkinter import ttk
import tkinter_func
import camera_func
from PIL import ImageTk,Image
import threading
import time

images_flash = [] #flash storage for stl images in stl explorer



#Creating the root
root = Tk()
root.title("STL Identifier database")
root.geometry('1920x1080')




#Creating the frame
frame = Frame(root, width = 620, height = 930, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

#Creating Textbox for stl file explorer path
text_stl_path = Text(root, height=1, width=20)
text_stl_path.place(x = 1260, y = 10 , anchor = NW)
text_stl_path.insert(INSERT, "stl_files/")

#Creating the scrollbar
yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

#Creating the canvas
canvas = Canvas(frame, width = 620, height = 910, bd=0, yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
canvas.configure(yscrollcommand=yscrollbar.set)

#create selected frame & canvas
selected_frame = Frame(root, width = 100, height = 200, relief=SUNKEN)
selected_frame.grid_rowconfigure(0, weight=1)
selected_frame.grid_columnconfigure(0, weight=1)

selected_scrollbar = Scrollbar(selected_frame)
selected_scrollbar.grid(row=0, column=1, sticky=N+S)

selected_canvas = Canvas(selected_frame, width = 300, height = 200, bd=0, yscrollcommand = selected_scrollbar.set)
selected_canvas.grid(row=0, column=0, sticky=N+S+E+W)
selected_canvas.configure(yscrollcommand= selected_scrollbar.set)

#Creating the stl viewer 
label_viewer = Label(root, width = 400, height = 400) # label for the first vtk window
label_viewer.place(x = 10,y = 10,anchor = NW)

label_viewer2 = Label(root, width = 400, height = 400) #Label for the second vtk window
label_viewer2.place(x = 420,y = 10,anchor = NW)


#Create labels for vtk viewer state
todisplay_xyz = 'camera 1  x:   ' + str(round(tkinter_func.camera_location[0][0],1)) + '  y:  ' + str(round(tkinter_func.camera_location[0][1],1)) + '  z:  ' + str(round(tkinter_func.camera_location[0][2],1))
label_xyz = Label(root, width = 40, height = 1, fg="black", font=("Helvetica", 12), text = todisplay_xyz, anchor = 'w') #Label that display xyz of camera 1
label_xyz.place(x = 850,y = 10,anchor = NW)

todisplay_xyz_2 = 'camera 2  x:   ' + str(round(tkinter_func.camera_location[1][0],1)) + '  y:  ' + str(round(tkinter_func.camera_location[1][1],1)) + '  z:  ' + str(round(tkinter_func.camera_location[1][2],1))
label_xyz2 = Label(root, width = 40, height = 1, fg="black", font=("Helvetica", 12), text = todisplay_xyz_2, anchor = 'w') #Label that display xyz of camera 2
label_xyz2.place(x = 850,y = 35,anchor = NW)


todisplay_actor = 'actor color:   ' + str(round(tkinter_func.actor_color[0],3)) + ',  ' +  str(round(tkinter_func.actor_color[1],3)) + ',  ' + str(round(tkinter_func.actor_color[2],3))
label_actor_color = Label(root, width = 40, height = 1, fg="black", font=("Helvetica", 12), text = todisplay_actor, anchor = 'w') #Label that display color of actor
label_actor_color.place(x = 850,y = 60,anchor = NW)

todisplay_background = 'background color:   ' + str(round(tkinter_func.background_color[0],3)) + ',  ' + str(round(tkinter_func.background_color[0],3)) + ',  ' + str(round(tkinter_func.background_color[0],3))
label_background_color = Label(root, width = 40, height = 1, fg="black", font=("Helvetica", 12), text = todisplay_background, anchor = 'w') #Label that display color of background
label_background_color.place(x = 850,y = 85,anchor = NW)

#Stl viewer & Camera viewer
viewer1 = tkinter_func.stl_viewer(label_viewer,label_viewer2)
viewer1.add_stl("stl_files/keyboard.stl")

a = tkinter_func.menubar(root,viewer1,label_actor_color,label_background_color,label_xyz,label_xyz2)

#Creating button for updating stl explorer
image_store = []
explorer1 = tkinter_func.stl_explorer(canvas,120,selected_canvas)
btn_update = Button(root, text='update', command= lambda: explorer1.create_stl_image(3,text_stl_path.get("1.0",'end-1c'),tkinter_func.stl_file_list,image_store))
btn_update.place(x = 1440, y = 5 , anchor = NW)





#Creating callback for mouse click
def callback(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    index = canvas.find_closest(x, y)[0]
    if index%2 == 1:
        index = int((index+1)/2)
    else:
        index = int(index/2) 
    viewer1.add_stl(tkinter_func.stl_file_list[index-1])
    viewer1.get_output2()

def callback_selected(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    index = canvas.find_closest(x, y)[0]
    if index%2 == 1:
        index = int((index+1)/2)
    else:
        index = int(index/2) 
    explorer1.add_selected(index)

def on_mousewheel(event):
    viewer1.zoom(-1*(event.delta/2400))
    #print(event.delta)

def scroll_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

lastx,lasty = 0 , 0

def func(event):
    global lastx
    global lasty
    x,y = event.x,event.y
    if lastx == 0 and lasty == 0:
        lastx,lasty = x,y
    if abs(x-lastx) > 5 or abs(y-lasty) > 5:
        if abs(lasty - y) < 20 and abs(lastx-x) < 20:
            #print(lastx-x,y-lasty)
            viewer1.spherical_rotation(lastx-x,lasty-y)
        lastx = x
        lasty = y


canvas.bind("<Button-1>", callback)
canvas.bind("<Button-3>", callback_selected)
canvas.bind("<MouseWheel>", scroll_mousewheel)
#label_viewer.bind("<Button-1>", callback2)
label_viewer.bind("<MouseWheel>", on_mousewheel)
label_viewer.bind("<B1-Motion>",func)
label_viewer2.bind("<B1-Motion>",func)

#Configure the scrollbar and canvas
yscrollbar.config(command=canvas.yview)
canvas.config(scrollregion=canvas.bbox(ALL))

#frame.pack()
frame.place(x = 1260,y = 40, anchor = NW)
selected_frame.place(x = 850, y = 200, anchor = NW)

root.mainloop()




