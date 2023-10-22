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
        C1_int = int.from_bytes(C1, byteorder='big')  # Convert C1 from bytes to an integer
        s = pow(C1_int, a, p)

        decrypted_audio_data = bytes((byte * mod_inverse(s, p) % p for byte in C2))

        with open(output_file, 'wb') as file:
            file.write(decrypted_audio_data)

        etiqueta_resultado.config(text=f"Audio decrypted and saved in '{output_file}'")

    def click_encriptar_audio():
        archivo_entrada = filedialog.askopenfilename(title="Select Input Audio File")
        archivo_salida = filedialog.asksaveasfilename(title="Select Output Audio File")

        p, g, A, a = generar_claves()

        C1, C2 = encriptar_audio(archivo_entrada, p, g, A)

        with open(archivo_salida, 'wb') as file:
            file.write(C1.to_bytes((C1.bit_length() + 7) // 8, byteorder='big'))  # Convert C1 to bytes
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
    # Function to handle encryption of an image with static keys
    def encrypt_image_static():
        image_file_path = filedialog.askopenfilename()
        if not image_file_path:
            return

        try:
            img = Image.open(image_file_path)
            img = img.convert("RGB")
            width, height = img.size

            encrypted_pixels = []
            for i in range(width):
                for j in range(height):
                    r, g, b = img.getpixel((i, j))
                    r_c1, r_c2 = elgamal_encrypt(r)
                    g_c1, g_c2 = elgamal_encrypt(g)
                    b_c1, b_c2 = elgamal_encrypt(b)
                    encrypted_pixels.append((r_c1, r_c2, g_c1, g_c2, b_c1, b_c2))

            encrypted_image = Image.new("RGB", (width, height))
            pixel_index = 0
            for i in range(width):
                for j in range(height):
                    r_c1, r_c2, g_c1, g_c2, b_c1, b_c2 = encrypted_pixels[pixel_index]
                    r_plain = elgamal_decrypt(r_c1, r_c2)
                    g_plain = elgamal_decrypt(g_c1, g_c2)
                    b_plain = elgamal_decrypt(b_c1, b_c2)
                    encrypted_image.putpixel((i, j), (r_plain, g_plain, b_plain))
                    pixel_index += 1

            encrypted_image.save("encrypted_image.png")
            info_label.config(text="Image encrypted and saved as encrypted_image.png")

        except Exception as e:
            info_label.config(text="Error: " + str(e))

    # Function to handle decryption of an image with static keys
    def decrypt_image_static():
        image_file_path = filedialog.askopenfilename()
        if not image_file_path:
            return

        try:
            img = Image.open(image_file_path)
            img = img.convert("RGB")
            width, height = img.size

            decrypted_pixels = []
            for i in range(width):
                for j in range(height):
                    r, g, b = img.getpixel((i, j))
                    r_c1, r_c2 = elgamal_encrypt(r)
                    g_c1, g_c2 = elgamal_encrypt(g)
                    b_c1, b_c2 = elgamal_encrypt(b)
                    decrypted_pixels.append((r_c1, r_c2, g_c1, g_c2, b_c1, b_c2))

            decrypted_image = Image.new("RGB", (width, height))
            pixel_index = 0
            for i in range(width):
                for j in range(height):
                    r_c1, r_c2, g_c1, g_c2, b_c1, b_c2 = decrypted_pixels[pixel_index]
                    r_plain = elgamal_decrypt(r_c1, r_c2)
                    g_plain = elgamal_decrypt(g_c1, g_c2)
                    b_plain = elgamal_decrypt(b_c1, b_c2)
                    decrypted_image.putpixel((i, j), (r_plain, g_plain, b_plain))
                    pixel_index += 1

            decrypted_image.save("decrypted_image.png")
            info_label.config(text="Image decrypted and saved as decrypted_image.png")

        except Exception as e:
            info_label.config(text="Error: " + str(e))

    heading_label = tk.Label(ventana, text="Image Encryption with ElGamal", font=("Arial", 16))
    heading_label.pack(pady=10)

    button_encriptar = tk.Button(ventana, text="Encrypt Image", command= encrypt_image_static)
    button_encriptar.pack(pady=5)

    button_desencriptar = tk.Button(ventana, text="Decrypt Image", command= decrypt_image_static)
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

    # Create info label
    info_label = tk.Label(ventana, text="")
    info_label.pack()

    gI = 2
    pI = 23
    xI = 6  # Private key
    public_keyI = 8  # Public key

    # ElGamal encryption and decryption functions
    def elgamal_encrypt(plain_text):
        kI = 7  # Static value for k (should be random in practice)
        c1 = pow(gI, kI, pI)
        c2 = (plain_text * pow(public_keyI, kI, pI)) % pI
        return c1, c2

    def elgamal_decrypt(c1, c2):
        s = pow(c1, xI, pI)
        plaintext = (c2 * pow(s, pI - 2, pI)) % pI
        return plaintext

    ventana.mainloop()

def generar_claves():
    p = 23
    g = 2
    A = pow(g, a, p)
    return (p, g, A, a)

if __name__ == "__main__":
    open_menu()


