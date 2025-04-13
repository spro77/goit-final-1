#!/usr/bin/env python3
from organizer import handlers


def main():
    organizer = handlers.load_data()

    def print_menu(_=None):
        menu_text = "\nMainMenu:"
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
        "0": ("save & exit", None),
        "?": ("help", print_menu),
    }

    print('Organizer v1.0')
    print(print_menu())

    while True:
        choice = input("Organizer: ").strip()
        if choice not in commands:
            print("Invalid selection. Try again.")
            continue

        desc, handler = commands[choice]
        if choice == "0":
            handlers.save_data(organizer)
            print("Data saved. Goodbye!")
            break

        result = handler(organizer)
        if result:
            print(result)


if __name__ == "__main__":
    main()
