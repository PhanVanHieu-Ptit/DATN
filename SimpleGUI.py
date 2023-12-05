import tkinter as tk
from tkinter import filedialog
import os

def upload_file():
    file_path = filedialog.askopenfilename()
    print(file_path)
    # Add code to handle the uploaded file
    # You can store the file path in a variable and use it when needed
    # For example, you could pass the file path to your models for classification

def classify_document(model, file_path):
    # Add code to load and use the selected models to classify the document
    # Update the result_label with the predicted category
    # You need to define this function based on your specific models and data
    result = "Category: [Predicted Category]"
    result_label.config(text=result)



if __name__ == '__main__':
    app = tk.Tk()
    app.title("Document Category Classifier")
    app.geometry("400x200")

    upload_button = tk.Button(app, text="Upload File", command=upload_file)
    upload_button.pack()

    model_choice = tk.StringVar()  # Variable to store the selected models
    model_choice.set("Model 1")  # Set a default models

    model_option1 = tk.Radiobutton(app, text="Model 1", variable=model_choice, value="Model 1")
    model_option2 = tk.Radiobutton(app, text="Model 2", variable=model_choice, value="Model 2")



    model_option1.pack()
    model_option2.pack()

    print(model_option1)
    print(model_option2)

    result_label = tk.Label(app, text="Category: ")
    result_label.pack()

    classify_button = tk.Button(app, text="Classify Document",
                                command=lambda: classify_document(model_choice.get(), file_path))
    classify_button.pack()

    app.mainloop()



