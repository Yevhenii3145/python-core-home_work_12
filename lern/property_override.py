# Якщо батьківcький клас має приватні атрибути
# та доступ до них реалізован через проперті
# а ми бажаємо іх перевизначити у потомках
class Private:
    def __init__(self, value):
        # ми можемо так
        self.__value = value
        # або через проперти
        # self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

# для застосування правил встановлення значення для нашого класу
# инит обов'язковий  та завикористанням нашего проперти!!!
# super().__init__(value)  не застосуе для батьківського __value наш setter

# Варіант ПЕРШИЙ - наші проперті викликають проперті батька через супер
# super(MySuper, MySuper).value.fget(self)
# super(MySuper, MySuper).value.fset(self, value)


class MySuper(Private):
    def __init__(self, value):
        self.value = value

    @property
    def value(self) -> str:
        temp = super(MySuper, MySuper).value.fget(self)
        return f"MySuper {temp}"

    @value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise Exception(f"'{value}' is not a valid")
        super(MySuper, MySuper).value.fset(self, value)

# Варіант ДРУГИЙ - наші проперті викликають проперті батька явно
# Private.value.fget(self)
# Private.value.fset(self, value)


class MySetterGetter(Private):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        temp = Private.value.fget(self)
        return f"MySetterGetter : {temp}"

    @value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise Exception(f"'{value}' is not a valid")
        Private.value.fset(self, value)

# якщо нам потрібно ЛИШЕ перевизначити метод СЕТТЕР
# то щоб не створювати зайвий проперти на читання
# ми явно вкажемо новий setter
# Варіант ТРЕТІЙ  перевизначимо проперті самого батька
# за допомогою декоратора @Private.value.setter
# та Private.value.fset(self, value)


class MySetter(Private):
    def __init__(self, value):
        self.value = value

    @Private.value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise Exception(f"'{value}' is not a valid")
        Private.value.fset(self, value)


m = MySuper(123)
print(m.value)
m.value = 234
print(m.value)
m = MySetterGetter(345)
print(m.value)
m.value = 4567
print(m.value)
m = MySetter(567)
print(m.value)
m.value = 6789
print(m.value)
