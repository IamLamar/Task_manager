from django.db import models

from user.models import CustomUser
from task.choices import StatusChoices


class Project(models.Model):
    name = models.CharField(verbose_name="Название", max_length=40)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    title = models.CharField(verbose_name="Название",max_length=50)
    description = models.TextField()
    status = models.CharField(choices=StatusChoices, default=StatusChoices.NEW, verbose_name='Статус',max_length=128)
    project = models.ForeignKey(Project,verbose_name="Проект",on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"  

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст")
    task = models.ForeignKey(Task,verbose_name="Задача",related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,verbose_name="Пользователь",on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return self.text
    

class Log(models.Model):
    date = models.DateField(auto_now_add=True)
    data = models.CharField(max_length=128,verbose_name="Данные")
    user = models.ForeignKey(CustomUser,verbose_name="Пользователь",on_delete=models.CASCADE)
    table = models.CharField(max_length=128,verbose_name="Таблица")


