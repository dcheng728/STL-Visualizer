from vtk.util.numpy_support import vtk_to_numpy
import threading
import random
import vtk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os
import math
import time
import numpy as np

stl_file_list = []

actor_color = [0.5,0.5,0.5]
background_color = [0.94,0.94,0.94]
#background_color = [0.5,0.5,0.5]

camera_location = []

np_images = []

cam1_image = []
cam2_image = []
cam1_label = []
cam2_label = []

camera_location.append([970,-650,500])
camera_location.append([970,650,500])
class_names = []
pi = 3.14159265359

selected_path = []

class stl_viewer():
    global actor_color
    global background_color

    def __init__(self,Label,Label2):
    #Initializes window, renderer, label, actor, camera
        self.label = Label
        self.label2 = Label2

        self.ren = vtk.vtkRenderer()

        self.renWin = vtk.vtkRenderWindow()
        self.renWin.SetSize(400,400)
        self.renWin.AddRenderer(self.ren)
        self.renWin.OffScreenRenderingOn()

        #set color for the renderer
        self.ren.SetBackground(background_color[0], background_color[1], background_color[2])
        self.camera = vtk.vtkCamera()
        self.camera.SetThickness(10000)
        self.ren.SetActiveCamera(self.camera)
        self.camera.SetPosition(camera_location[0][0],camera_location[0][1],camera_location[0][2])
        #self.camera.SetRoll(90)
        self.actor = vtk.vtkActor()

    #Defines light attributes
        self.light1 = vtk.vtkLight()
        self.light1.PositionalOn()
        self.light1.SetColor(0.9,0.9,0.9)
        self.light1.SetPosition(0,-200,700)
        self.light1.SetFocalPoint(0,-200,0)
        self.light1.SetIntensity(1.0)

        self.light2 = vtk.vtkLight()
        self.light2.PositionalOn()
        self.light2.SetColor(0.9,0.9,0.9)
        self.light2.SetPosition(0,200,700)
        self.light2.SetFocalPoint(0,200,0)
        self.light2.SetIntensity(1.0)

        self.ren.AddLight(self.light1)
        self.ren.AddLight(self.light2)

    def angle(self,point1, point2):
        """
        inputs two points in list format
        returns the angle between these two points in degrees
        """
        d1 = math.sqrt(point1[0]**2+point1[1]**2+point1[2]**2)
        d2 = math.sqrt(point2[0]**2+point2[1]**2+point2[2]**2)

        point3 = [point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]]
        d3 = math.sqrt(point3[0]**2+point3[1]**2+point3[2]**2)

        thing = (d1*d1 + d2*d2 - d3*d3)/(2*d1*d2)
        if thing > 1:
            thing = 2-thing
        try:
            angle = math.acos(thing)
            return angle*180/pi
        except:
            print(thing)
            print('d1 ' + str(d1))
            print('d2 ' + str(d2))
            print('p1 ' + str(point1))
            print('p2 ' + str(point2))
    
    def find_supp(self,point):
        d = math.sqrt(point[0]**2+point[1]**2)
        return d*d/point[2]

    def find_perpendicular_vector(self,point1,point2):
        point2 = [point2[0]*1000,point2[1]*1000,point2[2]*1000]
        """
        point1 is where the camera is
        point2 is your second point

                a
            -------------
            \  ?       /
             \        /
           b  \      /  c
               \    /
                \  /
                 \/


        """
        #finding length of a
        point3 = [point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]]
        d3 = math.sqrt(point3[0]**2+point3[1]**2+point3[2]**2)


        #finding unit vector of a
        u_point3 = [point3[0]/d3,point3[1]/d3,point3[2]/d3]

        #finding length of b
        d1 = math.sqrt(point1[0]**2+point1[1]**2+point1[2]**2)
        
        #finding length of c
        d2 = math.sqrt(point2[0]**2+point2[1]**2+point2[2]**2)

        #angle = math.acos(thing) 
        thing = (d3**2+ d1**2-d2**2)/(2*d1*d3)
        distance = d1/thing
        #distance = 1000
        transformation = [u_point3[0]*distance,u_point3[1]*distance,u_point3[2]*distance]
        return [point1[0]+transformation[0],point1[1]+transformation[1],point1[2]+transformation[2]]

    def add_stl(self,path = 'stl_files/qq.stl'):
        """
        Add a stl file to the viewer
        """

        stlreader = vtk.vtkSTLReader()
        stlreader.SetFileName(path)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(stlreader.GetOutputPort())
        # actor
        self.actor.SetMapper(mapper)
        # color the actor
        self.actor.GetProperty().SetColor(actor_color[0],actor_color[1],actor_color[2]) # (B,G,R)
        x,y,z = self.actor.GetCenter()
        self.camera.SetFocalPoint(x,y,z)
        self.ren.AddActor(self.actor)

    def calculate_camera_angle(self):
        planesArray = [0 for i in range(24)]
        self.camera.GetFrustumPlanes(1, planesArray)
        bot_p = planesArray[8:12]

        x,y,z = self.camera.GetPosition()
        camera_location = [x,y,z]

        #Virtual Point that is perpendicular to the camera position, desired angle to be rotated to
        new_z = self.find_supp(camera_location)
        virtual_point = [-camera_location[0],-camera_location[1],new_z]

        #New bot plane vector that is perpendicular to the position of the camera
        new_bot_p = self.find_perpendicular_vector(camera_location,bot_p)

        #Find angle that needs to be rotated
        angle = self.angle(new_bot_p,virtual_point)
        return angle

    def get_output(self,Label):
        self.actor.GetProperty().SetColor(actor_color[0],actor_color[1],actor_color[2])
        self.ren.SetBackground(background_color[0], background_color[1], background_color[2])
        
        angle = self.calculate_camera_angle()
        if (angle > 1):
            current = self.camera.GetRoll()
            #sign = self.get_sign(new_bot_p,virtual_point)
            sign = -1
            self.camera.SetRoll(current+sign)
            angle2 = self.calculate_camera_angle()
            if angle2 > angle:
                sign = -sign
            #print(sign)
            self.camera.SetRoll(current+sign*angle)
            angle = self.calculate_camera_angle()
            print(angle)


    #Screenshot the window and convert it to imagetk format
        vtk_win_im = vtk.vtkWindowToImageFilter()
        vtk_win_im.SetInput(self.renWin)
        vtk_win_im.Update()
        vtk_image = vtk_win_im.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        img = vtk_to_numpy(vtk_array).reshape(height, width, components)
        proc = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(proc)
        imgtk = ImageTk.PhotoImage(image=im_pil)

        Label.configure(image=imgtk)
        Label.image = imgtk
    #done
        return img

    def get_output_no_label(self):
        self.actor.GetProperty().SetColor(actor_color[0],actor_color[1],actor_color[2])
        self.ren.SetBackground(background_color[0], background_color[1], background_color[2])
        
        angle = self.calculate_camera_angle()
        if (angle > 1):
            current = self.camera.GetRoll()
            #sign = self.get_sign(new_bot_p,virtual_point)
            sign = -1
            self.camera.SetRoll(current+sign)
            angle2 = self.calculate_camera_angle()
            if angle2 > angle:
                sign = -sign
            #print(sign)
            self.camera.SetRoll(current+sign*angle)
            angle = self.calculate_camera_angle()
            print(angle)
    #Screenshot the window and convert it to imagetk format
        vtk_win_im = vtk.vtkWindowToImageFilter()
        vtk_win_im.SetInput(self.renWin)
        vtk_win_im.Update()
        vtk_image = vtk_win_im.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        img = vtk_to_numpy(vtk_array).reshape(height, width, components)

        return img

    def get_output2(self):
        self.camera.SetPosition(camera_location[0][0],camera_location[0][1],camera_location[0][2])
        self.get_output(self.label)
        self.camera.SetPosition(camera_location[1][0],camera_location[1][1],camera_location[1][2])
        self.get_output(self.label2)

    def make_folder(self):
        if len(selected_path) != 0:
            w,h = self.renWin.GetSize()
            self.renWin.SetSize(120,120)
            class_names = selected_path
            for i in range(len(selected_path)):
                self.add_stl(path = selected_path[i])
                self.camera.SetPosition(camera_location[0][0],camera_location[0][1],camera_location[0][2])
                for phi in range(5):
                    self.spherical_rotation(0,36)
                    for theta in range(10):
                        self.spherical_rotation(36,0)
                        img = self.get_output_no_label()
                        cam1_image.append(img)
                        cam1_label.append(class_names.index(selected_path[i]))
                        #cv2.imshow('',img)
                        #cv2.waitKey(10)

                self.camera.SetPosition(camera_location[1][0],camera_location[1][1],camera_location[1][2])
                for phi in range(5):
                    self.spherical_rotation(0,36)
                    for theta in range(10):
                        self.spherical_rotation(36,0)
                        img = self.get_output_no_label()
                        cam2_image.append(img)
                        cam2_label.append(class_names.index(selected_path[i]))

            print(len(cam1_image))
            print(len(cam2_image))
            for n in range(len(cam1_image)):
                np_images.append(np.concatenate((cam1_image[n],cam2_image[n]),axis = 1))
                cv2.imshow('',np_images[n])
                cv2.waitKey(10)
        
        
            self.renWin.SetSize(w,h)
        

    def spherical_rotation(self,left,top):
        planesArray = [0 for i in range(24)]
        self.camera.GetFrustumPlanes(1, planesArray)
        top_p = planesArray[0:4]
        left_p = planesArray[12:16]
            
        x,y,z = self.actor.GetCenter()
        self.actor.RotateWXYZ(top,top_p[0],top_p[1],top_p[2])
        self.actor.RotateWXYZ(left,left_p[0],left_p[1],left_p[2])

        self.actor.SetPosition(0,0,0)
        center_x, center_y, center_z = self.actor.GetCenter()
        self.actor.SetPosition(0-center_x,0-center_y,0-center_z)
        
        center_x, center_y, center_z = self.actor.GetCenter()
        self.camera.SetFocalPoint(center_x,center_y,center_z)
        self.get_output2()




    def zoom(self,input_d):
        print(input_d)
"""
        ratio = input_d
        center_x, center_y, center_z = self.actor.GetCenter()
        camera_x, camera_y, camera_z = self.camera.GetPosition()
        diff_x, diff_y, diff_z = camera_x - center_x, camera_y - center_y, camera_z - center_z
        camera_location = [camera_x-diff_x*ratio,camera_y-diff_y*ratio,camera_z-diff_z*ratio]
        self.camera.SetPosition(camera_location[0],camera_location[1],camera_location[2])
        todisplay = 'x: ' + str(round(camera_location[0],1)) + '  y: ' + str(round(camera_location[1],1)) + '  z: ' + str(round(camera_location[2],1))
        self.label_xyz.configure(text = todisplay)
        print(diff_x,diff_y,diff_z)
        self.get_output2()
"""


class menubar():
    """
    This class is plainly functions for the menubar to use
    """
    def __init__(self,root,viewer,actor_label,background_label,xyz_label,xyz_label2):
        self.viewer = viewer
        self.actor_label = actor_label
        self.background_label = background_label
        self.xyz_label = xyz_label
        self.xyz_label2 = xyz_label2
        menubar = Menu(root)
        viewmenu = Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Set Actor Color",command = self.set_actor_color)
        viewmenu.add_command(label="Set Background Color",command = self.set_background_color)
        viewmenu.add_command(label="Set Camera Location",command = lambda:self.set_camera_location(0))
        viewmenu.add_command(label='Set Camera2 Location',command = lambda:self.set_camera_location(1))
        menubar.add_cascade(label="View", menu=viewmenu)
        root.config(menu=menubar)

    def set_actor_color(self):
        def ok(window,b,g,r):
            actor_color[0] = float(b.get())
            actor_color[1] = float(g.get())
            actor_color[2] = float(r.get())

            todisplay_actor = 'actor color:   ' + str(round(actor_color[0],3)) + ',  ' +  str(round(actor_color[1],3)) + ',  ' + str(round(actor_color[2],3))
            self.actor_label.configure(text = todisplay_actor)

            self.viewer.get_output2()
            window.destroy()
        actor_color_window = Tk()
        actor_color_window.title("Change Actor Color")
        actor_color_window.geometry('300x100')
        B = Entry(actor_color_window, width=5)
        B.place(x = 30, y = 30, anchor = NW)
        G = Entry(actor_color_window, width=5)
        G.place(x = 130, y = 30, anchor = NW)
        R = Entry(actor_color_window, width=5)
        R.place(x = 230, y = 30, anchor = NW)
        btn_update = Button(actor_color_window, text='OK', width = 5, height = 1, command = lambda: ok(actor_color_window,B,G,R))
        btn_update.place(x = 125, y = 60 , anchor = NW)

    def set_background_color(self):
        def ok(window,b,g,r):
            background_color[0] = float(b.get())
            background_color[1] = float(g.get())
            background_color[2] = float(r.get())

            todisplay_bg = 'actor color:   ' + str(round(background_color[0],3)) + ',  ' +  str(round(background_color[1],3)) + ',  ' + str(round(background_color[2],3))
            self.background_label.configure(text = todisplay_bg)

            self.viewer.get_output2()
            window.destroy()
        background_color_window = Tk()
        background_color_window.title("Change Background Color")
        background_color_window.geometry('300x100')
        B = Entry(background_color_window, width=5)
        B.place(x = 30, y = 30, anchor = NW)
        G = Entry(background_color_window, width=5)
        G.place(x = 130, y = 30, anchor = NW)
        R = Entry(background_color_window, width=5)
        R.place(x = 230, y = 30, anchor = NW)
        btn_update = Button(background_color_window, text='OK', width = 5, height = 1, command = lambda: ok(background_color_window,B,G,R))
        btn_update.place(x = 125, y = 60 , anchor = NW)

    def set_camera_location(self,num):
        '''
        Pop up a window to set the camera location
        '''
        global camera_location
        def ok(window,X,Y,Z):
            camera_location[num][0] = float(X.get())
            camera_location[num][1] = float(Y.get())
            camera_location[num][2] = float(Z.get())
            todisplay_xyz = 'camera ' + str(num+1) + ' x:   ' + str(round(camera_location[num][0],1)) + '  y:  ' + str(round(camera_location[num][1],1)) + '  z:  ' + str(round(camera_location[num][2],1))
            self.xyz_label.configure(text = todisplay_xyz)
            self.viewer.get_output2()
            window.destroy()
        camera_location_window = Tk()
        camera_location_window.title("Change Camera Location")
        camera_location_window.geometry('300x100')

        X = Entry(camera_location_window, width=5)
        X.place(x = 30, y = 30, anchor = NW)
        X.insert(0,camera_location[num][0])

        Y = Entry(camera_location_window, width=5)
        Y.place(x = 130, y = 30, anchor = NW)
        Y.insert(0,camera_location[num][1])

        Z = Entry(camera_location_window, width=5)
        Z.place(x = 230, y = 30, anchor = NW)
        Z.insert(0,camera_location[num][2])

        btn_update = Button(camera_location_window, text='OK', width = 5, height = 1, command = lambda: ok(camera_location_window,X,Y,Z))
        btn_update.place(x = 125, y = 60 , anchor = NW)



class stl_explorer():
    def __init__(self,canvas,size,canvas2):
        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.SetSize(size,size)
        self.renWin.AddRenderer(self.ren)
        self.renWin.OffScreenRenderingOn()
        self.stl_names = []

        self.canvas2 = canvas2        
        self.canvas = canvas

        #set color for the renderer
        self.ren.SetBackground(background_color[0], background_color[1], background_color[2])
        #Set up camera components
        self.camera = vtk.vtkCamera()
        self.ren.SetActiveCamera(self.camera)
        self.camera.SetPosition(300,300,300)
        self.camera.SetThickness(10000)

        self.actor = vtk.vtkActor()

    
    def add_selected(self,num):
        if stl_file_list[num-1] not in selected_path:
            selected_path.append(stl_file_list[num-1])
        print(selected_path)
        
        return True

    def delete_selected(self,path):
        return True


    def stl_to_np(self,stl_path,stl_list):
        self.stl_names = []
        output = []
        for filenames in os.listdir(stl_path):
            if filenames[len(filenames)-4:len(filenames)] == ".stl":
                self.stl_names.append(filenames)
                self.add_stl(stl_path+filenames)
                print(stl_path+filenames)
                stl_list.append(stl_path+filenames)
                self.ren.ResetCamera()
                self.camera.SetFocalPoint(0,0,0)
                output.append(self.get_output())
        return output

    def create_stl_image(self,per_row,stl_path,stl_list,image_list):
        if (per_row < 6):
            self.canvas.delete("all")
            canvas_w = self.canvas.winfo_width()
            img_size = int((canvas_w-5)/per_row)
            self.renWin.SetSize(img_size-5,img_size-5)
            images = self.stl_to_np(stl_path,stl_list)
            for n in range(len(images)):
                np_img = cv2.cvtColor(images[n],cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(np_img)
                imgtk = ImageTk.PhotoImage(image=im_pil) 
                col = n%per_row
                row = divmod(n,per_row)[0]
                self.canvas.create_image(5+img_size*col,5+img_size*row,image=imgtk, anchor=NW)
                self.canvas.create_text(5+img_size*col+img_size*0.5,5+img_size*row+img_size*0.9,fill="darkblue",font="Times 15",
                        text= self.stl_names[n])
                image_list.append(imgtk)

        else:    
            print("!!ERROR: Input canvas is not a tkinter.canvas object, unable to create image")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
    
    def add_stl(self,path = 'stl_files/qq.stl'):
        """
        Add a stl file to the viewer
        """

        stlreader = vtk.vtkSTLReader()
        stlreader.SetFileName(path)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(stlreader.GetOutputPort())
        # actor
        self.actor.SetMapper(mapper)
        # color the actor
        self.actor.GetProperty().SetColor(actor_color[0],actor_color[1],actor_color[2]) # (B,G,R)
        x,y,z = self.actor.GetCenter()
        self.camera.SetFocalPoint(x,y,z)
        self.ren.AddActor(self.actor)
    
    def get_output(self):
        self.actor.GetProperty().SetColor(actor_color[0],actor_color[1],actor_color[2])
        self.ren.SetBackground(background_color[0], background_color[1], background_color[2])
        
        self.actor.SetPosition(0,0,0)
        center_x, center_y, center_z = self.actor.GetCenter()
        self.actor.SetPosition(0-center_x,0-center_y,0-center_z)

        vtk_win_im = vtk.vtkWindowToImageFilter()
        vtk_win_im.SetInput(self.renWin)
        vtk_win_im.Update()
        vtk_image = vtk_win_im.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        img = vtk_to_numpy(vtk_array).reshape(height, width, components)

        return img


