~~Отправил видео проблемы в слаке, помимо этого:~~
######_Сделано!_

Нужно прибить футер, не красиво, когда он оказывается наверху страницы
######_Сделано!_

~~Вкладка создать рецепт не подчёркивается синей чёрточкой~~
######_Сделано!_

~~Письмо о сбросе пароля не приходит(~~
######_Сделано!_

Страницы из футера лучше тоже унаследовать от базового шаблона, но это уже на ваш вкус

~~Почему-то не правильно отображается кол-во покупок: https://ibb.co/pJXFc0V~~
######_Сделано!_

~~А ещё если удалить при этом, то получится вот такое: https://ibb.co/30XHBs7~~
######_Сделано!_

**Кнопка отписаться от автора срабатывает не с первого раза (странно)
И удаление из избранного нажатием на звездочку срабатывает не с первого раза
3 и 4 пункты довольно странные, потому что страница на микросекунду перезагружается, появляется чистый html, затем опять появляются стили**
###### _Заменил всю статику и JS скрипты на прилагаемую в задании! Пока не помогло._ 

**https://ibb.co/HXHZVFL по поводу футера, мне кажется он должен быть растянут на всю страницу и находиться в самом низу, по-крайней мере, по макетам так**

~~Вкладка "Создать рецепт" - не подчёркивается синим, когда активна~~
######_Сделано!_

~~При редактировании рецепта пропадают все ингредиенты~~
######_Сделано!_

~~Кнопка создать аккаунт должна находиться справа~~
######_Сделано!_

~~При отсутствии покупок - цифра 0 не должна показываться~~
######_Сделано!_

~~Нужно добавить или скинуть мне логин пароль от стафф юзера, чтобы я мог посмотреть админку~~
######_Сделано!_

~~Судя по макетам - кнопка "Создать аккаунт" должна быть синей~~
######_Сделано!_


~~Нужно загрузить больше рецептов, чтобы можно было потестить pagination~~

###### _Сделано!_

~~Шаблоны об авторе и технологии лучше тоже наследовать от базового~~

###### _Сделано!_

~~Футер немного уезжает, если контент страницы пустой, например, если перейти в подписки, когда их нет, футер практически сразу под навигацией, лучше его прибить к низу страницы~~
###### _Сделано!_

~~Текущая вкладка должна иметь под собой синюю полоску и синий цвет шрифта, сейчас это работает только на главной~~

###### _Сделано!_

~~При заполнении ингредиентов должен появляться выпадающий список с автодополнением~~
###### _Сделано!_

Выпадающий список появляется. Если поставить пробел получим весь список.
Если букву/буквы получим список содержащий эту букву/буквы.
Немного не понял что значит "список с автодополнением"?

~~При указании отрицательного значения времени приготовления выпадает ошибка, убедитесь, что это значение больше или равно нулю, должно быть строго больше нуля.~~
###### _Сделано!_

Выпадает ошибка "Убедитесь, что это значение больше либо равно 1." 

~~Если указать несуществующий ингредиент (а можно указать любой. т.к выпадающего списка нет), то происходит 404 ошибка~~
###### _Сделано!_

Сейчас реализована следующая логика:
1. Если вводим букву/буквы JS присылает ответ на запрос со списком доступных ингредиентов. Вибираем, добавляем.
2. Если вводим пробел, получаем весь список доступных ингредиентов.
3. Если ничего не вводится (попытка создать рецепт без ингредиентов) и нажимается кнопка “Создать рецепт“, то в форме подсвечивается красным  ошибка: “Необходимо указать хотя бы один ингредиент для рецепта”
4. Если добавляется не существующий в списке ингредиент, а после этого нажимается кнопка “Создать рецепт“, то появляется ошибка 'Необходимо выбирать ингредиент из выпадающего списка'

Если должно работать по другому, прошу направить где посмотреть, в ТЗ этого не нашел.

~~Можно создать рецепт без ингредиентов~~
###### _Сделано!_
При попытке сделать рецепт без ингредиентов появляется ошибка "Необходимо указать хотя бы один ингредиент для рецепта"

Во время переключения между страницами на мгновение видна страница без стилей, не уверен в чём может проблема, но скорее всего что-то с nginx
Проверил порядок загрузки стилей, нигде не нашел нарушений.
Google тоже не помог. Написал в чат группы, может наставники подскажут.


~~Ссылка на автора со страницы рецепта некликабельна~~

###### _Сделано!_

Ссылка кликабельна, ведет на страницу автора рецепта.