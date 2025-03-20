
# 📝Notes API – Управление заметками и пользователями

## 📌 Описание
Этот проект представляет собой API для управления заметками с поддержкой ролей пользователей (Admin, User и Editor).  
**Стек технологий:** Django + MySQL + JWT + Redis + Docker .

## 📡🔗 Взаимодейтвие фронтенда и бэкенда реализовано с помощью REST API. 
- **✅ Разделение фронтенда и бэкенда.**
- **✅ Масштабируемость.**
- **✅ Стандартные HTTP-методы.**
- **✅ Простота интеграции.**
- **✅ Безопасность – поддержка JWT, ролевой модели, хранения токенов в Redis.**
- **✅ Гибкость.**
- **✅ Производительность – кеширование.**

## 🔑 Токены в Redis:
- ** Реализована привязка токена к IP и User-Agent**
- ** Принудительная инвалидация при logout** 
- ** Белый список (whitelist)** 
- ** Чёрный список (blacklist)** 


## 🚀 Основные функции
- **📌 Регистрация**
- **🔑 Авторизация через JWT (токен хранится в куках)**
- **🔑 Хранение в Redis белого и черного списка JWT**
- **📝 CRUD-операции с заметками**
- **🛡️ Разграничение доступа (права User,Admin и Editor)**
- **📜 Логирование действий пользователей**
- **🐳 Готовый Dockerfile и docker-compose.yml**

## 📦 Установка и запуск  

#### После клонирования нужно скопировать файл .env в корень проекта.  

### 🐳 Запуск проекта в Docker
```bash
   git clone https://github.com/AlexKrutskikh/Notes_API
   cd Notes_API
   docker-compose up -d
  ```
### В процессе сборки запускаются 4 контейнера:

- 🚀 backend – backend API

- 🗄️ db – база данных

- 🔄 web – обратный прокси

- 🔴 redis – кеш для токенов

## После успешного запуска API будет доступно по адресу:
➡ http://localhost

### 🖥️ Локальный запуск
```bash
   git clone https://github.com/AlexKrutskikh/Notes_API
   cd Notes_API
   python manage.py runserver
  ```
#### Обновите переменные окружения в файле .env: 
###### Замените DB_HOST=db на DB_HOST=localhost.

###### Проект подключится к базе в ранее поднятом контейнере

После успешного запуска API будет доступно по адресу:  
➡ http://127.0.0.1:8000

### 📜  Все действия в API логируются в файл logs/django.log в корне проекта.

## 🌐 Описание API:

### 📧 "api/auth/v1/registration/user/"
#### 📌 Отправка данных для регистрации.

#### request-body:
```json
{
  "last_name": "Иван",
  "first_name": "Иванов",
  "username": "Иван",
  "phone": "+79992193109",
  "email": "ivan@gmail.com",
  "password": "SecurP@ssw0rd"
}
```
#### request-body:
###### 200 OK (успешный запрос):
```json
{
    "message": "Successfully created"
}
```
###### 400 Bad Request:
```json
{
    "errors": {
        "last_name": "This last name is already in use",
        "first_name": "This first name is already in use",
        "username": "This username is already in use",
        "phone": "This phone number is already registered",
        "email": "This email is already in use"
    }
}
```
### 🔐  "api/auth/v1/authorization/user/"
#### 📌 Авторизация пользователя.

Этот endpoint принимает логин и пароль и отправляет JWT токены в cookie
при успешном входе

#### request-body:
```json
{
  "username": "Ivan",
  "password": "SecurP@ssw0rd"
}
```
#### request-body:
###### 200 OK (успешный запрос):
```json
{
    "message": "Successfully logged in"
}
```
###### 400 Bad Request:
```json
{
    "error": "User does not exist"
}
```
### 🔐  "api/auth/v1/logout/user/"
#### 📌 Logout пользователя.

Выход из системы

### 🔑  "/v1/refresh-token"
#### 📌 Обновление токенов.

Этот endpoint обновляет access_token и refresh_token 

#### request-body:
###### 200 OK (успешный запрос):
```json

{
    "success": true,
    "message": "Токен обновлен"
}
```
### 📝 "api/notes/v1/create/note/"
#### 📌 Создание новой заметки.

Этот endpoint создает новую заметку, связывает ее с пользователем с помощью токена из cookie.

#### request-body:
```json
{
  "title": "string",
  "body": "string"
}
```
#### request-body:
###### 200 OK (успешный запрос):
```json
{
    "message": "Successfully created",
    "id_note": 9
}
```
### 📝 "api/notes/v1/update/note/"
#### 📌 Обновление заметки.

Этот endpoint обновляет заметку.

#### request-body:
```json
{
  "title": "Тест4",
  "body": "Тест4",
  "note_id": 3
}
```
#### request-body:
###### 200 OK (успешный запрос):
```json
{
    "message": "Successfully updated",
    "id_note": 9
}
```
###### 404 Bad Request:
```json
{
    "error": "Note not found."
}
```
###### 403 Bad Request:
```json
{
    "detail": "You do not have permission to perform this action."
}
```
### 📝 "api/notes/v1/delete/note/"
#### 📌 Удаление заметки.

Этот endpoint удаляет заметку.

#### request-body:
```json
{
  "title": "Тест1",
  "body": "Тест1",
  "note_id": 9
}
```
#### request-body:
###### 200 OK (успешный запрос):
```json
{
    "message": "Successfully moved to trash",
    "id_note": 9
}

```
###### 404 Bad Request:
```json
{
    "error": "Note not found."
}
```
###### 403 Bad Request:
```json
{
    "detail": "You do not have permission to perform this action."
}
```
### 📝 "/api/notes/v1/get-all/notes/"
#### 📌 Получение всех заметок.

Этот endpoint отдает все заметки для роли админ.

#### request-body:
###### 200 OK (успешный запрос):
```json
{
        "id": 9,
        "title": "Тест4",
        "body": "Тест4",
        "created_at": "2025-03-20T09:46:52.814869Z",
        "updated_at": "2025-03-20T09:51:28.139839Z",
        "is_deleted": true
    }

```

###### 404 Bad Request:
```json
{
    "message": "Notes not found"
}
```
###### 403 Bad Request:
```json
{
    "detail": "You do not have permission to perform this action."
}
```
### 📝 "/api/notes/v1/get-my/note/"
#### 📌 Получение своих заметок.

Этот endpoint свои заметки.

#### request-body:
###### 200 OK (успешный запрос):
```json
    {
        "id": 9,
        "title": "Тест4",
        "body": "Тест4",
        "created_at": "2025-03-20T09:46:52.814869Z",
        "updated_at": "2025-03-20T09:51:28.139839Z",
        "is_deleted": true
    }


```
###### 404 Bad Request:
```json
{
    "message": "Notes not found"
}
```
### 📝 "api/notes/v1/get-note/1/"
#### 📌 Получение заметки по id.

Этот endpoint отадет заметку по id.

#### request-body:
###### 200 OK (успешный запрос):
```json
    {
        "id": 9,
        "title": "Тест4",
        "body": "Тест4",
        "created_at": "2025-03-20T09:46:52.814869Z",
        "updated_at": "2025-03-20T09:51:28.139839Z",
        "is_deleted": true
    }

```
###### 403 Bad Request:
```json
{
    "detail": "You do not have permission to perform this action."
}
```
###### 404 Bad Request:
```json
{
    "message": "Notes not found"
}
```

### 📝 "api/notes/v1/restore/note/"
#### 📌 Восстановление заметки.

Этот endpoint восстанавливает заметку из корзины.

#### request-body:
```json
{
  "note_id": 3
}
```
#### request-body:
###### 200 OK (успешный запрос):
```json
{"message": "Successfully restored", 
  "id_note": 3
}
```
###### 403 Bad Request:
```json
{
    "detail": "You do not have permission to perform this action."
}
```
###### 404 Bad Request:
```json
{
    "message": "Notes not found"
}
```