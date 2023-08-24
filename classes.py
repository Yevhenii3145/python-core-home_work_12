from collections import UserDict
from datetime import datetime
import pickle
import re


class Name:
    def __init__(self, name):
        self.__name = None
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if len(name) == 0 or name == None:
            raise ValueError(f"Name can't be empty!")
        self.__name = name

    def __str__(self):
        return str(self.name)


class Phone:
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        if not phone.isnumeric():
            raise ValueError("Phone contains unsupported characters")
        self.__phone = phone

    def __repr__(self):
        return str(self.phone)


class Birthday:
    def __init__(self, birthday):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        if type(birthday) == tuple:
            raise ValueError(f"Birthday cant be in 2 dates")
        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Data must be yyyy-mm-dd")
        self.__birthday = birthday


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.birthday = birthday
        self.name = name
        self.phone = phone
        self.phones = []
        if phone:
            self.add_phone(phone)

    def days_to_birthday(self, birthday):
        birthday = datetime.strptime(birthday, "%Y-%m-%d")
        today = datetime.now()
        birthday = birthday.replace(year=today.year)
        days_to_date = birthday - today
        if days_to_date.days < 0:
            return f"was {days_to_date.days} days ago"
        return f"{days_to_date.days} days to birthday"

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change_phone(self, phone_old: Phone, phone_new: Phone):
        index = self.__check_phone(phone_old)
        if index >= 0:
            self.phones.pop(index)
            self.phones.insert(index, phone_new)
            return f"Phone {phone_old.phone} success change to phone {phone_new.phone}"
        return f"Phone {phone_old.phone} dos not in phones"

    def delete_phone(self, phone: Phone):
        index = self.__check_phone(phone)
        if index >= 0:
            self.phones.pop(index)
            return f"Phone {phone.phone} was deleted"
        return f"Phone {phone.phone} dos not in phones"

    def __check_phone(self, phone: Phone) -> int | None:
        for i, p in enumerate(self.phones):
            if p.phone == phone.phone:
                return i
        return None

    def __repr__(self) -> str:
        return f"{self.name.name} : {', '.join([p.phone for p in self.phones])} : {self.birthday.birthday} ({self.days_to_birthday(self.birthday.birthday)})"


class AddressBook(UserDict):
    file_name = "data.bin"

    def add_record(self, record: Record):
        self.data[record.name.name] = record

    def iterator(self, N=None):
        start = 0
        while True:
            if N:
                result = list(self.data.values())[start: start + N]
            else:
                result = list(self.data.values())[start:]
                return result
            if not result:
                break
            yield result
            start += N

    def save_data(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)

    def load_data(self, filename):
        with open(filename, "rb") as fh:
            data = pickle.load(fh)
        self.data = data

    def search(self, user_data: str):
        finder = []
        for k, v in self.data.items():
            if k == user_data or re.findall(user_data, str(v)):
                finder.append(self.data[k])
        return finder

    def __repr__(self):
        return str(self.data)


if __name__ == "__main__":
    ab = AddressBook()

    name1 = Name("Anton")
    phone1 = Phone("1234")
    bd1 = Birthday("2002-04-11")
    name2 = Name("Alisa")
    phone2 = Phone("1111")
    bd2 = Birthday("2001-1-13")
    rec1 = Record(name1, phone1, bd1)
    rec2 = Record(name2, phone2, bd2)
    ab.add_record(rec1)
    ab.add_record(rec2)
    # print(ab)
    print(ab.search("1234"))
    print(ab.search("Alisa"))

    # ab.save_data('phone.bin')

    # paginator = ab.iterator(1)
    # for i in paginator:
    #     print(i)
    #     input('Press any button')
