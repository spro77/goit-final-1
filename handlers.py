from entities import *
import pickle


# Decorators
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone(10 digits) please."
        except KeyError:
            return "Contact doesn't exists in your contact list."
        except IndexError:
            return "Enter the argument for the command."
        except Exception as e:
            return e

    return inner


# General Handlers
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# AdressBook Handlers
@input_error
def add_contact(book):
    name = input("Enter contact name (mandatory): ")
    phone = input("Enter phone (10 digits): ")
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook) -> str:
    name, phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(phone, new_phone)
        return "Contact changed."
    raise SyntaxError(f"Give name, phone and new number of the contact.")


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return 'No contacts saved.'

    result = []

    for name, record in book.data.items():
        phones = '; '.join(str(phone) for phone in record.phones)
        birthday_info = f", birthday: {record.birthday.value.strftime('%d.%m.%Y')}" if record.birthday else ''
        result.append(f'{name}: {phones}{birthday_info}')
    return "\n".join(result)


@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones])
        return phones
    raise KeyError()


@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, date, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return f"Birthday added to Contact: {name}"
    raise KeyError(f"Contact {name} not found.")


@input_error
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{name}'s birthday is {record.birthday} "
    raise KeyError(f"Contact {name} not found.")


@input_error
def birthdays(book: AddressBook):
    for contact in book.get_upcoming_birthdays():
        print(
            f"Don't forget to wish {contact['name']} a happy birthday on {contact['congratulation_date']}")


def save_adressbook_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_adressbook_data(filename="addressbook.pkl"):
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


# placeholders
@input_error
def search_contact(book: AddressBook) -> str:
    query = input("Enter a name or number to search for: ").lower()
    results = []

    for name, record in book.data.items():
        name_match = query in name.lower()
        phone_match = any(query in phone.value for phone in record.phones)

        if name_match or phone_match:
            phones = ", ".join(p.value for p in record.phones)
            birthday_info = record.birthday.value.strftime(
                '%d.%m.%Y') if record.birthday else ''
            results.append(f"{name}: {phones}{birthday_info}")

    return "\n".join(results) if results else "No matches found."

@input_error
def delete_contact( book: AddressBook) -> str:
    name = input("Enter contact name (mandatory): ").lower()
    record = book.find(name)
    if record:
        book.delete(name)
        return "Contact was deleted"
    raise KeyError()


def list_notes(notebook: NoteBook) -> str:
    pass


def search_notes(args, notebook: NoteBook) -> str:
    pass


def edit_note(args, notebook: NoteBook) -> str:
    pass


def delete_note(args, notebook: NoteBook) -> str:
    pass
