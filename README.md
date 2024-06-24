# --> Блог - социальная сеть <--
***

### Общее описание
Это социальная сеть для людей, которые хотят создать что-то своё, выразить себя, свои мысли и чувства,
хотят поделиться своим уникальным взглядом на мир.

### Возможности проекта
  * регистрация/авторизация пользователей с применением шаблонов
  * возможность восстановления пароля через почту
  * генерация индивидуальных страниц пользователей
  * редактирование профиля пользователя
  * отображение всех публикаций пользователя на личной странице
  * создание публикации с возможностью добавления изображения
  * создание отложенной публикации
  * удаление публикаций и коментариев
  * отображение публикаций в выбранной категории
  * добавление коментариев к публикации авторизованным пользователем
  * чтение и запись данных в БД SQLite3
  * Настроены кастомные страницы для ошибок 403 CSRF, 404 и 500 с применением собственных шаблонов.

### Подготовка проекта к запуску под Linux

* Клонируем репозиторий на пк
  ```
  git clone git@github.com:PetrovKRS/Blog-SocialNetwork.git
  ```
* переходим в рабочую папку склонированного проекта
* разворачиваем виртуальное окружение
  ```
  python3 -m venv venv
  ```
  ```
  source venv/bin/activate
  ```
* устанавливаем зависимости из файла requirements.txt
  ```
  pip install --upgrade pip
  ```
  ```
  pip install -r requirements.txt
  ```
* выполняем миграции
  ```
  python3 manage.py migrate
  ```
* В папке c бэкендом файл env_example переименовываем в .env и
  заменяем в нем данные на свои
  ```
    # settings
    SECRET_KEY=django-insecure-https://github.com/PetrovKRS/Blog-SocialNetwork
    ALLOWED_HOSTS=localhost,127.0.0.1,yourDomain.ru
    DEBUG=False
  ```
* запускаем тестовый сервер
  ```
  python3 manage.py runserver
  ```
* заходим в брауузер и ислледуем
  ```
  http://127.0.0.1:8000/
  ```

***
### <b> Стек технологий: </b>

![Python](https://img.shields.io/badge/-Python_3.9-df?style=for-the-badge&logo=Python&labelColor=yellow&color=blue)
![Django](https://img.shields.io/badge/-Django-df?style=for-the-badge&logo=Django&labelColor=darkgreen&color=blue)
![Django](https://img.shields.io/badge/-SQLite-df?style=for-the-badge&logo=SQLite&labelColor=red&color=blue)
![Django](https://img.shields.io/badge/-HTML-df?style=for-the-badge&logo=&labelColor=red&color=blue)
![GitHub](https://img.shields.io/badge/-GitHub-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)

***
## Ознакомительная версия
[Для ознакомления ...](https://petrovkrs.pythonanywhere.com)

***
### Автор проекта: 
[![GitHub](https://img.shields.io/badge/-Андрей_Петров-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)](https://github.com/PetrovKRS)
*** 
