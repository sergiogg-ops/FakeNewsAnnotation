#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttkb
from pandas import read_json
from sklearn.metrics import f1_score, accuracy_score
import os

# CONSTANTES DE CONTROL
DATA_PATH = 'data.json'
LABEL = {'Real': 1, 'Fake': 0}
MAX = 10
# COLORES
BG_COLOR = "#f0f0f0"
HEADLINE_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
BUTTON_TEXT_COLOR = "white"
FRAME_BG = "#ffffff"
PROGRESS_BG = "#e0e0e0"
PROGRESS_COLOR = "#2ecc71"
# ASPECTO
THEME = 'solar'
CONTROL_FONT = ('georgia', 14)

def read_data(path):
    '''
    Reads the news dataset from the given path and returns the texts, headlines and labels.

    Parameters:
        path (str): The path to the JSON file containing the dataset.
    
    Returns:
        texts (list): The list of texts.
        headlines (list): The list of headlines.
        labels (list): The list of labels.
    '''
    data = read_json(path).sample(MAX)
    texts = data['text'].tolist()
    headlines = data['title'].tolist()
    labels = [LABEL[l] for l in data['label']]
    return texts, headlines, labels

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    '''
    Creates a rounded rectangle on the given canvas.

    Parameters:
        canvas (tk.Canvas): The canvas where the rectangle will be drawn.
        x1 (int): The x-coordinate of the top-left corner.
        y1 (int): The y-coordinate of the top-left corner.
        x2 (int): The x-coordinate of the bottom-right corner.
        y2 (int): The y-coordinate of the bottom-right corner.
        radius (int): The radius of the corners.
        kwargs (dict): Additional arguments for the rectangle.
    
    Returns:
        int: The id of the created rectangle
    '''
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

def create_rounded_button(parent, text, command, width, height, corner_radius, bg_color, fg_color):
    '''
    Creates a rounded button on the given parent widget.

    Parameters:
        parent (tk.Widget): The parent widget where the button will be placed.
        text (str): The text displayed on the button.
        command (function): The function to be called when the button is pressed.
        width (int): The width of the button.
        height (int): The height of the button.
        corner_radius (int): The radius of the corners.
        bg_color (str): The background color of the button.
        fg_color (str): The text color of the button.
    
    Returns:
        tk.Canvas: The created button.
    '''
    def on_enter(e):
        canvas.itemconfig(button_id, fill="#2980b9")
    
    def on_leave(e):
        canvas.itemconfig(button_id, fill=bg_color)

    canvas = tk.Canvas(parent, width=width, height=height, bg=BG_COLOR, highlightthickness=0)
    button_id = create_rounded_rectangle(canvas, 0, 0, width, height, corner_radius, fill=bg_color)
    canvas.create_text(width/2, height/2, text=text, font=CONTROL_FONT, fill=fg_color)
    
    canvas.bind("<ButtonPress-1>", command)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas

class RoundedFrame(tk.Frame):
    def __init__(self, parent, bg_color, corner_radius, **kwargs):
        '''
        Rounded frame widget.

        Parameters:
            parent (tk.Widget): The parent widget where the frame will be placed.
            bg_color (str): The background color of the frame.
            corner_radius (int): The radius of the corners.
            kwargs (dict): Additional arguments for the frame.
        '''
        super().__init__(parent, **kwargs)
        self.bg_color = bg_color
        self.corner_radius = corner_radius

        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bind("<Configure>", self.draw_rounded_frame)

    def draw_rounded_frame(self, event=None):
        self.canvas.delete("all")
        width, height = self.winfo_width(), self.winfo_height()
        create_rounded_rectangle(self.canvas, 0, 0, width, height, self.corner_radius, fill=self.bg_color, outline="")

class CustomProgressBar(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg_color, fill_color, **kwargs):
        '''
        Custom progress bar widget.

        Parameters:
            parent (tk.Widget): The parent widget where the progress bar will be placed.
            width (int): The width of the progress bar.
            height (int): The height of the progress bar.
            corner_radius (int): The radius of the corners.
            bg_color (str): The background color of the progress bar.
            fill_color (str): The fill color of the progress bar.
            kwargs (dict): Additional arguments for the progress bar.
        '''
        super().__init__(parent, width=width, height=height, bg=BG_COLOR, highlightthickness=0, **kwargs)
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.width = width
        self.height = height
        self.value = 0

        self.draw_bar()

    def draw_bar(self):
        self.delete("all")
        create_rounded_rectangle(self, 0, 0, self.width, self.height, self.corner_radius, fill=self.bg_color, outline="")
        if self.value > 0:
            fill_width = (self.value / 100) * self.width
            create_rounded_rectangle(self, 0, 0, fill_width, self.height, self.corner_radius, fill=self.fill_color, outline="")

    def set(self, value):
        self.value = value
        self.draw_bar()

def load_next_text():
    '''
    Displays the next text in the list of texts.
    '''
    global curr_t, result, gold
    if curr_t < len(texts):
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, texts[curr_t])
        classification_var.set("")
        index_label.config(text=f"Article {curr_t + 1} of {len(texts)}")
        headline.config(text=headlines[curr_t])
        progress_bar.set(curr_t / len(texts) * 100)
    else:
        f1 = f1_score(gold, result)
        acc = accuracy_score(gold, result)
        messagebox.showinfo("Done", f"You have classified all texts.\n\nF1 Score: {f1:.2%}\nAccuracy: {acc:.2%}")
        root.quit()

def confirm_classification(event):
    '''
    Confirms the selected classification and loads the next text.

    Parameters:
        event (tk.Event): The event that triggered the function.
    '''
    global curr_t
    selected_option = classification_var.get()
    if selected_option:
        result[curr_t] = int(selected_option)
        curr_t += 1
        load_next_text()
    else:
        messagebox.showwarning("Warning", "Please select an option before confirming.")

if __name__ == "__main__":
    try:
        texts, headlines, gold = read_data(DATA_PATH)
    except:
        messagebox.showerror("Error", "The data file could not be read.\nIt must be a JSON file located at: " + os.path.join(os.getcwd(),DATA_PATH) + "\nIf it is there, it might be corrupted.")
        exit(1)
    result = [0]*len(texts)
    curr_t = 0

    # General settings
    root = tk.Tk()
    root.title("Fake News Classification")
    root.configure(bg=BG_COLOR)
    try:
        root.iconphoto(True, tk.PhotoImage(file='prhlt_logo.png'))
    except:
        messagebox.showwarning("Warning", "The logo file could not be found. Please make sure it is in the same directory as the script:\n" + os.path.join(os.getcwd(),'prhlt_logo.png'))
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=40, pady=20)

    # Upper frame
    header_frame = tk.Frame(main_frame, bg=BG_COLOR)
    header_frame.pack(fill="x", pady=(0, 20))

    index_label = tk.Label(header_frame, text="", font=('helvetica', 12), bg=BG_COLOR)
    index_label.pack(side="left")

    headline = tk.Label(header_frame, text="", font=('helvetica', 18, 'bold'), fg=HEADLINE_COLOR, bg=BG_COLOR, wraplength=screen_width-100)
    headline.pack(side="right", expand=True)

    # Text frame
    text_frame = tk.Frame(main_frame, bg=BG_COLOR)
    text_frame.pack(fill="both", expand=True, pady=10)

    text_display = tk.Text(text_frame, wrap="word", font=("helvetica", 14), bg=FRAME_BG, relief="flat", padx=20, pady=20)
    text_display.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame, command=text_display.yview)
    scrollbar.pack(side="right", fill="y")
    text_display.config(yscrollcommand=scrollbar.set)

    # Control section
    classification_frame = tk.Frame(main_frame, bg=BG_COLOR)
    classification_frame.pack(pady=20)

    classification_var = tk.StringVar(value="")
    
    style = ttkb.Style(THEME)
    style.configure('success.Outline.Toolbutton', font=CONTROL_FONT)
    style.configure('warning.Outline.Toolbutton', font=CONTROL_FONT)

    radio_f = ttk.Radiobutton(classification_frame, text="Real", variable=classification_var, value=str(LABEL['Real']),
                              style='success.Outline.Toolbutton')
    radio_f.pack(side="left", padx=20)

    radio_t = ttk.Radiobutton(classification_frame, text="Fake", variable=classification_var, value=str(LABEL['Fake']), 
                              style='warning.Outline.Toolbutton')
    radio_t.pack(side="left", padx=20)

    #confirm_button = tk.Button(main_frame, text="Confirm", font=CONTROL_FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    #confirm_button.bind("<ButtonPress-1>", confirm_classification)
    confirm_button = create_rounded_button(main_frame, "Confirm", confirm_classification, 120, 40, 20, BUTTON_COLOR, BUTTON_TEXT_COLOR)
    confirm_button.pack(pady=20)

    progress_bar = CustomProgressBar(main_frame, width=300, height=20, corner_radius=10, bg_color=PROGRESS_BG, fill_color=PROGRESS_COLOR)
    progress_bar.pack(pady=10)

    load_next_text()

    root.mainloop()