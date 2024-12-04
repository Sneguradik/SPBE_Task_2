# Taks 2 Парсер акций

## Описание работы парсера

Второй парсер предназначен для извлечения данных с сайта Yahoo Finance. Поскольку API Yahoo Finance больше недоступно, вместо него используется сервис [Alpha Vantage](https://www.alphavantage.co/), предоставляющий аналогичные данные.

Парсер получает рассчитанные показатели для выбранных тикеров (например, цены открытия, закрытия, объемы торгов и другие метрики). Однако важно учитывать ограничения Alpha Vantage:

- Лимит 25 запросов в день.

Данные сохраняются в формате CSV в указанной пользователем директории или в директории по умолчанию.

---

## Инструкция по сборке

1. **Склонировать репозиторий:**
   ```bash
   git clone <URL_вашего_репозитория>
   cd <название_папки_репозитория>
2. **Создать виртуальное окружение:**
    ```bash
    python -m venv .venv
    ```
3. **Активировать виртуальное окружение:**
   - На Windows:
       ```bash
     .venv\Scripts\Activate
     ```
- На MacOS/Linux:
    ```bash
    source venv/bin/activate
    ```
4. **Установить зависимости:**
    ```bash
   pip install -r requirements.txt
   ```
5. **Создать файл `.env` в корневой папке проекта и добавить ваш API ключ:**
    ```dotenv
   Alpha_Vantage_API_Key=ВАШ_API_КЛЮЧ
   ```
6. **Включение/выключение api парсера:**
    В `main.py` раскомментировать эти строчки
    ```python
   ...
   async def main(args):
    ...
    #api_data = await api_main(tickers, os.getenv('Alpha_Vantage_API_Key'))
    ...
    #df_api = DataFrame(api_data)
    ...
    #df_api.to_csv(os.path.join(args.output, 'stats/page_api.csv'))

   ```
---
## Инструкция по запуску
Для запуска парсера используйте следующую команду:
```bash
python main.py [-i ПУТЬ_К_CSV] [-o ПУТЬ_ДЛЯ_СОХРАНЕНИЯ]
```

### Аргументы:
- `-i` (необязательно) — путь к CSV файлу с тикерами.
По умолчанию: `data/tickers.csv`.

- `-o` (необязательно) — путь для сохранения результата работы.
По умолчанию: `data`.

---
## Пример файла tickers.csv
```csv
Tickers
MSFT
AAPL
```
---
## Примеры запуска
1. Использование значений по умолчанию:
    ```bash
    python main.py
   ```
2. Указание пути к входному файлу:
    ```bash
   python main.py -i custom_folder/custom_tickers.csv
   ```
3. Указание пути для сохранения результата:
    ```bash
   python main.py -o output_folder
   ```
4. Указание обоих аргументов:
    ```bash
   python main.py -i custom_folder/custom_tickers.csv -o output_folder
    ```