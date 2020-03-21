from vtk.util.numpy_support import vtk_to_numpy
import vtk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os
import math

class stl_explorer():
    def __init__(self,canvas,size):
        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.SetSize(size,size)
        self.renWin.AddRenderer(self.ren)
        self.renWin.OffScreenRenderingOn()
        
        #set color for the renderer
        self.ren.SetBackground(0.1, 0.1, 0.1)
        self.canvas = canvas
        self.actor = vtk.vtkActor()
        
        #Set up camera components
        self.camera = vtk.vtkCamera()
        self.ren.SetActiveCamera(self.camera)
        self.camera.SetPosition(300,300,300)
        
        #Set up screenshot components
        self.stlreader = vtk.vtkSTLReader()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.stlreader.GetOutputPort())

    def screenshot(self):
        vtk_win_im = vtk.vtkWindowToImageFilter()
        vtk_win_im.SetInput(self.renWin)
        vtk_win_im.Update()
        vtk_image = vtk_win_im.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        return vtk_to_numpy(vtk_array).reshape(height, width, components)

    def stl_to_np(self,stl_path,stl_list):
        self.flash_image = []
        for filenames in os.listdir(stl_path):
            if filenames[len(filenames)-4:len(filenames)] == ".stl":
                self.stlreader.SetFileName(stl_path+filenames)
                stl_list.append(stl_path+filenames)
                self.actor.SetMapper(self.mapper)
                # color the actor
                self.actor.GetProperty().SetColor(0.8,0.8,0.8) # (R,G,B)
                self.ren.AddActor(self.actor)
                x,y,z = self.actor.GetCenter()
                self.camera.SetFocalPoint(x,y,z)
                self.flash_image.append(self.screenshot())

    def create_stl_image(self,per_row,stl_list):
        self.image_store = []
        if (type(self.canvas) == 'tkinter.Canvas'):
            canvas_w = self.canvas.winfo_width()
            img_size = int((canvas_w-5)/per_row)
            self.renWin.SetSize(img_size-5,img_size-5)
            stl_to_np('stl_files/',stl_list)
            for n in range(len(self.flash_image)):
                np_img = cv2.cvtColor(self.flash_image[n],cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(np_img)
                imgtk = ImageTk.PhotoImage(image=im_pil) 
                col = n%per_row
                row = divmod(n,per_row)[0]
                if col == 0:
                    col = per_row
                self.canvas.create_image(col*img_size+5,row*img_size+5,image=imgtk, anchor=NW)
                self.image_store.append(imgtk)
                self.canvas.config(scrollregion=can.bbox(ALL))
        else:    
            print("!!ERROR: Input canvas is not a tkinter.canvas object, unable to create image")






def screenshot(renderwindow):
    vtk_win_im = vtk.vtkWindowToImageFilter()
    vtk_win_im.SetInput(renderwindow)
    vtk_win_im.Update()
    vtk_image = vtk_win_im.GetOutput()
    width, height, _ = vtk_image.GetDimensions()
    vtk_array = vtk_image.GetPointData().GetScalars()
    components = vtk_array.GetNumberOfComponents()
    return vtk_to_numpy(vtk_array).reshape(height, width, components)

def stl_to_np(stl_path,stl_list):
    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(120,120)
    renWin.AddRenderer(ren)
    renWin.OffScreenRenderingOn()
    #set color for the renderer
    ren.SetBackground(0.1, 0.1, 0.1)

    camera = vtk.vtkCamera()
    ren.SetActiveCamera(camera)
    camera.SetPosition(300,300,00)

    output = []
    actor = vtk.vtkActor()
    for filenames in os.listdir(stl_path):
        if filenames[len(filenames)-4:len(filenames)] == ".stl":
            #Read STL file
            stlreader = vtk.vtkSTLReader()
            stlreader.SetFileName(stl_path+filenames)
            stl_list.append(stl_path+filenames)
            print(stl_path+filenames)
            # mapper
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(stlreader.GetOutputPort())
            # actor

            actor.SetMapper(mapper)
            # color the actor
            actor.GetProperty().SetColor(0.8,0.8,0.8) # (R,G,B)
            x,y,z = actor.GetCenter()
            camera.SetFocalPoint(x,y,z)
            ren.AddActor(actor)
            output.append(screenshot(renWin))
    return output

def add_stl_images_to_canvas(can,stl_path,stl_list,image_store):
    images_np = stl_to_np(stl_path,stl_list)
    num = len(images_np)
    gap = 20
    per_row = 5
    num_col = int((num-(num%per_row))/per_row)
    img_size = 600/per_row
    imagelist = []

    for n in range(num):
        proc = cv2.resize(images_np[n],(int(img_size*0.9),int(img_size*0.9)))
        proc = cv2.cvtColor(proc,cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(proc)
        imgtk = ImageTk.PhotoImage(image=im_pil) 
        imagelist.append(imgtk)
    for n in range(num):
        col = n%per_row
        row = divmod(n,per_row)[0]
        if col == per_row:
            col = per_row
        can.create_image(col*img_size+gap,row*img_size+gap+gap,image=imagelist[n], anchor=NW)
        image_store.append(imagelist[n])
    can.config(scrollregion=can.bbox(ALL))
    """
    for y in range(row):
        for x in range(per_row):
            imagetk = imagelist[y*per_row+x]
            can.create_image(gap+x*(img_size+gap),gap+y*(img_size+gap),image=imagetk, anchor=NW)
            image_store.append(imgtk)
    """