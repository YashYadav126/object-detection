import cv2
import cvlib as cv  
from cvlib.object_detection import draw_bbox
from gtts import gTTS
import os
import tkinter as tk
from tkinter import filedialog

def speech(text):
    print(text)
    lang = "en"
    output = gTTS(text=text, lang=lang, slow=False)
    output.save('output.mp3')
    os.system("start output.mp3")

class InputSourceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Object Detection Input Source")

        
        self.title_label = tk.Label(master, text="Object Detection", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        
        self.subtitle_label = tk.Label(master, text="Please select the input source:", font=("Helvetica", 12))
        self.subtitle_label.grid(row=1, column=0, columnspan=3)

        
        self.webcam_button = tk.Button(master, text="Webcam", command=self.use_webcam, width=20, height=2, font=("Helvetica", 12))
        self.webcam_button.grid(row=2, column=0, pady=10)

       
        self.video_button = tk.Button(master, text="Video File", command=self.use_video, width=20, height=2, font=("Helvetica", 12))
        self.video_button.grid(row=2, column=1, pady=10)

        
        self.image_button = tk.Button(master, text="Image File", command=self.use_image, width=20, height=2, font=("Helvetica", 12))
        self.image_button.grid(row=2, column=2, pady=10)

        
        self.close_button = tk.Button(master, text="Close", command=master.quit, width=20, height=2, font=("Helvetica", 12))
        self.close_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.source = None

    def use_webcam(self):
        self.source = 0
        self.master.quit()

    def use_video(self):
        file_path = filedialog.askopenfilename(title="Select video file", filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*")))
        if file_path:
            self.source = file_path
            self.master.quit()

    def use_image(self):
        file_path = filedialog.askopenfilename(title="Select image file", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        if file_path:
            self.source = file_path
            self.master.quit()

root = tk.Tk()
input_gui = InputSourceGUI(root)
root.mainloop()

if input_gui.source is None:
    exit()


if isinstance(input_gui.source, int):
    video = cv2.VideoCapture(input_gui.source)
else:
    video = cv2.VideoCapture(input_gui.source)

labels = []
while True:
    ret, frame = video.read()
    if not ret:
        break

    bbox, label, conf = cv.detect_common_objects(frame, confidence=0.5)
    output_image = draw_bbox(frame, bbox, label, conf)

   
    for l, c in zip(label, conf):
        cv2.putText(output_image, f"{l}: {c:.2f}", (bbox[label.index(l)][0], bbox[label.index(l)][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        output_image = cv2.resize(output_image, (640, 480))

    cv2.imshow('object detection', output_image)

    for item in label:
        if item in labels:
            pass
        else:
            labels.append(item) 

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

i = 0
new = []
for label in labels:
    if i == 0:
        new.append(f"i found a {label}, ")
    else:
        new.append(f"and a {label}")

    i += 1

speech(" ".join(new))