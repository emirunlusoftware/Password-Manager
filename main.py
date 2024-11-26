from cryptography.fernet import Fernet
from itertools import zip_longest
import os
import random
import readchar
import string
import sys
import time





### FUNCTIONS ###


def clean_screen():
    os.system("cls") if os.name == "nt" else os.system("clear")



def print_noline(*args, **kwargs):
    print(*args, end = "", flush = True, **kwargs)



def format_numbers():
    numbers = list(string.digits)
    password_length = 0
    while True:
        password_length_digit = readchar.readchar()

        if password_length_digit == "\b" and password_length != 0:
            print_noline("\b \b")
            password_length //= 10
        elif password_length_digit in numbers:
            password_length_digit = int(password_length_digit)
            password_length = password_length * 10 + password_length_digit
            print_noline(password_length_digit)
        elif password_length_digit == "\r":
            if password_length > 999:
                print("\n\nERROR: The length of password cannot be more than 999")
                password_length = 0
                print_noline("Şifrenin uzunluğunu girin: ")
            else:
                return password_length if password_length > 0 else 12



def create_random_password(password_length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(password_length))



def enter_your_password():
    show_password = False
    password_array = []

    while True:
        password_char = readchar.readchar()

        if password_char == "\r":
            if len(password_array) == 0:
                continue
            return ''.join(password_array)

        elif password_char == " ":
            show_password = not show_password

            for i in range(len(password_array)):
                print_noline("\b \b")

            for i in range(len(password_array)):
                if show_password:
                    print_noline(password_array[i])
                else:
                    print_noline("*")
            continue

        elif password_char == "\b":
            if len(password_array) == 0:
                continue
            password_array.pop()
            print_noline("\b \b")
            continue

        else:
            password_array.append(password_char)
            if show_password:
                print_noline(password_char)
            else:
                print_noline("*")



def encrypt(password):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return key, encrypted_password



def allow_encryption(password, pressed_key = None):
    pressed_key = readchar.readchar().upper()
    while pressed_key.upper() not in {"Y", "N"}:
        pressed_key = readchar.readchar().upper()
    print(pressed_key)

    if pressed_key.upper() == "Y":
        key, encrypted_password = encrypt(password)
        return key, encrypted_password
    else:
        return "-", password



def save_password(password_name, password, key):
    with open("password_examples","ab") as file:
        file.write(f"{password_name}\nPASSWORD: {password}\nFERNET KEY: {key}\n".encode("utf-8"))

    print_noline("\nYour password has been saved")
    for _ in range (1,3):
        print_noline(".")
        time.sleep(1)
    return True





def main():
    while True:
        go_back_main_menu = False
        clean_screen()
        print("PASSWORD MANAGER\n" +
              "<Create, encrypt and save your passwords>\n\n"+
              "(1)Create passwords and save them\n"+
              "(2)List saved passwords\n\n" +
              "(E)Exit")

        pressed_key = readchar.readchar()

        if pressed_key == "1":
            clean_screen()

            print("...CREATE PASSWORDS...\n\n" +
                  "(1)Random Password Generator\n" +
                  "(2)Create manually\n\n"+
                  "(M)Main menu")

            while True:
                pressed_key = readchar.readchar()

                if pressed_key == "1":
                    clean_screen()

                    print("...RANDOM PASSWORD CREATOR...\n\n")
                    print_noline("Enter the length of your password: ")
                    password = create_random_password(format_numbers())
                    print_noline("\nEncrypt? (Yes: Y/No: N): ")
                    key, password = allow_encryption(password)

                    print(f"\nYour created password: {password}\n\n" +
                          "(S)Save this password\n" +
                          "(M)Main menu")

                    while True:
                        pressed_key = readchar.readchar()

                        if pressed_key.lower() == "s":
                            password_name = input("\nEnter a name for your password: ")
                            go_back_main_menu = save_password(password_name, password, key)
                            break
                        elif pressed_key.lower() == "m":
                            go_back_main_menu = True
                            break

                    if go_back_main_menu == True:
                        break

                elif pressed_key == "2":
                    clean_screen()
                    print("...CREATE MANUALLY...\n" +
                          "(Note: Press Spacebar to make your password visible/non-visible)\n")
                    print_noline("Enter your new password:   ")
                    password = enter_your_password()
                    print_noline("\nConfirm your new password: ")
                    password2 = enter_your_password()

                    while password != password2:
                        print_noline("\nERROR: Passwords don't match." +
                                     "\nConfirm your new password: ")
                        password2 = enter_your_password()

                    print_noline("\nEncrypt? (Yes: Y/No: N): ")
                    key, password = allow_encryption(password)

                    password_name = input("\nEnter a name for your password: ")
                    go_back_main_menu = save_password(password_name, password, key)

                elif pressed_key.lower() == "m":
                    go_back_main_menu = True

                if go_back_main_menu == True:
                    break
                

        elif pressed_key == "2":
            while True:
                clean_screen()
                print_noline("Password: ")
                access_passwords = enter_your_password()
                if access_passwords == "0000":
                    break

            clean_screen()
            try:
                with open("password_examples", "rb") as file:
                    content = file.read().decode("utf-8")
                    file.seek(0)
                    lines = content.splitlines()

                    print("...Saved passwords... |name first: password second|\n")
                    for i in range(0,len(lines),3):
                        group = lines[i:i+3]
                        print("\n".join(group))
                        print()

                    print(".....................\n")
                    print("(nothing here)" + "\n\n(M)Main Menu"
                          if not content.strip() else
                          "(D)Delete password" + "\n(E)Export passwords as .txt file" + "\n(M)Main Menu")
                    file_found = True
            except FileNotFoundError:
                file_found = False
                print("No saved passwords file detected, created a new one.")
                with open("password_examples", "wb") as file:
                    pass
                print("All you need to do is just start saving your passwords and as you do, they'll be shown here." +
                      "\n\n(M)Main Menu")

            while (pressed_key := readchar.readchar().lower()) != "m":
                if file_found and content:
                    if pressed_key.lower() == "d":
                        print_noline("\nWrite the FULL NAME of the password you want to delete: ")
                        password_name = input().strip()
                        with open("password_examples", "rb") as file:
                            content = file.read().decode("utf-8")
                            lines = content.splitlines()

                        new_lines = []
                        delete_mode = deleted = False
                        for line in lines:
                            if line.strip() == password_name:
                                delete_mode = deleted = True
                                continue

                            if delete_mode:
                                if line.strip().startswith("PASSWORD:") or line.strip().startswith("FERNET KEY:"):
                                    continue
                                else:
                                    delete_mode = False

                            new_lines.append(line)

                        with open("password_examples", "wb") as file:
                            file.write("\n".join(new_lines).encode("utf-8"))

                        if deleted:
                            print_noline("\nThe password has been deleted")
                        else:
                            print_noline("\nPassword not found.\n\n(D)Try Again\n(M)Main Menu\n")
                            continue
                        for _ in range (1,3):
                            print_noline(".")
                            time.sleep(1)

                        break

                    elif pressed_key.lower() == "e":
                        with open("password_examples.txt", "w") as file:
                            with open("password_examples", "rb") as binary_file:
                                content = binary_file.read().decode("utf-8")
                                file.write(content)
                            print_noline("Done")

                        for _ in range (1,3):
                            print_noline(".")
                            time.sleep(1)
                        break



        elif pressed_key.lower() == "e":
            sys.exit()





# END OF FUNCTIONS
# RUN main() FUNCTION
if __name__ == "__main__":
    main()
