"""Отображение таблиц в admin панели."""

from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    """Добавляет возможность устанавливать связи с таблицой genre."""

    model = GenreFilmWork


class PersonFilmworkInline(admin.TabularInline):
    """Добавляет возможность устанавливать связи с таблицой person."""

    model = PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Отображение таблицы genre в админ панели."""

    # Отображение полей в списке
    list_display = ('name', 'description', 'created', 'modified')

    # Поиск по полям
    search_fields = ('name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Отображение таблицы film_work в админ панели."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    # Отображение полей в списке
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'created',
        'modified',
    )

    # Фильтрация в списке
    list_filter = ('type', 'creation_date')

    # Поиск по полям
    search_fields = ('title', 'description', 'id', 'creation_date')
    list_editable = ['type']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Отображение таблицы person в админ панели."""

    # Отображение полей в списке
    list_display = ('full_name', 'created', 'modified')

    # Поиск по полям
    search_fields = ('full_name', 'id')
