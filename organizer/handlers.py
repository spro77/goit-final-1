import os
from curses.ascii import isdigit
from colorama import Fore, Style
from organizer.entities import Organizer, Record, Note
from organizer.validators import *
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
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Contact added.{Style.RESET_ALL}"
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

    return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Contact changed.{Style.RESET_ALL}"


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


def get_data_path(filename="organizer.pkl"):
    data_dir = os.path.join(os.path.expanduser("~"), ".organizer")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)


def save_data(book: Organizer, filename="organizer.pkl"):
    full_path = get_data_path(filename)
    book.save(full_path)


def load_data(filename="organizer.pkl"):
    full_path = get_data_path(filename)
    return Organizer.load(full_path)


@input_error
def add_note(book: Organizer) -> str:
    while True:
        title = safe_input('Enter the title: ', allow_empty=False)
        if title is None:
            return "Note creation cancelled."
        if not title.strip():
            print(f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Title can't be empty{Style.RESET_ALL}")
            continue
        break

    note = book.find_note(title)
    if note is not None:
        return "Note is already in notebook"

    text = safe_input("Write the note: ")
    if text is None:
        return "Note creation cancelled."

    note = Note(title, text)
    book.add_note(note)

    tags_input = safe_input("Optional tags, comma separated: ", allow_empty=True)
    if tags_input is None:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note created.{Style.RESET_ALL}"

    if tags_input:
        for tag in [t.strip() for t in tags_input.split(',') if t.strip()]:
            try:
                note.tags.append(tag)
            except ValueError as e:
                print(e)

    print(f"{' ' * INDENT}{str(note)}")
    return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note created.{Style.RESET_ALL}"


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
        confirmation = safe_input(f"Do you want to delete Contact '{name}'? (Y/N): ", allow_empty=False)
        if confirmation is None or confirmation.lower() != 'y':
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Deletion cancelled.{Style.RESET_ALL}"

        book.delete_contact(name)
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Contact was deleted{Style.RESET_ALL}"
    raise KeyError()


def list_notes(book: Organizer):
    book.show_notes()
    return


def search_notes(book: Organizer) -> str:
    choice = safe_input("Do you want to search tags (1) or text (2). Enter 1 or 2: ", allow_empty=False)
    if choice is None or choice == "/":
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Search was canceled{Style.RESET_ALL}"

    if choice == "1":
        tags_input = safe_input("Enter tags to search for (comma separated): ", allow_empty=False)
        if tags_input is None:
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Search was canceled{Style.RESET_ALL}"

        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        found_notes_set = set()

        for tag in tags:
            notes = book.find_notes_by_tags(tag)
            if notes:
                found_notes_set.update(notes)

        if found_notes_set:
            return "\n".join(sorted(found_notes_set))
        else:
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Notes were not found{Style.RESET_ALL}"

    elif choice == "2":
        text = safe_input("Enter text to search for: ", allow_empty=False)
        if text is None:
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Search was canceled{Style.RESET_ALL}"

        notes = book.find_notes_by_text(text)
        if notes:
            return "\n".join(str(note) for note in notes)
        else:
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Notes were not found{Style.RESET_ALL}"
    else:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Invalid choice.{Style.RESET_ALL}"


def edit_note(book: Organizer) -> Optional[str]:
    notes = book.notes
    book.show_notes()
    if not notes:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}No notes to edit.{Style.RESET_ALL}"

    selected_index_input = safe_input("Enter the number of the note you want to edit: ")
    if selected_index_input is None:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Edit cancelled.{Style.RESET_ALL}"
    try:
        selected_index = int(selected_index_input)
        note = list(notes.values())[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None

    print(f"\nEditing note: {note.title.value}")

    changes_made = False

    new_title = safe_input("Update Title or skip: ", allow_empty=True)
    if new_title is None:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Edit cancelled.{Style.RESET_ALL}"
    if new_title:
        note.title = length_validator(new_title)
        changes_made = True

    new_description = safe_input("Update Note or skip: ", allow_empty=True)
    if new_description is None:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Edit cancelled.{Style.RESET_ALL}"
    if new_description:
        note.value = length_validator(new_description)
        changes_made = True

    if safe_input("Do you want to update tags? (y/n): ") == 'y':
        while True:
            print(f"\n{' ' * INDENT}Tag Management:")
            print(f"{' ' * (INDENT * 2)}1: Add tags")
            print(f"{' ' * (INDENT * 2)}2: Change existing tags")
            print(f"{' ' * (INDENT * 2)}3: Delete tags")

            def level3_input(prompt, allow_empty=False):
                indented_prompt = " " * (INDENT * 2) + Fore.BLUE + prompt + Style.RESET_ALL
                user_input = input(f"{indented_prompt} ('/' to exit tag editing): ").strip()

                if user_input == '/':
                    return None

                if not user_input and not allow_empty:
                    print(" " * (INDENT * 2) + "This field cannot be empty. Please try again or type '/' to exit.")
                    return level3_input(prompt, allow_empty)

                return user_input

            action = level3_input("Select an option (1/2/3/4): ")
            if action is None or action == '4':
                print(f"\n{' ' * INDENT}Current note:")
                print(f"{' ' * INDENT}{str(note)}")
                break

            if action == '1':
                while True:
                    new_tag = level3_input("Enter a new tag (or press Enter to stop): ", allow_empty=True)
                    if new_tag is None:
                        break
                    if not new_tag:
                        break
                    try:
                        note.tags.append(new_tag)
                        changes_made = True
                        print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Tag added.{Style.RESET_ALL}")
                    except ValueError as e:
                        print(f"{' ' * (INDENT * 2)}{e}")

            elif action == '2':
                if not note.tags:
                    print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}No tags available to change.{Style.RESET_ALL}")
                    continue

                for idx, tag in enumerate(note.tags):
                    print(f"{' ' * (INDENT * 2)}{idx}: {tag}")

                tag_index_input = level3_input("Select the number of the tag to change: ")
                if tag_index_input is None:
                    continue

                try:
                    tag_index = int(tag_index_input)
                    if tag_index < 0 or tag_index >= len(note.tags):
                        print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Invalid tag number.{Style.RESET_ALL}")
                        continue
                    new_tag_value = level3_input("Enter new value for the tag: ")
                    if new_tag_value is None:
                        continue
                    note.tags[tag_index] = new_tag_value
                    changes_made = True
                    print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Tag updated.{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Invalid selection.{Style.RESET_ALL}")

            elif action == '3':
                if not note.tags:
                    print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}No tags available to delete.{Style.RESET_ALL}")
                    continue

                for idx, tag in enumerate(note.tags):
                    print(f"{' ' * (INDENT * 2)}{idx}: {tag}")

                tag_index_input = level3_input("Select the number of the tag to delete: ")
                if tag_index_input is None:
                    continue

                try:
                    tag_index = int(tag_index_input)
                    if tag_index < 0 or tag_index >= len(note.tags):
                        print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Invalid tag number.{Style.RESET_ALL}")
                        continue
                    deleted_tag = note.tags.pop(tag_index)
                    changes_made = True
                    print(
                        f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Tag '{deleted_tag}' has been deleted.{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{' ' * (INDENT * 2)}{Fore.LIGHTBLACK_EX}Invalid selection.{Style.RESET_ALL}")

    if changes_made:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note updated.{Style.RESET_ALL}"
    else:
        return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}No changes made to note.{Style.RESET_ALL}"


def delete_note(book: Organizer) -> str:
    try:
        title = safe_input("Enter a title of note to delete: ", allow_empty=False)
        if title is None:
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Delete was cancelled{Style.RESET_ALL}"
        note = book.find_note(title)
        if note:
            book.delete_note(title)
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note was deleted{Style.RESET_ALL}"
        else:
            return f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}Note was not found{Style.RESET_ALL}"
    except Exception as e:
        return f"Error: {str(e)}"
