from datetime import datetime, date, timedelta
from collections import UserDict

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Enter the argument for the command"
        except IndexError:
            return "Invalid index"
    return wrapper

def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date_obj = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_contact(self, name, birthday):
        try:
            self.data[name] = {"birthday": string_to_date(birthday)}
        except ValueError:
            return "Invalid date format. Use YYYY.MM.DD"

    def get_upcoming_birthdays(self, days=7, current_date=None):
        upcoming_birthdays = []
        today = current_date if current_date else date.today()
        
        for name, info in self.data.items():
            birthday = info['birthday']
            this_year_birthday = birthday.replace(year=today.year)
            
            if this_year_birthday < today:
                this_year_birthday = birthday.replace(year=today.year + 1)
            
            if today <= this_year_birthday <= today + timedelta(days=days):
                upcoming_birthdays.append({
                    "name": name,
                    "congratulation_date": this_year_birthday.strftime("%Y.%m.%d")
                })
        
        return upcoming_birthdays

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    def get_birthday(self, name):
        if name in self.data and "birthday" in self.data[name]:
            return self.data[name]["birthday"]
        return None

    def show_all_contacts(self):
        if not self.data:
            return "No contacts available."
        result = "All contacts:\n"
        for name, info in self.data.items():
            phones = ", ".join(info.get("phones", []))
            birthday = info.get("birthday", "").strftime("%Y.%m.%d") if "birthday" in info else "N/A"
            result += f"Name: {name}, Phones: {phones}, Birthday: {birthday}\n"
        return result

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday_str):
        try:
            self.birthday = datetime.strptime(birthday_str, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def add_phone(self, phone_number):
        if len(phone_number) == 10 and phone_number.isdigit():
            self.phones.append(phone_number)
            return True
        else:
            return False

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Please provide both name and phone number."
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    if phone and record.add_phone(phone):
        message += " Phone number added successfully."
    elif phone:
        message += " Invalid phone number. Please enter a 10-digit numeric phone number."
    return message

@input_error
def change_contacts(args, book):
    if len(args) < 2:
        return "Please provide both name and new phone number."
    name, new_phone = args
    if name in book.data:
        book.data[name]['phone'] = new_phone
        return f"Phone number updated successfully for {name}."
    else:
        return f"Error: {name} does not exist in the contacts."

@input_error
def phone_user(args, contacts):
    if len(args) < 1:
        return "Please provide a name."
    name = args[0]
    if name in contacts:
        return f'{name}: {contacts[name]["phone"]}'
    else:
        return "No user in contacts."

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Please provide both name and birthday."
    name, birthday = args
    return book.add_contact(name, birthday)

@input_error
def show_birthday(args, book):
    if len(args) < 1:
        return "Please provide a name."
    name = args[0]
    birthday = book.get_birthday(name)
    if birthday:
        return f"{name}'s birthday is on {birthday.strftime('%Y.%m.%d')}."
    else:
        return f"No birthday found for {name}."

@input_error
def birthdays(args, book):
    current_date = date.today()
    upcoming_birthdays = book.get_upcoming_birthdays(current_date=current_date)
    if upcoming_birthdays:
        result = "Upcoming birthdays:\n"
        result += "\n".join([f"{entry['name']} - {entry['congratulation_date']}" for entry in upcoming_birthdays])
        return result
    else:
        return "No upcoming birthdays in the next week."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contacts(args, book))
        
        elif command == "phone":
            print(phone_user(args, book.data))

        elif command == "all":
            print(book.show_all_contacts())

        elif command == "add-birthday":
            print(add_birthday(args, book))
        
        elif command == "show-birthday":
            print(show_birthday(args, book))
        
        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()