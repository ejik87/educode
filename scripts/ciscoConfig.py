from netmiko import ConnectHandler


auth_filename = 'auth.txt'  # Файл с аутентификационными данными
hosts_filename = 'hosts.txt'  # Имя файла с перечнем IP адресов целевых коммутаторов.
# cmd_filename = 'cisco_commands.txt'


def main():

    try:
        with open(auth_filename, 'r') as auth_file:
            usr, passwd = auth_file.read().splitlines()
    except (FileNotFoundError, ValueError):  # Если файл не найдёт, или он пустой то вводим в ручную
        usr = input('Enter Username: ')  # Имя пользователя для авторизации в коммутаторах.
        passwd = input('Enter Password: ')  # Соответственно пароль для коммутов.

    try:
        with open(hosts_filename, 'r') as hosts_file:
            sw = hosts_file.read().splitlines()
    except (FileNotFoundError, ValueError):  # Если файл не найдёт, или он пустой то вводим в ручную
        sw = input('hosts.txt No found!\n Enter cisco ip address: ').split(' ,;')

    cmd_exec(usr, passwd, sw)


def cmd_exec(user, passwd, hosts):
    # try:
    #     with open(cmd_filename, 'r') as commands_file:
    #         commands = commands_file.read().splitlines()
    # except (FileNotFoundError, ValueError):
    #     commands = input('cisco_commands.txt No found!\n Enter commands for switch: ').split(' ,;')

    for host in hosts:
        cisco = {
            # "device_type": "cisco_ios",
            "device_type": "linux",  # Для отладки на линухах.
            "host": host,
            "username": user,
            "password": passwd,
        }
        switch_connect = ConnectHandler(**cisco)  # считывание пары ключ-значение.
        output = switch_connect.send_config_from_file('cisco_commands.txt')  # отправка конфигурации из указанного файла
        # switch_connect.send_command()
        # output = switch_connect.send_config_set(commands)

        print(f"\n\n--------- Device {cisco['host']} ---------")
        print(output)
        print("--------- End ---------")

        switch_connect.disconnect()  # Закрытие соединения.
        user_check = input('Press Enter for continue. Or type "Exit". ')
        if user_check:
            break
            
        # ios_config = switch_connect.save_config(f'{cisco["host"]}.ios')  # сохранить текущую конфигурацию в режиме startup - config;
        # print(ios_config)


if __name__ == "__main__":
    main()
