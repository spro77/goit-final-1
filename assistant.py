from entities import *
from handlers import *


def main():
    try:
        book = load_addressbook_data()
        notebook = load_notebook_data()

        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_addressbook_data(book)
                save_notebook_data(notebook)
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                birthdays(book)
            elif command == "all":
                print(book)
            elif command == "add-note":
                print(add_note(args, notebook))
            elif command == 'show-notes':
                print(notebook)
            else:
                print("Invalid command.")
    except:
        save_addressbook_data(book)
        save_notebook_data(notebook)
        print("Addres book and Notebook saved")


if __name__ == '__main__':
    main()
