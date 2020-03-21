import cv2
import numpy
from tkinter import *
from PIL import Image, ImageTk
import threading

class camera():
    def __init__(self):
        self.thread_list = [1,2,3]
        self.root = Tk()
        self.root.title("Camera")
        self.root.geometry('1280x720')

        self.labels = []

        self.labels.append(Label(self.root, width = 400, height = 300))
        self.labels[0].place(x = 20,y = 10,anchor = NW)

        self.labels.append(Label(self.root, width = 400, height = 300))
        self.labels[1].place(x = 440,y = 10,anchor = NW)

        self.labels.append(Label(self.root, width = 400, height = 300))
        self.labels[2].place(x = 860,y = 10,anchor = NW)

        self.btn_1 = Button(self.root, text='update', command= lambda: self.start_cam_thread(0))
        self.btn_1.place(x = 200, y = 400 , anchor = NW)

        self.btn_2 = Button(self.root, text='update', command= lambda: self.start_cam_thread(1))
        self.btn_2.place(x = 600, y = 400 , anchor = NW)

        self.btn_3 = Button(self.root, text='update', command= lambda: self.start_cam_thread(2))
        self.btn_3.place(x = 1000, y = 400 , anchor = NW)


    def start_cam(self,camera_num):
        try:
            cap = cv2.VideoCapture(camera_num)
            while True:
                ret, frame = cap.read()
                np_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                np_img = cv2.resize(np_img,(400,300))
                im_pil = Image.fromarray(np_img)
                imgtk = ImageTk.PhotoImage(image=im_pil)
                self.labels[camera_num].configure(image=imgtk)
                images = imgtk
            cap.release()
        except:
            print('failed')
        #cv2.destroyAllWindows()
    def start_cam_thread(self,camera_num):
        self.thread_list[camera_num] = threading.Thread(target=self.start_cam, args=(camera_num,))
        self.thread_list[camera_num].start()

"""
cam = camera()
cam.root.mainloop()
"""

cap = cv2.VideoCapture(1)
#cap.set(3, 1920)
#cap.set(4, 1080)

while True:
    ret, frame = cap.read()
    #print(frame.shape)
    print(cap.get(15))
    cv2.imshow('',frame)
    cv2.waitKey(10)
    