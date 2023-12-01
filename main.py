from collections import UserDict
import re
import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Invalid phone number. Must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(self.validate(value))

    @staticmethod
    def validate(value):
        try:
            return datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name_value, phones=None, birthday=None):
        self.name = Name(name_value)
        self.phones = phones if phones is not None else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, Phones: {phones}{birthday}"


class AddressBook(UserDict):
    def add_record(self, record_inf):
        self.data[record_inf.name.value] = record_inf

    def find(self, name_value):
        return self.data.get(name_value)

    def delete(self, name_value):
        if name_value in self.data:
            del self.data[name_value]

    def get_birthdays_per_week(self):
        current_date = datetime.datetime.now().date()
        one_week_later = current_date + datetime.timedelta(days=7)
        birthdays_this_week = []
        for name_value, record_inf in self.data.items():
            if record_inf.birthday and current_date <= record_inf.birthday.value < one_week_later:
                birthdays_this_week.append(name_value)
        return birthdays_this_week


# Тестування коду
book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("01.01.1980")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("02.02.1985")
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")
    print(john)

found_phone = john.find_phone("5555555555") if john else None
if found_phone:
    print(f"{john.name}: {found_phone}")

book.delete("Jane")

# Перевірка днів народження на наступному тижні
birthdays_next_week = book.get_birthdays_per_week()
print("Birthdays next week:", birthdays_next_week)
