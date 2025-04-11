from curses.ascii import isdigit
from colorama import Fore, Style
from entities import *
import pickle

INDENT = 11


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
    indented_prompt = " " * INDENT + Fore.BLUE + prompt + Style.RESET_ALL
    user_input = input(f"{indented_prompt} ('/' to main menu): ").strip()

    if user_input == '/':
        print(" " * INDENT + f"{Style.DIM}{Fore.WHITE}Operation cancelled.{Style.RESET_ALL}")
        return None

    if not user_input and not allow_empty:
        print(" " * INDENT + "This field cannot be empty. Please try again or type '/' to return to menu.")
        return safe_input(prompt, allow_empty)

    return user_input


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(book: Organizer) -> str:
    name = safe_input("Enter contact name", allow_empty=False)
    if name is None:
        return ""

    record = Record(name)

    while True:
        phone = safe_input("Optional phone (10 digits)", allow_empty=True)
        if phone is None:
            return ""
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except ValueError as e:
            print(f"{' ' * INDENT}{e}")

    birthday = safe_input("Optional birthday (DD.MM.YYYY)", allow_empty=True)
    if birthday is None:
        return ""
    if birthday:
        try:
            record.add_birthday(birthday)
        except ValueError as e:
            return " " * INDENT + str(e)

    email = safe_input("Optional email", allow_empty=True)
    if email is None:
        return ""
    if email:
        try:
            record.email = email
        except ValueError as e:
            return " " * INDENT + str(e)

    address = safe_input("Optional address", allow_empty=True)
    if address is None:
        return ""
    if address:
        try:
            record.address = address
        except ValueError as e:
            return " " * INDENT + str(e)

    try:
        book.add_contact(record)
        return " " * INDENT + "Contact added."
    except KeyError:
        # This should be caught by our input_error decorator
        # which will display "Contact exists in your contact list"
        raise


@input_error
def change_contact(book: Organizer) -> str:
    name = safe_input("Enter contact name", allow_empty=False)
    if name is None:
        return ""

    record = book.find_contact(name)
    if not record:
        raise KeyError()

    birthday = safe_input("Change birthday? (enter as DD.MM.YYYY or skip)", allow_empty=True)
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
        phone = safe_input("Change phone number? (enter or skip)", allow_empty=True)
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
def show_all(book: Organizer):
    if not book.contacts:
        return ' ' * INDENT + f'{Fore.LIGHTBLACK_EX}No contacts saved.{Style.RESET_ALL}'

    result = []
    for _, record in book.contacts.items():
        result.append(' ' * INDENT + str(record))

    return "\n".join(result)


@input_error
def birthdays(book: Organizer):
    days = safe_input('Enter number of check to days: (7):', allow_empty=True)
    if days is None:
        return ""

    if days.isdigit():
        for contact in book.get_upcoming_birthdays(int(days)):
            print(
                f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Don't forget to wish {Style.RESET_ALL}{Style.BRIGHT}{contact['name']}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX} a happy birthday on {Style.RESET_ALL}{Style.BRIGHT}{contact['congratulation_date']}")
    else:
        for contact in book.get_upcoming_birthdays():
            print(
                f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Don't forget to wish {Style.RESET_ALL}{Style.BRIGHT}{contact['name']}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX} a happy birthday on {Style.RESET_ALL}{Style.BRIGHT}{contact['congratulation_date']}")


def save_data(book: Organizer, filename="organizer.pkl"):
    book.save(filename)


def load_data(filename="organizer.pkl"):
    return Organizer.load(filename)


@input_error
def add_note(book: Organizer) -> str:
    title = safe_input('Input value for the title of the note: ')
    if title is None:
        return "Note creation cancelled."

    note = book.find_note(title)
    if note is not None:
        return "Note is already in notebook"

    text = safe_input("Write the note description: ")
    if text is None:
        return "Note creation cancelled."

    note = Note(title, text)
    book.add_note(note)

    is_need_add_tag = safe_input("Do you want to add a tag to the note? (y/n): ")
    if is_need_add_tag is None:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note added.{Style.RESET_ALL}"

    if is_need_add_tag.strip().lower() == 'y':
        while True:
            new_tag = safe_input("Enter a new tag (or press Enter to stop): ", allow_empty=True)
            if new_tag is None:
                return "Note created."
            if not new_tag:
                break
            try:
                note.tags.append(new_tag)
            except ValueError as e:
                print(e)

    return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note added.{Style.RESET_ALL}"


@input_error
def search_contact(book: Organizer) -> str:
    query = safe_input("Enter a name or number to search for", allow_empty=False)
    if query is None:
        return ""

    query = query.lower()
    results = []

    for name, record in book.contacts.items():
        name_match = query in name.lower()
        phone_match = record.phone and query in record.phone.value.lower()

        if name_match or phone_match:
            results.append(" " * INDENT + str(record))

    return "\n".join(results) if results else " " * INDENT + "No matches found."


@input_error
def delete_contact(book: Organizer) -> str:
    name = safe_input("Enter contact name", allow_empty=False)
    if name is None:
        return ""

    record = book.find_contact(name)
    if record:
        book.delete_contact(name)
        return f"{' ' * INDENT}Contact was deleted"
    raise KeyError()


def list_notes(book: Organizer):
    book.show_notes()
    return


def search_notes(args, book: Organizer) -> str:
    pass


def edit_note(book: Organizer) -> Optional[str]:
    notes = book.notes
    book.show_notes()
    if not notes:
        return "No notes to edit."

    selected_index_input = safe_input("Enter the number of the note you want to edit: ")
    if selected_index_input is None:
        return "Edit cancelled."

    try:
        selected_index = int(selected_index_input)
        note = list(notes.values())[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None

    print(f"\nEditing note: {note.title.value}")

    if safe_input("Do you want to change the title? (y/n): ") == 'y':
        new_title = safe_input("Set new value for title: ")
        if new_title is None:
            return "Edit cancelled."
        note.title = length_validator(new_title)

    if safe_input("Do you want to change the note description? (y/n): ") == 'y':
        new_description = safe_input("Set new value for note: ")
        if new_description is None:
            return "Edit cancelled."
        note.value = length_validator(new_description)

    if safe_input("Do you want to update tags? (y/n): ") == 'y':
        while True:
            print("\nWhat do you want to do with tags?")
            print("1: Add tags")
            print("2: Change existing tags")
            print("3: Delete tags")
            action = safe_input("Select an option (1/2/3): ")
            if action is None:
                return "Edit cancelled."

            if action == '1':
                while True:
                    new_tag = safe_input("Enter a new tag (or press Enter to stop): ", allow_empty=True)
                    if new_tag is None:
                        return "Edit cancelled."
                    if not new_tag:
                        break
                    try:
                        note.tags.append(new_tag)
                    except ValueError as e:
                        print(e)
                break

            elif action == '2':
                if not note.tags:
                    print("No tags available to change.")
                    break

                for idx, tag in enumerate(note.tags):
                    print(f"{idx}: {tag}")

                tag_index_input = safe_input("Select the number of the tag to change: ")
                if tag_index_input is None:
                    return "Edit cancelled."

                try:
                    tag_index = int(tag_index_input)
                    if tag_index < 0 or tag_index >= len(note.tags):
                        print("Invalid tag number.")
                        continue
                    new_tag_value = safe_input("Enter new value for the tag: ")
                    if new_tag_value is None:
                        return "Edit cancelled."
                    note.tags[tag_index] = new_tag_value
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    continue
                break

            elif action == '3':
                if not note.tags:
                    print("No tags available to delete.")
                    break

                for idx, tag in enumerate(note.tags):
                    print(f"{idx}: {tag}")

                tag_index_input = safe_input("Select the number of the tag to delete: ")
                if tag_index_input is None:
                    return "Edit cancelled."

                try:
                    tag_index = int(tag_index_input)
                    if tag_index < 0 or tag_index >= len(note.tags):
                        print("Invalid tag number.")
                        continue
                    deleted_tag = note.tags.pop(tag_index)
                    print(f"Tag '{deleted_tag}' has been deleted.")
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    continue
                break

    return "Note updated."


def delete_note( book: Organizer) -> str:
    try:
        title = safe_input("Enter a title of note to delete: ", allow_empty=False)
        if title is None:
            return 'Delete was cancelled'
        note = book.find_note(title)
        if note:
            book.delete_note(title)
            return f"{" " * INDENT}Note was deleted"
        else:
            return f"{" " * INDENT}Note was not found"
    except Exception as e:
        return f"Error: {str(e)}"



