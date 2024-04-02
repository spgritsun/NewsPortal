from main.models import *

# 1. Создать двух пользователей
user1 = User.objects.create_user('Алоизий Могарыч')
user2 = User.objects.create_user('Иван Бездомный')

# 2. Создать два объекта модели Author, связанные с пользователями.
auth1 = Author.objects.create(user=user1)
auth2 = Author.objects.create(user=user2)

# Добавить 4 категории в модель Category.
cat1 = Category.objects.create(category_name='Спорт')
cat2 = Category.objects.create(category_name='Образование')
cat3 = Category.objects.create(category_name='Наука')
cat4 = Category.objects.create(category_name='Политика')

# 2. Добавить 2 статьи и одну новость
post1 = Post.objects.create(author=auth1, is_news=False, post_headline='Развитие молодежного футбола в России',
                            post_text='История российского футбола началась еще в конце 19 ... В данной работе '
                                      'анализируются деятельность государства по созданию таковых условий, а также уже достигнутые успехи и существующие проблемы и перспективы.')
post2 = Post.objects.create(author=auth2, is_news=False, post_headline='Внедрение ИИ в образовательные технологии',
                            post_text='Диагностика коммуникативных навыков'
                                      'с использованием ИИ может быть полезной в обучении и развитии сейлз-менеджеров, педагогов и других специалистов, в чьей работе много коммуникации. Эксперт в пример привёл'
                                      'проект, в котором по аудиозаписи встречи или совещания пытались измерить коммуникативные навыки участников.')

post3 = Post.objects.create(author=auth1, is_news=True, post_headline='Уверенная победа Дональда Трампа',
                            post_text='Новость последних минут из США: соперница Дональда'
                                      'Трампа Никки Хейли объявила о своем выходе из предвыборной гонки. Тем самым она признала сокрушительное поражение по итогам «супервторника», когда праймериз прошли сразу в 15 штатах.')

# 3. Присвоение категорий статьям и новости.
post1.categories.add(cat1)
post2.categories.add(cat2, cat3)
post3.categories.add(cat4)

# 4. Создание комментариев к постам.
# 4.1 Сначала создадим дополнительных пользователей для большего разнообразия комментариев. Они не будут авторами.
user3 = User.objects.create_user('Васисуалий Лоханкин')
user4 = User.objects.create_user('Варфоломей Коробейников')
user5 = User.objects.create_user('Эрнест Щукин')

# 4.2 Создадим комментарии к постам.
com1 = Comment.objects.create(post = post1, user = user3, comment_text = 'Верной дорогой идёте, товарищи!')
com2 = Comment.objects.create(post = post2, user = user4, comment_text = 'До чего дошёл прогресс!')
com3 = Comment.objects.create(post = post3, user = user5, comment_text = 'Даёшь Трампа! Трамп -наш президент!')
com4 = Comment.objects.create(post = post2, user = user1, comment_text = 'Круто! Так держать!')
com5 = Comment.objects.create(post = post1, user = user2, comment_text = 'Спартак - чемпион!')

# 5 Применяем функции like(), dislike() к постам и комментариям.
# 5.1 корректируем рейтинги постов.
post1.like()
post1.like()
post1.like()
post1.dislike()
post2.dislike()
post2.dislike()
post2.like()
post2.like()
post2.like()
post3.like()
post3.like()
post3.like()
post3.like()
post3.dislike()
# 5.2 корректируем рейтинги комментариев.
com1.like()
com1.like()
com1.like()
com2.like()
com2.dislike()
com3.dislike()
com4.dislike()
com4.like()
com4.like()
com4.like()
com5.like()
com5.like()
com5.like()
com5.dislike()

# 6. Обновляем рейтинг пользователей.
auth1.update_rating()
auth2.update_rating()

# 7. Выводим рейтинг лучшего автора.
best_auth = Author.objects.order_by('-author_rating').first()
>>> best_auth.user
<User: Алоизий Могарыч>

# 8. Выводим дату добавления, имя автора, рейтинг, заголовок и превью лучшего поста.
best_post = Post.objects.all().order_by('post_rating').last()

# 8.1 Дата добавления поста
>>> best_post.post_time
datetime.datetime(2024, 4, 2, 8, 0, 36, 208207, tzinfo=datetime.timezone.utc)
# 8.2 Имя автора
>>> best_post.author.user
<User: Алоизий Могарыч>
# 8.3 Рейтинг поста
>>> best_post.post_rating
3
# 8.4 Заголовок поста
>>> best_post.post_headline
'Уверенная победа Дональда Трампа'
# 8.5 Превью поста
>>> best_post.preview()
'Новость последних минут из США: соперница Дональда Трампа Никки Хейли объявила о своем выходе из предвыборной гонки. Тем сам...'

# 9. Все комментарии к лучшему посту.
>>> b_p_comments = best_post.comment_set.values('comment_time', 'user', 'comment_rating','comment_text')
>>> b_p_comments
<QuerySet [{'comment_time': datetime.datetime(2024, 4, 2, 9, 13, 9, 861545,
                tzinfo=datetime.timezone.utc), 'user': 5, 'comment_rating': -1, 'comment_text': 'Даёшь Трампа! Трамп -наш президент!'}]>
# 9.1 Дата и время комментария к лучшему посту (он единственный).
>>> b_p_comments_time = b_p_comments[0]['comment_time']
>>> b_p_comments_time
datetime.datetime(2024, 4, 2, 9, 13, 9, 861545, tzinfo=datetime.timezone.utc)
# 9.2 Имя автора комментария
>>> b_p_comments_username = User.objects.get(pk=b_p_comments[0]['user'])
>>> b_p_comments_username
<User: Эрнест Щукин>
# 9.3 Рейтинг комментария.
>>> b_p_comments_rating = b_p_comments[0]['comment_rating']
>>> b_p_comments_rating
-1
# 9.4 Текст комментария.
>>> b_p_comments_text = b_p_comments[0]['comment_text']
>>> b_p_comments_text
'Даёшь Трампа! Трамп -наш президент!'