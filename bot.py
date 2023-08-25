import typing
from address_book import AddressBook, Record

PHONE_BOOK = AddressBook()


def input_error(func: typing.Callable) -> typing.Callable:

    def inner(*args: str, **kwargs: dict) -> str:
        try:
            return f"{func(*args, **kwargs)}"
        except (KeyError, ValueError, IndexError, TypeError) as error:
            return f"DECORATOR An error has occurred. Er: {error}"
    return inner


@input_error
def say_hello() -> str:
    return "How can I help you?"


@input_error
def add_user(name: str, phone_num: str, birthday: str = None) -> str:

    if name in PHONE_BOOK:
        PHONE_BOOK[name].add_phone(phone_num)
        return f"In phone book with user '{name}' added phone '{phone_num} in list phone'"
    else:
        record = Record(name, phone_num, birthday)
        PHONE_BOOK.add_record(record)
    return f"In phone book with user '{name}' added phone '{phone_num}'"


@input_error
def change_contact(name: str, old_phone: str, new_phone: str) -> str:

    if name not in PHONE_BOOK:
        raise ValueError(f"User '{name}' is not in phone book")
    elif old_phone not in (str(p.phone) for p in PHONE_BOOK[name].phones):
        raise ValueError(f"User '{name}' do not have a number {old_phone}")
    PHONE_BOOK[name].edit_phone(old_phone, new_phone)
    return f"In phone book changed phone number '{old_phone}' of user '{name}' to '{new_phone}'"


@input_error
def to_delete(name, phone):

    if name not in PHONE_BOOK:
        raise ValueError(f"User '{name}' is not in phone book")
    elif phone not in (str(p.phone) for p in PHONE_BOOK[name].phones):
        raise ValueError(f"User '{name}' do not have a number {phone}")

    PHONE_BOOK[name].remove_phone(phone)
    print("ITOG", PHONE_BOOK[name])
    if len(PHONE_BOOK[name].phones) == 0:
        PHONE_BOOK.pop(name)

    return f"In phone book deleted phone number '{phone}' of user '{name}"


@input_error
def get_phone(name: str) -> str:

    if name not in PHONE_BOOK:
        raise ValueError(f"User '{name}' is not in phone book.")
    return f"Target phone number for user '{name}' is '{', '.join(str(p.phone) for p in PHONE_BOOK[name].phones)}'"


@input_error
def show_all(N=None) -> str:
    if not PHONE_BOOK:
        return "The phone book is empty."

    if N:
        paginator = PHONE_BOOK.iterator(int(N))
    elif N == None:
        paginator = PHONE_BOOK.iterator()
        for iteration in paginator:
            for name in iteration:
                print(name)
            return
    for iteration in paginator:
        for name in iteration:
            print(name)
        input('Press any button')


@input_error
def search(search_str):
    return PHONE_BOOK.search_coincidences(search_str)


@input_error
def to_close() -> str:
    return "Good bye!"


def default_handler(*args) -> str:
    return f"I don't know such a command"


COMANDS: dict[str, typing.Callable] = {
    'hello': say_hello,
    'add': add_user,
    'change': change_contact,
    'phone': get_phone,
    'show all': show_all,
    'search': search,
    'close': to_close,
    'delete': to_delete,
}


def get_handler(comand: str) -> typing.Callable:
    return COMANDS.get(comand, default_handler)


def main() -> None:
    print("I'm a Bot")

    try:
        PHONE_BOOK.load_data("phone.bin")
    except FileNotFoundError:
        print("file phone.bin do not exist!")

    while True:
        user_input = input("Please input a command: ").lower()

        if user_input in ["good bye", "close", "exit"]:
            handler = get_handler('close')
            request_data = user_input.replace('good bye', "").replace(
                "close", "").replace("exit", "").split()
            print(handler(*request_data))
            PHONE_BOOK.save_data("phone.bin")
            break

        elif 'show all' in user_input:
            handler = get_handler('show all')
            request_data = user_input.replace('show all', "").split()
            handler(*request_data)
            continue

        list_of_request = user_input.strip().split(' ')
        comand = list_of_request[0]
        request_data = list_of_request[1:]

        print("RECVEST DATA", request_data)

        try:
            handler = get_handler(comand)
            print(handler(*request_data))
        except KeyError as error:
            print(f"I don't know such a command.Er: {error}")


if __name__ == "__main__":
    main()
