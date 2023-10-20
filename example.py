import random
from sympy import mod_inverse
import tkinter as tk
from tkinter import messagebox

# Key Generation
def generate_keys():
    p = 239847179
    g = 2
    a = random.randint(2, p - 2)
    A = pow(g, a, p)
    return (p, g, A, a)

# Encryption
def encrypt(plain_text, p, g, A):
    k = random.randint(2, p - 2)
    C1 = pow(g, k, p)
    C2 = (plain_text * pow(A, k, p)) % p
    return (C1, C2)

# Decryption
def decrypt(C1, C2, p, a):
    s = pow(C1, a, p)
    plain_text = (C2 * mod_inverse(s, p)) % p
    return plain_text

def encrypt_and_decrypt():
    try:
        message = int(entry.get())
    except ValueError:
        messagebox.showerror("Error", "Solo se aceptan enteros.")
        return

    p, g, A, a = generate_keys()

    public_key_label.config(text=f"Public Key (p, g, A): ({p}, {g}, {A})")
    private_key_label.config(text=f"Private Key (a): {a}")

    C1, C2 = encrypt(message, p, g, A)
    encrypted_message_label.config(text=f"Mensaje Encriptado (C1, C2): ({C1}, {C2})")

    decrypted_message = decrypt(C1, C2, p, a)
    decrypted_message_label.config(text=f"Mensaje Desencriptado: {decrypted_message}")

# Create the Tkinter window with a size of 500x500
window = tk.Tk()
window.title("Encriptación ElGamal")
window.geometry("500x300")  # Set the window size to 500x500

# Create a heading label
heading_label = tk.Label(window, text="ElGamal", font=("Arial", 18))
heading_label.pack(pady=10)

# Create and place input elements on the window
entry_label = tk.Label(window, text="Ingresa un entero:")
entry_label.pack(pady=5)
entry = tk.Entry(window)
entry.pack(pady=5)

encrypt_button = tk.Button(window, text="Encriptar y Desencriptar", command=encrypt_and_decrypt)
encrypt_button.pack(pady=5)

# Create and place labels for displaying results
public_key_label = tk.Label(window, text="")
public_key_label.pack(pady=5)

private_key_label = tk.Label(window, text="")
private_key_label.pack(pady=5)

encrypted_message_label = tk.Label(window, text="")
encrypted_message_label.pack(pady=5)

decrypted_message_label = tk.Label(window, text="")
decrypted_message_label.pack(pady=5)

window.mainloop()
