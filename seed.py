#!/usr/bin/env python3
from entities import Record, AddressBook
import pickle
import os

def seed_demo_data():
    """
    Create and populate a new AddressBook with demo contacts
    """
    book = AddressBook()

    # Mock data
    contacts = [
        {"name": "John Smith", "phone": "1234567890", "birthday": "15.06.1985",
         "email": "john@example.com", "address": "123 Main St"},
        {"name": "Alice Johnson", "phone": "9876543210", "birthday": "03.12.1990",
         "email": "alice@example.com", "address": "456 Oak Ave"},
        {"name": "Bob Williams", "phone": "5551234567", "birthday": "22.07.1982",
         "email": "bob@example.com", "address": "789 Pine Rd"},
        {"name": "Emma Davis", "phone": "3334445555", "birthday": "17.04.1992",
         "email": "emma@example.com", "address": "101 Maple Dr"},
        {"name": "Michael Brown", "phone": "7778889999", "birthday": "08.09.1975",
         "email": "michael@example.com", "address": "202 Cedar Ln"},
        {"name": "Sarah Wilson", "phone": "1112223333", "birthday": "30.01.1988",
         "email": "sarah@example.com", "address": "303 Birch Ave"},
        {"name": "David Taylor", "phone": "4445556666", "birthday": "25.11.1979",
         "email": "david@example.com", "address": "404 Spruce St"},
        {"name": "Jennifer Lee", "phone": "6667778888", "birthday": "12.08.1995",
         "email": "jennifer@example.com", "address": "505 Elm Blvd"},
        {"name": "Robert Garcia", "phone": "2223334444", "birthday": "19.03.1980",
         "email": "robert@example.com", "address": "606 Walnut Way"},
        {"name": "Lisa Martinez", "phone": "8889990000", "birthday": "07.05.1991",
         "email": "lisa@example.com", "address": "707 Chestnut Pl"}
    ]

    for contact in contacts:
        record = Record(contact["name"])
        record.add_phone(contact["phone"])
        record.add_birthday(contact["birthday"])
        record.email = contact["email"]
        record.address = contact["address"]
        book.add_record(record)

    with open("addressbook.pkl", "wb") as f:
        pickle.dump(book, f)

    print(f"Demo contacts added to addressbook.pkl")
    return book

if __name__ == "__main__":
    if os.path.exists("addressbook.pkl"):
        confirm = input("addressbook.pkl already exists. Overwrite with demo data? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            exit()

    seed_demo_data()