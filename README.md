Project_DRF

Запуск проекта:

Обязательно наличие Docker Desktop на вашем устройстве

Для запуска проекта необходимо создать файл .env, в котором указать данные ключами, паролями и др. секретной информацией. Переменные находятся в файле .env_sample

Настроить зависимости из файла requirements.txt

Создание образа и его запуск производим командой: docker-compose up -d --build

После запуска сервера в Docker переходим по полученной ссылке.