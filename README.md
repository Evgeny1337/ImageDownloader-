
# Загрузчик в Telegram фотографий космоса

## Набор скриптов на Python для работы с изображениями NASA и SpaceX

Этот набор скриптов предоставляет возможность загружать изображения с сайта NASA и SpaceX, а также отправлять их в Telegram-канал. Скрипты используют API NASA, SpaceX и Telegram Bot API для выполнения своих задач.

### Скрипты

1. fetch_nasa_images.py
   - Этот скрипт позволяет загружать фотографии с сайта NASA.
   - Аргументы:
     - -a <Количество изображений>: Загрузить все изображения из архива.
     - -e: Получить изображения Земли из проекта EPIC.

2. fetch_spacex_images.py
   - Этот скрипт позволяет получать изображения из запусков SpaceX.
   - Аргументы:
     - -a <launch_id>: Получить изображения из указанного запуска.
     - -f: Получить изображения из последнего запуска.

3. script.py
   - Этот скрипт агрегирует функционал fetch_nasa_images.py и fetch_spacex_images.py, позволяя запускать их вместе для одновременной загрузки изображений с обоих источников.

4. send_all_tg_image.py
   - Этот скрипт отправляет все скаченные изображения из директории images в указанный Telegram-канал с определённой задержкой.
   - Аргументы:
     - a <Время задержки между отправлениями> Отправляет все скаченные изображение из директории images в указанный Telegram-канал.
   - Скрипт работает только при наличии изображений в директории.
5. send_one_tg_image.py
   - Этот скрипт отправляет одно скаченное изображение из директории images в указанный Telegram-канал.
   - Скрипт работает только при наличии изображений в директории.

### Вспомогательные скрипты

1. downloader.py
   - Содержит функцию для загрузки изображений в папку images и получения имени файла с расширением по его URL.
2. set_tg_chatid.py
   - Запускается в Telegram-чате, куда необходимо отправлять изображения.
   - Бот, токен которого используется, должен быть администратором канала. После отправки команды /savechatid, идентификатор чата будет сохранён в файл .env.

### Зависимости

Для корректной работы скриптов необходимо установить следующие библиотеки:

- `requests====2.32.3` — для выполнения HTTP-запросов.
- `python-telegram-bot==13.0`— для работы с Telegram Bot API.
- `python-dotenv==1.0.1`— для работы с переменными окружения.

Все зависимости находятся в файле requirements.txt:

```bash
   pip install -r requirements.txt:
```

### Настройки .env

Для работы скриптов необходимо создать файл .env в корневом каталоге проекта и добавить в него следующие переменные:
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
NASA_API_KEY=your_nasa_api_key

### Пример использования

1. Загрузка всех изображений NASA:

   ```bash
      python fetch_nasa_images.py -a
   ```

2. Загрузка изображений с последнего запуска SpaceX:

   ```bash
      python fetch_spacex_images.py -f
   ```

3. Запуск всех скриптов для загрузки изображений:

   ```bash
      python script.py
   ```

4. Отправка всех изображений в Telegram:

   ```bash
      python send_all_tg_image.py -a 30
   ```

5. Отправка одного изображения в Telegram (Выбор сулчайного изображения из папки images):

   ```bash
      python send_one_tg_image.py -r
   ```

### Важно

- Убедитесь, что у вас есть доступ к API NASA и SpaceX, и соответствующие ключи API указаны в файле .env.
- Бот должен быть администратором канала для отправки сообщений.
