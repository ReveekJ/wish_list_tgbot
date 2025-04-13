#!/bin/sh

# запуск миграций бд
alembic upgrade head

# запуск taskiq
taskiq worker src.services.schedule_notifications_manager.taskiq_brokers.broker:broker -fsd &
taskiq scheduler src.services.schedule_notifications_manager.taskiq_brokers.broker:scheduler -fsd --skip-first-run &

# запуск бота
exec python3.12 -m src.tgbot.main
