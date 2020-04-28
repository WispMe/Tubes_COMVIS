from tkinter import *
from tkinter import messagebox
from imutils.video import VideoStream
from source.detection_code import camera
import argparse
import cv2
import time
from collections import deque
from PIL import Image
from PIL import ImageTk


class display:
    def __init__(self):
        self.root = Tk()
        self.root.title("Comvis#7")
        self.root.geometry("240x120")

        self.atas = Frame(self.root)
        self.frame = LabelFrame(self.root, text="info"  )
        self.layar = LabelFrame(self.root, text="camera")


        self.title = Label(self.root, text="BOOK CODE", font='Helvetica 14 bold')
        self.title.pack(pady=5)
        self.atas.pack(side=TOP)
        self.layar.pack(side=LEFT)

        self.open = Button(self.atas, text="Open Camera", command=self.opencamera)
        self.open.pack(pady=2)
        self.about = Button(self.atas, text="About", command=self.kelompok)
        self.about.pack(pady=2)

    def opencamera(self):
        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
                        help="max buffer size")
        args = vars(ap.parse_args())

        pts = deque(maxlen=args["buffer"])
        # if a video path was not supplied, grab the reference
        # to the webcam

        vs = VideoStream(src=0).start()
        # allow the camera or video file to warm up
        time.sleep(2.0)

        print("[INFO] warming up camera...")
        self.root.geometry("640x320")
        camera(self.frame, vs, pts, self.layar)

    def kelompok(self):
        kelompok = "Created by:\n1. Dony Tontiardo\n2. Faiz Adil Khatami\n3. Gilang Run Bhayuntoro\n4. Oshi Paulina Sancho Liman\n5. Renaldi Utama Jaya"
        messagebox.showinfo(title="About", message = kelompok)
