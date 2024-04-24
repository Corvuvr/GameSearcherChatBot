import Scripts.askGptForGame as askGptForGame
import Scripts.gameParserWeb as gameParserWeb
import Scripts.getGenres as getGenres

import json

sep: str = '-' * 50

def simulateSalebot() -> None:
    # Это - симуляция user-story при использовании Salebot.
    # Я бы мог просто скинуть ссылку на бота, но у меня закончилась подписка на сервис...
    with open("Files/launchParams.json", "r") as file: 
        # В launchParams будут храниться примеры данных, которые Salebot передаёт в скрипты.
        launchParams: dict  = json.load(file)

    # Пользователь хочет найти игру по интересующим его критериям, но перед этим хочет узнать, 
    # игры каких жарнов доступны для поиска. Он нажимает соответствующую кнопку в чат-боте
    # и Salebot ищет в файле getGenres.py функцию handle(data) и вызывает её: 
    getGenresReply: str = getGenres.handle(
        # Мы используем json.dumps(), поскольку симулируем взаимодействие с Salebot, 
        # который таким образом передаёт данные в скрипт.
        json.dumps(launchParams["Query 0"])
    )
    # Пользователь получил ответ от чат-бота:
    print(f'{sep}\nGenres availile: {getGenresReply}\n{sep}')
    # Пользователь заполнил форму, выбрав понравившиеся ему жанры.
    gameParserReply: str = gameParserWeb.handle(
        json.dumps(launchParams["Query 1"])
    )
    # Затем пользователь получил ответ:
    print(f'{gameParserReply}\n{sep}')
    # В завершение, пользователь решил узнать, существует ли какая-нибудь игра, 
    # похожая на ту, что ему когда-то очень понравилась:  
    yagptReply: str = askGptForGame.handle(
        json.dumps(launchParams["Query 2"])
    )
    # Подключённый YaGPT ответит на его вопрос, если Python найдёт в базе с играми похожее название.
    print(f'{sep}\n{yagptReply}\n{sep}')
    
if __name__== "__main__":
    simulateSalebot() 