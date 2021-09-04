# 2021_09_03_Foxhound_leadersofdigital_hack
Хакатон "Цифровой прорыв", 3-5 сентября 2021 г
## Развертывание через docker-compose
1. Установить [docker](https://docs.docker.com/engine/install/ubuntu/)
2. Установить [docker-compose](https://docs.docker.com/compose/install/)
3. В папке compose создать файлы .env и .uwsgi.env и заполнить их в соответствии с примерами
4. Запустить файл build.sh с правами суперпользователя
```bash
sudo ./build.sh
```
5. Настроить внешний nginx, который будет пересылать все запросы на порт приложения
## Команды docker-compose 
Все команды необходимо выполнять в папке compose
- Остановить все контейнеры
```bash
sudo docker-compose stop
```
- Перезапустить контейнер
```bash
sudo docker-compose restart {container_name}
```
- Запуск manage.py shell
```bash
sudo docker-compose exec web python manage.py shell
```