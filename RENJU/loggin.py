import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
import os, random, math
import game

def show_game_window():
    root.destroy()
    game.play_init()

# Обработка события входа
def login():
    login = login_entry.get()
    password = password_entry.get()
    if not login or not password:
        mb.showerror("Авторизация", "Пожалуйста, заполните все поля")
        return
    with open("DataFile.json", "r") as file:
        lines = file.readlines()
        user_found = False
        incorrect_password = False
        for line in lines:
            stored_username, stored_password = line.strip().split('•')
            if login == stored_username:
                if password == stored_password:
                    user_found = True
                    mb.showinfo("Авторизация", f"Добро пожаловать, {login}!")
                    RSA()
                    show_game_window()
                    break
                else:
                    incorrect_password = True
                    break
        if not user_found or incorrect_password:
            mb.showerror("Вход", "Неверный логин или пароль")
        return

# Обработка события регистрации нового пользователя
def add_user():
    login = login_entry.get()
    password = password_entry.get()
    if not login or not password:
        mb.showwarning('Ошибка', 'Пожалуйста, заполните все поля')
        return
    else:
        if len(login) < 3 or len(password) < 4 or len(login) > 15 or len(password) > 15:
            mb.showwarning('Ошибка регистрации',
                           'Логин должен быть более 3 символов , макс. длина 15 символов!\n'
                           'Пароль должен быть более 4 символов, макс. длина 15 символов!')
            return
        elif not any(char.isdigit() for char in login):
            mb.showwarning('Ошибка регистрации', 'Логин должен содержать хотя бы одну цифру.')
            return
        elif not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            mb.showwarning('Ошибка регистрации',
                           'Пароль должен содержать хотя бы одну цифру и одну букву.')
            return
    with open("DataFile.json", "r") as file:
        lines = file.readlines()
        for line in lines:
            stored_data = line.strip().split('•')
            if len(stored_data) == 2:
                stored_login, _ = stored_data
                if login == stored_login:
                    mb.showwarning("Регистрация", "Пользователь с таким именем уже существует")
                    return
    with open('DataFile.json', 'a') as file:
        file.write(f'{login}•{password}\n')
        mb.showinfo('Успешная регистрация', 'Вы успешно зарегистрировались!')
    RSA()
    show_game_window()

# RSA шифрование данных
def RSA():
    # Чтение данных из файла
    with open('DataFile.json', 'r') as file:
        data = file.read()

    # Генерация ключей
    public_key, private_key = generate_keys()
    # Шифрование данных
    encrypted_data = encrypt(data, public_key)

    # Запись зашифрованных данных в файл
    with open('EncryptedDataFile.json', 'w') as file:
        file.write(' '.join(map(str, encrypted_data)))

# Функция для проверки простоты числа
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Функция для генерации простых чисел p и q
def generate_primes():
    p = 0
    q = 0
    while not is_prime(p):
        p = random.randint(100, 1000)
    while not is_prime(q) or q == p:
        q = random.randint(100, 1000)
    return p, q

# Функция для вычисления функции Эйлера
def calculate_phi(p, q):
    return (p - 1) * (q - 1)

# Функция для вычисления обратного числа по модулю
def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x

# Функция для генерации открытого и закрытого ключей
def generate_keys():
    p, q = generate_primes()
    n = p * q
    phi = calculate_phi(p, q)
    e = random.randint(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randint(1, phi)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

# Функция для шифрования данных
def encrypt(data, public_key):
    e, n = public_key
    encrypted_data = [pow(ord(char), e, n) for char in data]
    return encrypted_data

# Функция для дешифрования данных
def decrypt(encrypted_data, private_key):
    d, n = private_key
    decrypted_data = [chr(pow(char, d, n)) for char in encrypted_data]
    return ''.join(decrypted_data)

# Проверяем наличие файла данных, если нет - создаем
if not os.path.exists('DataFile.json'):
    with open('DataFile.json', 'w'):
        pass

# виджеты интерфейса для окна входа
root = Tk()
root.geometry(f'{660}x{390}+{460}+{225}')  # Размеры и положение окна
root.resizable(False, False)  # Запрещаем изменение размеров окна
root.title("Вход/Регистрация")  # Заголовок окна
root['bg'] = 'black'

main_label = tk.Label(text='Вход/Регистрация', bg='black', fg="white", font='Bahnschrift 24',pady=20)
main_label.pack()

login_label = tk.Label(text="Логин:", bg='black', fg="white", font='Bahnschrift 24', pady=0)
login_label.pack()
login_entry = tk.Entry(root, bg='black', fg="white", font='Bahnschrift 16')
login_entry.pack()

password_label = tk.Label(text="Пароль:", bg='black', fg="white", font='Bahnschrift 24', pady=0)
password_label.pack()
password_entry = tk.Entry(root, bg='black', fg="white", font='Bahnschrift 16', show="*")
password_entry.pack()

sign_btn = tk.Button(text="Войти", command=login, bg='black', fg="white", font='Bahnschrift 16')
sign_btn.pack(pady=15)

login_btn = tk.Button(text="Зарегистрироваться", command=add_user, bg='black', fg="white", font='Bahnschrift 16')
login_btn.pack()

root.mainloop()