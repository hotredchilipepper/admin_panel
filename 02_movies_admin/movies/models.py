"""Описание всех моделей таблиц проекта."""

import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Этот Класс предназначен для соблюдения принципу DRY.

    Есть два поля описанные ниже, которые есть в нескольких таблицах.
    """

    # auto_now_add автоматически выставит дату создания записи
    # Дата создание записи об этом кинопроизведении.
    created = models.DateTimeField(_('created'), auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    # Это поле изменятся при каждом обновлении записи.
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        """Этот класс не является представлением таблицы."""

        abstract = True


class UUIDMixin(models.Model):
    """Этот Класс предназначен для соблюдения принципу DRY.

    Поле id(uuid) которые есть во всех таблицах.
    """

    # Явно объявляем primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Этот класс не является представлением таблицы."""

        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Модель описания таблицы жанров."""

    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        """Явно указываем схему в базе данных."""

        db_table = 'content\".\"genre'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        """Корректное отображение имени.

        Returns:
            str: значение name
        """
        return self.name


class FilmType(models.TextChoices):
    """Модель описания поля типа кинопроизведения."""

    MOVIE = 'MO', _('Movie')
    TV_SHOW = 'TV', _('TV Show')


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Модель описания таблицы кинопроизведений."""

    # Название будет с ограничением в 255 символов.
    title = models.CharField(_('title'), max_length=255)
    # Поле описания может быть пустым.
    description = models.TextField(_('description'), blank=True)
    # Дата выхода в кинопрокат.
    creation_date = models.DateField(_('creation_date'), blank=True)
    # Рейтинг фильма.
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    # Тип кинопроизведения два вида movie или tv_show.
    type = models.CharField(
        _('type'),
        max_length=2,
        choices=FilmType.choices,
        default=FilmType.MOVIE,
    )

    certificate = models.CharField(
        _('certificate'),
        max_length=512,
        blank=True,
    )
    # Параметр upload_to указывает,
    # в какой подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT.
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/',
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        """Явно указываем схему в базе данных."""

        db_table = 'content\".\"film_work'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        """Корректное отображение имени.

        Returns:
            str: значение title
        """
        return self.title


class GenreFilmWork(UUIDMixin):
    """Модель описания связей таблицы жанров и кинопроизведений."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Явно указываем схему в базе данных."""

        db_table = 'content\".\"genre_film_work'


class Person(UUIDMixin, TimeStampedMixin):
    """Модель описания таблицы персон."""

    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        """Явно указываем схему в базе данных."""

        db_table = 'content\".\"person'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        """Корректное отображение имени.

        Returns:
            str: значение full_name
        """
        return self.full_name


class PersonFilmWork(UUIDMixin):
    """Модель описания связей таблицы персон и кинопроизведений."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        """Явно указываем схему в базе данных."""

        db_table = 'content\".\"person_film_work'
