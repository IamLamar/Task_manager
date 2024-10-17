from django.db import models


class StatusChoices(models.TextChoices):
    NEW = 'new','New'
    IN_PROGRESS = 'in progress','In progress'
    DONE = 'done','Done'

    # Первое константа - имя переменной. Второе как мы в коде обращаемся к статусу, Третье как отображается в результате