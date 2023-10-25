from sympy import mod_inverse
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os

# Static key values
a = 3  # Your private key
k = 5  # Your random value for encryption

def open_menu():
    ventana = tk.Tk()
    ventana.title("Encriptación ElGamal")
    ventana.geometry("500x500")

    # Load and display the background image
    background_image = PhotoImage(file="background.png")
    background_label = tk.Label(ventana, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Main menu interface
    heading_label = tk.Label(ventana, text="Encriptación ElGamal", font=("Arial", 20))
    heading_label.pack(pady=10)
    heading_label.configure(bg="#1d2528", fg="#FFFFFF")

    image = PhotoImage(file="lock.png")
    image_label = tk.Label(ventana, image=image, bg="#1d2528")
    image_label.pack()

    def archivo():
        open_archivo()

    def pdf():
        open_pdf()

    def imagen():
        open_imagen()


    # Load icons and resize them
    icon_file1 = Image.open("icon1.png")
    icon_file1 = icon_file1.resize((32, 32))  # Adjust the size as needed
    icon_file1 = ImageTk.PhotoImage(icon_file1)

    icon_file2 = Image.open("icon2.png")
    icon_file2 = icon_file2.resize((32, 32))  # Adjust the size as needed
    icon_file2 = ImageTk.PhotoImage(icon_file2)

    icon_file3 = Image.open("icon3.png")
    icon_file3 = icon_file3.resize((32, 32))  # Adjust the size as needed
    icon_file3 = ImageTk.PhotoImage(icon_file3)

    button1 = tk.Button(ventana, text=" Encriptar Texto", command=archivo, compound="left", image=icon_file1, padx=5, pady=5)
    button2 = tk.Button(ventana, text=" Encriptar PDF", command=pdf, compound="left", image=icon_file2, padx=5, pady=5)
    button3 = tk.Button(ventana, text=" Encriptar Imagen", command=imagen, compound="left", image=icon_file3, padx=5, pady=5)

    # Configure the button colors
    button1.configure(bg="#2aa3f4", fg="#FFFFFF")
    button2.configure(bg="#2aa3f4", fg="#FFFFFF")
    button3.configure(bg="#2aa3f4", fg="#FFFFFF")

    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

    label_result = tk.Label(ventana, text="", font=("Arial", 16))
    label_result.pack(pady=10)

    ventana.mainloop()


#--------------ENCRIPTACION Y DECRIPTACION DE TEXTO------------------
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
        archivo_entrada = filedialog.askopenfilename(title="Seleccionar Archivo de entrada")
        archivo_salida = filedialog.asksaveasfilename(title="Seleccionar Archivo de salida")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'r') as file:
            texto_plano = int(file.read())

        C1, C2 = encriptar(texto_plano, p, g, A)

        with open(archivo_salida, 'w') as file:
            file.write(f"{C1}\n{C2}")

        etiqueta_resultado.config(text=f"Archivo '{archivo_entrada}' encriptado y guardado en '{archivo_salida}'")

    def click_desencriptar_texto():
        archivo_entrada = filedialog.askopenfilename(title="Seleccione el archivo encriptado")
        archivo_salida = filedialog.asksaveasfilename(title="Seleccione el archivo de salida")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'r') as file:
            C1, C2 = map(int, file.readlines())

        mensaje_desencriptado = desencriptar(C1, C2, p, a)

        with open(archivo_salida, 'w') as file:
            file.write(str(mensaje_desencriptado))

        etiqueta_resultado.config(text=f"Archivo '{archivo_entrada}' decriptado y guardado en '{archivo_salida}'")

    button_encriptar.config(command=click_encriptar_texto)
    button_desencriptar.config(command=click_desencriptar_texto)

    ventana.mainloop()



#--------------ENCRIPTACION Y DECRIPTACION DE PDF-------------------
def open_pdf():
    ventana = tk.Toplevel()
    ventana.title("Encriptación de PDF")
    ventana.geometry("400x300")

    def generate_or_use_fixed_key_pair():
        # Check if key files exist, if not, generate them
        if not os.path.exists('private.pem') or not os.path.exists('public.pem'):
            key = RSA.generate(2048)
            with open('private.pem', 'wb') as priv_file, open('public.pem', 'wb') as pub_file:
                priv_file.write(key.export_key('PEM'))
                pub_file.write(key.publickey().export_key('PEM'))

        with open('private.pem', 'rb') as priv_file, open('public.pem', 'rb') as pub_file:
            rsa_private_key = RSA.import_key(priv_file.read())
            rsa_public_key = RSA.import_key(pub_file.read())

        return rsa_private_key, rsa_public_key

    def encrypt_pdf(pdf_file, rsa_public_key):
        symmetric_key = os.urandom(16)  # Generate a 128-bit random key
        cipher = AES.new(symmetric_key, AES.MODE_EAX)

        with open(pdf_file, 'rb') as file:
            plaintext = file.read()

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        rsa_cipher = PKCS1_OAEP.new(rsa_public_key)
        encrypted_key = rsa_cipher.encrypt(symmetric_key)

        with open(pdf_file + ".enc", 'wb') as file:
            file.write(encrypted_key)
            file.write(cipher.nonce)
            file.write(ciphertext)
            file.write(tag)

    def decrypt_pdf(encrypted_pdf_file, rsa_private_key):
        with open(encrypted_pdf_file, 'rb') as file:
            encrypted_key = file.read(256)
            nonce = file.read(16)
            ciphertext = file.read()

        rsa_cipher = PKCS1_OAEP.new(rsa_private_key)
        symmetric_key = rsa_cipher.decrypt(encrypted_key)

        cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)

        decrypted_file = os.path.splitext(encrypted_pdf_file)[0] + "_decrypted.pdf"
        with open(decrypted_file, 'wb') as file:
            file.write(plaintext)

    def upload_pdf():
        file_path = filedialog.askopenfilename()
        if file_path:
            encrypt_pdf(file_path, rsa_public_key)
            print("PDF Encriptado con éxito!")

    def decrypt_uploaded_pdf():
        file_path = filedialog.askopenfilename()
        if file_path:
            decrypt_pdf(file_path, rsa_private_key)
            print("PDF Decriptado con éxito!")

    def volver_atras():
        ventana.destroy()

    # Generate or use fixed RSA key pair
    rsa_private_key, rsa_public_key = generate_or_use_fixed_key_pair()

    # Add a heading label
    heading_label = tk.Label(ventana, text="Encriptación y Desencriptación de PDF", padx=5, pady=10)
    heading_label.pack()

    # Create buttons with padding
    button_encriptar = tk.Button(ventana, text="Subir y Encriptar PDF", command=upload_pdf, padx=5, pady=5)
    button_desencriptar = tk.Button(ventana, text="Subir y Desencriptar PDF", command=decrypt_uploaded_pdf, padx=5, pady=5)
    button_atras = tk.Button(ventana, text="Volver Atrás", command=volver_atras)

    button_desencriptar.configure(bg="#2aa3f4")
    button_encriptar.configure(bg="#2aa3f4")
    button_atras.configure(bg="#2aa3f4")
    button_encriptar.configure(fg="#FFFFFF")
    button_desencriptar.configure(fg="#FFFFFF")
    button_atras.configure(fg="#FFFFFF")

    button_encriptar.pack(pady=5)
    button_desencriptar.pack(pady=5)
    button_atras.pack(pady=5)


    ventana.mainloop()


#--------------ENCRIPTACION Y DECRIPTACION DE IMAGEN-------------------
def open_imagen():
    ventana = tk.Toplevel()
    ventana.title("Encriptación de Imagen con ElGamal")
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
            info_label.config(text="Imagen encriptada y guardada como encrypted_image.png")

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
            info_label.config(text="Imagen decriptada y guardada como decrypted_image.png")

        except Exception as e:
            info_label.config(text="Error: " + str(e))

    heading_label = tk.Label(ventana, text="Encriptación de imagen con ElGamal", font=("Arial", 16))
    heading_label.pack(pady=10)

    button_encriptar = tk.Button(ventana, text="Encriptar imagen", command= encrypt_image_static)
    button_encriptar.pack(pady=5)

    button_desencriptar = tk.Button(ventana, text="Decriptar imagen", command= decrypt_image_static)
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
