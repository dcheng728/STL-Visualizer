import cv2
import numpy as np
import glob

cap = cv2.VideoCapture(1)
cap.set(3,1024)
cap.set(4,769)

path = 'distortion/B/'


n = 0

ret = np.load(path+'ret.npy')
mtx = np.load(path+'mtx.npy')
dist = np.load(path+'dist.npy')
rvecs = np.load(path+'rvecs.npy')
tvecs = np.load(path+'tvecs.npy')

d = 1

while True:
    ret, frame = cap.read()
    h,  w = frame.shape[:2]
    #print(h,w)

    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    x,y,w,h = 180,120,200,200
    #dst = dst[y:y+h, x:x+w]
    
    print(frame.shape)
    #print(cap.get(15))
    if d == -1:
        cv2.imshow('dst',dst)
    else:
        cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        d = -d

        #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
        
        #if ret == True:
            #print('jhkjhjkhkj')
            #cv2.imwrite(path + str(n) + '.jpg',frame)
            #n += 1
      
"""

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('C:/python_project_ssd/GUI_stl/distortion/B/*.jpg')
print(len(images))

start = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print(start)
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey(500)
    start += 1

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

np.save(path+'ret.npy',ret)
np.save(path+'mtx.npy',mtx)
np.save(path+'dist.npy',dist)
np.save(path+'rvecs.npy',rvecs)
np.save(path+'tvecs.npy',tvecs)
"""

