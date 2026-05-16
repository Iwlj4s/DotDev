# DotDev Frontend (Vue 3 + TypeScript)

## Установка и запуск

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Перейти на `http://localhost:5173`.

## Адаптация к API

- Отредактируйте `VITE_API_BASE_URL` в `.env`.
- Эндпоинты и модели находятся в `src/api/` и `src/stores/`.
- Если бэкенд использует cookie-based auth — `withCredentials: true` в `src/api/client.ts`.

## OAuth: использование фронтенд callback (recommended for local dev)

По умолчанию OAuth может редиректить на бэкенд, который сам ставит cookie и делает редирект на фронт. Для более надёжного локального флоу можно настроить GitHub OAuth так, чтобы он редиректил на фронтенд — тогда фронтенд примет `code` и отправит его в бэкенд через `POST /api/v1/github_auth/login`.

Шаги для этого варианта:

- В GitHub OAuth App укажите `Authorization callback URL` как `http://127.0.0.1:5173/auth/callback` (или `http://localhost:5173/auth/callback`, но используйте один и тот же хост везде).
- В бэкенде в `.env` установите `REDIRECT_URI` равным тому же URL (если бэкенд использует REDIRECT_URI при формировании ссылки на GitHub).
- После успешного редиректа GitHub вернёт пользователя на `http://127.0.0.1:5173/auth/callback?code=...`. Фронтенд автоматически отправит `code` в бэкенд и затем вызовет `GET /api/v1/users/me/` для получения информации о текущем пользователе.

В этом репозитории уже реализован маршрут `src/pages/AuthCallback.vue`, который выполняет этот обмен и сохраняет минимальное состояние в `localStorage`.

## Что настроить

- `VITE_API_BASE_URL` — URL вашего бэкенда.
- Эндпоинты: `/api/v1/users/me/`, `/api/v1/projects/`, `/api/v1/users/user/{id}`.
- Поля сущностей (в сторе) подгонять под ответы бэкенда.
