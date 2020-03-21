import cv2
import numpy as np
from PIL import Image, ImageTk
import threading

"""
0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
5. CV_CAP_PROP_FPS Frame rate.
6. CV_CAP_PROP_FOURCC 4-character code of codec.
7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
"""
camera_state = ['closed','closed']

hook_mask = [np.zeros((480,640)),np.zeros((480,640))]
for x in range(250,550):
    y = int(x*0.5522)+50
    hook_mask[0][y-170:y,x-1:x] = 1

for x in range(250,550):
    y = int((640-x)*0.5522)+50
    hook_mask[1][y-170:y,x-1:x] = 1

class camera_viewer:
    def __init__(self,label1,label2):
        self.path = ['Captured Images/A/20.05/','Captured Images/B/20.05/']
        self.image_num = 1

        self.thread_list = [1,2,3]
        self.labels = [label1,label2]

        self.bg_path = [self.path[0] + '150.jpg',self.path[1] + '150.jpg']
        self.bg = [cv2.imread(self.bg_path[0]),cv2.imread(self.bg_path[1])]
        self.bg_sub_bool = [False,False]

        self.guibg = cv2.imread('guibg2.png')


        self.images = [0,0]
        self.gray_bool = [False,False]

        self.hook_bool = [False,False]

        #define color channels of images as sharable variables to lessen calculation
        self.channels = [['b','g','r'],['g','b','r']]

        self.binary_thresh = [30,30]

    """
    def start_cam(self,num):
        try:
            cap = cv2.VideoCapture(num)
            cap.set(3,1024)
            cap.set(4,769)
            while True:
                ret, frame = cap.read()
                self.images[num-1] = frame

                np_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                np_img = np_img[150:550,300:700]
                im_pil = Image.fromarray(np_img)
                imgtk = ImageTk.PhotoImage(image=im_pil)
                self.labels[num-1].configure(image=imgtk)
                images = imgtk
                camera_state[num-1] = 'opened'
        except:
            print('failed to initiate camera')
        #cv2.destroyAllWindows()
    
    def start_cam_thread(self,num):
        if camera_state[num-1] == 'closed':
            self.thread_list[num] = threading.Thread(target=self.start_cam,args = (num,))
            self.thread_list[num].start()
    """

    def bg_remove(self,image,num):
        b,g,r = cv2.split(image)
        b = cv2.GaussianBlur(b, (5, 5), 0)
        g = cv2.GaussianBlur(g, (5, 5), 0)
        r = cv2.GaussianBlur(r, (5, 5), 0)

        bg_b,bg_g,bg_r = cv2.split(self.bg[num-1])
        bg_b = cv2.GaussianBlur(bg_b, (5, 5), 0)
        bg_g = cv2.GaussianBlur(bg_g, (5, 5), 0)
        bg_r = cv2.GaussianBlur(bg_r, (5, 5), 0)

        difference_b = cv2.absdiff(b, bg_b)
        difference_g = cv2.absdiff(g, bg_g)
        difference_r = cv2.absdiff(r, bg_r)

        final = cv2.add(difference_b,difference_g,difference_r)

        _, mask = cv2.threshold(final, self.binary_thresh[num-1], 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        gui_bg = cv2.bitwise_and(self.guibg,self.guibg,mask = mask_inv)
        res = cv2.bitwise_and(image,self.guibg,mask = mask)
        image = cv2.add(gui_bg,res)

        return res

    def center_hook(self,image,num):
        b,g,r = cv2.split(image)
    
        b = cv2.GaussianBlur(b, (5, 5), 0)
        g = cv2.GaussianBlur(g, (5, 5), 0)
        r = cv2.GaussianBlur(r, (5, 5), 0)

        r_b = cv2.absdiff(r,b)
        r_g = cv2.absdiff(r,g)
        red_channel = cv2.add(r_b,r_g)

        _, red_thresh = cv2.threshold(red_channel, 230, 255, cv2.THRESH_BINARY)
        
        kernel = np.ones((2,2),np.uint8)
        kernel2 = np.ones((25,25),np.uint8)
        kernel3 = np.ones((5,5),np.uint8)

        opening = cv2.morphologyEx(red_thresh, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel2)
        dilation = cv2.erode(dilation, kernel3)

        _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        area = []
        if len(contours) != 0:
            for i in range(len(contours)):
                area.append(cv2.contourArea(contours[i]))
                if 500 < area[i] <3500:
                    x,y,w,h = cv2.boundingRect(contours[i])
                    cv2.rectangle(image,(x,y),(x+w,y+h),(120,120,200),2)
                    
                    x = int(x+w/2)
                    y = int(y+h/2)
                    if hook_mask[num-1][y][x] == 1.0:
                        cv2.rectangle(image,(x-100,y),(x+100,y+200),(200,200,200),1)      

        return image


        """
        _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        area = []
        if len(contours) != 0:
            for i in range(len(contours)):
                area.append(cv2.contourArea(contours[i]))
                if 500 < area[i] <3500:
                #c = []
                #c.append(contours[i])
                #cv2.drawContours(frame2, c, -1, (255, 255, 255), 3) 
                    x,y,w,h = cv2.boundingRect(contours[i])
                    cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,255,255),2)
                    print('x: ' + str(x+w/2))
                    print('y: ' + str(y+h/2))
                    print('--------------------')
                    x = x+int(w/2)
                    y = y+int(h/2)
                    break
                    print(hook_mask[y][x])
                if hook_mask[y][x] == 1.0:
                    image[280:480,0:200] = image[y-25:y+175,x-100:x+100]


        return Image
        """

    def start_cam(self,num):
        while True:
            frame = cv2.imread(self.path[num-1] + str(self.image_num*10) + ".jpg")
            if self.bg_sub_bool[num-1] == True:
                frame = self.bg_remove(frame,num)

            if self.hook_bool[num-1] == True:
                frame = self.center_hook(frame,num)

            if self.gray_bool[num-1] == True:
                gray_c = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.merge((gray_c,gray_c,gray_c))

            np_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            np_img = np_img[40:440,120:520]
            im_pil = Image.fromarray(np_img)
            imgtk = ImageTk.PhotoImage(image=im_pil)
            self.labels[num-1].configure(image=imgtk)                
            images = imgtk
            camera_state[num-1] = 'opened'
            if self.image_num%2 == num-1:
                self.image_num += 1

            if self.image_num == 1000:
                self.image_num = 1
    
    def bg_sub(self,num):
        self.bg_sub_bool[num-1] = not self.bg_sub_bool[num-1]
    
    def gray(self,num):
        self.gray_bool[num-1] = not self.gray_bool[num-1]
    
    def hook(self,num):
        self.hook_bool[num-1] = not self.hook_bool[num-1]

    def start_cam_thread(self,num):
        if camera_state[num-1] == 'closed':
            self.thread_list[num] = threading.Thread(target=self.start_cam,args = (num,))
            self.thread_list[num].start()

        


    

