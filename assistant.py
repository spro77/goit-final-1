from entities import *
from handlers import *

def main():
    try:
        book = load_data()
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book)
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
                print(add_birthday(args,book))
            elif command == "show-birthday":
                print(show_birthday(args,book))
            elif command == "birthdays":
                birthdays(book)
            elif command == "all":
                print(book)
            else:
                print("Invalid command.")
    except:
        save_data(book)
        print("Addres book saved")
        
if __name__ == '__main__':
    main()