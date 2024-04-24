import pandas as pd
import json

def getGenres(tableLocation: str) -> str:
    # Возвращает жанры, по которым можно производить поиск в таблице
    genres = set()
    dataFrame = pd.read_csv(
        tableLocation, 
        encoding = "utf-8", 
        sep=',',
        dtype={'id': 'Int64','name': 'string'}, 
        on_bad_lines='skip'
        )
    for rowId in dataFrame.index:
        genres.update(set(str(dataFrame['genres'][rowId]).lower().split(sep="||")))
    genres.discard("nan")
    # Сортируем полученный сет
    genres = tuple(genres)
    return ', '.join(str(genre).capitalize() for genre in genres)

def handle(data):
    return getGenres(json.loads(data)["TableLocation"])