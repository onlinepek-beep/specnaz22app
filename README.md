# Спецназ 22

Внутреннее PWA-приложение для учёта производства вышивального участка.

## Стек
- Python
- FastAPI
- HTML / CSS / JavaScript
- Session authentication

## Роли
- Оператор
- Руководитель
- Администратор

## Машины
- Velles №1
- Velles №2

## Запуск
```powershell
py -m pip install fastapi uvicorn python-multipart itsdangerous
py -m uvicorn backend.main:app --reload
```

Открыть: http://127.0.0.1:8000

## Тестовые учётные записи
- Руководитель: manager / manager
- Оператор: operator / operator
- Администратор: admin / admin

## Статус
Базовый каркас приложения: авторизация, роли, навигация, главная, изделия, история, профиль и темы.
Следующий этап — полноценный учёт производства и база данных.
