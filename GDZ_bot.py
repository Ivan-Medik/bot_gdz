import telebot

TOKEN = "998715458:AAGxzlpd1l9rg4bIMesIYobd9Hn-rHkyTM0"

bot = telebot.TeleBot(TOKEN)

bot.run()

number_class_list = []
book_list = []
page_list = []
publisher_list = []

@bot.message_handler(commands = ["my_name"])
def name_user_message(message):
    text_for_user = bot.reply_to(message, "Как вас зовут?")
    bot.register_next_step_handler(text_for_user, otvet_user)
    print("[+]Сообщение name_user_message доставлено.")
def otvet_user(message):
    name = message.text
    file_with_name = open("name_user.txt", "w")
    file_with_name.write(name)
    file_with_name.close()
    text = "Информация успешно обновлена!"
    bot.send_message(message.chat.id, text)
    print("[+]Имя обновлено.")

@bot.message_handler(commands = ["start","menu"])
def start_message(message):
    with open(r"name_user.txt", "r") as file:
        for name_user in file:
            name = name_user
    text_message = "Привет " + name + " !\nЯ гдз бот.\n1.Выбери класс - /class\n2.Выбери предмет - /lesson\n3.Выбери издателя - /publisher\n4.Выбери страницу/номер упражнения - /page\n\nРешение - /decision"
    bot.send_message(message.chat.id, text_message)
    print("[+]Сообщение start_message доставлено.")

@bot.message_handler(commands = ["publisher"])
def publisher_message(message):
    text_message = bot.reply_to(message, "Введи издателя с большой буквы:")
    bot.register_next_step_handler(text_message, publisher_user)
    print("[+]Сообщение publisher_message доставлено.")
def publisher_user(message):
    publisher = str(message.text)
    publisher_list.clear()
    publisher_list.append(publisher)
    text_message = "Информация успешно обновлена!\nМеню - /menu"
    bot.send_message(message.chat.id, text_message)
    print("[+]Сообщение publisher_user доставлено.")

@bot.message_handler(commands = ["lesson"])
def lesson_message(message):
    text_message = bot.reply_to(message, "Введи предмет с большой буквы:\n(если нужна рабочая тетрадь, указывайте это после предмета - (рб)")
    bot.register_next_step_handler(text_message, lesson_user)
    print("[+]Сообщение lesson_message доставлено.")
def lesson_user(message):
    book = message.text
    book_list.clear()
    book_list.append(book)
    text_message = "Информация успешно обновлена!\nМеню - /menu"
    bot.send_message(message.chat.id, text_message)
    print("[+]Сообщение lesson_user доставлено.")

@bot.message_handler(commands = ["class"])
def class_message(message):
    text_message = bot.reply_to(message, "Введи номер класса без букв:")
    bot.register_next_step_handler(text_message, number_class)
    print("[+]Сообщение class_message доставлено.")
def number_class(message):
    number_class = message.text
    number_class_list.clear()
    number_class_list.append(number_class)
    text_message = "Информация успешно обновлена!\nМеню - /menu"
    bot.send_message(message.chat.id, text_message)
    print("[+]Сообщение number_class доставлено.")

@bot.message_handler(commands = ["page"])
def page_message(message):
    text_message = bot.reply_to(message, "Введи номер страницы:")
    bot.register_next_step_handler(text_message, page_in_book)
    print("[+]Сообщение number_class доставлено.")
def page_in_book(message):
    page = int(message.text)
    if page <= int("1100"):
        page_list.clear()
        page_list.append(page)
        text_message = "Информация успешно обновлена!\nМеню - /menu"
        bot.send_message(message.chat.id, text_message)
        print("[+]Сообщение page_in_book доставлено.")
    else:
        text_message = "Упс!Кажется страница превысила допустимое значение. Если это было сделано не специально, то напишит моему создателю - ...\nМеню - /menu"
        bot.send_message(message.chat.id, text_message)
        print("[+]Сообщение page_in_book_negativ доставлено.")

@bot.message_handler(commands = ["decision"])
def decision_message(message):
    if int(number_class_list[0]) == int("7"):
        class_number = number_class_list[0]
        number_class_list.clear()
    elif int(number_class_list[0]) == int("8"):
        class_number = number_class_list[0]
        if book_list[0] == str("Геометрия"):
            book = "geometria"
            if publisher_list[0] == str("Атанасян"):
                publisher = "atanasyan-8"
                page_in_book = (str(page_list[0]) + "-task")
                page_list.clear()
        elif book_list[0] == str("Алгебра"):
            book = "algebra"
            if publisher_list[0] == str("Макарычев"):
                publisher = "makarychev-8"
                page_in_book = (str(page_list[0]) + "-nom")
                page_list.clear()
        elif book_list[0] == str("Английский"):
            book = "english"
            book_list.clear()
            if publisher_list[0] == str("Ваулина"):
                publisher = "reshebnik-spotlight-8-angliyskiy-v-fokuse-vaulina-yu-e"
                page_in_book = page_list[0]
                page_list.clear()
        elif book_list[0] == str("Английский(рб)"):
            book = "english"
            rab_book = "workbook"
    elif int(number_class_list[0]) == int("9"):
        class_number = number_class_list[0]
        number_class_list.clear()
    text_sms = "Лови)\nhttps://gdz.ru/class-" + str(class_number) + "/" + book + "/" + publisher + "/" + str(page_in_book)
    bot.send_message(message.chat.id, text_sms)
    print("[+]Сообщение с решением доставлено.")

print("Бот исправен и готов к использованию.")

bot.polling()
