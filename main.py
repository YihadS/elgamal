import random
from sympy import mod_inverse
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage

# Static key values
a = 123456  # Your private key
k = 789012  # Your random value for encryption

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

    button1 = tk.Button(ventana, text="Encriptar Texto", command=archivo)
    button2 = tk.Button(ventana, text="Encriptar Audio")
    button3 = tk.Button(ventana, text="Encriptar Imagen")

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
    ventana.title("Encriptación de Archivos")
    ventana.geometry("400x300")

    # File encryption interface

    heading_label = tk.Label(ventana, text="Encriptación de Archivos con ElGamal", font=("Arial", 16))
    heading_label.pack(pady=10)

    button_encriptar = tk.Button(ventana, text="Encriptar Archivo")
    button_encriptar.pack(pady=5)

    button_desencriptar = tk.Button(ventana, text="Desencriptar Archivo")
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

    def click_encriptar():
        archivo_entrada = filedialog.askopenfilename(title="Seleccionar Archivo de Entrada")
        archivo_salida = filedialog.asksaveasfilename(title="Seleccionar Archivo de Salida")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'r') as file:
            texto_plano = int(file.read())

        C1, C2 = encriptar(texto_plano, p, g, A)

        with open(archivo_salida, 'w') as file:
            file.write(f"{C1}\n{C2}")

        etiqueta_resultado.config(text=f"Archivo '{archivo_entrada}' encriptado y guardado en '{archivo_salida}'")

    def click_desencriptar():
        archivo_entrada = filedialog.askopenfilename(title="Seleccionar Archivo Encriptado")
        archivo_salida = filedialog.asksaveasfilename(title="Seleccionar Archivo de Salida")

        p, g, A, a = generar_claves()

        with open(archivo_entrada, 'r') as file:
            C1, C2 = map(int, file.readlines())

        mensaje_desencriptado = desencriptar(C1, C2, p, a)

        with open(archivo_salida, 'w') as file:
            file.write(str(mensaje_desencriptado))

        etiqueta_resultado.config(text=f"Archivo '{archivo_entrada}' desencriptado y guardado en '{archivo_salida}'")

    button_encriptar.config(command=click_encriptar)
    button_desencriptar.config(command=click_desencriptar)

    ventana.mainloop()

def generar_claves():
    p = 239847179
    g = 2
    A = pow(g, a, p)
    return (p, g, A, a)

if __name__ == "__main__":
    open_menu()
