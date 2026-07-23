# Developer Landing API

Бэкенд-сервис для лендинг-презентации разработчика. Обработка формы обратной связи с AI-интеграцией, email-уведомлениями и метриками.

## Стек технологий

- **Backend**: Python 3.9+, FastAPI, Uvicorn
- **AI**: OpenAI API (GPT-4o-mini)
- **Хранение**: Файловая система (JSON)
- **Логирование**: Loguru
- **Безопасность**: Rate limiting (slowapi), валидация (Pydantic), CORS

## Архитектура

Слойная архитектура:

```
app/
├── api/          # Контроллеры (роутеры)
├── services/     # Бизнес-логика (AI, Email, Metrics, Rate Limit)
├── schemas/      # Pydantic-схемы валидации
├── middleware/   # Логирование запросов, глобальный error handler
├── core/         # Конфиг, логгер, исключения
└── repositories/ # Работа с файловым хранилищем
```

## Как запустить проект

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Скопируйте `.env.example` в `.env` и заполните переменные:
```bash
cp .env.example .env
```

3. Создайте директорию для хранилища:
```bash
mkdir -p storage
```

4. Запустите сервер:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Swagger документация: `http://localhost:8000/docs`

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `APP_NAME` | Название приложения |
| `OPENAI_API_KEY` | Ключ OpenAI API |
| `OWNER_EMAIL` | Email владельца сайта |
| `SMTP_HOST` | SMTP хост |
| `SMTP_PORT` | SMTP порт |
| `SMTP_USER` | SMTP пользователь |
| `SMTP_PASSWORD` | SMTP пароль |
| `SMTP_FROM_EMAIL` | Отправитель |
| `CORS_ORIGINS` | Разрешенные origins через запятую |

## Реализация API

### POST /api/contact
Отправка формы обратной связи.

**Request:**
```json
{
  "name": "Иван",
  "phone": "+998901234567",
  "email": "ivan@example.com",
  "comment": "Хочу заказать сайт"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Иван",
    "phone": "+998901234567",
    "email": "ivan@example.com",
    "comment": "Хочу заказать сайт"
  },
  "ai": {
    "sentiment": "positive",
    "category": "sales",
    "auto_reply": "Здравствуйте! Спасибо за интерес к нашим услугам."
  }
}
```

**Обработка ошибок:**
- `422` — валидационные ошибки
- `429` — rate limit превышен
- `500` — внутренняя ошибка сервера

### GET /api/health
Проверка статуса сервиса.

```json
{ "status": "ok" }
```

### GET /api/metrics
Статистика обращений.

```json
{
  "total_requests": 14,
  "positive": 0,
  "negative": 0,
  "general": 14
}
```

### GET /
Health check для корня.

```json
{ "message": "API Working" }
```

## AI-интеграция

**Инструмент**: OpenAI API (модель `gpt-4o-mini`)

**Функции AI:**
1. Анализ тональности комментария
2. Автоматическая генерация ответа
3. Классификация типа запроса (support/sales/general)

**Промпт:**
```
Analyze this customer message. Return ONLY valid JSON:
{"sentiment": "positive/negative/neutral", "category": "support/sales/general", "auto_reply": "short polite reply"}
```

**Graceful fallback:**
Если AI недоступен или API ключ не настроен, возвращается дефолтный ответ:
```json
{
  "sentiment": "unknown",
  "category": "general",
  "auto_reply": "Thank you for contacting us."
}
```
Сервис продолжает работать, отправляет email и обновляет метрики.

## Хранение данных

- **Логи запросов**: `storage/requests.log` (Loguru, ротация 10MB)
- **Метрики**: `storage/metrics.json` (JSON-файл)
- **Rate limiting**: в памяти (slowapi) с ключом по IP
- **База данных**: не используется

## Обработка ошибок

Глобальный `ExceptionHandler` возвращает `500` с стандартизированным ответом. Все сервисные ошибки логируются в файл. Отдельные catch-блоки защищают AI и email-отправку от падения основного потока.

## Безопасность

- Валидация всех входных данных через Pydantic
- Rate limiting: 5 запросов в минуту на IP
- CORS настроен через переменные окружения
- SMTP-учетные данные не коммитятся (в `.gitignore`)

## Что сделано с помощью AI

При генерации кода использовался AI для:
- Структурирования архитектуры по слоям
- Написания boilerplate для FastAPI роутов
- Формирования промптов для OpenAI
- Документации README

Вручную доработано:
- Интеграция email-сервиса
- Обработка edge-cases в метриках
- Настройка CORS и exception handler'ов
- Switch с Gemini на OpenAI из-за отсутствия пакета в зависимостях
