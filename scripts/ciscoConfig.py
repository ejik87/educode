from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
from os import mkdir, path
from datetime import datetime


auth_filename = 'auth.txt'  # Файл с аутентификационными данными
hosts_filename = 'hosts.txt'  # Имя файла с перечнем IP адресов целевых коммутаторов.
cmd_filename = 'commands.txt'


def print_banner():
    print('''
    -----------------------------------------------------------------------
    |                   Cisco automation configurator                     |
    |                      You can use config files                       |
    |            Credentials: user and password; auth.txt file            |
    |                 IP of target devices; hosts.txt file                |
    |          Device configuration commands; commands.txt file           |
    |_____________________________________________________________________|
    ''')


def get_pages(ssh, command='sh run'):
    """
    # Функция получения многостраничного вывода
    """
    # ssh.enable()
    prompt = ssh.find_prompt()
    ssh.send_command("terminal length 100")
    ssh.write_channel(f"{command}\n")
    output = ""
    while True:
        try:
            page = ssh.read_until_pattern(f"More|{prompt}")
            if "More" in page:
                ssh.write_channel(" ")
            elif prompt in output:
                break
        except NetmikoTimeoutException:
            break
    return output


def get_config(ssh, command='sh run'):
    """
    # Функция получения конфига одной страницей
    """
    # ssh.enable()
    ssh.send_command("terminal length 0")
    output = ssh.send_command(f"{command}")
    return output


def main():
    print_banner()
    try:
        with open(auth_filename, 'r') as auth_file:
            usr, passwd = auth_file.read().splitlines()
    except (FileNotFoundError, ValueError):  # Если файл не найден, или он пустой то вводим в ручную
        usr = input('Enter Username: ')  # Имя пользователя для авторизации в коммутаторах.
        passwd = getpass('Enter Password: ')  # Соответственно пароль для коммутов.
    try:
        with open(hosts_filename, 'r') as hosts_file:
            sw = hosts_file.read().splitlines()
    except (FileNotFoundError, ValueError):  # Если файл не найден, или он пустой то вводим в ручную
        sw = input('hosts.txt No found!\n Enter cisco ip address: ').split(' ,;')
    # try:
    #     with open(cmd_filename, 'r') as commands_file:
    #         commands = commands_file.read().splitlines()
    # except (FileNotFoundError, ValueError):
    #     commands = input('commands.txt No found!\n Enter commands for switch: ').split(' ,;')
    cmd_exec(usr, passwd, sw)


def get_time_now():
    return datetime.now().strftime('%Y.%m.%d_%H.%M')


def cmd_exec(user, passwd, hosts):
    """
    # Функция выполнения запросов к устройстсву
    """
    global switch_connect
    for host in hosts:
        if not host or host[0] in '!#':  # Если попалась пустая строка или #, пропуск.
            continue
        cisco = {
            "device_type": "cisco_ios",
            "host": host,
            "username": user,
            "password": passwd,
            "secret": passwd,
            "session_log": "session_log.log",
            "session_log_record_writes": True,
            "session_log_file_mode": "append",
            # "encoding": "ascii",
        }
        print(f'====== Cоединяемся с {host} ======')
        try:
            switch_connect = ConnectHandler(**cisco)  # считывание пары ключ-значение.
        except NetmikoAuthenticationException as error:
            print('========ERROR=========', '\nНеверные данные аутентификации: ' + host)
            print(error, '\n=========END=========\n')
            continue
        except NetmikoTimeoutException as error:
            print('========ERROR=========', '\nНет ответа от устройства: ' + host)
            print(error, '\n=========END=========\n')
            continue
        except SSHException as error:
            print('========ERROR=========', '\nSSH недоступен. Проверьте включен ли SSH? ' + host)
            print(error, '=========END=========\n')
            continue
        except Exception as error:
            print('\n========ERROR=========', error, '\n=========END=========\n')
            user_check = input('Press Enter for continue. Or type "Exit". ')  # Для контроля ошибок
            if user_check:
                break

        switch_connect.enable()  # Перейти в режим enable
        prompt = switch_connect.find_prompt().rstrip('#')

        if not path.exists('./backup_cfg/'):
            mkdir('backup_cfg')
        with open(f'./backup_cfg/{prompt}_{get_time_now()}backup.ios', 'w') as backup_cfg:
            print(f'----------- Save backUp configuration ------------\n| ./backup_cfg/{prompt}_backup.ios')
            backup_cfg.write(get_config(switch_connect, 'sh run'))  # Сохраняем конфигу перед изменениями.
            print('----------- End save backUp configuration ------------')

        output = switch_connect.send_config_from_file(cmd_filename)  # отправка конфигурации из указанного файла
        # switch_connect.send_command()
        # output = switch_connect.send_config_set(commands)
        if not path.exists('./output/'):
            mkdir('output')
        with open(f'./output/{prompt}_exec_{get_time_now()}.txt', 'w') as output_file:
            print(f'----------- Execute log ------------\n| ./output/{prompt}_exec.txt')
            output_file.write(output)  # Сохраняем вывод в файл.

        print(f"\n\n--------- Device {cisco['host']} ---------")
        print(output)  # Вывести результаты выполнения команд
        print("--------- End ---------\n\n")

        # if not path.exists('./new_cfg/'):
        #     mkdir('new_cfg')
        # with open(f'./new_cfg/{prompt}.ios', 'w') as new_cfg:
        #     print(f'----------- Save New configuration ------------\n| ./new_cfg/{prompt}.ios')
        #     new_cfg.write(get_config(switch_connect, 'sh run'))  # Сохраняем конфигу после изменений.
        #     print('----------- End save New configuration ------------')

        # ssh.exit_enable_mode()  # Выйти из режима enable
        switch_connect.disconnect()  # Закрытие соединения.
        # user_check = input('Press Enter for continue. Or type "Exit". ')  # Для контроля ошибок
        # if user_check:
        #     break


'''
    В netmiko есть несколько способов отправки команд:
    • send_command - отправить одну команду
    • send_config_set - отправить список команд или команду в конфигурационном режиме
    • send_config_from_file - отправить команды из файла (использует внутри метод
    send_config_set)
    • send_command_timing - отправить команду и подождать вывод на основании таймера
    =============================================================================
    Метод send_config_from_file отправляет команды из указанного файла
     в конфигурационный режим.    
        Метод работает таким образом:
        • заходит в конфигурационный режим,
        • затем передает все команды
        • и выходит из конфигурационного режима
        • в зависимости от типа устройства, выхода из конфигурационного
         режима может и не быть. Например, для IOS-XR выхода
          не будет, так как сначала надо закоммитить изменения
    
    Дополнительные методы
    Кроме перечисленных методов для отправки команд, netmiko поддерживает такие методы:
    • config_mode - перейти в режим конфигурации: ssh.config_mode()
    • exit_config_mode - выйти из режима конфигурации: ssh.exit_config_mode()
    • check_config_mode - проверить, находится ли netmiko в режиме конфигурации 
      (возвращает True, если в режиме конфигурации, и False - если нет): ssh.check_config_mode()
    • find_prompt - возвращает текущее приглашение устройства: ssh.find_prompt()
    • commit - выполнить commit на IOS-XR и Juniper: ssh.commit()
    • disconnect - завершить соединение SSH
'''

if __name__ == "__main__":
    main()
