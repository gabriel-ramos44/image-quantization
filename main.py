import numpy as np
import struct
from PIL import Image
import os

def quantize_image():
    # Ask for user input for image file name and quantization bits
    image_file = input("Enter image file name: ")
    m = int(input("Enter number of bits for red channel (M): "))
    n = int(input("Enter number of bits for green channel (N): "))
    o = int(input("Enter number of bits for blue channel (O): "))

    # Open the image file
    img = Image.open(image_file)

    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Quantize the image by scaling down each color channel value, rounding to the nearest integer, and scaling back up
    """  
    We first divide each pixel value in the image by 2^(8-m)
    to scale it down to a range of 0 to 2^m-1.
    Then, we round the resulting value to the nearest integer
    and multiply it back up by 2^(8-m) to scale it back up to
    the original range. 
    This effectively quantizes the pixel value
    to the nearest multiple of 2^(8-m).
    We do the same thing for the green and blue
    channels using the values of N and O, respectively.
    """
    new_img_array = np.round(img_array / (2**(8-m))) * (2**(8-m))    # Quantize the red channel with m bits
    new_img_array[:,:,1] = np.round(img_array[:,:,1] / (2**(8-n))) * (2**(8-n))    # Quantize the green channel with n bits
    new_img_array[:,:,2] = np.round(img_array[:,:,2] / (2**(8-o))) * (2**(8-o))    # Quantize the blue channel with o bits
    
    new_img_array = new_img_array.astype(np.uint8)   # Convert the quantized image back to 8-bit unsigned integers
    

    # Get the dimensions of the quantized image
    height, width, channels = new_img_array.shape

    
    # Open a file for writing in binary mode
    with open("quantized_" + image_file + ".gsr", "wb") as f:
        # Write the width and height to the file header
        f.write(struct.pack("I", width))
        f.write(struct.pack("I", height))
    
        # Write the pixel data to the file
        for row in range(height):
            for col in range(width):
                pixel = new_img_array[row, col]
                f.write(bytes(pixel))
  
    # Save the quantized image as JPEG
    #quantized_img = Image.fromarray(new_img_array)
    #quantized_img.save("quantized_" + image_file + ".jpg")
    #print("Quantized image saved as: quantized_" + image_file + ".jpg")

    

def convert_gsr_to_jpeg():
    # Ask user for a '.gsr" image to convert to jpeg without doing quantization
    image_file = input("Enter GSR image file name to convert to JPEG: ")

    # Check if the file is a valid GSR file
    if not os.path.isfile(image_file):
        print("Invalid file name!")
        return
    elif not image_file.endswith(".gsr"):
        print("Invalid file extension!")
        return

    # Open the GSR image file
    with open(image_file, "rb") as f:
        # Read the width and height from the file header
        width_bytes = f.read(4)
        height_bytes = f.read(4)
        width = struct.unpack("I", width_bytes)[0]
        height = struct.unpack("I", height_bytes)[0]

        # Read the pixel data from the file
        pixel_data = f.read()
        num_pixels = len(pixel_data) // 3
        if len(pixel_data) % 3 != 0:
            print("Invalid file format!")
            return
        pixels = np.zeros((num_pixels, 3), dtype=np.uint8)
        for i in range(num_pixels):
            r = pixel_data[i*3]
            g = pixel_data[i*3+1]
            b = pixel_data[i*3+2]
            pixels[i,:] = [r, g, b]

    # Reshape the pixel data to the image dimensions
    img_array = np.reshape(pixels, (height, width, 3))

    # Save the GSR image as JPEG
    jpeg_img = Image.fromarray(img_array)
    jpeg_img.save(image_file[:-4] + ".jpg")
    print("JPEG image saved as: " + image_file[:-4] + ".jpg")

# Main program
while True:
    print("Select an option:")
    print("1. Quantize an image")
    print("2. Convert a .gsr image to JPEG")

    option = input("> ")

    if option == "1":
        quantize_image()
    if option == "2":
        convert_gsr_to_jpeg()