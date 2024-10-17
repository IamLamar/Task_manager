from django.urls import path
from .views import (ProjectListAPIView,ProjectCreateAPIView,ProjectUpdateAPIView,
                    ProjectDestroyAPIView,TaskCreateAPIView,
                    TaskListAPIView,TaskUpdateAPIView,TaskDestroyAPIView,
                    TaskStatusUpdateAPIView,CommentListAPIView,
                    CommentCreateAPIView,CommentUpdateAPIView,CommentDestroyAPIView,
                    TaskListCreateAPIView,TaskDoneUpdateAPIView,
                    TaskNameFindListAPIView,TaskSoftDeleteAPIView,TaskRestoreAPIView)


urlpatterns = [
    path('list/',ProjectListAPIView.as_view()),
    path('create/',ProjectCreateAPIView.as_view()),
    path('update/<int:pk>/',ProjectUpdateAPIView.as_view()),
    path('delete/<int:pk>/',ProjectDestroyAPIView.as_view()),
    path('list_task/',TaskListAPIView.as_view()),
    path('create_task/',TaskCreateAPIView.as_view()),
    path('update_task/<int:pk>/',TaskUpdateAPIView.as_view()),
    path('delete_task/<int:pk>/',TaskDestroyAPIView.as_view()),
    path('comment_list/',CommentListAPIView.as_view()),
    path('comment_create/',CommentCreateAPIView.as_view()),
    path('comment_update/<int:pk>/',CommentUpdateAPIView.as_view()),
    path('comment_delete/<int:pk>/',CommentDestroyAPIView.as_view()),
    path('pagination/',TaskListCreateAPIView.as_view()),
    path('task_status_update/<int:pk>/',TaskStatusUpdateAPIView.as_view()),
    path('task_update_to_done/<int:pk>/',TaskDoneUpdateAPIView.as_view()),
    path('task_name_find/',TaskNameFindListAPIView.as_view()),
    path('task_soft_delete/<int:pk>/',TaskSoftDeleteAPIView.as_view()),
    path('task_restore/<int:pk>/',TaskRestoreAPIView.as_view()),
]