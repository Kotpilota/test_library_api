from django.db import models


class Author(models.Model):
    last_name = models.CharField(
        max_length=100,
        db_index=True,  # Индекс для поиска и сортировки
        verbose_name="Фамилия"
    )
    first_name = models.CharField(
        max_length=100,
        db_index=True,  # Индекс для поиска и сортировки
        verbose_name="Имя"
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Отчество"
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,  # Индекс для фильтрации и сортировки по дате
        verbose_name="Дата рождения"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография"
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

        indexes = [
            # Составной индекс для сортировки по ФИО (самый частый случай)
            models.Index(
                fields=['last_name', 'first_name'],
                name='author_full_name_idx'
            ),
            # Индекс для поиска по фамилии + имени + отчеству
            models.Index(
                fields=['last_name', 'first_name', 'middle_name'],
                name='author_search_idx'
            ),
        ]

    @property
    def full_name(self):
        """
        Вычисляемое свойство для получения полного имени.
        Используется в сериализаторе и админке.
        """
        return " ".join(
            # filter(None, ...) убирает пустые значения (None, пустые строки)
            filter(None, (self.last_name, self.first_name, self.middle_name))
        )

    def __str__(self):
        return self.full_name


class Book(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="Автор"
    )
    year = models.PositiveSmallIntegerField(
        db_index=True,  # Индекс для фильтрации по году
        verbose_name="Год издания"
    )
    title = models.CharField(
        max_length=255,
        db_index=True,  # Индекс для поиска и сортировки по названию
        verbose_name="Название"
    )
    preface = models.TextField(
        blank=True,
        verbose_name="Предисловие"
    )
    cover = models.ImageField(
        upload_to="covers/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name="Обложка"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

        indexes = [
            # Составной индекс для фильтрации по автору + году
            # Покрывает запросы типа: "все книги автора", "книги автора за год"
            models.Index(
                fields=['author', 'year'],
                name='book_author_year_idx'
            ),

            # Составной индекс для фильтрации по году + названию
            # Для запросов: "книги за год", сортированные по названию
            models.Index(
                fields=['year', 'title'],
                name='book_year_title_idx'
            ),

            # Составной индекс автор + название для уникальности и быстрого поиска
            models.Index(
                fields=['author', 'title'],
                name='book_author_title_idx'
            ),
        ]

        constraints = [
            # Уникальность: один автор не может иметь две книги с одинаковым названием
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
            # Проверка корректности года издания
            models.CheckConstraint(
                check=models.Q(year__gte=1000) & models.Q(year__lte=2030),
                name='valid_publication_year'
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"
