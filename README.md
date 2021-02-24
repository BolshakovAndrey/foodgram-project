# foodgram-project

![Foodgram_workflow](https://github.com/BolshakovAndrey/foodgram-project/workflows/Foodgram_workflow/badge.svg)

***Foodgram*** - это сайт рецептов. Продуктовый помощник, позволяющий просматривать и создавать рецепты,
добавлять их в избранное, подписываться на авторов рецептов, формировать список покупок
с ингредиентами для приготовления понравившихся блюд.

Демо сайт доступен по этой ссылке http://178.154.250.13/

### Запуск проекта с использованием Docker

Клонируйте репозиторий или скопируйте следующие файлы и папки:
   ```
    nginx/
    docker-compose.yaml
    .env-example
   ```
1. При необходимости измените файл `.env.template`
   и переименуйте в `.env`
   

2. Для запуска проекта выполните:

   `docker-compose up -d`
   

3. Запускаем терминал внутри контейнера:
   
   `docker-compose exec web bash`


3. При первом запуске необходимо применить миграции:

   `cd code`  затем `python manage.py migrate`


4. Загрузить статику

   `python manage.py collectstatic`
   

5. Создайте пользователя с правами администратора:

   `python manage.py createsuperuser`


5. Для получения актуальной версии образа проекта выполните:

   `docker pull mydockerid2505/foodgram:final`
  