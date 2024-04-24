# GameSearcherChatBot
Бэкэнд для чат-бота, который ищет игры по описанию. Учебный проект. 
## Что это

В рамках университетского задания сделал бота на базе конструктора Salebot.

Бот может:
- Искать игру в базе данных по трём критериям: жанрам, дате выхода и оценке на metacritic.
- Запрашивать у YaGPT2 игру, похожую на названную.

![Gif Demo]([https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif](https://github.com/Corvuvr/GameSearcherChatBot/blob/main/Files/demo.gif))

У меня закончилась подписка на сервис - по этой причине, 
чтобы сымитировать работу сервиса Salebot, я написал тест simulateBotTest.py.
Но код может выполняться и самостоятельно - пример в simpleScenarioTest.py.

## Как Запустить

1. Установить _зависимости_ из `requirements.txt`.
2. Получить ___секретный ключ___ и свой ___id пользователя___ для доступа к YandexGPT.
3. Ввести эти данные в:
	- `launchParams.json`, если хотите запустить `simulateBotTest.py`.
	- `simpleScenarioTest.py`, если хотите запустить `simpleScenarioTest.py`.
1. Запустить тесты.
