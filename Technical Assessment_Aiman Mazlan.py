#!/usr/bin/env python
# coding: utf-8

# In[16]:


import cv2
import json
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


# Function to load a new image and annotation file
            
def load_image_and_annotation():
    # Get the path of the image file
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if img_path:
        # Load the image
        global img, img_tk
        img = cv2.imread(img_path)

        # Get the path of the annotation file
        annotation_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if annotation_path:
            # Load the annotation file
            global annotation
            with open(annotation_path) as f:
                annotation = json.load(f)

            # Get a list of unique class titles
            class_titles = set(obj['classTitle'] for obj in annotation['objects'])

            # Create a dropdown menu for class selection
            selected_class.set('All')
            class_menu = tk.OptionMenu(root, selected_class, 'All', *class_titles, command=lambda _: update_bounding_boxes())
            class_menu.place(x=210, y=10)

            # Calculate the scaling factor
            height, width, _ = img.shape
            desired_width = 550 # Set the desired width of the image
            scale = desired_width / width

            # Scale the image
            img = cv2.resize(img, (int(width*scale), int(height*scale)))

            # Convert the image to a Tkinter PhotoImage and display it on the canvas
            img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            # Call the update_bounding_boxes function to initialize the bounding boxes
            update_bounding_boxes()

# Create the main window
root = tk.Tk()
root.title("Image Detection")

# Set the window size
root.geometry("800x800")

# Create a "Select image" button
select_image_btn = tk.Button(root, text="Select image", command=load_image_and_annotation)
select_image_btn.place(x=10, y=10)

# Create a canvas to display the image
canvas = tk.Canvas(root, width=img.shape[1], height=img.shape[0])
canvas.place(x=10, y=40)

# Convert the image to a Tkinter PhotoImage and display it on the canvas
img_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Create a list to store the bounding box objects
bbox_list = []

# Function to update the bounding boxes
def update_bounding_boxes():
    # Remove the existing bounding boxes from the canvas
    for bbox in bbox_list:
        canvas.delete(bbox)
    # Clear the list of bounding box objects
    bbox_list.clear()
    # Loop through each object in the annotation file
    for obj in annotation['objects']:
        # Check if the object's classTitle matches the selected class
        if selected_class.get() == 'All' or obj['classTitle'] == selected_class.get():
            # Extract the coordinates of the bounding box
            x1, y1 = obj['points']['exterior'][0]
            x2, y2 = obj['points']['exterior'][1]
            
            # Scale the coordinates
            x1, y1 = int(x1*scale), int(y1*scale)
            x2, y2 = int(x2*scale), int(y2*scale)
            
            # Create a rectangle shape using the scaled coordinates
            bbox = canvas.create_rectangle(x1, y1, x2, y2, outline="#00FF00", width=2)
            
            # Add the bounding box object to the list
            bbox_list.append(bbox)

# Call the update_bounding_boxes function to initialize the bounding boxes
update_bounding_boxes()

# Start the main event loop
root.mainloop()


# In[ ]:




