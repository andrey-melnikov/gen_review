**EN/RU**

###EN:
  **What is it:** gen-review is an API for generating relevant reviews from google play apps.
  **How it works:** Runs of NGINX and python. You enter your game id and press generate button. The tool looks for apps that are similar to yours and parses reviews from it.
  You can filter those reviews by date, length, language and rating.
  In the end you get thouthands of reviews that are relevant to your target app.
  For example if your app is racing game then the tool will parse reviews from similar racing games.
  **Who might need this:** componies that sells fake reviews. If they want to decrease the deletions of their fake reviews in the google play then they need to make their reviews more 'human' and realistic.
  Fake reviews are often like this: "Cool app!" or "Love it! Woow" and so on. With my API you can generate realistic reviews like: "Love this app. Tried it month ago and it was so laggy and annoying but now it pretty good. The image editing is laggyin though".
  This way conpanies can decrease the percentage of deleted reviews by bot detection of Google and improve the quality of their service.
###RU:
  **Что это:** gen-review это API для генерации релевантных отзывов для приложений в Google Play.
  **Как это работает:** работает на NGINX и python. Вы указываете своё приложение, нажимаете кнопку сгенерировать отзывы.
  Программа смотрит приложения, которые похожи на ваше и копирует из них отзывы.
  Вы можете отфильтровать отзывы по дате, рейтингу, языку и длине.
  В конце вы получаете тысячи релевантных отзывов для своего приложения.
  **Пример: если ваше приложение - игра про гонки, то программа сама определит тип приложения и просмотрит игры с гонками и скопирует из них отзывы.
  Кому это может пригодиться:** компаниям, продающим фейковые отзывы для приложений Google Play. Если они хотят уменьшить процент удалений их фейковых отзывов со страниц в Google Play то тогда они должны сделать их отзывы более человеческими и реалистичными.
  Фейковые отзывы обычно выглядят так: "Классное приложение!". "Нравится вау" и так далее. С моим API можно генерировать огромное количество уникальных реалистичных отзывов: "Нравится это приложение, пробовал его месяц назад и подлагивало. Хотя щас вроде норм. Правда редактирование изоражении немножк глючит"
  Таким образом компании могут уменьшить процент удаления их отзывов Гуглом и улучших своё сервис
