from customtkinter import *
import customtkinter as ctk
from PIL import Image, ImageFilter
import numpy as np

# Window Appearance
ImageLabel = None
OriginalImage = None
root = CTk()
root._set_appearance_mode("dark")
root.geometry("1500x800")
root.title("Image Processing Software")
ctk.set_default_color_theme("green")

# Header
HeaderLabel = CTkLabel(root, text="Image Processing Software", font=(None, 30))
HeaderLabel.place(relx=0.53, y=20, anchor="n")

# S&P noise algorithm
def salt_and_pepper_noise(image, SaltProb, PepperProb):
    ImageArray = np.array(image)
    RandomValues = np.random.rand(*ImageArray.shape)
    ImageArray[RandomValues < SaltProb] = 255  # Salt
    ImageArray[RandomValues > 1 - PepperProb] = 0  # Pepper
    NoisyImage = Image.fromarray(ImageArray)
    return NoisyImage

# Submit Button
def click_handler(ImagePath=NONE):
    global OriginalImage
    try:
        if ImagePath: OriginalImage = Image.open(ImagePath)
        else: OriginalImage = Image.open(FileEntry.get())
        
        display_image(OriginalImage)
    except Exception as e:
        print(f"Error opening image: {e}")
        ErrorLabel = CTkLabel(root, text="*Unsupported File Type*", font=(None, 12), text_color="red")
        ErrorLabel.place(relx=0.5, y=100, anchor="n")

def display_image(image):
    global ImageLabel,FilteredImage
    ImageSize=(550,550)
    SelectedCTkImage = CTkImage(light_image=image, size=(ImageSize))
    
    if ImageLabel is None:
        ImageLabel = CTkLabel(root, text="", image=SelectedCTkImage)
        ImageLabel.place(x=800, y=110, anchor="n")
    else: ImageLabel.configure(image=SelectedCTkImage)
    FilteredImage = image

def checkbox_event():
    global OriginalImage
    if OriginalImage is None: return
    SelectedImage = OriginalImage
    if BlurCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.BLUR)
    elif SharpnessCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.SHARPEN)
    elif ContourCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.CONTOUR)
    elif DetailCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.DETAIL)
    elif EmbossCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.EMBOSS)
    elif SmoothCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.SMOOTH)
    elif EdgeEnhanceCheckBox.get(): SelectedImage = OriginalImage.filter(ImageFilter.EDGE_ENHANCE)
    elif SaltPepperCheckBox.get(): SelectedImage = salt_and_pepper_noise(OriginalImage, SaltProb=0.02, PepperProb=0.02)

    display_image(SelectedImage)

# File Left side
FileFrameX = 0  
FileFrameY = 0

blank_box = CTkFrame(root, width=300, height=1000)
blank_box.place(x=FileFrameX, y=FileFrameY)  # Center the box
blank_box.configure(fg_color="lightblue")

# File Entry and Submit Button
input_frame_x = 20  # X position of input frame
input_frame_y = 80  # Y position of input frame

FileEntry = CTkEntry(root, placeholder_text="Enter File Name", width=250)
FileEntry.place(x=input_frame_x, y=input_frame_y)

Button = CTkButton(root, text="Submit", command=click_handler)
Button.place(x=input_frame_x, y=input_frame_y+40)

# Checkboxes
CheckBoxFrame_X = 400 # X position of checkbox frame
CheckBoxFrame_Y = 700  # Y position of checkbox frame

CheckBoxSpacing = 120

BlurCheckBox = CTkCheckBox(root, text="Blur", command=checkbox_event)
BlurCheckBox.place(x=CheckBoxFrame_X, y=CheckBoxFrame_Y)

SharpnessCheckBox = CTkCheckBox(root, text="Sharpness", command=checkbox_event)
SharpnessCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing, y=CheckBoxFrame_Y)

ContourCheckBox = CTkCheckBox(root, text="Contour", command=checkbox_event)
ContourCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing*2, y=CheckBoxFrame_Y)

DetailCheckBox = CTkCheckBox(root, text="Detail", command=checkbox_event)
DetailCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing*3, y=CheckBoxFrame_Y)

EmbossCheckBox = CTkCheckBox(root, text="Emboss", command=checkbox_event)
EmbossCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing*4, y=CheckBoxFrame_Y)

SmoothCheckBox = CTkCheckBox(root, text="Smooth", command=checkbox_event)
SmoothCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing*5, y=CheckBoxFrame_Y)

EdgeEnhanceCheckBox = CTkCheckBox(root, text="edgeEnhance", command=checkbox_event)
EdgeEnhanceCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing*6, y=CheckBoxFrame_Y)

SaltPepperCheckBox = CTkCheckBox(root, text="Salt and Pepper Noise", command=checkbox_event)
SaltPepperCheckBox.place(x=CheckBoxFrame_X+CheckBoxSpacing*7, y=CheckBoxFrame_Y)

def select_file():
    FileName = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    if FileName:click_handler(FileName)

#File Browse
FileBrowseButton = CTkButton(root, text="Open File", command=select_file)
FileBrowseButton.place(x=FileFrameX+20, y=FileFrameY+20)

def save_image():
    if FilteredImage is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"),("JPEG files", "*.jpg"),("All files", "*.*")])
        if save_path: FilteredImage.save(save_path)

#File Save (with filter)
FileSaveButton = CTkButton(root, text="SaveFile",command=save_image)
FileSaveButton.place(x=FileFrameX+20, y=FileFrameY+750)

root.mainloop()