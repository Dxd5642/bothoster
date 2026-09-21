# Таблица API-эндпоинтов для User и Admin

`/auth` - регистрация, вход и управление автоирзацией
`/users` - профиль и потзовательские функции
`/admin` - администрирование и управление платформой

## Условные обозначения
| Обозначение | Значение                                       |
| ----------- | ---------------------------------------------- |
| Public      | Доступен без авторизации                       |
| User        | Только авторизованный пользователь             |
| Owner       | Пользователь работает только со своими данными |
| Admin       | Администратор                                  |

---

## Auth - авторизация и управление сессиями
| Метод    | Endpoint                      | Доступ | Описание                                       |
| -------- | ----------------------------- | ------ | ---------------------------------------------- |
| `POST`   | `/auth/registration`              | Public | Регистрация пользователя                       |
| `POST`   | `/auth/login`                 | Public | Вход, создание Redis-сессии, установка cookie  |
| `POST`   | `/auth/logout`                | User   | Выход из текущей сессии                        |
| `GET`    | `/auth/me`                    | User   | Получить текущего авторизованного пользователя |
| `POST`   | `/auth/forgot-password`       | Public | Запросить сброс пароля                         |
| `POST`   | `/auth/verify-email`          | Public | Подтвердить email                              |
| `POST`   | `/auth/resend-verification`   | Public | Повторно отправить подтверждение email         |
| `POST`   | `/auth/change-password`       | User   | Сменить пароль                                 |
| `GET`    | `/auth/sessions`              | User   | Список активных сессий                         |
| `DELETE` | `/auth/sessions/{session_id}` | Owner  | Завершить одну свою сессию                     |
| `POST`   | `/auth/logout-all`            | User   | Завершить все свои сессии                      |

---

## Users - профиль и настройки пользователя
| Метод    | Endpoint                                    | Доступ | Описание                              |
| -------- | ------------------------------------------- | ------ | ------------------------------------- |
| `GET`    | `/users/me`                                 | User   | Получить свой профиль                 |
| `PATCH`  | `/users/me`                                 | User   | Изменить профиль                      |
| `DELETE` | `/users/me`                                 | User   | Удалить аккаунт / запросить удаление  |
| `GET`    | `/users/me/settings`                        | User   | Получить настройки                    |
| `PATCH`  | `/users/me/settings`                        | User   | Изменить настройки                    |


---

## Admin - Управление пользователями
| Метод    | Endpoint                                | Доступ | Описание                                                |
| -------- | --------------------------------------- | ------ | ------------------------------------------------------- |
| `GET`    | `/admin/users`                          | Admin  | Список пользователей                                    |
| `GET`    | `/admin/users/{user_id}`                | Admin  | Подробная информация о пользователе                     |
| `PATCH`  | `/admin/users/{user_id}`                | Admin  | Изменить разрешённые поля пользователя                  |
| `DELETE` | `/admin/users/{user_id}`                | Admin  | Удалить / инициировать удаление аккаунта                |
| `POST`   | `/admin/users/{user_id}/ban`            | Admin  | Заблокировать пользователя                              |
| `POST`   | `/admin/users/{user_id}/unban`          | Admin  | Разблокировать пользователя                             |
| `POST`   | `/admin/users/{user_id}/suspend`        | Admin  | Временно ограничить аккаунт                             |
| `POST`   | `/admin/users/{user_id}/unsuspend`      | Admin  | Снять временное ограничение                             |
| `GET`    | `/admin/users/{user_id}/sessions`       | Admin  | Посмотреть метаданные активных сессий                   |
| `DELETE` | `/admin/users/{user_id}/sessions`       | Admin  | Завершить все сессии пользователя                       |
| `GET`    | `/admin/users/{user_id}/audit-log`      | Admin  | История административных действий над аккаунтом         |

## Admin - Управление статистика и мониториг платформы
| Метод | Endpoint                     | Доступ | Описание                         |
| ----- | ---------------------------- | ------ | -------------------------------- |
| `GET` | `/admin/dashboard`           | Admin  | Общая статистика платформы       |
| `GET` | `/admin/stats/users`         | Admin  | Статистика пользователей         |
| `GET` | `/admin/stats/registrations` | Admin  | Статистика регистраций           |
| `GET` | `/admin/stats/sessions`      | Admin  | Статистика активных сессий       |
| `GET` | `/admin/audit-logs`          | Admin  | Журнал административных действий |
| `GET` | `/admin/system/health`       | Admin  | Состояние компонентов системы    |
| `GET` | `/admin/system/metrics`      | Admin  | Метрики приложения               |

## Admin - модерация и поддержка
 | Метод   | Endpoint                                      | Доступ | Описание                              |
| ------- | --------------------------------------------- | ------ | ------------------------------------- |
| `GET`   | `/admin/reports`                              | Admin  | Список жалоб                          |
| `GET`   | `/admin/reports/{report_id}`                  | Admin  | Детали жалобы                         |
| `PATCH` | `/admin/reports/{report_id}`                  | Admin  | Изменить статус жалобы                |
| `POST`  | `/admin/reports/{report_id}/resolve`          | Admin  | Закрыть жалобу                        |
| `GET`   | `/admin/support/tickets`                      | Admin  | Список обращений                      |
| `GET`   | `/admin/support/tickets/{ticket_id}`          | Admin  | Просмотр обращения                    |
| `PATCH` | `/admin/support/tickets/{ticket_id}`          | Admin  | Изменить статус/назначить исполнителя |
| `POST`  | `/admin/support/tickets/{ticket_id}/messages` | Admin  | Ответить на обращение                 |
