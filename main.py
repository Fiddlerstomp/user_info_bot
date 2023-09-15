from os import getenv
import telebot
import json

BOT_KEY = getenv('USER_BOT')
bot = telebot.TeleBot(BOT_KEY)


class User:
    def __init__(self, user_id, user_name, user_first, user_last):
        self.id = user_id
        self.name = user_name
        self.first = user_first
        self.last = user_last


class Instance:
    def __init__(self):
        self.users = []
        self.known_users_id = set()
        with open('users.json', 'r', encoding='utf-8') as file:
            users_json = json.load(file)
        for user in users_json:
            new_user = User(user['id'], user['name'], user['first'], user['last'])
            self.users.append(new_user)
            self.known_users_id.add(user['id'])
        print(type(self.users))

    def add_user(self, user):
        self.users.append(user)
        self.known_users_id.add(user.id)
        self.record_data()

    def record_data(self):
        json_users = []
        for user in self.users:
            json_users.append(user.__dict__)
        with open('users.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_users, indent=2))


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in instance.known_users_id:
        new_user = User(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
        instance.add_user(new_user)
        print('new user')


if __name__ == '__main__':
    instance = Instance()


bot.infinity_polling()
