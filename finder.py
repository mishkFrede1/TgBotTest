from db_manager import Manager
manager = Manager()

user_text = (
    "##########################\n"
    "ID: {id}\n"
    "TELEGRAM_ID: {user_id}\n"
    "FIRST_NAME: {first_name}\n"
    "LAST_NAME: {last_name}\n"
    "AGE: {age}\n"
    "GENDER_FEMALE: {gender_female}\n"
    "ACCEPTED: {accepted}\n"
    "REJECTED: {rejected}\n"
    "##########################\n"
)

while True:
    print("----------------- DB FINDER -----------------")
    print("Список доступных команд:\n\n1)rejected - Все отклоненные пользователи\n2)accepted - Все принятые пользователи\n3)all - Все пользователи\n4)find - поиск по какому либо параметру\n")
    action = input("Введите команду: ")
    print("\n")

    match action:
        case "rejected":
            users = manager.all_rejected_users()
        case "accepted":
            users = manager.all_accepted_users()
        case "all":
            users = manager.all_users()
        case "find":
            print(
                "Список доступных параметров:\n\n"
                "1)id - ID записи (int)\n"
                "2)user_id - Telegram ID (int)\n"
                "3)first_name - Имя (str)\n"
                "4)last_name - Фамилия (str)\n"
                "5)age - Возраст (int)\n"
                "6)gender_female - Пол (bool)\n"
            )
            param_name = input("Введите название параметра: ")
            param_value = input("Введите значение параметра: ")

            if param_name == "gender_female":
                if param_value.lower() == "true" or param_value.lower() == "t":
                    param_value = True
                else:
                    param_value = False
            elif param_name == "id" or param_name == "user_id" or param_name == "age":
                param_value = int(param_value)

            users = manager.get_user_by_param(param_name, param_value)

    try:
        for user in users:
            print(user_text.format(
                id=user[0], 
                user_id=user[2], 
                first_name=user[3], 
                last_name=user[4], 
                age=user[5], 
                gender_female=user[6], 
                accepted=user[7], 
                rejected=user[8]
            ))
        input()
    except Exception as _ex:
        print("[ERROR]:", _ex)