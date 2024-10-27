class UserManager:
    def __init__(self,users={}):
        self.users=users
    def add_user(self,user_id,data):
        if user_id in self.users.keys():
            print(f'Клиент с id  {user_id} уже в списке')
        else:
            self.users[user_id]=data
            print(f'Клиент с id {user_id} добавлен')
    def remove_user(self,user_id):
        if user_id in self.users.keys():
            del self.users[user_id]
            print(f'Клиент с id {user_id} удален')
        else:
            print(f'Клиент с id {user_id} не найден')
    def update_user(self,user_id,user_data):
        if user_id not in self.users.keys():
            print(f'Клиент с id {user_id} не найден')
        else:
            self.users[user_id]=user_data
            print(f'Данные клиента с if {user_id} обновлены')
    def find_user(self,user_id):
        if user_id in self.users:
            return {user_id:self.users[user_id]}
        else:
            print((f'Клиент с id {user_id} не найден'))
            return
