from collections import UserDict
from datetime import datetime as dt, timedelta as td
from colorama import Fore, Style, init
init(autoreset=True)

from validators import *


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
        self.phones = []
        self._birthday = None
        self._address = None
        self._email = None

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
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        self.phones = list(
            filter(lambda phone: phone.value != number, self.phones))

    def edit_phone(self, number: str, new_value: str):
        for phone in self.phones:
            if phone.value == number:
                phone.value = new_value
                return True

        raise KeyError(f'Phone number: {number} not found')

    def find_phone(self, number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == number:
                return phone

        raise KeyError(f'Phone number: {number} not found')

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
        if not hasattr(self, 'phones'):
            self.phones = []
        if not hasattr(self, '_birthday'):
            self._birthday = None
        if not hasattr(self, '_address'):
            self._address = None
        if not hasattr(self, '_email'):
            self._email = None

    def __str__(self):
        info = [f"{Fore.LIGHTBLACK_EX}Name:{Style.RESET_ALL} {Style.BRIGHT}{self.name.value}{Style.RESET_ALL}"]

        if self.birthday:
            bd_str = self.birthday.value.strftime('%d.%m.%Y')
            info.append(f"{Fore.LIGHTBLACK_EX}bd:{Style.RESET_ALL} {Style.BRIGHT}{bd_str}{Style.RESET_ALL}")

        if self.phones:
            phones_str = '; '.join(phone.value for phone in self.phones)
            info.append(f"{Fore.LIGHTBLACK_EX}phone:{Style.RESET_ALL} {Style.BRIGHT}{phones_str}{Style.RESET_ALL}")

        if self.email:
            info.append(
                f"{Fore.LIGHTBLACK_EX}email:{Style.RESET_ALL} {Style.BRIGHT}{self.email.value}{Style.RESET_ALL}")

        if self.address:
            info.append(
                f"{Fore.LIGHTBLACK_EX}address:{Style.RESET_ALL} {Style.BRIGHT}{self.address.value}{Style.RESET_ALL}")

        return ', '.join(info)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if isinstance(record, Record):
            if record.name.value not in self.data:
                self.data[record.name.value] = record
            else:
                raise KeyError(
                    f"The {record.name.value} is already in contact list")
        else:
            raise ValueError(f"The {record} is not instance of Record")

    def find(self, name: str) -> Optional[Record]:
        if name in self.data:
            return self.data.get(name)

    def delete(self, name: str) -> Optional[Record]:
        if name in self.data:
            return self.data.pop(name)
        else:
            raise KeyError(f'{name} is absent in contact list')

    def get_upcoming_birthdays(self) -> list:
        try:
            birthday_people = []
            current_day = dt.today().date()
            for user, record in self.data.items():
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

                    if 0 <= difference <= 7:
                        if next_congratulations_weekday == 6:
                            next_congratulations += td(days=1)
                        elif next_congratulations_weekday == 5:
                            next_congratulations += td(days=2)
                        congratulations_date = dt.strftime(
                            next_congratulations, "%Y.%m.%d")
                        birthday_people.append(
                            {"name": user, "congratulation_date": congratulations_date})
            return birthday_people
        except Exception as e:
            print('Function argument must be user list.')
            return []

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)


# Notebook


class Note(Field):
    def __init__(self, title: str, value: str):
        self.title = Name(title)
        self._tags = []
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


class NoteBook(UserDict):
    def add_note(self, note: Note):
        if isinstance(note, Note):
            if note.title.value not in self.data:
                self.data[note.title.value] = note
            else:
                raise KeyError(
                    f"The {note.title.value} is already in list of notes")
        else:
            raise ValueError(f"The {note} is not instance of Note")

    def find(self, title: str) -> Optional[Record]:
        if title in self.data:
            return self.data.get(title)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
