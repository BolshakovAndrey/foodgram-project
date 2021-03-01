# foodgram-project

![Foodgram_workflow](https://github.com/BolshakovAndrey/foodgram-project/workflows/Foodgram_workflow/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2066521421574ba7816f8e1e70d751e9)](https://www.codacy.com/gh/BolshakovAndrey/foodgram-project/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=BolshakovAndrey/foodgram-project&amp;utm_campaign=Badge_Grade)


***Foodgram*** - это сайт рецептов. Продуктовый помощник, позволяющий просматривать и создавать рецепты, добавлять их в
избранное, подписываться на авторов рецептов, формировать список покупок с ингредиентами для приготовления понравившихся
блюд.

Демо сайт доступен по этой ссылке http://84.201.181.216/

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

6. Загрузить dumpdata (ингредиенты и тэги)

   `python manage.py loaddata myingredients.json`
   `python manage.py loaddata tags.json`

7. Для получения актуальной версии образа проекта выполните:

   `docker pull mydockerid2505/foodgram:final`
