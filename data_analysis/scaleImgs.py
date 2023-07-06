import os
from PIL import Image

def scale_images(folder_path, scale_factor):
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Iterate over each file in the folder
    for file_name in file_list:
        # Check if the file is an image
        if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
            # Open the image file
            image_path = os.path.join(folder_path, file_name)
            image = Image.open(image_path)

            # Get the new dimensions after scaling
            new_width = int(image.width * scale_factor)
            new_height = int(image.height * scale_factor)

            # Resize the image
            resized_image = image.resize((new_width, new_height))

            # Save the resized image
            resized_image.save(image_path)

            # Close the image file
            image.close()

# Example usage
folder_path = "."  # Replace with the actual folder path
scale_factor = 0.25

scale_images(folder_path, scale_factor)