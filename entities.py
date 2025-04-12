from validators import *
from datetime import datetime as dt, timedelta as td
from collections import UserDict
from colorama import Fore, Style, init
import pickle
from typing import Optional

init(autoreset=True)

INDENT = 11


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str): super().__init__(length_validator(value))


class Phone(Field):
    pattern = r'[0-9]{10}'

    def __init__(self, value: str):
        self.__value = value
        super().__init__(self.__value)

    @property
    def value(self): return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = phone_number_validator(self.pattern, value)


class Email(Field):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'

    def __init__(self, value: str):
        self.__value = value
        super().__init__(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = email_validator(self.pattern, value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            super().__init__(dt.strptime(value, "%d.%m.%Y").date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Address(Field):
    def __init__(self, value: str): super().__init__(address_validator(value))


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self._phone = None
        self._birthday = None
        self._address = None
        self._email = None

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, number: str):
        if number is None:
            self._phone = None
        else:
            self._phone = Phone(number)

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: str):
        if birthday is None:
            self._birthday = None
        else:
            self._birthday = Birthday(birthday)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address: str):
        if address is None:
            self._address = None
        else:
            self._address = Address(address)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        if email is None:
            self._email = None
        else:
            self._email = Email(email)

    def add_phone(self, number: str):
        self._phone = Phone(number)

    def remove_phone(self):
        self._phone = None

    def edit_phone(self, new_value: str):
        # Now only takes one parameter - the new value
        self._phone = Phone(new_value)

    def add_birthday(self, birthday: str):
        self.birthday = birthday

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.clear()
        self.__dict__.update(state)

        # Initialize any missing attributes to prevent attribute errors
        if not hasattr(self, 'name'):
            self.name = None
        if not hasattr(self, '_phone'):
            self._phone = None
        if not hasattr(self, '_birthday'):
            self._birthday = None
        if not hasattr(self, '_address'):
            self._address = None
        if not hasattr(self, '_email'):
            self._email = None

    def __str__(self):
        info = [
            f"{Fore.LIGHTBLACK_EX}Name:{Style.RESET_ALL} {Style.BRIGHT}{self.name.value}{Style.RESET_ALL}"]

        if self.birthday:
            bd_str = self.birthday.value.strftime('%d.%m.%Y')
            info.append(
                f"{Fore.LIGHTBLACK_EX}bd:{Style.RESET_ALL} {Style.BRIGHT}{bd_str}{Style.RESET_ALL}")

        if self._phone:
            info.append(
                f"{Fore.LIGHTBLACK_EX}phone:{Style.RESET_ALL} {Style.BRIGHT}{self._phone.value}{Style.RESET_ALL}")

        if self.email:
            info.append(
                f"{Fore.LIGHTBLACK_EX}email:{Style.RESET_ALL} {Style.BRIGHT}{self.email.value}{Style.RESET_ALL}")

        if self.address:
            info.append(
                f"{Fore.LIGHTBLACK_EX}address:{Style.RESET_ALL} {Style.BRIGHT}{self.address.value}{Style.RESET_ALL}")

        return ', '.join(info)


class Note(Field):
    def __init__(self, title: str, value: str, tags: list = None):
        self._title = Name(title)
        self._tags = tags if tags is not None else []
        super().__init__(length_validator(value))

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value: str):
        if value not in self.tags:
            tag = length_validator(value)
            self.tags.append(tag)
        else:
            raise ValueError("The tag is already in the tag list of the note")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = Name(value)

    def __str__(self):
        info = [
            f"{Fore.LIGHTBLACK_EX}Title:{Style.RESET_ALL} {Style.BRIGHT}{self.title.value}{Style.RESET_ALL}",
            f"{Fore.LIGHTBLACK_EX}Content:{Style.RESET_ALL} {Style.BRIGHT}{self.value}{Style.RESET_ALL}"
        ]

        if self.tags:
            tags_str = ', '.join(self.tags)
            info.append(f"{Fore.LIGHTBLACK_EX}Tags:{Style.RESET_ALL} {Style.BRIGHT}{tags_str}{Style.RESET_ALL}")

        return ', '.join(info)


class Organizer(UserDict):
    def __init__(self):
        super().__init__()
        self.contacts = {}
        self.notes = {}

    # Contact methods
    def add_contact(self, record: Record):
        if isinstance(record, Record):
            if record.name.value not in self.contacts:
                self.contacts[record.name.value] = record
            else:
                raise KeyError(f"The {record.name.value} is already in contact list")
        else:
            raise ValueError(f"The {record} is not instance of Record")

    def find_contact(self, name: str) -> Optional[Record]:
        for contact_name, record in self.contacts.items():
            if contact_name.lower() == name.lower():
                return record

    def delete_contact(self, name: str) -> Optional[Record]:
        if name in self.contacts:
            return self.contacts.pop(name)
        else:
            raise KeyError(f'{name} is absent in contact list')

    def get_upcoming_birthdays(self, days: int = 7) -> list:
        try:
            birthday_people = []
            current_day = dt.today().date()
            for user, record in self.contacts.items():
                if record.birthday:
                    user_birthday = record.birthday.value
                    next_congratulations = user_birthday.replace(
                        year=current_day.year)
                    difference = (next_congratulations - current_day).days
                    if difference < 0:
                        next_congratulations = user_birthday.replace(
                            year=current_day.year + 1)
                        difference = (next_congratulations - current_day).days

                    next_congratulations_weekday = next_congratulations.weekday()

                    if 0 <= difference <= days:
                        if next_congratulations_weekday == 6:
                            next_congratulations += td(days=1)
                        elif next_congratulations_weekday == 5:
                            next_congratulations += td(days=2)
                        congratulations_date = dt.strftime(
                            next_congratulations, "%Y.%m.%d")
                        birthday_people.append(
                            {"name": user, "congratulation_date": congratulations_date})

            birthday_people.sort(key=lambda x: x["congratulation_date"])

            return birthday_people
        except Exception as e:
            print('Function argument must be user list.')
            return []

    # Note methods
    def add_note(self, note: Note):
        if isinstance(note, Note):
            if note.title.value not in self.notes:
                self.notes[note.title.value] = note
            else:
                raise KeyError(f"The {note.title.value} is already in list of notes")
        else:
            raise ValueError(f"The {note} is not instance of Note")

    def find_note(self, title: str) -> Optional[Note]:
        if title in self.notes:
            return self.notes.get(title)

    def show_notes(self):
        if not self.notes:
            print(f"{' ' * INDENT}{Fore.LIGHTBLACK_EX}No notes available.{Style.RESET_ALL}")
            return self

        result = []
        for note in self.notes.values():
            result.append(' ' * INDENT + str(note))

        print("\n".join(result))
        return self
    
    def delete_note(self, title: str):
        if title in self.notes:
            return self.notes.pop(title)
    
    def find_notes_by_text(self, text: str):
        found_notes=[]
        for _, note in self.notes.items():
            search_phrase = f"{note.title.value} {note.value}".lower()
            if text.lower() in search_phrase:
                found_notes.append(note)
        if found_notes:
            return found_notes
        
    def find_notes_by_tags(self, text: str):
        found_notes=[]
        for _, note in self.notes.items():
            if any(text.lower() in tag.lower() for tag in note.tags):
                found_notes.append(note)
        if found_notes:
            return found_notes    
       
    def save(self, filename="organizer.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename="organizer.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
