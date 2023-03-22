<h2>Foodgram, &laquo;Продуктовый помощник&raquo;.</h2>
<p>Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список &laquo;Избранное&raquo;, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.</p>
<hr />
<h3>Стек технологий</h3>
<ul>
<li>Python</li>
<li>Django</li>
<li>Django REST Framework</li>
<li>PostgreSQL</li>
<li>Docker</li>
<li>Github Actions</li>
</ul>
<hr />
<h3>Зависимости</h3>
<ul>
<li>Перечислены в файле backend/requirements.txt</li>
</ul>
<hr />
<h3>Документация к API</h3>
<ul>
<li>Написана с использованием Redoc и доступна по адресу:</li>
</ul>
<hr />
<h3>Особенности реализации</h3>
<ul>
<li>Проект запускается в Docker контейнерах;</li>
<li>Образы foodgram_frontend и foodgram_backend запушены на DockerHub;</li>
<li>Реализован CI/CD;</li>
<li>Проект развернут на сервере:</li>
</ul>
<hr />
<h3>Развертывание на локальном сервере</h3>
<ul>
<li>Установите на сервере docker и docker-compose;</li>
<li>Создайте файл /infra/.env. Шаблон для заполнения файла нахоится в /infra/.env.example;</li>
<li>Выполните команду docker-compose up -d --buld;</li>
<li>Создайте суперюзера docker-compose exec backend python manage.py createsuperuser;</li>
<li>Заполните базу ингредиентами docker-compose exec backend python manage.py convert_from_csv;<br /><br /></li>
</ul>
<hr />
<h3>Автор проекта:</h3>
<p>Борокин Андрей</p>

- GITHUB: [exp-ext](https://github.com/exp-ext)

- [![Join Telegram](https://img.shields.io/badge/My%20Telegram-Join-blue)](https://t.me/Borokin)
