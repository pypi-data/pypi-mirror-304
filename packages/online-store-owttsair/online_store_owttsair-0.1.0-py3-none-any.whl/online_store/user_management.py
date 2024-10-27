class UserManager:
    def __init__(self):
        self.accounts = dict()

    def add_user(self, user_id, user_data):
        if user_id in self.accounts:
            print("Клиент с ID "+str(user_id)+" уже существует")
        else:
            self.accounts[user_id] = user_data
            print("Клиент с ID "+str(user_id)+" добавлен")

    def remove_user(self, user_id):
        if user_id not in self.accounts:
            print("Клиент с ID "+str(user_id)+" не найден")
        else:
            del self.accounts[user_id]
            print("Клиент с ID " + str(user_id) + " удален")

    def update_user(self, user_id, user_data):
        if user_id not in self.accounts:
            print("Клиент с ID "+str(user_id)+" не найден")
        else:
            self.accounts[user_id] = user_data
            print("Данные клиента с ID " + str(user_id) + " обновлены")

    def find_user(self, user_id):
        if user_id not in self.accounts:
            return("Клиент с ID " + str(user_id) + " не найден")
        else:
            p = dict()
            p[user_id] = self.accounts[user_id]
            return p