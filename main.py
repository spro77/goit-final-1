#!/usr/bin/env python3
import handlers

def main():
    current_book = handlers.load_addressbook_data()
    current_notebook = handlers.load_notebook_data()

    def print_menu(_=None):
        menu_text = "\nContact Manager:"
        for key, (desc, _) in commands.items():
            menu_text += f"\n  {key:>2}. {desc}"
        menu_text += "\n"
        return menu_text

    commands = {
        "1": ("add contact", handlers.add_contact),
        "2": ("list contacts", handlers.show_all),
        "3": ("search contact", handlers.search_contact),
        "4": ("edit contact", handlers.change_contact),
        "5": ("delete contact", handlers.delete_contact),
        "6": ("upcoming birthdays", handlers.birthdays),
        "7": ("add note", handlers.add_note),
        "8": ("list notes", handlers.list_notes),
        "9": ("search note", handlers.search_notes),
        "10": ("edit note", handlers.edit_note),
        "11": ("delete note", handlers.delete_note),
        "0": ("exit", None),
        "?": ("help", print_menu),
    }

    print(print_menu())

    while True:
        choice = input("Main Menu: ").strip()
        if choice not in commands:
            print("Invalid selection. Try again.")
            continue

        desc, handler = commands[choice]
        if choice == "0":
            handlers.save_addressbook_data(current_book)
            print("Data saved. Goodbye!")
            break

        target = current_book if ('contact' in desc or 'birthday' in desc) else current_notebook

        result = handler(target)
        if result:
            print(result)

if __name__ == "__main__":
    main()