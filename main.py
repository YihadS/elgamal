import random
from sympy import mod_inverse
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image
import pickle

# Static key values
a = 3  # Your private key
k = 5  # Your random value for encryption

def open_menu():
    ventana = tk.Tk()
    ventana.title("Encriptación ElGamal")
    ventana.geometry("500x500")

    # Main menu interface
    heading_label = tk.Label(ventana, text="Encriptación ElGamal", font=("Arial", 20))
    heading_label.pack(pady=10)
    heading_label.configure(bg="#FFFFFF")

    image = PhotoImage(file="lock.png")
    image_label = tk.Label(ventana, image=image)
    image_label.pack()

    def archivo():
        open_archivo()

    def audio():
        open_audio()

    def imagen():
        open_imagen()

    button1 = tk.Button(ventana, text="Encriptar Texto", command=archivo)
    button2 = tk.Button(ventana, text="Encriptar Audio", command=audio)
    button3 = tk.Button(ventana, text="Encriptar Imagen", command=imagen)

    button1.configure(bg="#2aa3f4")
    button2.configure(bg="#2aa3f4")
    button3.configure(bg="#2aa3f4")
    button1.configure(fg="#FFFFFF")
    button2.configure(fg="#FFFFFF")
    button3.configure(fg="#FFFFFF")

    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

    label_result = tk.Label(ventana, text="", font=("Arial", 16))
    label_result.pack(pady=10)

    ventana.mainloop()

def open_archivo():
    ventana = tk.Toplevel()
    ventana.title("Encriptación de Texto")
    ventana.geometry("400x300")

    # Text file encryption interface

    heading_label = tk.Label(ventana, text="Encriptación de Texto con ElGamal", font=("Arial", 16))
    heading_label.pack(pady=10)

    button_encriptar = tk.Button(ventana, text="Encriptar Texto")
    button_encriptar.pack(pady=5)

    button_desencriptar = tk.Button(ventana, text="Desencriptar Texto")
    button_desencriptar.pack(pady=5)

    def volver_atras():
        ventana.destroy()

    button_atras = tk.Button(ventana, text="Volver Atrás", command=volver_atras)
    button_atras.pack(pady=5)

    button_desencriptar.configure(bg="#2aa3f4")
    button_encriptar.configure(bg="#2aa3f4")
    button_atras.configure(bg="#2aa3f4")
    button_encriptar.configure(fg="#FFFFFF")
    button_desencriptar.configure(fg="#FFFFFF")
    button_atras.configure(fg="#FFFFFF")

    etiqueta_resultado = tk.Label(ventana, text="")
    etiqueta_resultado.pack(pady=10)

    def encriptar(texto_plano, p, g, A):
        C1 = pow(g, k, p)
        C2 = (texto_plano * pow(A, k, p)) % p
        return (C1, C2)

    def desencriptar(C1, C2, p, a):
        s = pow(C1, a, p)
        texto_plano = (C2 * mod_inverse(s, p)) % p
        return texto_plano

    def click_encriptar_texto():
        archivo_entrada = filedialog.askopenfilename(title="Seleccionar Archivo de Entrada")
        archivo_salida = filedialog.asksaveasfilename(title="Seleccionar Archivo de Salida")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'r') as file:
            texto_plano = int(file.read())

        C1, C2 = encriptar(texto_plano, p, g, A)

        with open(archivo_salida, 'w') as file:
            file.write(f"{C1}\n{C2}")

        etiqueta_resultado.config(text=f"Archivo '{archivo_entrada}' encriptado and saved in '{archivo_salida}'")

    def click_desencriptar_texto():
        archivo_entrada = filedialog.askopenfilename(title="Select Encrypted File")
        archivo_salida = filedialog.asksaveasfilename(title="Select Output File")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'r') as file:
            C1, C2 = map(int, file.readlines())

        mensaje_desencriptado = desencriptar(C1, C2, p, a)

        with open(archivo_salida, 'w') as file:
            file.write(str(mensaje_desencriptado))

        etiqueta_resultado.config(text=f"File '{archivo_entrada}' decrypted and saved in '{archivo_salida}'")

    button_encriptar.config(command=click_encriptar_texto)
    button_desencriptar.config(command=click_desencriptar_texto)

    ventana.mainloop()

def open_audio():
    ventana = tk.Toplevel()
    ventana.title("Audio Encryption")
    ventana.geometry("400x300")

    # Audio encryption interface

    heading_label = tk.Label(ventana, text="Audio Encryption with ElGamal", font=("Arial", 16))
    heading_label.pack(pady=10)

    button_encriptar = tk.Button(ventana, text="Encrypt Audio")
    button_encriptar.pack(pady=5)

    button_desencriptar = tk.Button(ventana, text="Decrypt Audio")
    button_desencriptar.pack(pady=5)

    def volver_atras():
        ventana.destroy()

    button_atras = tk.Button(ventana, text="Go Back", command=volver_atras)
    button_atras.pack(pady=5)

    button_desencriptar.configure(bg="#2aa3f4")
    button_encriptar.configure(bg="#2aa3f4")
    button_atras.configure(bg="#2aa3f4")
    button_encriptar.configure(fg="#FFFFFF")
    button_desencriptar.configure(fg="#FFFFFF")
    button_atras.configure(fg="#FFFFFF")

    etiqueta_resultado = tk.Label(ventana, text="")
    etiqueta_resultado.pack(pady=10)

    def encriptar_audio(audio_file, p, g, A):
        # Read binary audio data from the file
        with open(audio_file, 'rb') as file:
            audio_data = file.read()

        encrypted_audio_data = bytes((byte * pow(A, k, p) % p for byte in audio_data))

        C1 = pow(g, k, p)

        return (C1, encrypted_audio_data)

    def desencriptar_audio(C1, C2, p, a, output_file):
        s = pow(C1, a, p)
        decrypted_audio_data = bytes((byte * mod_inverse(s, p) % p for byte in C2))

        with open(output_file, 'wb') as file:
            file.write(decrypted_audio_data)

    def click_encriptar_audio():
        archivo_entrada = filedialog.askopenfilename(title="Select Input Audio File")
        archivo_salida = filedialog.asksaveasfilename(title="Select Output Audio File")

        p, g, A, a = generar_claves()

        C1, C2 = encriptar_audio(archivo_entrada, p, g, A)

        with open(archivo_salida, 'wb') as file:
            file.write(C1)
            file.write(C2)

        etiqueta_resultado.config(text=f"Audio encrypted and saved in '{archivo_salida}'")

    def click_desencriptar_audio():
        archivo_entrada = filedialog.askopenfilename(title="Select Encrypted Audio")
        archivo_salida = filedialog.asksaveasfilename(title="Select Output Audio File")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'rb') as file:
            C1 = file.read(32)  # Assuming C1 is 32 bytes
            C2 = file.read()

        desencriptar_audio(C1, C2, p, a, archivo_salida)

        etiqueta_resultado.config(text=f"Audio decrypted and saved in '{archivo_salida}'")

    button_encriptar.config(command=click_encriptar_audio)
    button_desencriptar.config(command=click_desencriptar_audio)

    ventana.mainloop()

def open_imagen():
    ventana = tk.Toplevel()
    ventana.title("Image Encryption")
    ventana.geometry("400x300")

    # Image encryption interface

    heading_label = tk.Label(ventana, text="Image Encryption with ElGamal", font=("Arial", 16))
    heading_label.pack(pady=10)

    button_encriptar = tk.Button(ventana, text="Encrypt Image")
    button_encriptar.pack(pady=5)

    button_desencriptar = tk.Button(ventana, text="Decrypt Image")
    button_desencriptar.pack(pady=5)

    def volver_atras():
        ventana.destroy()

    button_atras = tk.Button(ventana, text="Go Back", command=volver_atras)
    button_atras.pack(pady=5)

    button_desencriptar.configure(bg="#2aa3f4")
    button_encriptar.configure(bg="#2aa3f4")
    button_atras.configure(bg="#2aa3f4")
    button_encriptar.configure(fg="#FFFFFF")
    button_desencriptar.configure(fg="#FFFFFF")
    button_atras.configure(fg="#FFFFFF")

    etiqueta_resultado = tk.Label(ventana, text="")
    etiqueta_resultado.pack(pady=10)

    def encriptar_imagen(image_file, p, g, A, k):
        # Open and load the image
        img = Image.open(image_file)
        img_data = list(img.getdata())

        # Encrypt the image data
        encrypted_data = [(r * pow(A, k, p) % p, g, b) for r, g, b in img_data]

        return encrypted_data

    def desencriptar_imagen(encrypted_data, p, a, output_file):
        decrypted_data = [(r * mod_inverse(encrypted_data[i][1], p) % p, a, b) for i, (r, _, b) in
                          enumerate(encrypted_data)]

        # Get image dimensions from the output file
        with Image.open(output_file) as img:
            img_width, img_height = img.size

        img = Image.new('RGB', (img_width, img_height))
        img.putdata(decrypted_data)
        img.save(output_file)

    def click_encriptar_imagen():
        archivo_entrada = filedialog.askopenfilename(title="Select Input Image")
        archivo_salida = filedialog.asksaveasfilename(title="Select Output Image")

        p, g, A, a = generar_claves()
        k = 5  # Your random value for encryption

        encrypted_data = encriptar_imagen(archivo_entrada, p, g, A, k)

        # Determine the original image format
        with Image.open(archivo_entrada) as img:
            original_format = img.format

        # Save the encrypted image with the original format and extension
        img = Image.new('RGB', (1, 1))
        img.putdata([(0, 0, 0)])  # Create a dummy image with one pixel
        img.save(archivo_salida, format=original_format)

        # Save the encrypted data as a binary file
        with open(archivo_salida, 'ab') as file:
            pickle.dump(encrypted_data, file)

        etiqueta_resultado.config(text=f"Image encrypted and saved in '{archivo_salida}'")

    def click_desencriptar_imagen():
        archivo_entrada = filedialog.askopenfilename(title="Select Encrypted Image")
        archivo_salida = filedialog.asksaveasfilename(title="Select Output Image")

        # Determine the original image format
        with Image.open(archivo_entrada) as img:
            original_format = img.format

        # Extract the encrypted data from the image file
        with open(archivo_entrada, 'rb') as file:
            # Determine the size of the image data
            img_size = file.tell()

            # Load the encrypted data from the remainder of the file
            file.seek(img_size)
            encrypted_data = pickle.load(file)

        p, g, A, a = generar_claves()

        # Decrypt the image using the extracted encrypted data
        desencriptar_imagen(encrypted_data, p, a, archivo_salida)

        etiqueta_resultado.config(text=f"Image decrypted and saved in '{archivo_salida}'")

    button_encriptar.config(command=click_encriptar_imagen)
    button_desencriptar.config(command=click_desencriptar_imagen)

    ventana.mainloop()

def generar_claves():
    p = 23
    g = 2
    A = pow(g, a, p)
    return (p, g, A, a)

if __name__ == "__main__":
    open_menu()
