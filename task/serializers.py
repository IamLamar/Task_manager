from rest_framework import serializers

from task.models import Project,Task,Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ProjectStatusUpdateSerializer(serializers.Serializer):

    new_status = serializers.CharField(required=True,write_only=True)#Это поле не сохраняется в бд
    
    def validate(self,data):

        if not data['new_status'] in ['in_progress','done']:
            raise serializers.ValidationError(
                "Статус на который вы хотите поменять не существует"
            )
        
        return data


    def update(self,instance,validated_data):
        new_status = validated_data['new_status']# Обращаемся к словарю по ключу и получаем значение
        instance.status=new_status#Берётся поле из объекта, его статус приравниваем к новому статусу
        instance.save()# Сохраняем изменения в бд
        
        return instance#Возвращаем объект
    

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.CharField(required = False)

    class Meta:
        model  = Project
        fields = '__all__'

class TaskNameFindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    

