import os
from PIL import Image, ImageTk
import pandas as pd
from scipy.spatial.distance import cdist
import numpy as np
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
def predict_crop():
    input_data = np.array([float(value.get()) for value in input_values.values()])
    input_columns = df.columns[:-1]
    distances = cdist(df[input_columns], input_data.reshape(1, -1))
    min_distance_index = np.argmin(distances)
    predicted_crop = df.loc[min_distance_index, 'Crop']
    result_label.config(text=f"Predicted Crop: {predicted_crop}")
    display_crop_image(predicted_crop)
def display_crop_image(crop):
    image_folder = 'images'
    image_path = os.path.join(image_folder, f'{crop}.png')
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((800, 600), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        crop_image_label.config(image=img)
        crop_image_label.image = img
    else:
        print(f"Image for crop '{crop}' not found.")
def switch_to_image_tab(event):
    notebook.select(1)  
def enter_button_clicked():
    home_image_label.pack_forget()  
    welcome_label.pack_forget()  
    enter_button.pack_forget()   
    notebook.select(0)  
    notebook.pack(expand=True, fill='both')

    enter_button.config(state='disabled')  
def reload_button_clicked():
    for value in input_values.values():
        value.set('')
    result_label.config(text='')
    crop_image_label.config(image='')
    crop_image_label.image = None
app = tk.Tk()
app.title("Field Advisor")
style = ThemedStyle(app)
style.set_theme("clam")
app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
app.configure(bg=style.lookup("TFrame", "background"))
font_style = ("Arial", 12)
excel_file_path = 'agri1.csv'
df = pd.read_csv(excel_file_path)
input_values = {column: tk.StringVar() for column in df.columns[:-1]}
image_path_home = "logo.png"  
home_image_label = ttk.Label(app)
if os.path.exists(image_path_home):
    home_image = Image.open(image_path_home)
    home_image = home_image.resize((600, 400), Image.LANCZOS)
    home_image = ImageTk.PhotoImage(home_image)
    home_image_label = ttk.Label(app, image=home_image)
    home_image_label.image = home_image
    home_image_label.pack(padx=10, pady=10)
else:
    print("Image for home not found.")
welcome_label = ttk.Label(app, text="Welcome to the Field Advisor App", font=("Arial", 16), padding=(10, 20))
welcome_label.pack()

enter_button = ttk.Button(app, text="Enter", command=enter_button_clicked)
enter_button.pack(pady=20)

notebook = ttk.Notebook(app)
working_section = ttk.Frame(notebook)
for i in range(len(df.columns[:-1]) + 3):  
    working_section.grid_rowconfigure(i, weight=1)
    working_section.grid_columnconfigure(0, weight=1)
    working_section.grid_columnconfigure(1, weight=1)
for i, (label_text, input_var) in enumerate(zip(df.columns[:-1], input_values.values())):
    label = ttk.Label(working_section, text=label_text, font=font_style, background=style.lookup("TFrame", "background"), foreground="#336699")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="E")
    entry = ttk.Entry(working_section, textvariable=input_var, font=font_style, style="TEntry")
    entry.grid(row=i, column=1, padx=10, pady=5, sticky="W")
    entry.bind("<Enter>", lambda event, entry=entry: entry.config(style="Highlight.TEntry"))
    entry.bind("<Leave>", lambda event, entry=entry: entry.config(style="TEntry"))
predict_button = ttk.Button(working_section, text="Predict Crop", command=predict_crop, style="TButton")
predict_button.grid(row=len(df.columns[:-1]), column=0, columnspan=2, pady=10, sticky="NEWS")
predict_button.bind("<Enter>", lambda event, button=predict_button: button.config(style="Highlight.TButton"))
predict_button.bind("<Leave>", lambda event, button=predict_button: button.config(style="TButton"))
reload_button = ttk.Button(working_section, text="↻Reload", command=reload_button_clicked, style="TButton")
reload_button.grid(row=len(df.columns[:-1]) + 2, column=0, columnspan=2, pady=10, sticky="NEWS")
reload_button.bind("<Enter>", lambda event, button=reload_button: button.config(style="Highlight.TButton"))
reload_button.bind("<Leave>", lambda event, button=reload_button: button.config(style="TButton"))
result_label = ttk.Label(working_section, text="", font=font_style, background=style.lookup("TFrame", "background"), foreground="#336699")
result_label.grid(row=len(df.columns[:-1]) + 1, column=0, columnspan=2, pady=10, sticky="NEWS")

notebook.add(working_section, text='WORKING')

image_section = ttk.Frame(notebook)
crop_image_label = ttk.Label(image_section, text="Crop Image", font=font_style)
crop_image_label.pack(padx=10, pady=10)
notebook.add(image_section, text='IMAGE')

contact_section = ttk.Frame(notebook)
contact_image_path = ""
if os.path.exists(contact_image_path):
    contact_image = Image.open(contact_image_path)
    contact_image = contact_image.resize((800, 600), Image.LANCZOS)
    contact_image = ImageTk.PhotoImage(contact_image)
    contact_image_label = ttk.Label(contact_section, image=contact_image)
    contact_image_label.image = contact_image
    contact_image_label.pack(padx=10, pady=10)
else:
    print("Image for Contact Us not found.")
developed_by_label = ttk.Label(contact_section, text=" CODE CRAFTERS", font=font_style)
developed_by_label.pack(padx=10, pady=5)
notebook.add(contact_section, text='DEVELOPED BY')
app.mainloop()
