from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from NewsPortal.settings import LOGIN_REDIRECT_URL
from .forms import PostForm
from .models import Post
from .filters import PostFilter


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Переопределяем метод и отфильтровываем объекты по полю is_news
        if self.request.path == reverse('news_list'):
            return Post.objects.filter(is_news=True).order_by('-post_time')
        else:
            return Post.objects.filter(is_news=False).order_by('-post_time')


class PostList1(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts1'
    paginate_by = 10

    # Переопределяем функцию получения списка постов

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту, и если новость, покажем её.
    model = Post
    # Используем другой шаблон — detailed_post.html
    template_name = 'detailed_post.html'
    # Название объекта, в котором будет выбранная новость
    context_object_name = 'post'


class PostList2(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts1'
    paginate_by = 10


# Добавляем новое представление для создания постов.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_post'
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def is_it_news(self):
        if self.request.path == reverse(
                'news_create'):  # Здесь 'news_create' - это имя URL маршрута для создания новости
            is_news = True
        else:
            is_news = False
        return is_news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_news'] = self.is_it_news()
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        post = form.save(commit=False)
        if self.request.path == reverse(
                'news_create'):  # Здесь 'news_create' - это имя URL маршрута для создания новости
            post.is_news = True
        else:
            post.is_news = False
        return super().form_valid(form)


# Добавляем представление для изменения постов.
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление удаляющее пост.
class PostDelete(DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PersonalView(LoginRequiredMixin, TemplateView):
    template_name = 'personal/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/login/')
