from collections import UserDict
from datetime import datetime
import pickle
import re


class Field():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phonenumber: str):
        if not phonenumber.isnumeric():
            raise ValueError('Phone contains unsupported characters')
        self.__phone = phonenumber

    def __str__(self):
        return str(self.phone)


class Birthday:
    def __init__(self, birthday: str = None):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        if type(birthday) == tuple:
            raise ValueError(f'Birthday can not be in 2 dates')
        if birthday:
            try:
                datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Data must be yyyy-mm-dd')
        self.__birthday = birthday


class Record():
    def __init__(self, name: Name, phone=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.phones = []
        if phone:
            self.add_phone(phone)
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone: str):
        index = self.find_phone_index(phone)
        if index is not None:
            self.phones.pop(index)

    def edit_phone(self, old_phone: str, new_phone: str):
        index = self.find_phone_index(old_phone)
        if index is not None:
            self.phones[index] = Phone(new_phone)

    def find_phone_index(self, old_phone: str):
        for index, phone in enumerate(self.phones):
            if phone.phone == old_phone:
                return index
        return None

    def days_to_birthday(self):
        # 2023-08-24
        if self.birthday.birthday:
            datetime_of_birthday = datetime.strptime(
                self.birthday.birthday, '%Y-%m-%d')

            month_of_birthday = datetime_of_birthday.month

            date_of_today = datetime.now().date()
            this_year = date_of_today.year
            this_month = date_of_today.month

            # если месяц д.р. уже прошел то сдвигаем на год вперед, если только будет оставляем єтот год
            if this_month < month_of_birthday:
                target_birthday_day = datetime_of_birthday.replace(
                    year=this_year)
            else:
                target_birthday_day = datetime_of_birthday.replace(
                    year=this_year + 1)

            time_delta = target_birthday_day.date() - date_of_today

            return time_delta.days
        return None

    def __repr__(self) -> str:
        return f"{self.name}: {', '.join(str(p.phone) for p in self.phones)}  was_born: {self.birthday.birthday}  days_to_birthday: {self.days_to_birthday()}\n"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, N=None):
        start = 0
        while True:
            if N:
                result = list(self.data.values())[start:start+N]
            else:
                result = list(self.data.values())[start:]
                yield result
            if not result:
                break
            yield result
            start += N

    def load_data(self, filename):
        with open(filename, "rb") as file:
            try:
                data = pickle.load(file)
            # если вдруг что-то с файлом загрузки то присваиваем пустой словарь
            except EOFError:
                print("file is empty")
                data = {}
        self.data = data

    def save_data(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def search_coincidences(self, search_str: str):
        finder = []

        # self.data - это словарь где ключ - это имя, а значение это запись Record
        for key, value in self.data.items():

            searching_in_ph_list = ""
            for phone in value.phones:
                searching_in_ph_list += str(phone) + ";"

            if re.findall(search_str, key) or re.findall(search_str, searching_in_ph_list):
                finder.append(self.data[key])
        return finder

    def __repr__(self):
        return str(self.data)


if __name__ == '__main__':
    new_contact_1 = Record("Nina", "322223322")
    new_contact_2 = Record("Olga", "1488322")
    new_contact_3 = Record("Kizaru", "666")
    new_contact_4 = Record("Gleb", "322", "1993-02-27")
    new_phone_book = AddressBook()
    new_phone_book.add_record(new_contact_1)
    new_phone_book.add_record(new_contact_2)
    new_phone_book.add_record(new_contact_3)
    new_phone_book.add_record(new_contact_4)
    print(new_phone_book)
    print(datetime.now())
