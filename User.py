class User:
    # Constructor for User object, initializing six properties of the object
    def __init__(self, user_id, first_name, last_name, age, city, phone_number):
        self.__user_id = int(user_id)
        self.__first_name = str(first_name)
        self.__last_name = str(last_name)
        self.__age = int(age)
        self.__city = str(city)
        self.__phone_number = str(phone_number)

    # Accessors
    def get_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_age(self):
        return self.__age

    def get_city(self):
        return self.__city

    def get_phone_num(self):
        return self.__phone_number

    # Mutators
    def set_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_age(self, age):
        self.__age = age

    def set_city(self, city):
        self.__city = city

    def set_phone_num(self, phone_number):
        self.__phone_number = phone_number

    # User string function to display properties when called
    def __str__(self):
        return (f"User ID: {int(self.__user_id)}\n"
                f"{str(self.__first_name)} {str(self.__last_name)}\n"
                f"{str(self.__city)}\n"  
                f"{int(self.__age)}\n"
                f"{str(self.__phone_number)}\n"  
                f"------------")

    # User dictionary function to return a python dictionary object holding user properties in key/value pairs
    def __dict__(self):
        return {"id": self.__user_id, "first_name": str(self.__first_name), "last_name": str(self.__last_name),
                "age": str(self.__age), "city": self.__city, "phone_number": self.__phone_number}
