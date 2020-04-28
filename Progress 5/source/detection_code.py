from tkinter import *
# import the necessary packages
from imutils.video import VideoStream
from source.shapedetector import ShapeDetector
import numpy as np
import argparse
import cv2
import imutils
from PIL import Image
from PIL import ImageTk
import threading
import sqlite3 as sq

class camera:
    def __init__(self, window, vs, pts, layar):

        self.panel = None
        self.foto = layar
        self.frame2 = window
        self.vs = vs
        self.pts = pts

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        current_row = 0
        #create a label for databases entry
        self.judul_label = Label(self.frame2, text="Judul: ", font=18)
        self.judul_label.grid(row=current_row, column=0)
        self.judul_text = StringVar()
        self.judul_entry = Entry(self.frame2, textvariable=self.judul_text, font=18)
        self.judul_entry.grid(row=current_row, column=1)
        current_row += 1

        self.pengarang_label = Label(self.frame2, text="Pengarang: ", font=18)
        self.pengarang_label.grid(row=current_row, column=0)
        self.pengarang_text = StringVar()
        self.pengarang_entry = Entry(self.frame2, textvariable=self.pengarang_text, font=18)
        self.pengarang_entry.grid(row=current_row, column=1)
        current_row += 1

        self.genre_label = Label(self.frame2, text="Genre: ", font=18)
        self.genre_label.grid(row=current_row, column=0)
        self.genre_text = StringVar()
        self.genre_entry = Entry(self.frame2, textvariable=self.genre_text, font=18)
        self.genre_entry.grid(row=current_row, column=1)
        current_row += 1

        self.tahun_label = Label(self.frame2, text="Tahun: ", font=18)
        self.tahun_label.grid(row=current_row, column=0)
        self.tahun_text = StringVar()
        self.tahun_entry = Entry(self.frame2, textvariable=self.tahun_text, font=18)
        self.tahun_entry.grid(row=current_row, column=1)
        current_row += 1

        self.penerbit_label = Label(self.frame2, text="Penerbit: ", font=18)
        self.penerbit_label.grid(row=current_row, column=0)
        self.penerbit_text = StringVar()
        self.penerbit_entry = Entry(self.frame2, textvariable=self.penerbit_text, font=18)
        self.penerbit_entry.grid(row=current_row, column=1)
        current_row += 1

        self.start = Button(self.frame2, text="Run Again", command=self.resume)
        self.start.grid(row=current_row, column=0)
        self.frame2.pack(expand="yes", side="left", fill='y')


    def videoLoop(self):
        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
                        help="max buffer size")
        args = vars(ap.parse_args())


        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        lower = {'blue': (110, 100, 100), 'red': (-10, 100, 100), 'green': (40, 70, 70),
                 'yellow': (20, 100, 117)}  # assign new item lower['blue'] = (93, 10, 0)
        upper = {'blue': (130, 255, 255), 'red': (10, 255, 255), 'green': (70, 255, 255), 'yellow': (40, 255, 255)}

        # database session
        con = sq.connect('data_comvis.db')  # dB browser for sqlite needed
        con.text_factory = str
        cmd_db = con.cursor()  # SQLite command, to connect to db so 'execute' method can be called

        # make a call for ShapeDetector class
        sd = ShapeDetector()

        stopEvent = threading.Event()

        # keep looping
        while not self.stopEvent.is_set():
            # grab the current frame
            self.foto = self.vs.read()
            # handle the frame from VideoCapture or VideoStream
            # resize the frame, blur it, and convert it to the HSV
            # color space
            self.frame = imutils.resize(self.foto, width=300)
            blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask

            for key, value in upper.items():
                mask = cv2.inRange(hsv, lower[key], upper[key])
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                # find contours in the mask and initialize the current
                # (x, y) center of the ball
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                center = None
                # only proceed if at least one contour was found
                if len(cnts) > 0:
                    # find the largest contour in the mask, then use
                    # it to compute the minimum enclosing circle and
                    # centroid
                    c = max(cnts, key=cv2.contourArea)
                    (x, y, w, h) = cv2.boundingRect(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    # only proceed if the radius meets a minimum size
                    if (x + y + w + h) > 400:
                        # Do when reach the minimum contours length
                        shape = sd.detect(c)
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.putText(self.frame, key, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                        cv2.drawContours(self.frame, [c], -1, (0, 0, 0), 2)

                        cv2.putText(self.frame, shape, (x + 15, y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 0, 0), 2)
                        # cv2.circle(frame, (int(x), int(y)), int(radius),
                        #           (0, 255, 255), 2)
                        # cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        # Gets data from database
                        text = key + " " + shape
                        plus = 'FROM buku INNER JOIN kode_buku ON buku.id = kode_buku.id WHERE kode_buku.kode = "' + text + '"'
                        cmd_db.execute('SELECT * ' + plus)

                        data = cmd_db.fetchall()  # Gets the data from the table

                        for row in data:
                            self.judul_text.set(row[1])
                            self.pengarang_text.set(row[2])
                            self.genre_text.set(row[3])
                            self.tahun_text.set(row[4])
                            self.penerbit_text.set(row[5])
                            self.penerbit_text.set(row[6])

                        con.commit()
                        self.stopEvent.set()
                # update the points queue
                # pts.appendleft(center)

            # loop over the set of tracked points
            for i in range(1, len(self.pts)):
                # if either of the tracked points are None, ignore
                # them
                if self.pts[i - 1] is None or self.pts[i] is None:
                    continue
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(self.frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)
            # show the frame to our screen

            # Show image in GUI
            #self.frame = cv2.cvtColor(self.frame, cv2.COLOR_HSV2BGR)
            #self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = Image.fromarray(self.frame)
            self.frame = ImageTk.PhotoImage(self.frame)
            #cv2.imshow("Frame", self.frame)
            #key = cv2.waitKey(1) & 0xFF

            # if the panel is not None, we need to initialize it
            if self.panel is None:
                self.panel = Label(image=self.frame)
                self.panel.image = self.frame
                self.panel.pack(side="left", padx=10, pady=10)

            # otherwise, simply update the panel
            else:
                self.panel.configure(image=self.frame)
                self.panel.image = self.frame

    def resume(self):
        # Resume the Thread
        kosong = ""
        self.judul_text.set(kosong)
        self.pengarang_text.set(kosong)
        self.genre_text.set(kosong)
        self.tahun_text.set(kosong)
        self.penerbit_text.set(kosong)
        self.penerbit_text.set(kosong)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()