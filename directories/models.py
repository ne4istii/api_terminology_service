from django.db import models


class Item(models.Model):
    uid = models.CharField(
        verbose_name='UID',
        help_text='Укажите UID элемента справочника',
        max_length=100
    )
    code = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Код элемента справочника',
        help_text='Укажите код элемента справочника'
    )
    value = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Значение элемента справочника',
        help_text='Укажите значение элемента справочника'
    )

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'
        ordering = ('code',)
        constraints = [
            models.UniqueConstraint(
                fields=('code', 'value'),
                name='code_value_constraint'
            ),
        ]

    def __str__(self):
        return f'{self.code} / {self.value}'


class Directory(models.Model):
    uid = models.CharField(
        verbose_name='UID',
        help_text='Укажите UID справочника',
        max_length=50,
        unique=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        help_text='Укажите наименование справочника',
        max_length=200,
        unique=True
    )
    title = models.CharField(
        verbose_name='Краткое наименование справочника',
        help_text='Укажите короткое наименование справочника',
        max_length=200
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Укажите подробное описание справочника',
    )

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        ordering = ('-uid',)

    def __str__(self):
        return f'{self.uid} / {self.name}'


class Version(models.Model):
    directory = models.ForeignKey(
        Directory,
        on_delete=models.CASCADE,
        help_text='Справочник',
        verbose_name='Выберите справочник',
        related_name='versions'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации справочника',
        help_text='Дата публикации справочника'
        # auto_now_add=True,
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Версия справочника',
        help_text='Укажите версию справочника'
    )
    items = models.ManyToManyField(
        Item,
        through='ItemsVersion',
        help_text='Элементы справочника',
        verbose_name='Добавьте элементы справочника',
        related_name='versions',
    )

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('directory', 'name'),
                name='directory_name_constraint'
            ),
        ]

    def __str__(self):
        return f'{self.directory.name} / {self.name} / {self.pub_date}'


class ItemsVersion(models.Model):
    version = models.ForeignKey(
        Version,
        verbose_name='Версия справочника',
        on_delete=models.CASCADE,
        related_name='itemsversion'
    )
    item = models.ForeignKey(
        Item,
        verbose_name='Элемент справочника',
        on_delete=models.CASCADE,
        related_name='itemsversion'
    )

    def __str__(self):
        return f'{self.version} / {self.item.code}'
