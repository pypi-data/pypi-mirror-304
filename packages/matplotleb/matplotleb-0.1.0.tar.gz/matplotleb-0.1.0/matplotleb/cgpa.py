import tkinter as tk
from tkinter import messagebox # Import messagebox for pop-up messages

# Create the main window
master = tk.Tk()
master.title("CGPA Calculation")
master.geometry("1000x600")
master.configure(bg="#d0f0c0") # Set background to light green

# Frame 1
frame1 = tk.Frame(master, width=1000, height=150, bg="#d0f0c0")
frame1.pack(padx=20, pady=20)

tk.Label(frame1, text="Manonmaniam Sundaranar University", font=("Times New Roman", 20, "bold"), bg="#d0f0c0").grid(row=1, column=7)
tk.Label(frame1, text="Reaccredited with 'A' Grade (CGPA 3.13 Out of 4.0) by NAAC (3rd Cycle)", font=("Times New Roman", 10), bg="#d0f0c0").grid(row=2, column=7)
tk.Label(frame1, text="Tirunelveli - 627012, Tamil Nadu, India", font=("Times New Roman", 13), bg="#d0f0c0").grid(row=3, column=7)

# Frames for input and buttons
frame2 = tk.Frame(master, bg="#d0f0c0")
frame3 = tk.Frame(master, bg="#d0f0c0")
frame2.pack()
frame3.pack()

# Entry fields
prog = tk.Entry(frame2, width=30)
name = tk.Entry(frame2, width=30)
regNo = tk.Entry(frame2, width=30)

# Entry fields for grades
entry = [tk.Entry(frame2, width=10) for _ in range(8)]

tk.Label(frame2, text="Programme:", bg="#d0f0c0").grid(row=3, column=2, pady=20)
prog.grid(row=3, column=3)
tk.Label(frame2, text="Name:", bg="#d0f0c0").grid(row=3, column=5)
name.grid(row=3, column=6)
tk.Label(frame2, text="Reg.No:", bg="#d0f0c0").grid(row=3, column=7)
regNo.grid(row=3, column=8)

# Serial numbers
tk.Label(frame2, text="S.No", bg="#d0f0c0").grid(row=4, column=2, pady=20)
for i in range(8):
    tk.Label(frame2, text=i + 1, bg="#d0f0c0").grid(row=i + 5, column=2)

# Subjects
subList = [
    "Discrete Mathematics",
    "Linux and Shell Programming",
    "Python Programming",
    "Data Engineering",
    "Soft Computing",
    "Data Engineering Lab",
    "Python Programming Lab",
    "Skill Enhancement Course"
]
tk.Label(frame2, text="Subject", bg="#d0f0c0").grid(row=4, column=3, pady=20)
for i, subject in enumerate(subList):
    tk.Label(frame2, text=subject, bg="#d0f0c0").grid(row=i + 5, column=3, sticky="w")

# Subject credits
scredits = [4, 4, 4, 4, 4, 2, 2, 1]
tk.Label(frame2, text="Sub Credit", bg="#d0f0c0").grid(row=4, column=5, pady=20)
for i, credit in enumerate(scredits):
    tk.Label(frame2, text=credit, bg="#d0f0c0").grid(row=i + 5, column=5)

# Grade inputs
tk.Label(frame2, text="Grade", bg="#d0f0c0").grid(row=4, column=6, pady=20)
for i in range(len(entry)):
    entry[i].grid(row=i + 5, column=6, padx=15)

# Result Labels for Grade Points and Credits
grade_point_labels = [tk.Label(frame2, text="", bg="#d0f0c0") for _ in range(8)]
credit_obtained_labels = [tk.Label(frame2, text="", bg="#d0f0c0") for _ in range(8)]

tk.Label(frame2, text="Grade Point", bg="#d0f0c0").grid(row=4, column=7, pady=20)
tk.Label(frame2, text="Credit Obtained", bg="#d0f0c0").grid(row=4, column=8, pady=20, padx=10)

for i in range(8):
    grade_point_labels[i].grid(row=i + 5, column=7)
    credit_obtained_labels[i].grid(row=i + 5, column=8)

# Grade mapping
gradeDict = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "RA": 0, "AA": 0}

# Labels for results
total_label = tk.Label(frame2, text="", bg="#d0f0c0")
total_label.grid(row=18, column=8, pady=20)
cgpa_label = tk.Label(frame2, text="", bg="#d0f0c0")
cgpa_label.grid(row=19, column=8)
classification_label = tk.Label(frame2, text="", bg="#d0f0c0")
classification_label.grid(row=20, column=8, pady=20)

def fade_in(window):
    # Fade-in effect
    for i in range(0, 100, 2): # Change from 0 to 100 in steps of 2
        window.attributes('-alpha', i / 100.0) # Set opacity
        window.update()
        window.after(10) # Adjust the speed of fading

def calculate():
    c = 0
    gc = 0
    has_invalid_grade = False # Flag to check for RA or AA
    
    for i in range(len(entry)):
        v = entry[i].get().upper()
        if v in gradeDict:
            if v == "RA" or v == "AA":
                has_invalid_grade = True # Set flag if RA or AA is found
                credit = 0 # No grade points
                gc += credit * scredits[i] # Credit obtained is still counted
            else:
                credit = gradeDict[v]
                c += scredits[i]
                gc += credit * scredits[i]
            
            # Update results in the window
            grade_point_labels[i].config(text=credit)
            credit_obtained_labels[i].config(text=credit * scredits[i])
        else:
            grade_point_labels[i].config(text="-")
            credit_obtained_labels[i].config(text="-")

    # Calculate CGPA only if there are no RA or AA
    if has_invalid_grade:
        cgpa = 0 # Set CGPA to 0 or skip calculation
        classification = "Can't Calculate"
    else:
        cgpa = gc / c if c > 0 else 0
        # Determine classification
        if cgpa >= 7.5:
            classification = "First Class with Distinction"
        elif cgpa >= 6.0:
            classification = "First Class"
        elif cgpa >= 5.0:
            classification = "Second Class"
        else:
            classification = "Fail"

    # Show results in the main window
    total_label.config(text=gc)
    cgpa_label.config(text=f"{cgpa:.2f}" if not has_invalid_grade else "-")
    classification_label.config(text=classification)

    # Create a pop-up window for displaying results
    result_window = tk.Toplevel(master)
    result_window.title("Calculation Result")
    result_window.geometry("400x300")
    result_window.configure(bg="#d0f0c0")
    result_window.attributes('-alpha', 0) # Start transparent

    # Display name in the pop-up window
    name_display = name.get() # Get the name from the entry field
    tk.Label(result_window, text=name_display, font=("Times New Roman", 16, "bold"), bg="#d0f0c0").pack(pady=10)

    # Display results
    result_message = f"Total Credits: {gc}\nCGPA: {'-' if has_invalid_grade else f'{cgpa:.2f}'}\nClassification: {classification}"
    tk.Label(result_window, text=result_message, font=("Times New Roman", 12), bg="#d0f0c0").pack(pady=20)

    # Start fade-in effect
    fade_in(result_window)

tk.Button(frame2, text="Calculate", width=10, command=calculate, bg="#4caf50", fg="white").grid(row=18, column=6)
tk.Label(frame2, text="Total", bg="#d0f0c0").grid(row=18, column=7, pady=20)
tk.Label(frame2, text="CGPA", bg="#d0f0c0").grid(row=19, column=7)
tk.Label(frame2, text="Classification", bg="#d0f0c0").grid(row=20, column=7)
tk.Label

master.mainloop()
