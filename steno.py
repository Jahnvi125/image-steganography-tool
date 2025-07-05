from tkinter import *
from tkinter import messagebox as mb
from PIL import Image

# Function to convert data to binary
def generate_data(data):
    binary_data = []
    for char in data:
        binary_data.append(format(ord(char), '08b'))
    return binary_data

# Function to encode data in the image
def encode_image(img, data):
    binary_data = generate_data(data)
    data_len = len(binary_data)
    img_data = iter(img.getdata())

    for i in range(data_len):
        pixels = [value for value in next(img_data)[:3] +
                  next(img_data)[:3] +
                  next(img_data)[:3]]
        
        for j in range(8):
            if (binary_data[i][j] == '1' and pixels[j] % 2 == 0):
                pixels[j] += 1
            elif (binary_data[i][j] == '0' and pixels[j] % 2 != 0):
                pixels[j] -= 1

        if i == data_len - 1:
            if pixels[-1] % 2 == 0:
                pixels[-1] += 1
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

# Function to encode the text into an image
def main_encryption(img_path, text, output_image_name):
    try:
        img = Image.open(img_path)
    except Exception as e:
        mb.showerror("Error", f"Failed to open image. Reason: {e}")
        return

    new_img = img.copy()
    encoded_pixels = encode_image(img, text)
    w, h = new_img.size
    x, y = 0, 0

    for pixel in encoded_pixels:
        new_img.putpixel((x, y), pixel)
        x += 1
        if x == w:
            x = 0
            y += 1

    output_image_name = output_image_name if output_image_name.endswith('.png') else output_image_name + '.png'
    new_img.save(output_image_name, 'PNG')
    mb.showinfo("Success", f"Image saved as {output_image_name}")

# Function to decode data from an image
def main_decryption(img_path, strvar):
    try:
        img = Image.open(img_path)
    except Exception as e:
        mb.showerror("Error", f"Failed to open image. Reason: {e}")
        return

    img_data = iter(img.getdata())
    binary_data = ""
    decoded_text = ""

    while True:
        pixels = [value for value in next(img_data)[:3] +
                  next(img_data)[:3] +
                  next(img_data)[:3]]
        
        bin_str = ''.join(['1' if pixel % 2 != 0 else '0' for pixel in pixels[:8]])
        decoded_text += chr(int(bin_str, 2))
        
        if pixels[-1] % 2 != 0:
            break

    strvar.set(decoded_text)
    if decoded_text:
        mb.showinfo("Decoded text", f"The decoded text is: {decoded_text}")
    else:
        mb.showinfo("Info", "No hidden text was found.")

# GUI functions
def encode_image_gui():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='AntiqueWhite')
    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='AntiqueWhite').place(x=220, rely=0)

    Label(encode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=50)

    text_to_encode = Entry(encode_wn, width=35)
    text_to_encode.place(x=350, y=90)

    output_filename = Entry(encode_wn, width=35)
    output_filename.place(x=350, y=130)

    Button(encode_wn, text='Encode the Image', font=('Helvetica', 12), bg='PaleTurquoise', 
           command=lambda: main_encryption(img_path.get(), text_to_encode.get(), output_filename.get())).place(x=220, y=175)

def decode_image_gui():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='Bisque')

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='Bisque').place(x=220, rely=0)

    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12), bg='Bisque').place(x=10, y=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(x=350, y=50)

    text_strvar = StringVar()

    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='PaleTurquoise', 
           command=lambda: main_decryption(img_entry.get(), text_strvar)).place(x=220, y=90)

    Label(decode_wn, text='Decoded text:', font=("Times New Roman", 12), bg='Bisque').place(x=180, y=130)

    decoded_text_entry = Entry(decode_wn, width=94, textvariable=text_strvar, state='disabled')
    decoded_text_entry.place(x=15, y=160, height=100)

# Main Window
root = Tk()
root.title('Image Steganography')
root.geometry('300x200')
root.resizable(0, 0)
root.config(bg='NavajoWhite')

Label(root, text='Image Steganography', font=('Comic Sans MS', 15), bg='NavajoWhite').pack(pady=10)

Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=encode_image_gui).pack(pady=10)
Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=decode_image_gui).pack(pady=10)

root.mainloop() 