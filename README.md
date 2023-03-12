# image-quantization

## The program gives user two options

### 1- Quantize an image
    First, we ask the user for the number of bits to use for each color channel (M, N, and O) in the quantization process.

    Then, we load the image into a NumPy array using the numpy.array() function. Each pixel in the image is represented by a triplet of values representing the red, green, and blue (RGB) color channels.

    The next step is to perform the quantization. We first divide each pixel value in the image by 2^(8-m) to scale it down to a range of 0 to 2^m-1. Then, we round the resulting value to the nearest integer and multiply it back up by 2^(8-m) to scale it back up to the original range. 
    This effectively quantizes the pixel value to the nearest multiple of 2^(8-m). We do the same thing for the green and blue channels using the values of N and O, respectively.

    Finally, we convert the quantized image data back to an array of 8-bit unsigned integers using the numpy.astype() function and save it to disk in the custom '.gsr' file format.

### 2- Convert a .gsr image to JPEG
    First, we ask the user for the filename of the '.gsr' image to convert.

    Then, we use the Pillow Image.open() function to open the image file and create an Image object.

    We extract the pixel data from the Image object using the numpy.asarray() function and convert it to a NumPy array.

    The next step is to convert the quantized 8-bit pixel values back to their original 24-bit RGB values. We do this by multiplying each pixel value by 2^(8-m), 2^(8-n), and 2^(8-o) for the red, green, and blue channels, respectively.

    Finally, we create a new Pillow Image object from the 24-bit RGB NumPy array using the Image.fromarray() function and save it to disk in the JPEG format using the Image.save() method.
    
## .GSR File Format conversion

  Write the width and height of the image to the file header. This is done using the struct.pack() function to pack each value as an unsigned 32-bit integer ("I") and write it to the file.

Next, write the pixel data to the file. The program loop over each row and column of the image, and write each pixel to the file as a sequence of three bytes, in the order (R, G, B).


## Comparision
24 bit pepers image before an after quantization to 8 8 0 (RGB)

![image](https://user-images.githubusercontent.com/65772647/224569146-4bf246dd-4e8d-4296-867b-0b702d7fd565.png)
