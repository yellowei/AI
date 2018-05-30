import cv2
import numpy
# import zbar
import time
import threading
import tkinter as Tkinter
from PIL import Image, ImageTk

class BarCodeScanner(threading.Thread, Tkinter.Toplevel):
    def __init__(self):
        # i made this as a global variable so i can access this image
        # outside ie,. beyond the thread to update the image on to the  tkinter window
        global imgtk
        imgtk = None
        threading.Thread.__init__(self)
        self.WINDOW_NAME = 'Camera'
        self.CV_SYSTEM_CACHE_CNT = 5 # Cv has 5-frame cache
        self.LOOP_INTERVAL_TIME = 0.2
        cv.NamedWindow(self.WINDOW_NAME, cv.CV_WINDOW_NORMAL)
        self.cam = cv2.VideoCapture(-1)
        self.confirm = 0

    def scan(self, aframe):
        imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY)
        # to show coloured image, as from the other code mentioned in the other code
        imgcol = cv2.cvtColor(aframe, cv2.COLOR_BGR2RGBA)
        imgcol_array = Image.fromarray(imgcol)
        imgtk = ImageTk.PhotoImage(image=imgcol_array)

        raw = str(imgray.data)
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        width = int(self.cam.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(self.cam.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        imageZbar = zbar.Image(width, height,'Y800', raw)
        scanner.scan(imageZbar)

        for symbol in imageZbar:
            print( 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data)
            return symbol.data

    def run(self):
        self.datalst = []
        print ('BarCodeScanner run', time.time())
        while True:
            for i in range(0,self.CV_SYSTEM_CACHE_CNT):
                self.cam.read()
            img = self.cam.read()
            self.data = self.scan(img[1])

            cv2.imshow(self.WINDOW_NAME, img[1])
            cv.WaitKey(1)
            time.sleep(self.LOOP_INTERVAL_TIME)
            if self.data:
                self.datalst.append(self.data)
            # i have added this section so that it waits for scan
            # if a scan is made it and if gets same value after 2 scans
            # it has to stop webcam
            if len(self.datalst) == 2 and len(set(self.datalst)) <= 1:
                # I want to close the webcam before closing the toplevel window
                #self.cam.release()
                #cv2.destroyAllWindows()
                break
        self.cam.release()

def Video_Window():
    video_window = Tkinter.Toplevel()
    video_window.title('QR Scan !!')
    img_label = Tkinter.Label(video_window)
    img_label.pack(side=Tkinter.TOP)
    close_button = Tkinter.Button(video_window, text='close', command = video_window.destroy)
    close_button.pack(side=Tkinter.TOP)

    def update_frame():
        global imgtk
        img_label.configure(image=imgtk)
        img_label.after(10,update_frame)
    update_frame()

def main():
    root = Tkinter.Tk()
    button_scanQr = Tkinter.Button(root, text='QR Scan', command=start_scan)
    button_scanQr.pack()
    root.mainloop()

def start_scan():
    scanner = BarCodeScanner()
    scanner.start()

    Video_Window()
    #scanner.join()

main()