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
            # РЕШЕНИЕ: Составной индекс для сортировки по ФИО
            # ПОЧЕМУ: В 99% случаев авторы сортируются именно так: сначала фамилия, потом имя
            # Это покрывает самые частые запросы и избегает filesort в БД
            models.Index(
                fields=['last_name', 'first_name'],
                name='author_full_name_idx'
            ),

            # РЕШЕНИЕ: Расширенный индекс для поиска включает отчество
            # ПОЧЕМУ: В русской культуре поиск часто ведется по полному ФИО
            # Индекс покрывает запросы типа WHERE last_name LIKE 'Толс%' AND first_name LIKE 'Лев%'
            # Порядок полей важен - начинаем с самого селективного (фамилия)
            models.Index(
                fields=['last_name', 'first_name', 'middle_name'],
                name='author_search_idx'
            ),
        ]

    @property
    def full_name(self):
        """
        РЕШЕНИЕ: Вычисляемое свойство вместо отдельного поля в БД
        ПОЧЕМУ:
        1. Избегаем дублирования данных (нарушение нормализации)
        2. Нет риска рассинхронизации при изменении ФИО
        3. Экономим место в БД (при миллионах записей это критично)
        4. filter(None, ...) элегантно убирает пустые значения
        """
        return " ".join(
            filter(None, (self.last_name, self.first_name, self.middle_name))
        )

    def __str__(self):
        return self.full_name


class Book(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,  # РЕШЕНИЕ: PROTECT вместо CASCADE
        # ПОЧЕМУ: При удалении автора случайно не потеряем все его книги
        # В библиотечной системе это критично - данные должны сохраняться
        related_name="books",
        verbose_name="Автор"
    )
    year = models.PositiveSmallIntegerField(
        db_index=True,  # РЕШЕНИЕ: Индекс для фильтрации по году
        # ПОЧЕМУ: Частый запрос "книги за определенный период"
        # PositiveSmallIntegerField экономит место (2 байта vs 4 у IntegerField)
        verbose_name="Год издания"
    )
    title = models.CharField(
        max_length=255,
        db_index=True,  # РЕШЕНИЕ: Индекс для поиска и сортировки по названию
        # ПОЧЕМУ: Поиск по названию - основной use case для пользователей
        verbose_name="Название"
    )
    preface = models.TextField(
        blank=True,
        verbose_name="Предисловие"
    )
    cover = models.ImageField(
        upload_to="covers/%Y/%m/%d/",  # РЕШЕНИЕ: Организация файлов по датам
        # ПОЧЕМУ: Избегаем переполнения одной папки тысячами файлов
        # Упрощает backup и администрирование файловой системы
        blank=True,
        null=True,
        verbose_name="Обложка"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

        indexes = [
            # РЕШЕНИЕ: Составной индекс author + year
            # ПОЧЕМУ: Покрывает запросы:
            # 1. "все книги автора" (используется только author часть)
            # 2. "книги автора за год" (используется полный индекс)
            # 3. Ускоряет JOIN с Author при фильтрации по году
            models.Index(
                fields=['author', 'year'],
                name='book_author_year_idx'
            ),

            # РЕШЕНИЕ: Индекс year + title (а не title + year)
            # ПОЧЕМУ: Год более селективен чем первые буквы названия
            # Эффективен для запросов "книги 1869 года, отсортированные по названию"
            models.Index(
                fields=['year', 'title'],
                name='book_year_title_idx'
            ),

            # РЕШЕНИЕ: Составной индекс author + title
            # ПОЧЕМУ: Поддерживает уникальность и ускоряет поиск конкретной книги автора
            # Часто ищут именно так: "Толстой Война и мир"
            models.Index(
                fields=['author', 'title'],
                name='book_author_title_idx'
            ),
        ]

        constraints = [
            # РЕШЕНИЕ: Уникальность на уровне БД, а не только Django
            # ПОЧЕМУ: Гарантирует целостность даже при прямых INSERT в БД
            # Один автор логически не может написать две книги с одинаковым названием
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),

            # РЕШЕНИЕ: Check constraint на уровне БД
            # ПОЧЕМУ: Валидация в БД быстрее и надежнее чем только в Python
            # Защищает от некорректных данных при bulk операциях
            # Диапазон 1000-2030 покрывает все реальные книги + запас на будущее
            models.CheckConstraint(
                check=models.Q(year__gte=1000) & models.Q(year__lte=2030),
                name='valid_publication_year'
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"
