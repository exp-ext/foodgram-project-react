<h2>Foodgram, &laquo;Продуктовый помощник&raquo;.</h2>

![статус](https://github.com/exp-ext/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

<p align="center">
<img src="https://github.com/exp-ext/foodgram-project-react/blob/master/backend/static/img/top-banner.jpg?raw=true" width="1200">
</p>
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
<li>Написана с использованием Redoc и доступна по адресу: https://grandmasrecipes.fun/api/docs/redoc </li>
</ul>
<hr />
<h3>Особенности реализации</h3>
<ul>
<li>Проект запускается в Docker контейнерах;</li>
<li>Образы foodgram_frontend и foodgram_backend запушены на DockerHub;</li>
<li>Реализован CI/CD;</li>
<li>Проект развернут на сервере: https://grandmasrecipes.fun/ </li>
</ul>
<hr />
<h3>Развертывание на сервере c получением сертификата</h3>
<ul>
<li>Установите на сервере docker и docker-compose-plugin;</li>
<li>Клонируйте на локальный компьютер репозиторий;</li>
<li>Создайте файл /infra/.env. Шаблон для заполнения файла находится в /infra/.env.example;</li>
<li>В файле ./infra/nginx/default.conf.template закомментируйте строки 14:18 для получения сертификата.</li>
<li>Скопируйте папку infra со всем содержимым на сервер `scp -r ~/foodgram-project-react/infra name@IP.ad.re.ss:~/`
</li>
<li>На сервере, перейдите в папку infra/ и получите сертификаты в Let's Encrypt запустив скрипт `sudo ./init-letsencrypt.sh`</li>
<li>Остановите сервер `docker compose down` </li>
<li>Раскомментируйте строки 14:18 в файле ./infra/nginx/default.conf.template</li>
<li>В папке infra выполните команду `docker compose up -d --build`;</li>
<li>Создайте суперюзера `docker compose exec backend python manage.py createsuperuser`</li>
<br /><br />
</ul>
<hr />
<h3>Автор проекта:</h3>
<p>Борокин Андрей</p>

GITHUB: [exp-ext](https://github.com/exp-ext)

[![Join Telegram](https://img.shields.io/badge/My%20Telegram-Join-blue)](https://t.me/Borokin)
