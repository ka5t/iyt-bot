# IYT quiz bot

_Disclaimer: English version may be supported if anyone interested. Most of end-users are russian native, thus docs will be written in kind-of russian._

Телеграм-бот [@IYT_QuizBot](http://t.me/IYT_QuizBot).
Содержит некоторую базу вопросов с вариантами ответов. Помогает выучить МППСС-72, и ряд базовых понятий, необходимых для управления парусным судном.

Просьба репортить найденные ошибки и недочеты в [задачи данного репозитория](https://github.com/justrp/iyt-bot/issues/new)

Если кто-то захочет добавить свои вопросы, это можно сделать через стандартную процедуру пулл-реквестов (или через те же задачи из предыдущей ссылки, или через личку @justrp в телеге).

## Синтаксис файлов с вопросами

**Файл с вопросом должен быть описан в yml-формате; его имя должно заканчиваться на `.yml`, он должен быть размещен в директории [./resources/questions/](resources/questions).**

<!-- sorry for that syntax, but markdown still does not support multiline  code blocks with syntax highlighting in any other way but html with no indentation -->
<table>
<tr>
<th>Имя поля</th>
<th>Тип поля</th>
<th>Комментарий</th>
<th>Пример значения</th>
</tr>
<tr>
<td>question</td>
<td>str</td>
<td>
    
Вопрос. Конфликтует с `image` (должен присутствовать либо вопрос, либо изображение).
</td>
<td>

```yaml
question: Тип вооружение с косым гротом и одним стакселем называется..
```
</td>
</tr>
<tr>
<td>image</td>
<td>str</td>
<td>
    
Имя изоображения. Файл с таким именем должен быть опубликован в директории [resources/imgs](resources/imgs).</td>
<td>
    
```yaml
image: sudno_mech_50m_na_nas.png
```    
</td>
</tr>
<tr>
<td>options</td>
<td>list(str)</td>
<td>Список вариантов ответов (необходимо указать как минимум два; один из вариантов ответов должен быть верным)</td>
<td>

```yml
options:
  - "Кеч"
  - "Йол"
  - "Шлюп"
  - "Тендер"
```
</td>
</tr>
<tr>
<td>correct</td>
<td>str</td>
<td>
    
Правильный вариант ответа. Должен совпадать с одним из вариантов из `options`.
</td>
<td>
    
```yml
correct: "Шлюп"
```
</td>
</tr>
</table>

## Как добавить вопрос, если гитхаб не пугает
* Создать отдельный yml-файл в директории [./resources/questions/](resources/questions). Пример синтаксиса можно подсмотреть в любом соседнем файле.
    * В случае, если создаваемый вопрос - визуальный (состоит из картинки с вариантами ответов), следует разместить изображение в директории [resources/imgs](.resources/imgs)
* Создать пулл-реквест и убедиться, что проверка прошла успешно
