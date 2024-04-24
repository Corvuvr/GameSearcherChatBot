from difflib import SequenceMatcher
import pandas as pd
import json

def fromMarkdownToPlainText(mdText : str) -> str:
    # Подключить недостающие библиотеки:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    from markdown import markdown
    from bs4 import BeautifulSoup
    # Обработать текст, сначала из markdown в html
    html = markdown(str(mdText)) 
    # Затем из html в string
    return ''.join(BeautifulSoup(html, features="html.parser").findAll(text=True)).replace("\n\n\n", "\n\n") 

def isGame(query : str, tableLocation: str) -> bool:
    # Является ли запрос названием игры? Защищает ресурсы от использования не по назначению
    data_frame = pd.read_csv(
        tableLocation, 
        encoding = "utf-8", 
        sep=',',
        dtype={'id': 'Int64','name': 'string'}, 
        on_bad_lines='skip'
        )
    for row_id in data_frame.index:
        try:
            dataframe_game = str(data_frame['name'][row_id]).lower()
            ratio = SequenceMatcher(None, dataframe_game, query).ratio()
            if ratio > 0.5: return True
        except:
            continue
    return False

def askGPT(query : str, tableLocation: str = None, yandexCloudId: str = None, yagptSecretKey: str = None) -> str:
    if not isGame(query, tableLocation): 
        return """К сожалению, запрашиваемая вами игра не найдена. 
        Проверьте, правильно ли вы ввели название."""
    # Собираем запрос
    import pip._vendor.requests
    query = f"Посоветуй мне игру, похожую на {query}."
    settings = {
        "modelUri": "gpt://b1gv4pt48kbp38ach7ef/yandexgpt-lite",
        "completionOptions": {
            "stream": False, # Синхронный/Асинхронный режимы
            "temperature": 0.1, # Насколько подробно отвечает. Варьируется от 0 до 1 
            "maxTokens": "2000" # Макс кол-во токенов
        },
        "messages": [
            {
                "role": "system",
                "text": query
            }
        ]
    }
    headers = {
        "x-folder-id": yandexCloudId, # Мой ID на яндекс облаке
        "Authorization": yagptSecretKey # Не трогать тут секретный ключ, если потеряем, то пизда рулям
    }
    # Отправляем, получаем ответ
    response = pip._vendor.requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion", 
        headers=headers, 
        json=settings
    )
    # Обрабатываем в сплошной текст и возвращаем
    return fromMarkdownToPlainText(json.loads(response.text)["result"]["alternatives"][0]["message"]["text"])

def handle(data) -> str:
    # Функция принимает данные от конструктора Salebot 
    data = json.loads(data)
    query = str(data["Game"]).lower()
    return askGPT(query, data["TableLocation"], data["YandexCloudId"], data["YaGPTSecretKey"])