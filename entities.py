from collections import UserDict
import re
from typing import Optional
from datetime import datetime as dt, timedelta as td

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value): super().__init__(self.__validate_name(value))

    def __validate_name(self, value):
        if len(value) == 0: raise ValueError('Name is too short, need more than 0 symbol')
        else: return value 

class Phone(Field):
    pattern = r'[0-9]{10}'

    def __init__(self, value): 
        self.__value = value
        super().__init__(self.__value)

    @property
    def value(self): return self.__value

    @value.setter
    def value(self, value): 
        self.__value = self.__validate_number(value)

    def __validate_number(self, number):
        if re.fullmatch(self.pattern, number.strip()): return number
        else: raise ValueError('The "phone number" field must contain 10 digits')

class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(dt.strptime(value, "%d.%m.%Y").date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self._birthday = None

    @property
    def birthday(self):
        return self._birthday
    
    @birthday.setter
    def birthday(self, birthday: str):
        if birthday is None: self._birthday = None
        else: self._birthday = Birthday(birthday)

    def add_phone(self, number: str): self.phones.append(Phone(number))
    
    def remove_phone(self, number: str): self.phones = list(filter(lambda phone: phone.value!=number, self.phones))

    def edit_phone(self, number: str, new_value):
        for phone in self.phones:
            if phone.value == number:
                phone.value = new_value
                return True

        raise KeyError(f'Phone number: {number} not found')

    def find_phone(self, number:str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == number: return phone
        
        raise KeyError(f'Phone number: {number} not found')

            
    def add_birthday(self, birthday: str):
        self.birthday = birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if isinstance(record, Record):
            if record.name.value not in self.data: self.data[record.name.value] = record
            else: raise KeyError(f"The {record.name.value} is already in contact list")
        else: raise ValueError(f"The {record} is not instance of Record")

    def find(self, name: str) -> Optional[Record]:
        if name in self.data: return self.data.get(name)

    def delete(self, name: str) -> Optional[Record]:
        if name in self.data: return self.data.pop(name)
        else: raise KeyError(f'{name} is absent in contact list')
        
    def get_upcoming_birthdays(self) -> list:
        try:
            birthday_people = []
            current_day = dt.today().date()
            for user,record in self.data.items():
                if record.birthday:
                    user_birthday = record.birthday.value
                    next_congratulations = user_birthday.replace(year=current_day.year)
                    difference = (next_congratulations - current_day).days
                    if difference < 0:
                        next_congratulations = user_birthday.replace(year=current_day.year + 1)
                        difference = (next_congratulations - current_day).days

                    next_congratulations_weekday = next_congratulations.weekday()

                    if 0 <= difference <= 7:
                        if next_congratulations_weekday == 6: next_congratulations += td(days=1)
                        elif next_congratulations_weekday == 5: next_congratulations += td(days=2)
                        congratulations_date = dt.strftime(next_congratulations, "%Y.%m.%d")
                        birthday_people.append({"name": user, "congratulation_date": congratulations_date})
            return birthday_people
        except Exception as e:
            print('Function argument must be user list.')
            return []
        
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)