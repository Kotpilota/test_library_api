from django.db import models


class Author(models.Model):
    last_name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Фамилия"
    )
    first_name = models.CharField(
        max_length=100,
        db_index=True,
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

    @property
    def full_name(self):
        return " ".join(
            # filter(None, ...) убирает пустые значения
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
        db_index=True,
        verbose_name="Год издания"
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
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

    def __str__(self):
        return f"{self.title} ({self.year})"
