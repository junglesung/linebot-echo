# Text Line Bot

This is a very simple [Line bot](https://developers.line.me/en/docs/messaging-api/overview/) writen in [Python](https://www.python.org/) and executed on [Heroku](https://www.heroku.com/). 

## Getting started

Change to your channel secret and access token.

```
LINE_CHANNEL_SECRET = 'YOUR_LINE_CHANNEL_SECRET'
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN'
```

Reply the same words

```
line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
```

or say something to yourself

```
line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Say something'))
```

## Reference
### Line bot

[Tutorial](https://devcenter.heroku.com/articles/getting-started-with-python)

[Source code](https://github.com/line/line-bot-sdk-python)

### Heroku

[Tutorial](https://devcenter.heroku.com/articles/getting-started-with-python)

[Source code](https://github.com/heroku/python-getting-started)

### Flask

[Web site](http://flask.pocoo.org/)
