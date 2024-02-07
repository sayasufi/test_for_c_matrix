import logging
import os


def setup_logging(log_file: str = "cache.log", stdout_logging: bool = False):
    """Создаем функцию инициализирующую логгер"""

    # Очистка файла логов если в нем больше 1000 строк
    with open(log_file, "w+") as file:
        if len(file.readlines()) > 1000:
            os.system(r'cat /dev/null>{}'.format(log_file))

    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # Создаем форматтер для логов
    formatter = logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s")
    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Если указан аргумент командной строки,
    # добавляем обработчик для вывода в stdout
    if stdout_logging:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(
            logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s")
        )
        logger.addHandler(stdout_handler)

    return logger
