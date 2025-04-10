from curses.ascii import isdigit
from colorama import Fore, Style
from entities import *
import pickle

# Global constants
INDENT = 11  # Number of spaces for indentation

# Decorators


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{' ' * INDENT}{Style.DIM}{Fore.WHITE}Give me name and phone(10 digits) please.{Style.RESET_ALL}"
        except KeyError:
            return f"{' ' * INDENT}{Style.DIM}{Fore.WHITE}Contact doesn't exist in your contact list.{Style.RESET_ALL}"
        except IndexError:
            return f"{' ' * INDENT}{Style.DIM}{Fore.WHITE}Enter the argument for the command.{Style.RESET_ALL}"
        except Exception as e:
            return f"{' ' * INDENT}{Style.DIM}{Fore.WHITE}{str(e)}{Style.RESET_ALL}"

    return inner


def safe_input(prompt, allow_empty=False):
    """Custom input function that allows returning to the main menu"""
    indented_prompt = " " * INDENT + prompt
    user_input = input(f"{indented_prompt} ('/' to return to menu): ").strip()

    if user_input == '/':
        print(" " * INDENT +
              f"{Style.DIM}{Fore.WHITE}Operation cancelled.{Style.RESET_ALL}")
        return None

    if not user_input and not allow_empty:
        print(" " * INDENT + "This field cannot be empty. Please try again or type '/' to return to menu.")
        return safe_input(prompt, allow_empty)

    return user_input


# General Handlers
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(book) -> str:
    name = safe_input("Enter contact name (mandatory)", allow_empty=False)
    if name is None:
        return ""

    record = Record(name)

    while True:
        phone = safe_input("Enter phone (10 digits)", allow_empty=True)
        if phone is None:
            return ""
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except ValueError as e:
            print(f"{' ' * INDENT}{e}")

    birthday = safe_input("Enter birthday (DD.MM.YYYY)", allow_empty=True)
    if birthday is None:
        return ""
    if birthday:
        try:
            record.add_birthday(birthday)
        except ValueError as e:
            return " " * INDENT + str(e)

    email = safe_input("Enter email", allow_empty=True)
    if email is None:
        return ""
    if email:
        try:
            record.email = email
        except ValueError as e:
            return " " * INDENT + str(e)

    address = safe_input("Enter address", allow_empty=True)
    if address is None:
        return ""
    if address:
        try:
            record.address = address
        except ValueError as e:
            return " " * INDENT + str(e)

    try:
        book.add_record(record)
        return " " * INDENT + "Contact added."
    except KeyError:
        # This should be caught by our input_error decorator
        # which will display "Contact exists in your contact list"
        raise


@input_error
def change_contact(book: AddressBook) -> str:
    name = safe_input("Enter contact name", allow_empty=False)
    if name is None:
        return ""

    record = book.find(name)
    if not record:
        raise KeyError()

    birthday = safe_input(
        "Change birthday? (enter as DD.MM.YYYY or skip)", allow_empty=True)
    if birthday is None:
        return ""
    if birthday:
        try:
            record.add_birthday(birthday)
        except ValueError as e:
            return " " * INDENT + str(e)

    email = safe_input("Change email? (enter or skip)", allow_empty=True)
    if email is None:
        return ""
    if email:
        try:
            record.email = email
        except ValueError as e:
            return " " * INDENT + str(e)

    address = safe_input("Change address? (enter or skip)", allow_empty=True)
    if address is None:
        return ""
    if address:
        try:
            record.address = address
        except ValueError as e:
            return " " * INDENT + str(e)

    while True:
        phone = safe_input(
            "Change phone number? (enter or skip)", allow_empty=True)
        if phone is None:
            return ""
        if not phone:
            break
        try:
            record.edit_phone(phone)
            break
        except ValueError as e:
            print(f"{' ' * INDENT}{e}")

    return " " * INDENT + "Contact changed."


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return ' ' * INDENT + 'No contacts saved.'

    result = []
    for _, record in book.data.items():
        result.append(' ' * INDENT + str(record))

    return "\n".join(result)


@input_error
def birthdays(book: AddressBook):
    days = safe_input('Enter number of check to days: (7):', allow_empty=True)
    if days.isdigit():
        for contact in book.get_upcoming_birthdays(int(days)):
            print(
                f"Don't forget to wish {contact['name']} a happy birthday on {contact['congratulation_date']}")
    else:
        for contact in book.get_upcoming_birthdays():
            print(
                f"Don't forget to wish {contact['name']} a happy birthday on {contact['congratulation_date']}")


def save_addressbook_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_addressbook_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# NoteBook Handlers
def save_notebook_data(notebook: NoteBook, filename="notebook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


def load_notebook_data(filename="notebook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()


@input_error
def add_note(args, notebook: NoteBook) -> str:
    title = " ".join(args)
    note = notebook.find(title)
    message = "Note is already in notebook"
    if note is None:
        text = input("Write the note description: ")
        print(text)
        note = Note(title, text)
        notebook.add_note(note)
        # isNeedAddTag = input("Do you want to add a tag to note? (y/n): ")
        message = 'Note added.'
    return message


@input_error
@input_error
def search_contact(book: AddressBook) -> str:
    query = safe_input(
        "Enter a name or number to search for", allow_empty=False)
    if query is None:
        return ""

    query = query.lower()
    results = []

    for name, record in book.data.items():
        name_match = query in name.lower()
        phone_match = record.phone and query in record.phone.value.lower()

        if name_match or phone_match:
            results.append(" " * INDENT + str(record))

    return "\n".join(results) if results else " " * INDENT + "No matches found."


@input_error
def delete_contact(book: AddressBook) -> str:
    name = input("Enter contact name: ").lower()
    record = book.find(name)
    if record:
        book.delete(name)
        return "Contact was deleted"
    raise KeyError()


# placeholders
def list_notes(notebook: NoteBook) -> str:
    pass


def search_notes(args, notebook: NoteBook) -> str:
    pass


def edit_note(args, notebook: NoteBook) -> str:
    pass


def delete_note(args, notebook: NoteBook) -> str:
    pass
