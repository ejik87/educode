from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
from os import mkdir, path
from datetime import datetime
import functools
import logging


HOST_FILENAME = 'hosts.txt'  # Имя файла с перечнем IP адресов целевых коммутаторов.
AUTH_FILENAME = 'auth.txt'  # Файл с аутентификационными данными
CMD_FILENAME = 'commands.txt'
backup_conf = False  # Флаг для сохранения резервной копии конфига перед выполнением конфигурации
save_conf = False  # Флаг для сохранения конфига в файл
save_output = False  # Флаг сохранять вывод ответа на команды из консоли в файл
write_conf = False  # записывать новую конфигурацию в постоянную память устройства.
TRY_COUNT = 3  # Колличество повторов при выполнении запросов

fault_hosts = {}  # {host: error,}


def print_banner():
    print('''
    -----------------------------------------------------------------------
    |                   Cisco automation configurator                     |
    |                      You can use config files                       |
    |            Credentials: user and password; auth.txt file            |
    |                 IP of target devices; hosts.txt file                |
    |          Device configuration commands; commands.txt file           |
    |_____________________________________________________________________|''')


def get_time_now():
    return datetime.now().strftime('%Y.%m.%d_%H.%M')


""" ЛОГИРОВАНИЕ """
"""эта строка указывает, что лог-сообщения paramiko будут выводиться только если они уровня WARNING и выше"""
logging.getLogger("paramiko").setLevel(logging.INFO)
logging.getLogger("netmiko").setLevel(logging.INFO)
logging.basicConfig(
    filename=f'{get_time_now()}_ciscoConfig.log',
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    level=logging.DEBUG,
    datefmt='%H:%M:%S')


def repeat(num_times):
    def decorator_repeat(func):
        """ # декоратор для нескольких попыток выполнения кода"""

        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
                logging.debug(f'Repeat from decorator: func: {func.__str__}, args: {args}. Out func is {value}')
                if value:
                    try:
                        if value.__enter__:  # TODO что это получается?
                            return value
                        elif 'failed' in value:
                            continue
                        return value
                    except Exception as err:
                        logging.error(f'wrapper Exception {err}')
                else:
                    continue

        return wrapper_repeat

    return decorator_repeat


def get_credential(file):
    try:
        with open(file, 'r') as auth_file:
            username, password = auth_file.read().splitlines()
            logging.debug(f'Opening file: {file}')
    except (FileNotFoundError, ValueError):  # Если файл не найден, или он пустой то вводим в ручную
        logging.warning(f'File {file} not found.')
        print(f'{file} Не найден! Введите учётные данные >>>\n')
        username = input('Имя пользователя: ')  # Имя пользователя для авторизации в коммутаторах.
        password = getpass('Пароль: ')  # Соответственно пароль для коммутов.
        logging.debug(f'User enter username <<< {username} and password')
    return [username, password]


def get_hosts(file):
    try:
        with open(file, 'r') as hosts_file:
            hosts = hosts_file.read().splitlines()
            logging.debug(f'Opening file: {file}')
    except (FileNotFoundError, ValueError):  # Если файл не найден, или он пустой то вводим в ручную
        logging.warning(f'File {file} not found.')
        hosts = input(f'{file} Не найден!\n Введите ip-адреса: ').split(' ,;')
        logging.debug(f'User enter hosts <<< {hosts}')
    return hosts


def get_commands(file):
    try:
        with open(file, 'r') as commands_file:
            commands = commands_file.read().splitlines()
            logging.debug(f'Opening file: {file}')
    except (FileNotFoundError, ValueError):
        logging.warning(f'File {file} not found.')
        commands = input(f'{file} Не найден!\n Введите комманды для выполнения в устройствах: ').split(' ,;')
        logging.debug(f'User enter commands <<< {commands}')
    return commands


def set_cfg_flag():
    """
    Установка флагов для сохранения конфигураций
    """
    global backup_conf, save_conf, write_conf, save_output
    if input('Сохранить резервную копию конфигурации?: ').lower() in ['yes', 'y', 'да', 'д']:
        backup_conf = True
        logging.debug('User set backup config flag')
    else:
        backup_conf = False
    if input('Сохранить итоговую конфигурацию устройства?: ').lower() in ['yes', 'y', 'да', 'д']:
        save_conf = True
        logging.debug('User set ending config flag')
    else:
        save_conf = False
    if input('Записать итоговую конфигурацию в постоянную память устройства?: ').lower() in ['yes', 'y', 'да', 'д']:
        write_conf = True
        logging.debug('User set save end config device flag')
    else:
        write_conf = False
    if input('Сохранить вывод команд в файл?: ').lower() in ['yes', 'y', 'да', 'д']:
        save_output = True
        logging.debug('User set save output commsnds flag')
    else:
        save_output = False


def fail_check(var):
    """ Проверка в ответе сообщения об ошибке и выполнения повторно"""
    for _ in range(TRY_COUNT):
        if '% Authorization failed' in var:
            logging.error(f'Fail check func is >>> {var}')
            continue
        else:
            return var
    return var


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
        logging.debug(f'Send command "terminal length 0" in get_config func')
        output = self.ssh.send_command(f"{command}")
        logging.debug(f'Getting config in get_config func')
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
            logging.info(f'Init connection to {cisco["host"]}')
            # self.prompt = self.ssh.find_prompt().rstrip('>#')
            self.prompt = self.ssh.base_prompt
            return self.ssh

        except NetmikoAuthenticationException as error:
            err_print = f' ERROR!: Неверные данные аутентификации: {self.host}\n{error}'
            logging.error(err_print)
            print(err_print + f'\n {" ".join(["=" * 10])}\n')
            return error
        except NetmikoTimeoutException as error:
            err_print = f' ERROR!: Нет ответа от устройства: {self.host}'
            logging.error(err_print)
            print(err_print + f'\n {" ".join(["=" * 10])}\n')
            return error, err_print
        except SSHException as error:
            err_print = f' ERROR: SSH недоступен. Проверьте включен ли SSH? {self.host}'
            logging.error(err_print)
            print(err_print + f'\n {" ".join(["=" * 10])}\n')
            return error


def main():
    print_banner()
    '''# Загружаем данные для работы'''
    username, password = get_credential(AUTH_FILENAME)
    hosts = get_hosts(HOST_FILENAME)
    commands = get_commands(CMD_FILENAME)
    ''' Установка флагов для сохранения конфигураций '''
    set_cfg_flag()
    ''' ============================================ '''

    """ # выполнения запросов к устройстсву """
    for host in hosts:
        if not host or host[0] in '!#':  # Если попалась пустая строка или ! #, пропуск.
            continue
        cisco_job = CiscoConfig(username, password, host)
        logging.debug(f'Init connections to {host}')
        connection_out = cisco_job.init_connection()
        if not cisco_job.ssh:
            logging.error(f'Try connect to {host}, error {connection_out}')
            err_print = f"\n\n--------- Device IP: {cisco_job.host} подключение не установлено ---------\n\n"
            fault_hosts[cisco_job.host] = connection_out
            logging.error(err_print)
            print(err_print)
            continue
        cisco_job.ssh.enable()  # Перейти в режим enable
        logging.debug(f'Enter to enable mode')
        """ ========= Создаём резервную копию конфигурации =========== """
        if backup_conf:
            backup_path = 'backup_cfg'
            backup_file_path = f'./{backup_path}/{cisco_job.prompt}_{get_time_now()}backup.ios'
            if not path.exists(f'./{backup_path}/'):
                logging.debug(f'Making dir {backup_path}')
                mkdir(backup_path)
            with open(backup_file_path, 'w') as backup_cfg:
                print(f'----------- Сохранение резервной конфигурации... ------------\n| {backup_file_path}')
                backup_cfg.write(cisco_job.get_config())  # Сохраняем конфигу перед изменениями.
                logging.info(f'Save backUp config: {backup_file_path}')
                print('----------- Сохранение резервной конфигурации закончено! ------------')
        """============================================================"""

        """ ============ Выполнение основных комманд =============="""
        print(f"\n--------- Device {cisco_job.prompt} IP: {cisco_job.host} ---------")
        if not cisco_job.ssh.check_config_mode():
            logging.debug(f'Enter config mode {cisco_job.prompt}')
            cisco_job.ssh.config_mode()
        output_dict = dict()
        for command in commands:
            if command[0] in '!#':  # Пропустить закоментированные команды
                logging.debug(f'Drop command {command}')
                continue
            for _ in range(TRY_COUNT):  # Пытаемся повторить выполенение команд при ошибке
                if not cisco_job.ssh.check_config_mode():
                    logging.debug(f'Enter config mode {cisco_job.prompt} before command >>> {command}')
                    logging.debug(cisco_job.ssh.config_mode())
                logging.debug(f'Execute command {command} in {cisco_job.prompt}')
                output_dict[command] = cisco_job.ssh.send_command(command)
                if 'ailed' in output_dict[command]:
                    logging.error(f'Error executing command {command}, response: {output_dict[command]}')
                    continue
                else:
                    logging.debug(f'Execute {command} OK!')
                    break
            # output_dict[command] = repeat(cisco_job.ssh.send_command(command))

        """ =============== Сохраняем ответы команд в файл ============== """
        if save_output:
            cfg_dir_path = 'output'
            cfg_file_path = f'./{cfg_dir_path}/{cisco_job.prompt}_{get_time_now()}.txt'
            if not path.exists(f'./{cfg_dir_path}/'):
                logging.debug(f'Making dir {cfg_dir_path}')
                mkdir(cfg_dir_path)
            with open(cfg_file_path, 'w') as output_file:
                print(f'----------- Сохранение ответов команд... ------------\n| {cfg_file_path}')
                logging.info(f'Save response commands: {cfg_file_path}')
                for key, val in output_dict.items():
                    output_file.write(f'{cisco_job.prompt}# {key}:\n{val}')
                print('----------- Сохранение ответов команд закончено! ------------')
        """==================================================================="""

        # output = switch_connect.send_config_from_file(cmd_filename)  # отправка конфигурации из указанного файла
        # output = switch_connect.send_config_set(commands)
        if cisco_job.ssh.check_config_mode():
            logging.debug(f'Check config mode {cisco_job.prompt} and enter them')
            cisco_job.ssh.exit_config_mode()

        """ =============== Создаём текущую копию конфигурации ============== """
        if save_conf:
            cfg_dir_path = 'new_cfg'
            cfg_file_path = f'./{cfg_dir_path}/{cisco_job.prompt}.ios'
            if not path.exists(f'./{cfg_dir_path}/'):
                logging.debug(f'Making dir {cfg_dir_path}')
                mkdir(cfg_dir_path)
            with open(cfg_file_path, 'w') as new_cfg:
                print(f'----------- Сохранение новой конфигурации... ------------\n| {cfg_file_path}')
                logging.info(f'Save new config: {cfg_file_path}')
                new_cfg.write(f'{get_time_now()}\n{cisco_job.get_config()}')  # Сохраняем конфигу после изменений.
                print('----------- Сохранение новой конфигурации закончено! ------------')
        """==================================================================="""

        """================== Запись нового конфига в постоянную память ======================"""
        if write_conf:
            cisco_job.ssh.exit_config_mode()
            logging.debug(f'Exit config mode {cisco_job.prompt}')
            cisco_job.ssh.send_command('write')
            logging.debug(f'Write config to memory {cisco_job.prompt}')

        cisco_job.ssh.disconnect()  # Закрытие соединения.
        logging.info(f'Disconnect with {cisco_job.prompt} IP: {host}')

        """ ===== Вывод ответов от устройства ===== """
        logging.debug(f'Printing console response from device {cisco_job.prompt}')
        for key, val in output_dict.items():
            print(f'\n>>>{cisco_job.prompt}# {key}:\n{val}', end='\n')  # Вывести результаты выполнения команд
        print("\n--------------------- End ---------------------\n\n")

    """ Печать неудавшихся подключений"""
    if fault_hosts:
        logging.error(f'Host`s with fault connections {fault_hosts}')
        print(f"{len(fault_hosts)} Ошибок")
        for host, error in fault_hosts.items():
            print(f'Неудачное выполнение на {host}\nОшибка: {error}')


'''
    В netmiko есть несколько способов отправки команд:
    • send_command - отправить одну команду
    • send_config_set - отправить список команд или команду в конфигурационном режиме
    • send_config_from_file - отправить команды из файла (использует внутри метод send_config_set)
    • send_command_timing - отправить команду и подождать вывод на основании таймера
    =============================================================================
     def send_command(self, command_string, expect_string=None, delay_factor=1.0, max_loops=500, auto_find_prompt=True,
      strip_prompt=True, strip_command=True, normalize=True, use_textfsm=False, textfsm_template=None, use_ttp=False,
       ttp_template=None, use_genie=False, cmd_verify=True) 
    
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
     def session_preparation(self)   Подготовьте сеанс после установления соединения
            Этот метод обрабатывает некоторые различия, возникающие между различными устройствами. в начале сеанса.
            В целом он должен включать:
             self._test_channel_read()
             self.set_base_prompt()
              self.disable_paging()
               self.set_terminal_width()
                self.clear_buffer() 
            
    Кроме перечисленных методов для отправки команд, netmiko поддерживает такие методы:
    • config_mode - перейти в режим конфигурации: ssh.config_mode()
    • exit_config_mode - выйти из режима конфигурации: ssh.exit_config_mode()
    • check_config_mode - проверить, находится ли netmiko в режиме конфигурации 
      (возвращает True, если в режиме конфигурации, и False - если нет): ssh.check_config_mode()
    • find_prompt - возвращает текущее приглашение устройства: ssh.find_prompt()
    • disconnect - завершить соединение SSH
'''

if __name__ == "__main__":
    logging.debug(f'Start programm {get_time_now()}')
    main()
    logging.debug(f'End programm {get_time_now()}')
