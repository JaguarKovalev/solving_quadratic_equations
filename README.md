# Решение Квадратного Уравнения

Это веб-приложение на Django, разработанное в рамках практической работы по курсу "Проектирование веб-ресурсов" в МПГУ. Приложение решает квадратные уравнения вида:

\[ ax^2 + bx + c = 0 \]

Пользователь может вводить коэффициенты через параметры GET-запроса и видеть решение на веб-странице.

## Функционал
- Решение квадратных уравнений для любых действительных коэффициентов `a`, `b` и `c`.
- Обработка граничных случаев, таких как линейные уравнения (`a = 0`) и отсутствие действительных корней.
- Удобные сообщения об ошибках для некорректных вводов.

## Начало работы

### Предварительные требования
- Python 3.12+
- Poetry для управления зависимостями

### Установка
1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/JaguarKovalev/solving_quadratic_equations
   cd solving_quadratic_equations
   ```

2. Установите зависимости с помощью Poetry:
   ```sh
   poetry install
   ```

3. Настройте проект Django:
   ```sh
   poetry run python manage.py migrate
   ```

4. Запустите сервер разработки:
   ```sh
   poetry run python manage.py runserver
   ```

5. Откройте приложение по адресу [http://127.0.0.1:8000/solver/solve/](http://127.0.0.1:8000/solver/solve/).

## Использование
На главной странице можно ввести коэффициенты `a`, `b` и `c`, чтобы решить квадратное уравнение. Решение будет отображено непосредственно на странице.

Пример URL: `/solver/solve/?a=1&b=-3&c=2`

## Запуск тестов
Чтобы запустить тесты для данного проекта, используйте следующую команду:

```sh
poetry run python manage.py test solver
```

## Структура проекта
- `my_quadratic_solver/`: Основная папка проекта, содержащая настройки.
- `solver/`: Папка приложения, содержащая представления, шаблоны и тесты.
- `templates/`: HTML-шаблоны для отображения результатов.

## Используемые технологии
- Django 5.1.2
- Python 3.12

## Лицензия
Этот проект разработан в учебных целях и не предназначен для использования в продакшене.

## Автор
Проект разработан Ягуаром Ковалёвым в рамках практической работы по курсу "Проектирование веб-ресурсов" в МПГУ.

