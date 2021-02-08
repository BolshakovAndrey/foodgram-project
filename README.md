# foodgram-project

![example workflow name](https://github.com/BolshakovAndrey/foodgram-project/workflows/Foodgram-CI/badge.svg)

***Foodgram*** - сайт рецептов - продуктовый помощник, позволяющий просматривать и создавать рецепты,
добавлять их в избранное, подписываться на авторов рецептов, формировать список покупок
с ингредиентами для приготовления понравившихся блюд.

Демо сайт доступен по этой ссылке https:130.193.57.127

### Запуск проекта с использованием Docker

Клонируйте репозиторий или скопируйте следующие файлы и папки:
   ```
    nginx/
    docker-compose.yaml
    .env-example
    .db.env-example
   ```
1. При необходимости измените файлы `.env.local-example`, `.db.env-example`
   и переименуйте их в `.env` и `.db.env`
2. Для запуска проекта выполните:

   `make run` или `docker-compose up -d`

   После успешного запуска, проект доступен по адресу http://localhost:80
3. При первом запуске необходимо применить миграции:

   `docker exec -ti foodgram-web ./manage.py migrate`

4. Для загрузки тестовых данных выполните:

   `docker exec -ti foodgram-web ./manage.py loaddata dump.json`

5. Для получения актуальной версии образа проекта выполните:

   `docker pull mydockerid2505/foodgram:final`
  