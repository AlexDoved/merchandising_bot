import logging

from aiogram.utils import executor

from init_bot import dp
from data_base import sqlite_db
from handlers import (handlers_for_users, additional_handlers,
                      first_brand_outlets, second_brand_outlets,
                      admin_outlets, documents_handlers,
                      admin_samples, access_control)

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    """Запуск бота."""
    print('Бот запущен и готов к работе!')
    sqlite_db.sql_start()


admin_outlets.register_handlers_admin_outlets(dp)
admin_samples.register_handlers_admin_samples(dp)
access_control.register_access_bot_handler(dp)
handlers_for_users.register_handlers_for_users(dp)
documents_handlers.register_document_handlers_client(dp)
first_brand_outlets.register_first_brand_handlers(dp)
second_brand_outlets.register_second_brand_handlers(dp)
additional_handlers.register_additional_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
