import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

df = pd.read_csv(r"C:\Users\Vaishnavi\Documents\my Extra work\TYMiniProject\Datasetfinal_HousePricePrediction.csv")
df.dropna(subset=['bhk', 'type', 'locality', 'Rent_price'], inplace=True)
df['type'] = df['type'].astype(str).str.strip()
df['locality'] = df['locality'].astype(str).str.strip()

le_type = LabelEncoder()
le_locality = LabelEncoder()
df['type_encoded'] = le_type.fit_transform(df['type'])
df['locality_encoded'] = le_locality.fit_transform(df['locality'])

X = df[['bhk', 'type_encoded', 'locality_encoded']]
y = df['Rent_price']

model = DecisionTreeRegressor()
model.fit(X, y)

def create_prediction_page():
    prediction_root = tk.Tk()
    prediction_root.title("PREDICTING HOUSE RENT PRICES")
    screen_width = prediction_root.winfo_screenwidth()
    screen_height = prediction_root.winfo_screenheight()
    prediction_root.geometry(f"{screen_width}x{screen_height}")

    
    image_path = r"C:\Users\Vaishnavi\Documents\my Extra work\TYMiniProject\houseMainImage.jpg"
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(prediction_root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        prediction_root.bg_photo = bg_photo
    except Exception as e:
        print(f"Error loading background image: {e}")
    
    title_label = tk.Label(prediction_root, text="PREDICTING HOUSE RENT PRICES", font=("Helvetica", 28, "bold"),
                           bg="lightgray", fg="black", pady=10)
    title_label.place(relx=0.5, rely=0.05, anchor="center")

    
    bhk_options = sorted([str(int(bhk)) for bhk in df['bhk'].unique()])
    type_options = sorted(df['type'].unique().tolist())
    locality_options = sorted(df['locality'].unique().tolist())

    bhk_var = tk.StringVar()
    type_var = tk.StringVar()
    locality_var = tk.StringVar()
    
    def create_dropdown(label_text, var, y_pos, options):
        label = tk.Label(prediction_root, text=label_text, font=("Helvetica", 18, "bold"), bg="lightgray")
        label.place(relx=0.35, rely=y_pos, anchor="center")

        entry = ttk.Combobox(prediction_root, textvariable=var, values=options, state="readonly", font=("Helvetica", 16))
        entry.place(relx=0.58, rely=y_pos, anchor="center")
        entry.config(width=30)  
        return entry

    create_dropdown("BHK Type:", bhk_var, 0.25, bhk_options)
    create_dropdown("Type of House:", type_var, 0.35, type_options)
    create_dropdown("Locality:", locality_var, 0.45, locality_options)
    
    result_label = tk.Label(prediction_root, text="", font=("Helvetica", 16), bg="lightgray")
    result_label.place(relx=0.5, rely=0.7, anchor="center")

    def predict_price():
        try:
            bhk = int(bhk_var.get())
            house_type = type_var.get().strip()
            locality = locality_var.get().strip()

            if house_type not in le_type.classes_:
                result_label.config(text="⚠ Type of house not found in dataset.")
                return
            if locality not in le_locality.classes_:
                result_label.config(text="⚠ Locality not found in dataset.")
                return

            type_encoded = le_type.transform([house_type])[0]
            locality_encoded = le_locality.transform([locality])[0]

            match = df[
                (df['bhk'] == bhk) &
                (df['type_encoded'] == type_encoded) &
                (df['locality_encoded'] == locality_encoded)
            ]

            if match.empty:
                result_label.config(text="⚠ No Matching House Available for the entered BHK, type, and locality.\nPlease enter a valid combination.")
                return

            input_data = np.array([[bhk, type_encoded, locality_encoded]])
            predicted_price = model.predict(input_data)[0]
            result_label.config(text=f"✅ Predicted Rent Price: ₹{int(predicted_price):,} / month")
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    predict_btn = tk.Button(prediction_root, text="Predict Price", font=("Helvetica", 16, "bold"),
                            bg="orange", fg="black", padx=20, pady=10, command=predict_price)
    predict_btn.place(relx=0.5, rely=0.6, anchor="center")

    prediction_root.mainloop()

def open_prediction_page():
    root.destroy()
    create_prediction_page()

root = tk.Tk()
root.title("Welcome - House Rent Prediction System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

image_path = r"C:\Users\Vaishnavi\Documents\my Extra work\TYMiniProject\Wellcome Image.jpg"
try:
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    root.bg_photo = bg_photo
except Exception as e:
    print(f"Background image error: {e}")

welcome_label = tk.Label(
    root,
    text="WELCOME TO THE HOUSE RENT PREDICTION SYSTEM",
    font=("Helvetica", 30, "bold"),
    fg="white",
    bg="black",
    padx=20,
    pady=20
)
welcome_label.place(relx=0.5, rely=0.15, anchor="center")

start_button = tk.Button(
    root,
    text="START PREDICTING",
    font=("Helvetica", 20, "bold"),
    bg="orange",
    fg="black",
    padx=30,
    pady=15,
    command=open_prediction_page
)
start_button.place(relx=0.5, rely=0.3, anchor="center")

root.mainloop()
