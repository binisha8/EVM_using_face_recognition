import cv2
import os
while True:
 def is_voter_id_valid(voter_id):
    # Check if voter ID already exists in the images directory
    image_files = os.listdir("C:\\Users\\ASUS\\my_images\\my needed code\\my_images")
    for filename in image_files:
        if filename.endswith(".jpg"):
            existing_voter_id = filename.split("_")[1].split(".")[0]
            if existing_voter_id == voter_id:
                return False
    return True

 def capture_image(first_name, last_name, voter_id):
    # Create directories to store images
    if not os.path.exists("C:\\Users\\ASUS\\my_images\\my needed code\\my_images"):
        os.makedirs("C:\\Users\\ASUS\\my_images\\my needed code\\my_images")

    # Check if voter ID is valid
    if not is_voter_id_valid(voter_id):
        print("Error: Voter ID already exists. Please choose a different one.")
        return

    # Open the webcam (the default webcam, usually index 0)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Couldn't open the webcam.")
        return

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't capture a frame.")
        cap.release()
        return

    # Save the captured frame as an image file
    folder_path = "C:\\Users\\ASUS\\my_images\\my needed code\\my_images"
    filename = f"{first_name}_{last_name}_{voter_id}.jpg"
    file_path = os.path.join(folder_path, filename)
    cv2.imwrite(file_path, frame)
    print(f"Image saved successfully: {file_path}")

    # Release the webcam
    cap.release()

 if __name__ == "__main__":
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    voter_id = input("Enter your voter's card ID: ")
    capture_image(first_name, last_name, voter_id)

 choice=input("Enter 'Q' to quit:").upper()
 if choice=='Q':
   break

