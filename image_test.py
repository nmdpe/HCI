import cv2

def get_image():
    cap=cv2.VideoCapture(0)
    if cap.isOpened():
        ret,frame=cap.read()
        if ret:
            cv2.imwrite('./image.jpg',frame)
        cap.release() 
    cv2.destroyAllWindows()

get_image()