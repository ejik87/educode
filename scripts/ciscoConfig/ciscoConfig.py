from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
from os import mkdir, path
from datetime import datetime
import functools

hosts_filename = 'hosts.txt'  # Имя файла с перечнем IP адресов целевых коммутаторов.
auth_filename = 'auth.txt'  # Файл с аутентификационными данными
cmd_filename = 'commands.txt'


BACKUP_CONF = False  # Флаг для сохранения резервной копии конфига перед выполнением конфигурации
SAVE_CONF = False  # Флаг для сохранения конфига в файл
TRY_COUNT = 3  # Колличество повторов при выполнении запросов


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


def get_time_now():
    return datetime.now().strftime('%Y.%m.%d_%H.%M')


def retry_func(func):
    """ # декоратор для нескольких попыток выполнения кода"""
    def wrapper(*args, **kwargs):
        for _ in range(TRY_COUNT):
            if func(*args, **kwargs):
                return func(*args, **kwargs)
            else:
                continue

    return wrapper


def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
                if value:
                    return value
                else:
                    continue
        return wrapper_repeat
    return decorator_repeat


def get_credential(file):
    try:
        with open(file, 'r') as auth_file:
            username, password = auth_file.read().splitlines()
    except (FileNotFoundError, ValueError):  # Если файл не найден, или он пустой то вводим в ручную
        print(f'{file} Not found! Enter credential >>>\n')
        username = input('Enter Username: ')  # Имя пользователя для авторизации в коммутаторах.
        password = getpass('Enter Password: ')  # Соответственно пароль для коммутов.
    return [username, password]


def get_hosts(file):
    try:
        with open(file, 'r') as hosts_file:
            hosts = hosts_file.read().splitlines()
    except (FileNotFoundError, ValueError):  # Если файл не найден, или он пустой то вводим в ручную
        hosts = input(f'{file} Not found!\n Enter ip address: ').split(' ,;')
    return hosts


def get_commands(file):
    try:
        with open(file, 'r') as commands_file:
            commands = commands_file.read().splitlines()
    except (FileNotFoundError, ValueError):
        commands = input(f'{file} Not found!\n Enter commands for switch: ').split(' ,;')
    return commands


def set_cfg_flag():
    """
    Установка флагов для сохранения конфигураций
    """
    global BACKUP_CONF, SAVE_CONF
    bkp_cfg_quest = input('Сохранить резервную копию конфигурации?: ')
    if bkp_cfg_quest.lower() in ['yes', 'y', 'да', 'д']:
        BACKUP_CONF = True
    else:
        BACKUP_CONF = False
    sv_cfg_quest = input('Сохранить итоговую конфигурацию устройства?: ')
    if sv_cfg_quest.lower() in ['yes', 'y', 'да', 'д']:
        SAVE_CONF = True
    else:
        SAVE_CONF = False


class CiscoConfig:

    def __init__(self, user, pwd, host):
        self.host = host
        self.cmd = []
        self.username = user
        self.password = pwd
        self.ssh = None
        self.prompt = None

    def get_pages(self, command='sh run'):
        """
        # Функция получения многостраничного вывода
        """
        # ssh.enable()
        prompt = self.ssh.find_prompt()
        self.ssh.send_command("terminal length 100")
        self.ssh.write_channel(f"{command}\n")
        output = ""
        while True:
            try:
                page = self.ssh.read_until_pattern(f"More|{prompt}")
                if "More" in page:
                    self.ssh.write_channel(" ")
                elif prompt in output:
                    break
            except NetmikoTimeoutException:
                break
        return output

    def get_config(self, command='sh run'):
        """
        # Функция получения конфига одной страницей
        """
        # ssh.enable()
        self.ssh.send_command("terminal length 0")
        output = self.ssh.send_command(f"{command}")
        return output

    @repeat(TRY_COUNT)
    def init_connection(self):
        cisco = {
            "device_type": "cisco_ios",
            "host": self.host,
            "username": self.username,
            "password": self.password,
            "secret": self.password,
            "session_log": "session_log.log",
            "session_log_record_writes": True,
            "session_log_file_mode": "append",
            # "encoding": "ascii",
        }
        try:
            print(f'====== Cоединяемся с {self.host} ======')
            self.ssh = ConnectHandler(**cisco)  # считывание пары ключ-значение.
            self.prompt = self.ssh.find_prompt().rstrip('>#')
            return True

        except NetmikoAuthenticationException as error:
            print('========ERROR=========', '\nНеверные данные аутентификации:', self.host)
            print(error, '\n=========END=========\n')
            return False
        except NetmikoTimeoutException as error:
            print('========ERROR=========', '\nНет ответа от устройства:', self.host)
            print(error, '\n=========END=========\n')
            return False
        except SSHException as error:
            print('========ERROR=========', '\nSSH недоступен. Проверьте включен ли SSH?', self.host)
            print(error, '\n=========END=========\n')
            return False


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


def main():
    print_banner()
    '''# Загружаем данные для работы'''
    username, password = get_credential(auth_filename)
    hosts = get_hosts(hosts_filename)
    commands = get_commands(cmd_filename)
    ''' Установка флагов для сохранения конфигураций '''
    set_cfg_flag()
    ''' ============================================ '''

    """ # выполнения запросов к устройстсву """
    for host in hosts:
        if not host or host[0] in '!#':  # Если попалась пустая строка или ! #, пропуск.
            continue
        cisco_job = CiscoConfig(username, password, host)
        cisco_job.init_connection()
        if not cisco_job.ssh:
            print(f"\n\n--------- Device IP: {cisco_job.host} Not Connected ---------")
            continue
        cisco_job.ssh.enable()  # Перейти в режим enable

        """ ========= Создаём резервную копию конфигурации =========== """
        if BACKUP_CONF:
            backup_path = 'backup_cfg'
            if not path.exists(f'./{backup_path}/'):
                mkdir(backup_path)
            with open(f'./{backup_path}/{cisco_job.prompt}_{get_time_now()}backup.ios', 'w') as backup_cfg:
                print(f'----------- Save backUp configuration ------------\n|\
                 ./{backup_path}/{cisco_job.prompt}_backup.ios')
                backup_cfg.write(cisco_job.get_config())  # Сохраняем конфигу перед изменениями.
                print('----------- End save backUp configuration ------------')
        """============================================================"""

        print(f"\n\n--------- Device {cisco_job.prompt} IP: {cisco_job.host} ---------")
        if not cisco_job.ssh.check_config_mode():
            cisco_job.ssh.config_mode()
        output_dict = dict()
        for command in commands:
            output_dict[command] = cisco_job.ssh.send_command(command)
        # output = switch_connect.send_config_from_file(cmd_filename)  # отправка конфигурации из указанного файла
        # output = switch_connect.send_config_set(commands)

        if cisco_job.ssh.check_config_mode():
            cisco_job.ssh.exit_config_mode()

        """ =============== Создаём текущую копию конфигурации ============== """
        if SAVE_CONF:
            cfg_dir_path = 'new_cfg'
            if not path.exists(f'./{cfg_dir_path}/'):
                mkdir(cfg_dir_path)
            with open(f'./{cfg_dir_path}/{cisco_job.prompt}.ios', 'w') as new_cfg:
                print(f'----------- Save New configuration ------------\n| ./{cfg_dir_path}/{cisco_job.prompt}.ios')
                new_cfg.write(f'{get_time_now()}\n{cisco_job.get_config()}')  # Сохраняем конфигу после изменений.
                # new_cfg.write(cisco_job.get_config())  # Сохраняем конфигу после изменений.
                print('----------- End save New configuration ------------')
        """==================================================================="""

        # cisco_job.ssh.exit_enable_mode()  # Выйти из режима enable
        cisco_job.ssh.disconnect()  # Закрытие соединения.

        """ ===== Вывод ответов от устройства ===== """
        for key, val in output_dict.items():
            print(f'\n>>>{cisco_job.prompt}# {key}:\n{val}', end='\n')  # Вывести результаты выполнения команд

        """ Записываем лог работы """
        # out_path = 'output'
        # if not path.exists(f'./{out_path}/'):
        #     mkdir(out_path)
        # with open(f'./{out_path}/{cisco_job.prompt}_exec_{get_time_now()}.txt', 'w') as output_file:
        #     print(f'----------- Execute log ------------\n| ./{out_path}/{cisco_job.prompt}_exec.txt')
        #     output_file.write(output)  # Сохраняем вывод в файл.
        print("\n--------- End ---------\n\n")


if __name__ == "__main__":
    main()
