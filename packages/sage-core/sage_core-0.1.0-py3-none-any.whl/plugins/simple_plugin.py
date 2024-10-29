# plugins/simple_plugin.py

import logging
from sage_core.message import Message


def init_plugin(core) -> None:
    """
    Инициализация простого плагина. Регистрирует обработчик для 'simple_event' сообщений.
    """

    def handle_simple_event(content):
        """
        Обработчик для 'simple_event' сообщений. Отправляет ответное сообщение.
        """
        try:
            response_message = Message(
                sender="simple_plugin",
                receiver=content.get("sender", "SAGECore"),
                content={"text": "Ответ от simple_plugin"},
                priority=Message.MEDIUM_PRIORITY
            )
            core.send_message(response_message)
            logging.info("simple_plugin отправил ответное сообщение.")
        except Exception as e:
            logging.error(f"Ошибка в simple_plugin при отправке сообщения: {e}")

    core.register_receiver("simple_event", handle_simple_event)
    logging.info("simple_plugin успешно инициализирован.")


def shutdown_plugin(core) -> None:
    """
    Завершение работы простого плагина.
    """
    logging.info("simple_plugin завершает работу.")
    # Здесь можно добавить код для очистки ресурсов, если необходимо
