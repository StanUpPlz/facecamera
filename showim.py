import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition



# Load the face cascade file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# create a Tkinter window
root = tk.Tk()

width= root.winfo_screenwidth()
height= root.winfo_screenheight()

root.title("Camera Feed")

# create a canvas widget to display the video feed
canvas_width = 640
canvas_height = 480
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

canvasImage = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvasImage.pack()

# initialize the camera
cap = cv2.VideoCapture(0)



image_paths = [] 
image_sizes = (100, 100)

images = []
coords = []


# define a function to update the canvas with the latest camera frame
def update_canvas():
    # read a frame from the camera
    global frame
    global x, y, w, h

    ret, frame = cap.read()
    if ret:
        # convert the frame from OpenCV's BGR format to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # create a Tkinter-compatible image from the frame
        image = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=image)
        # update the canvas with the new image
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        # keep a reference to the image to prevent it from being garbage collected
        canvas.img_tk = img_tk
    # schedule the update_canvas function to be called again after 10 milliseconds
    canvas.after(100, update_canvas)

# start the update_canvas function to begin displaying the camera feed
update_canvas()


def save():
    global frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_roi = frame[y:y+h, x:x+w]
    filename = 'image{}.jpg'.format(len(image_paths))
    cv2.imwrite(filename, face_roi)
    image_paths.append(filename)
    # image = Image.open(filename)
    # image = image.resize(image_sizes, Image.ANTIALIAS)
    # image_tk = ImageTk.PhotoImage(image)
    # canvas_image = canvasImage.create_image(x, y, image=image_tk)
    # images.append(image_tk)
    # coords.append((x-image_sizes[0]/2, y-image_sizes[1]/2, x+image_sizes[0]/2, y+image_sizes[1]/2))
    showimage(image_paths)
    
def showimage(image_paths):
   for i, path in enumerate(image_paths):
    x, y = (i+1)*100, canvas_height//2
    size = image_sizes
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    image_tk = ImageTk.PhotoImage(image)
    canvas_image = canvasImage.create_image(x, y, image=image_tk)
    images.append(image_tk)
    coords.append((x-size[0]/2, y-size[1]/2, x+size[0]/2, y+size[1]/2))

# Define a function to handle clicks on the canvas
def on_click(event):
    for i, coord in enumerate(coords):
        if coord[0] < event.x < coord[2] and coord[1] < event.y < coord[3]:
            i1 = face_recognition.load_image_file(image_paths[i])
            ioi = face_recognition.face_encodings(i1)[0]          
            print(ioi)
            break

# Bind the on_click function to the canvas
canvasImage.bind("<Button-1>", on_click)
   

button = tk.Button(root,text ="save",command= save)
button.pack()




# start the Tkinter main loop
root.state('zoomed')
root.geometry("%dx%d" % (width, height))
root.mainloop()

# release the camera when the window is closed
cap.release()
