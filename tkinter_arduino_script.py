import os
import face_recognition as fr
import serial
import time
import cv2
import tkinter as tk
from tkinter import ttk, messagebox

# Define the serial port and baud rate
serial_port = 'COM8'  
baud_rate = 9600

# Open serial port
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  # Wait for Arduino to initialize
admin_image_path = "C:\\Users\\ASUS\\my_images\\my needed code\\my_images\\binisha_mahaj_00000.jpg"  # Replace with the path to the admin's image
admin_encoding = fr.face_encodings(fr.load_image_file(admin_image_path))[0]
ADMIN_PASSWORD = "admin123"
MAX_PASSWORD_ATTEMPTS = 3

# Initialize the variable to track password attempts
password_attempts = 0

# Function to load registered voters' data
def load_registered_data():
    registered_data = {}
    for filename in os.listdir("C:\\Users\\ASUS\\my_images\\my needed code\\my_images"):
        if filename.endswith('.jpg'):
            parts = filename.split('_')
            if len(parts) >= 3:
                first_name = parts[0]
                last_name = parts[1]
                voter_id = '_'.join(parts[2:]).split('.')[0]
                registered_data[voter_id] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'image_path': os.path.join("C:\\Users\\ASUS\\my_images\\my needed code\\my_images", filename),
                    'voted': False  # Initially, no one has voted
                }
            else:
                print(f"Error: Invalid filename format for {filename}. Skipping.")
    return registered_data

# Function to send commands to Arduino based on face recognition results
def send_command_to_arduino(command):
    ser.write(command)
    time.sleep(0.5)  # Add a delay to ensure Arduino has enough time to process the command

# Function for custom face recognition
def face_recognition_custom(captured_frame, registered_face_path):
    face_encodings = fr.face_encodings(captured_frame)
    if not face_encodings:
        return False  # No face detected in the captured frame

    captured_encoding = face_encodings[0]  # Take the first face encoding
    registered_image = fr.load_image_file(registered_face_path)
    registered_encoding = fr.face_encodings(registered_image)[0]  # Take the first face encoding

    if registered_encoding is None:
        return False  # No face detected in the registered image

    distance = fr.face_distance([registered_encoding], captured_encoding)
    return distance[0] <= 0.6  # Adjust the tolerance level as needed

# Function to display result (only accessible by admin)
def display_result():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Admin Access", "Please enter the admin password.")
        return

    global password_attempts
    if password == ADMIN_PASSWORD:
        # Display result
        print("Displaying result:")
        send_command_to_arduino(b'c')
    else:
        password_attempts += 1
        remaining_attempts = MAX_PASSWORD_ATTEMPTS - password_attempts
        if remaining_attempts > 0:
            messagebox.showerror("Admin Access", f"Incorrect password. {remaining_attempts} attempt{'s' if remaining_attempts > 1 else ''} remaining.")
            entry_password.delete(0, tk.END)  # Clear the password entry field
        else:
            messagebox.showerror("Admin Access", "Maximum attempts reached. Access denied.")

# Function to handle exit and show admin access button
def exit_and_show_admin_access():
    button_exit.grid_remove()
    button_admin_access.grid(row=4, columnspan=2, pady=(10, 20))

# Function to handle admin access
def admin_access():
    # Display activating camera message
    print("Activating Camera...")

    # Open the webcam (the default webcam, usually index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open the webcam.")
        return False

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't capture a frame.")
        cap.release()
        return False

    # Release the webcam
    cap.release()

   

    # Show the captured frame
    cv2.imshow("Camera Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Perform face recognition
    if face_recognition_custom(frame, admin_image_path):
        print("Face recognized. Please enter password.")
        label_password.grid(row=5, column=0, padx=(10, 0))
        entry_password.grid(row=5, column=1)
        button_display_result.grid(row=6, columnspan=2, pady=(10, 20), padx=20)
    else:
        messagebox.showerror("Admin Access", "Face not recognized. Access denied.")

# Function to handle user submission
def submit(registered_voters):
    # Display activating camera message
    print("Activating Camera...")
    # Open the webcam (the default webcam, usually index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open the webcam.")
        return False

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't capture a frame.")
        cap.release()
        return False

    # Release the webcam
    cap.release()

    # Show the captured frame
    cv2.imshow("Camera Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    voter_id = entry_voter_id.get()
    # Check if the voter ID exists in the registered voters dictionary
    if voter_id not in registered_voters:
        print(f"Error: Voter ID {voter_id} not found.")
        messagebox.showerror("Voter ID Not Found", f"Voter ID {voter_id} not found.")
        send_command_to_arduino(b'b')  # Command to display "Invalid Person" on LCD
        return False
    # Check if the voter has already voted
    if registered_voters[voter_id]['voted']:
        print(f"Error: Voter {voter_id} has already voted.")
        messagebox.showerror("Already Voted", f"Voter {voter_id} has already voted.")
        send_command_to_arduino(b'e')  # Command to display "Already Voted" on LCD
        return False
    # Check if the entered first name, last name, and voter ID match the pre-registered data
    if (registered_voters[voter_id]['first_name'] != first_name or
        registered_voters[voter_id]['last_name'] != last_name):
        print("Error: Voter details do not match pre-registered data.")
        messagebox.showerror("Invalid Voter Details", "Voter details do not match pre-registered data.")
        send_command_to_arduino(b'b')  # Command to display "Invalid Person" on LCD
        return False


    # Open the webcam (the default webcam, usually index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open the webcam.")
        return False

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't capture a frame.")
        cap.release()
        return False

    # Release the webcam
    cap.release()

    # Perform face recognition
    if face_recognition_custom(frame, registered_voters[voter_id]['image_path']):
        print(f"Welcome {first_name} {last_name} (Voter ID: {voter_id})")
        send_command_to_arduino(b'a')
        time.sleep(1)

        # Mark the voter as voted
        registered_voters[voter_id]['voted'] = True
              # Wait for acknowledgment from Arduino
        while True:
            if ser.in_waiting:
                message = ser.readline().decode().strip()
                if message == "Vote Taken":
                    print("Vote Taken")
                    break

               # Increment vote count for the chosen candidate
        clear_fields()

    else:
        print("Error: Face not recognized. You are not registered.")
        send_command_to_arduino(b'f')
        time.sleep(1)
        return False

# Function to clear input fields
def clear_fields():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_voter_id.delete(0, tk.END)

# Create Tkinter window
root = tk.Tk()
root.title("Voting System")

# Set window size and center it on the screen
window_width = 400
window_height = 350
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Load registered voters' data
registered_voters = load_registered_data()

# Create style for themed widgets
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="black", background="lightblue")
style.configure("TLabel", font=("Helvetica", 10), foreground="black")
style.configure("TEntry", font=("Helvetica", 10))

# Create labels and entry fields for user details
label_first_name = ttk.Label(root, text="First Name:")
label_first_name.grid(row=0, column=0, padx=(20, 5), pady=(20, 5))
entry_first_name = ttk.Entry(root)
entry_first_name.grid(row=0, column=1, padx=5, pady=(20, 5))

label_last_name = ttk.Label(root, text="Last Name:")
label_last_name.grid(row=1, column=0, padx=(20, 5), pady=5)
entry_last_name = ttk.Entry(root)
entry_last_name.grid(row=1, column=1, padx=5, pady=5)

label_voter_id = ttk.Label(root, text="Voter ID:")
label_voter_id.grid(row=2, column=0, padx=(20, 5), pady=(5, 20))
entry_voter_id = ttk.Entry(root)
entry_voter_id.grid(row=2, column=1, padx=5, pady=(5, 20))

button_submit = ttk.Button(root, text="Submit", command=lambda: submit(registered_voters))
button_submit.grid(row=3, column=0, padx=(20, 5), pady=5)
button_clear = ttk.Button(root, text="Clear", command=clear_fields)
button_clear.grid(row=3, column=1, padx=5, pady=5)

button_exit = ttk.Button(root, text="Exit", command=exit_and_show_admin_access)
button_exit.grid(row=4, column=0, padx=(20, 5), pady=(5, 20))

# Create Admin Access button (initially hidden)
button_admin_access = ttk.Button(root, text="Admin Access", command=admin_access)
button_admin_access.grid(row=4, column=1, padx=5, pady=(5, 20))
button_admin_access.grid_remove()

# Create label and entry field for admin password
label_password = ttk.Label(root, text="Admin Password:")
entry_password = ttk.Entry(root, show="*")

# Create button to display result (only accessible by admin)
button_display_result = ttk.Button(root, text="Display Result", command=display_result)

root.mainloop()

# Close the serial connection when done
ser.close()
