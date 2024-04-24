import pandas as pd
import json

class GameInfo(object):
    def __init__(self, 
                 name = "", 
                 metacritic = 0, 
                 releaseDate1 = 1900, 
                 releaseDate2 = 2024, 
                 genres = set()):
        self.name = name
        self.metacritic = metacritic
        self.releaseDate = {'first_year' : releaseDate1, 'last_year' : releaseDate2}
        self.genres = genres
    def printGame(self) -> None:
        print(f'{self.name = }\n{self.metacritic = }\n{self.releaseDate['first_year'] = }\n{self.genres}\n')

def metacriticError(observed : int, predicted : int) -> float:
    # Отклонение действительной оценки от искомой - от 0 до 1
    predicted: float = (predicted + 100) / 2
    return abs((observed - predicted)/100)

def compareGenres(observed : set, predicted : set) -> float:
    # Процент отклонения действителельных жанров от искомых - от 0 до 1
    predictedSize: int = len(predicted)
    entryCount = 0
    for element in observed:
        entryCount += 1 if element in predicted else 0
    result: float = 1 - (min(entryCount, predictedSize)/predictedSize)
    return result

def releasedInRange(yearReleased : int, year1 : int, year2 : int) -> int:
    # Вышла ли игра в указанном диапазоне - 0 или 1
    firstYear = min(year1, year2)
    lastYear = max(year1, year2)
    return int(yearReleased >= firstYear and yearReleased <= lastYear)

def getGetTheMostSimilarRowFromTable(inputData : dict) -> str:
    # Загружаем критерии в объект
    gameToSearch = GameInfo(
        name="", 
        metacritic=int(inputData["Metacritic"]), 
        releaseDate1=int(inputData["Year 1"]), 
        releaseDate2=int(inputData["Year 2"]), 
        genres=set(str(inputData["Genres"]).replace(" ", "").lower().split(sep=","))
        )
    # Объявляем аналитические данные
    similarity = 0
    currentSimilarity = 0
    theMostSimilarRowId = 0
    # Загружаем датасет
    dataFrame = pd.read_csv(
        inputData["TableLocation"], 
        encoding = "utf-8", 
        sep=',',
        dtype={'id': 'Int64','name': 'string', 'metacritic': 'Int64', 'genres' : 'string'}, 
        parse_dates=['released'], 
        on_bad_lines='skip', 
        dayfirst=True
        )
    dataFrame['metacritic'] = dataFrame['metacritic'].fillna(0)
    # Ищем похожие игры
    for rowId in dataFrame.index:
        try:
            # Загружаем табличные знаечния в объект
            current_game = GameInfo(
                name=dataFrame['name'][rowId], 
                metacritic=dataFrame['metacritic'][rowId], 
                releaseDate1=pd.to_datetime(dataFrame['released'][rowId], dayfirst=True).year,
                releaseDate2=pd.to_datetime(dataFrame['released'][rowId], dayfirst=True).year,
                genres=set(str(dataFrame['genres'][rowId]).lower().split(sep="||"))
                )
            # Оцениваем схожесть
            currentSimilarity = 2 \
                + releasedInRange(
                    yearReleased=current_game.releaseDate['first_year'], 
                    year1=gameToSearch.releaseDate['first_year'], 
                    year2=gameToSearch.releaseDate['last_year']) \
                - compareGenres(current_game.genres, gameToSearch.genres) \
                - metacriticError(current_game.metacritic, gameToSearch.metacritic)
            # Пошагово находим максимально схожую игру
            theMostSimilarRowId = rowId if currentSimilarity > similarity else theMostSimilarRowId
            similarity = currentSimilarity if currentSimilarity > similarity else similarity            
        except:
            continue
    # Выгружаем самую похожую игру из датасета
    gameToSearch = GameInfo(
                    name=dataFrame['name'][theMostSimilarRowId], 
                    metacritic=dataFrame['metacritic'][theMostSimilarRowId], 
                    releaseDate1=pd.to_datetime(dataFrame['released'][theMostSimilarRowId], dayfirst=True).year,
                    releaseDate2=pd.to_datetime(dataFrame['released'][theMostSimilarRowId], dayfirst=True).year,
                    genres=set(str(dataFrame['genres'][theMostSimilarRowId]).lower().split(sep="||"))
                    )
    return (
        "Бот нашёл игру, подходящую под ваше описание:\n" +
        "Название: " + str(gameToSearch.name) + \
        "\nЖанры: " + ", ".join(str(genre) for genre in gameToSearch.genres) + \
        "\nОценка на metacritic: " + str(gameToSearch.metacritic) + \
        "\nДата выхода: " + str(gameToSearch.releaseDate['first_year']) + \
        "\nСхожесть: " + str(similarity*100/3) + "%"
        )

def handle(data) -> str:
    data: dict = json.loads(data)
    return getGetTheMostSimilarRowFromTable(data)