class Contact_book:
    def __init__(self) -> None:
        self.user_name = ""
        self.user_phone = 0
        self.user_adress = ""

    def register_user(self):
        self.user_name = input()
        self.user_phone = input()
        self.user_adress = input()
        #comment