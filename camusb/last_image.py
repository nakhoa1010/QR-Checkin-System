import os
import time

# Specify the folder path where the new image might be added
folder_path = r'D:\document\95IDEAL\code\QR_Event-main\facepath'
while True:
    # Get the list of files in the folder before the new image is added
    before = os.listdir(folder_path)

    # Wait for a moment (for example, 1 second)
    time.sleep(1)

    # Add your new image to the folder programmatically or manually

    # Get the list of files in the folder after the new image is added
    after = os.listdir(folder_path)

    # Find the new image by comparing the lists
    new_image = set(after) - set(before)

    # Get the full path of the new image
    if new_image:
        new_image_path = os.path.join(folder_path, new_image.pop())
        print("Path of the new image:", new_image_path)
    else:
        print("No new image added to the folder.")