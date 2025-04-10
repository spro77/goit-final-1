# Contact Manager

A command-line contact and note management application.

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. Clone the repository:
    ```bash
   git clone https://github.com/spro77/goit-final-1.git
   cd goit-final-1
2. Create a virtual environment:
    ```bash
    python -m venv .venv
3. Activate the virtual environment:
    - On Windows:
        ```bash
        .venv\Scripts\activate
    - On macOS/Linux:
        ```bash
        source .venv/bin/activate
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
   
## Running the Application

### Seeding Demo Data (Optional)
To populate the application with demo contacts:
   ```bash
    python seed.py
```

Start the application:
```bash
  python main.py
```

## Features

- Contact management with phone numbers, birthdays, emails, and addresses
- Note-taking functionality with tags
- Upcoming birthday reminders
- Colorful terminal output