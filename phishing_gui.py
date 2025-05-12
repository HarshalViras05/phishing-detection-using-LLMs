import pandas as pd
import numpy as np
import openai
import tkinter as tk
from tkinter import messagebox, scrolledtext
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.metrics import classification_report


data = {
    'email': [
        'Your account has been locked. Click here to reset your password.',
        'Congratulations! You have won a $1000 gift card. Click here to claim.',
        'Please review the attached invoice for your records.',
        'Important update from your bank. Login now to confirm your details.',
        'Hey, are we still on for the meeting tomorrow?',
        'Your subscription has been renewed. Thank you for your purchase.',
        'You have a package waiting. Click here to schedule delivery.',
        'Just checking in—can you send me the Q2 reports?',
    ] * 20,
    'label': [1, 1, 0, 1, 0, 0, 1, 0] * 20
}
df = pd.DataFrame(data)
df = shuffle(df, random_state=42)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['email'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))


def classify_email():
    email_text = email_input.get("1.0", tk.END).strip()
    if not email_text:
        messagebox.showwarning("Input Error", "Please enter an email message.")
        return

    new_vector = vectorizer.transform([email_text])
    prediction = model.predict(new_vector)[0]
    result_text = "Phishing Email Detected (1)" if prediction == 1 else "Legit Email (0)"
    result_label.config(text=result_text)

def generate_email():
    api_key = api_key_entry.get().strip()
    if not api_key:
        messagebox.showerror("API Key Missing", "Please enter your OpenAI API key.")
        return

    openai.api_key = api_key
    prompt = "Generate a phishing email pretending to be from Netflix asking the user to update their billing information."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cybersecurity researcher generating a phishing simulation."},
                {"role": "user", "content": prompt}
            ]
        )
        phishing_email = response['choices'][0]['message']['content']
        email_input.delete("1.0", tk.END)
        email_input.insert(tk.END, phishing_email)
    except Exception as e:
        messagebox.showerror("API Error", str(e))


window = tk.Tk()
window.title("Phishing Email Classifier with GPT")
window.geometry("700x500")

tk.Label(window, text="Enter OpenAI API Key:", font=("Arial", 12)).pack(pady=5)
api_key_entry = tk.Entry(window, show="*", width=60, font=("Arial", 10))
api_key_entry.pack()

tk.Label(window, text="Email Content:", font=("Arial", 14)).pack(pady=10)
email_input = scrolledtext.ScrolledText(window, height=12, width=80, font=("Arial", 12))
email_input.pack()

tk.Button(window, text="Classify Email", command=classify_email, font=("Arial", 12), bg="#add8e6").pack(pady=10)
tk.Button(window, text="Generate Phishing Email (GPT)", command=generate_email, font=("Arial", 12), bg="#ffa07a").pack(pady=5)

result_label = tk.Label(window, text="", font=("Arial", 16), fg="green")
result_label.pack(pady=10)

window.mainloop()
