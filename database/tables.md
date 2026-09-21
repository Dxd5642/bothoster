
---

### Таблица `users`

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Уникальный идентификатор пользователя |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL | Уникальное имя пользователя |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Email пользователя |
| `is_verified` | BOOLEAN | NOT NULL, DEFAULT FALSE | Подтверждён ли email |
| `password_hash` | VARCHAR(255) | NOT NULL | Хеш пароля |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Активен ли пользователь |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Дата и время регистрации |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Дата и время последнего изменения |

**Связи:**
- `users.id` → `bots.owner_id` — один пользователь может иметь много ботов.



## Таблица `roles`

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Уникальный идентификатор роли |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL | Название роли |
| `description` | TEXT | NULL | Описание роли |

**Примеры ролей:**
- `user` — обычный пользователь
- `admin` — администратор

**Связи:**
- `roles.id` → `user_roles.role_id`



## Таблица `user_roles`

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `user_id` | UUID | PK, FK → users.id, NOT NULL | Идентификатор пользователя |
| `role_id` | UUID | PK, FK → roles.id, NOT NULL | Идентификатор роли |

**Первичный ключ:**
- `(user_id, role_id)`

**Связи:**
- `user_roles.user_id` → `users.id`
- `user_roles.role_id` → `roles.id`



## Таблица `bots`

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Уникальный идентификатор бота |
| `owner_id` | UUID | FK → users.id, NOT NULL | Владелец бота |
| `name` | VARCHAR(100) | NOT NULL | Название бота |
| `slug` | VARCHAR(100) | UNIQUE, NOT NULL | Уникальный URL-friendly идентификатор |
| `status_id` | UUID | FK → status_bot.id, NOT NULL | Текущий статус бота |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Дата создания |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Дата последнего изменения |

**Связи:**
- `bots.owner_id` → `users.id`
- `bots.status_id` → `status_bot.id`
- `bots.current_version_id` → `bot_versions.id`
- `bots.id` → `bot_versions.bot_id`



## Таблица `bot_versions`

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Уникальный идентификатор версии |
| `bot_id` | UUID | FK → bots.id, NOT NULL | Идентификатор бота |
| `version` | INTEGER | NOT NULL | Номер версии |
| `artifact_url` | TEXT | NULL | Ссылка на собранный артефакт |
| `entrypoint` | VARCHAR(255) | NOT NULL | Точка входа приложения |
| `runtime` | VARCHAR(50) | NOT NULL | Среда выполнения, например `python` |
| `runtime_version` | VARCHAR(20) | NOT NULL | Версия runtime, например `3.12` |
| `config` | JSONB | NULL | Конфигурация версии бота |
| `status_id` | UUID | FK → status_build_bot.id, NOT NULL | Статус сборки |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Дата создания версии |

**Ограничения:**
- `UNIQUE(bot_id, version)`

**Связи:**
- `bot_versions.bot_id` → `bots.id`
- `bot_versions.status_id` → `status_build_bot.id`



## Таблица `status_bot`

Справочник статусов бота.

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Уникальный идентификатор статуса |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL | Название статуса |
| `description` | TEXT | NULL | Описание статуса |

**Примеры статусов:**
- `draft` — бот создан, но ещё не запущен
- `active` — бот работает
- `paused` — бот приостановлен
- `error` — произошла ошибка
- `archived` — бот архивирован

**Связи:**
- `status_bot.id` → `bots.status_id`



## Таблица `status_build_bot`

Справочник статусов сборки версии бота.

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Уникальный идентификатор статуса |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL | Название статуса |
| `description` | TEXT | NULL | Описание статуса |

**Примеры статусов:**
- `draft` — версия подготовлена
- `building` — выполняется сборка
- `ready` — сборка успешно завершена
- `failed` — сборка завершилась ошибкой

**Связи:**
- `status_build_bot.id` → `bot_versions.status_id`
