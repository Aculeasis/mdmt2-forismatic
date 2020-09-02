# Пример плагина для [mdmTerminal2](https://github.com/Aculeasis/mdmTerminal2)
Содержит комментарии в [main.py](main.py)

При публикации плагина на GitHub рекомендую добавить к нему топик `mdmterminal2-plugin` - так его будет проще [найти](https://github.com/topics/mdmterminal2-plugin).
# Установка
```
cd mdmTerminal2/src/plugins
git clone https://github.com/Aculeasis/mdmt2-forismatic
```
И перезапустить терминал.
# Описание
Плагин получает случайное высказывание с сайта http://forismatic.com и проговаривает его:
- Если терминал был неактивен 12 часов.
- В ответ на фразу `скажи афоризм` или `расскажи афоризм`.

Работает только если язык терминала русский.
