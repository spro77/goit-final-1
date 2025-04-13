#!/usr/bin/env python3
from organizer.entities import Record, Note, Organizer
import os

def get_data_path(filename="organizer.pkl"):
    data_dir = os.path.join(os.path.expanduser("~"), ".organizer")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)


def seed_demo_data():
    """
    Create and populate a new Organizer with demo contacts and notes
    """
    organizer = Organizer()

    # Mock contact data
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

    # Add contacts
    for contact in contacts:
        record = Record(contact["name"])
        record.add_phone(contact["phone"])
        record.add_birthday(contact["birthday"])
        record.email = contact["email"]
        record.address = contact["address"]
        organizer.add_contact(record)

    # Mock note data
    notes = [
        {"title": "Shopping List", "value": "Milk, Bread, Eggs, Cheese", "tags": ["shopping", "groceries"]},
        {"title": "Meeting Notes", "value": "Discuss Q3 planning with team", "tags": ["work", "meetings"]},
        {"title": "Birthday Ideas", "value": "Gift ideas for Sarah: cookbook, scarf, jewelry",
         "tags": ["birthdays", "gifts"]},
        {"title": "Books to Read", "value": "1984, Dune, The Hobbit", "tags": ["books", "reading"]}
    ]

    # Add notes
    for note_data in notes:
        note = Note(note_data["title"], note_data["value"], note_data["tags"])
        organizer.add_note(note)

    # Save the organizer
    data_path = get_data_path()
    organizer.save(data_path)
    print(f"Demo contacts and notes added to {data_path}")
    return organizer


if __name__ == "__main__":
    data_path = get_data_path()
    if os.path.exists(data_path):
        confirm = input(f"{data_path} already exists. Overwrite? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            exit()

    seed_demo_data()