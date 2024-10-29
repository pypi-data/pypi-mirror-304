# sage_core/core.py

import sys
import logging
import importlib
import os
import time
import threading
from typing import Dict, Callable, Any, List
import queue

from sage_core.message import Message  # Абсолютный импорт

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class SAGECore:
    """
    Класс, представляющий ядро SAGE — универсальный движок для взаимодействия между плагинами.
    """
    def __init__(self, num_threads: int = 4):
        self.receivers: Dict[str, List[Callable[[Any], None]]] = {}
        self.connections: Dict[str, List[str]] = {}
        self.message_queue = queue.PriorityQueue()
        self.plugins: Dict[str, Any] = {}
        self.lock = threading.Lock()
        self.load_plugins()
        logging.info("Плагины зарегистрированы.")
        self.start_worker_threads(num_threads=num_threads)

    def register_receiver(self, name: str, handler: Callable[[Any], None]) -> None:
        """
        Регистрирует нового получателя сообщений.
        """
        with self.lock:
            if name not in self.receivers:
                self.receivers[name] = []
            self.receivers[name].append(handler)
            logging.debug(f"Получатель '{name}' зарегистрировал обработчик '{handler.__name__}'.")

    def unregister_receiver(self, name: str, handler: Callable[[Any], None]) -> None:
        """
        Отменяет регистрацию получателя сообщений.
        """
        with self.lock:
            if name in self.receivers and handler in self.receivers[name]:
                self.receivers[name].remove(handler)
                logging.debug(f"Получатель '{name}' отменил обработчик '{handler.__name__}'.")
                if not self.receivers[name]:
                    del self.receivers[name]

    def connect_plugins(self, from_plugin: str, to_plugin: str) -> None:
        """
        Устанавливает соединение между двумя плагинами.
        """
        with self.lock:
            if from_plugin not in self.connections:
                self.connections[from_plugin] = []
            if to_plugin not in self.connections:
                self.connections[to_plugin] = []
            if to_plugin not in self.connections[from_plugin]:
                self.connections[from_plugin].append(to_plugin)
                logging.debug(f"Соединение установлено от '{from_plugin}' к '{to_plugin}'.")
            if from_plugin not in self.connections[to_plugin]:
                self.connections[to_plugin].append(from_plugin)
                logging.debug(f"Соединение установлено от '{to_plugin}' к '{from_plugin}'.")

    def load_plugins(self) -> None:
        """
        Загружает и инициализирует все плагины из папки 'plugins/'.
        """
        current_dir = os.path.dirname(__file__)
        plugins_path = os.path.join(current_dir, '..', 'plugins')
        plugins_path = os.path.abspath(plugins_path)
        if not os.path.isdir(plugins_path):
            logging.warning("Папка 'plugins/' не найдена. Плагины не будут загружены.")
            return

        # Добавляем путь к плагинам в sys.path для импорта
        if plugins_path not in sys.path:
            sys.path.insert(0, plugins_path)

        for filename in os.listdir(plugins_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]  # Убираем '.py'
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'init_plugin') and callable(module.init_plugin):
                        module.init_plugin(self)
                        self.plugins[module_name] = module
                        logging.info(f"Плагин '{module_name}' успешно загружен.")
                    else:
                        logging.warning(f"Плагин '{module_name}' не содержит функцию 'init_plugin(core)'.")
                except Exception as e:
                    logging.error(f"Ошибка при загрузке плагина '{module_name}': {e}")

    def unload_plugin(self, module_name: str) -> None:
        """
        Выгружает плагин по имени модуля.
        """
        with self.lock:
            if module_name in self.plugins:
                try:
                    module = self.plugins[module_name]
                    if hasattr(module, 'shutdown_plugin') and callable(module.shutdown_plugin):
                        module.shutdown_plugin(self)
                    del self.plugins[module_name]
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                    logging.info(f"Плагин '{module_name}' успешно выгружен.")
                except Exception as e:
                    logging.error(f"Ошибка при выгрузке плагина '{module_name}': {e}")
            else:
                logging.warning(f"Плагин '{module_name}' не загружен.")

    def load_plugin(self, module_name: str) -> None:
        """
        Загружает плагин по имени модуля.
        """
        with self.lock:
            if module_name in self.plugins:
                logging.warning(f"Плагин '{module_name}' уже загружен.")
                return
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'init_plugin') and callable(module.init_plugin):
                    module.init_plugin(self)
                    self.plugins[module_name] = module
                    logging.info(f"Плагин '{module_name}' успешно загружен.")
                else:
                    logging.warning(f"Плагин '{module_name}' не содержит функцию 'init_plugin(core)'.")
            except Exception as e:
                logging.error(f"Ошибка при загрузке плагина '{module_name}': {e}")

    def send_message(self, message: Message) -> None:
        """
        Отправляет сообщение получателю через очередь сообщений.
        """
        self.message_queue.put(message)
        logging.debug(f"Сообщение от '{message.sender}' отправлено получателю '{message.receiver}' с приоритетом {message.priority}.")

    def worker(self):
        """
        Рабочий поток, обрабатывающий сообщения из очереди.
        """
        while True:
            try:
                message = self.message_queue.get()
                if message.receiver == '__shutdown__':
                    logging.debug("Получен сигнал остановки рабочего потока.")
                    self.message_queue.task_done()
                    break
                self.process_message(message)
                self.message_queue.task_done()
            except Exception as e:
                logging.error(f"Ошибка в рабочем потоке: {e}")

    def process_message(self, message: Message) -> None:
        """
        Обрабатывает одно сообщение.
        """
        with self.lock:
            if message.receiver in self.receivers:
                for handler in self.receivers[message.receiver]:
                    try:
                        handler(message.content)
                        logging.debug(f"Сообщение от '{message.sender}' получено получателем '{message.receiver}'.")
                    except Exception as e:
                        logging.error(f"Ошибка в получателе '{message.receiver}': {e}")
            else:
                logging.warning(f"Получатель '{message.receiver}' не найден.")

            # Отправляем сообщения подключенным плагинам
            if message.receiver in self.connections:
                for connected_plugin in self.connections[message.receiver]:
                    # Создаем новое сообщение с тем же содержимым и приоритетом
                    forwarded_message = Message(
                        sender=message.sender,
                        receiver=connected_plugin,
                        content=message.content,
                        priority=message.priority
                    )
                    self.message_queue.put(forwarded_message)
                    logging.debug(f"Сообщение от '{message.sender}' переадресовано получателю '{connected_plugin}' с приоритетом {forwarded_message.priority}.")

    def start_worker_threads(self, num_threads: int = 4) -> None:
        """
        Запускает рабочие потоки для обработки сообщений.
        """
        self.workers = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker, daemon=True)
            thread.start()
            self.workers.append(thread)
        logging.info(f"Запущено {num_threads} рабочих потоков для обработки сообщений.")

    def shutdown(self) -> None:
        """
        Останавливает все рабочие потоки.
        """
        with self.lock:
            for _ in self.workers:
                shutdown_message = Message(
                    sender="SAGECore",
                    receiver="__shutdown__",
                    content=None,
                    priority=Message.SHUTDOWN_PRIORITY
                )
                self.send_message(shutdown_message)
            logging.info("Отправлены сигналы остановки рабочих потоков.")
        for thread in self.workers:
            thread.join()
        logging.info("Все рабочие потоки остановлены.")

    def run(self) -> None:
        """
        Запускает главный цикл работы системы.
        """
        logging.info("SAGE Core запущен.")
        try:
            while True:
                # Основной цикл может быть пустым, так как обработка сообщений идет в рабочих потоках
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("SAGE Core остановлен пользователем.")
            self.shutdown()
            sys.exit(0)
