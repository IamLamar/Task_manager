from django.shortcuts import render

from rest_framework.views import APIView,View
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView,ListAPIView,UpdateAPIView,CreateAPIView,ListCreateAPIView

from task.serializers import ProjectSerializer,TaskSerializer,ProjectStatusUpdateSerializer,CommentSerializer,TaskNameFindSerializer
from task.models import Project,Task,Comment,Log
from task.permissions import IsOwnerProject
from task.pagination import TaskPagination

from user.models import CustomUser


class ProjectCreateAPIView(CreateAPIView):

    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data,status=201)
    

class ProjectListAPIView(ListAPIView):

    def get_queryset(self):
        queryset = Project.objects.all()
        user = self.request.query_params.get('user')
        if user:#Если строка не пустая
            user_obj = CustomUser.objects.filter(email=user).first()
            queryset = Project.objects.filter(user=user_obj)
        return queryset


class ProjectUpdateAPIView(UpdateAPIView):
    permission_classes = [IsOwnerProject]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    

class ProjectDestroyAPIView(DestroyAPIView):
    permission_classes = [IsOwnerProject]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskCreateAPIView(CreateAPIView):
      def post(self,request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Log.objects.create(data=request.data,user=request.user,table='Task')
        return Response(serializer.data,status=201)
      

class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        queryset = Task.objects.all()
        user = self.request.query_params.get('user')
        status = self.request.query_params.get('status')
        project = self.request.query_params.get('project')
        if user:
            user_obj = CustomUser.objects.filter(email=user).first()
            queryset = Task.objects.filter(user=user_obj)
        if status:
            queryset = Task.objects.filter(status=status)
        if project:
            project_obj = Project.objects.filter(name=project).first()
            queryset = Task.objects.filter(project=project_obj)
        return queryset
    

class TaskUpdateAPIView(UpdateAPIView):
    # permission_classes = [IsOwnerProject]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(DestroyAPIView):
    # permission_classes = [IsOwnerProject]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer  

class TaskStatusUpdateAPIView(UpdateAPIView):

    def put(self,request,pk):
        queryset = Task.objects.get(pk=pk)
        serializer = ProjectStatusUpdateSerializer(data=request.data,instance=queryset)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Log.objects.create(data=request.data,user=request.user,table='Status change')
        return Response(serializer.data)
    

class CommentListAPIView(ListAPIView):

    def get(self,request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset)
        return Response(serializer.data,status=200)
    
class CommentCreateAPIView(CreateAPIView):

    def post(self,request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)
    
class CommentUpdateAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDestroyAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TaskListCreateAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

class TaskDoneUpdateAPIView(UpdateAPIView):
    def put(self,request,pk):
        task = Task.objects.filter(pk=pk).first()
        if task.status == 'done':
            return Response("У этой задачи уже и так статус done",status=400)
        task.status = 'done'
        task.save()
        return Response("Вы успешно поменяли статус задачи на done",status=200)
    

# API-класс для поиска задач по названию с использованием GET-запросов
class TaskNameFindListAPIView(ListAPIView):
    serializer_class = TaskNameFindSerializer  # Указываем, какой сериализатор использовать для задач

    # Метод для фильтрации задач по названию
    def get_queryset(self):
        queryset = Task.objects.all()  # Получаем все объекты Task
        title = self.request.query_params.get('title')  # Получаем параметр 'title' из запроса
        if title:  # Если параметр 'title' существует
            queryset = Task.objects.filter(title=title)  # Фильтруем задачи по названию
        return queryset  # Возвращаем отфильтрованный или неотфильтрованный набор данных


# API-класс для мягкого удаления задачи с использованием POST-запросов
class TaskSoftDeleteAPIView(DestroyAPIView):

    # Метод для мягкого удаления задачи (устанавливаем 'is_deleted' в True)
    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)  # Получаем задачу по первичному ключу (pk)
            if task.is_deleted:  # Проверяем, удалена ли задача уже
                return Response('error: Task already deleted', status=400)  # Возвращаем ошибку, если задача уже удалена
            task.is_deleted = True  # Помечаем задачу как удаленную
            task.save()  # Сохраняем изменения в базе данных
            return Response('message: Task soft deleted successfully')  # Возвращаем сообщение об успешном удалении
        except Task.DoesNotExist:  # Обрабатываем случай, когда задача не найдена
            return Response('error: Task not found', status=404)  # Возвращаем ошибку, если задача не найдена


# API-класс для восстановления мягко удаленной задачи с использованием POST-запросов
class TaskRestoreAPIView(APIView):

    # Метод для восстановления задачи (устанавливаем 'is_deleted' в False)
    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)  # Получаем задачу по первичному ключу (pk)
            if not task.is_deleted:  # Проверяем, не удалена ли задача
                return Response('error: Task is not deleted', status=400)  # Возвращаем ошибку, если задача не удалена
            task.is_deleted = False  # Восстанавливаем задачу, снимая отметку удаления
            task.save()  # Сохраняем изменения в базе данных
            return Response('message: Task restored successfully', status=200)  # Возвращаем сообщение об успешном восстановлении
        except Task.DoesNotExist:  # Обрабатываем случай, когда задача не найдена
            return Response('error: Task not found', status=404)  # Возвращаем ошибку, если задача не найдена

        




    
    
        
