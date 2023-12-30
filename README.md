# QRKot 
##### Сервис для пожертвований.
#
## Описание
Данный проект представляет собой приложение для Благотворительного фонда поддержки котиков QRKot.
С помощью этого приложения можно:
  * Создать проект для сбора пожертвований (admin-only)
  * Пожертвовать деньги на один из проектов 

В приложении реализовано автоматическое пополнение проектов при поступлении нового пожертвования, и наоборот при создании нового проекта, на него автоматически поступят неиспользованные пожертвования.

### В проекте используются:
* ##### FastAPI v. 0.78.0
* ##### SQLAlchemy v. 1.4.36
* ##### Fastapi-users v. 10.0.4
* ##### Pydantic 1.9.1
* ##### Uvicorn v. 0.17.6

#
#### Для начала работы необходимо:
* Клонировать репозиторий и перейти в него в командной строке:
   ```
   git clone git@github.com:Sobiyk/cat_charity_fund.git
   ```

  ```
  cd cat_charity_fund
  ```

* Cоздать и активировать виртуальное окружение:

  ```
  py -3.9 -m venv venv
  ```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    . venv/scripts/activate
    ```

* Установить зависимости из файла requirements.txt:

  ```
  python3 -m pip install --upgrade pip
  ```

  ```
  pip install -r requirements.txt
  ```
 
* Шаблон заполнения файла .env
  ```
  APP_TITLE=QRKot
  APP_DESCRIPTION=Приложение для пожертвований
  DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
  SECRET=secret_key
  ```
* Выполните миграции
  ```
  alembic upgrade head
  ```
* Запустите проект
   ```
   uvicorn app.main:app
   ```

##### Автор: [Sobiy](https://github.com/Sobiyk)
