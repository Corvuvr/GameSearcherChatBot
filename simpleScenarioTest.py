import Scripts.askGptForGame as askGptForGame
import Scripts.gameParserWeb as gameParserWeb
import Scripts.getGenres as getGenres

import json

sep: str = '-' * 50

def simpleScenario():
    # ЭТО ПРИМЕР - ВВЕДИТЕ СОБСТВЕННЫЕ ДАННЫЕ И НИКОМУ НЕ ПОКАЗЫВАЙТЕ
    yandexCloudId = "dfrfds67ds4ds98dxf" 
    yaGPTSecretKey = "Api-Key dsashdjDKLHDFSLDSkfdljdfsaLDSKFJSDwF"
    # Ссылки на Google Sheets тоже работают (благодаря pandas) - так я подключал таблицу к Salebot, 
    # поскольку последний работает по принципу SaaS и не предлагает инфраструктуры как таковой.
    tableLocation = f"https://docs.google.com/spreadsheets/d/1A-BC10LGm-SY6OC-y_Vm8SUw3Q0g4NJIBFbazzqYhEo/export?format=csv"

    query1 = { "TableLocation": tableLocation }
    query2 = {
        "Metacritic": 70, 
        "Year 1": 2001, 
        "Year 2": 2010, 
        "Genres": "Action, RPG", 
        "TableLocation": tableLocation
    }
    query3 = {
        "Game": "Divinity 2 Ego draconis", 
        "TableLocation": tableLocation,  
        "YandexCloudId": yandexCloudId,
        "YaGPTSecretKey": yaGPTSecretKey
    }

    getGenresReply: str  = getGenres.handle(json.dumps(query1))
    gameParserReply: str = gameParserWeb.handle(json.dumps(query2))
    yagptReply: str      = askGptForGame.handle(json.dumps(query3))

    print(f'{sep}\nGenres availile: {getGenresReply}\n{sep}\n{gameParserReply}\n{sep}\n{yagptReply}\n{sep}')

if __name__== "__main__":
    simpleScenario() 