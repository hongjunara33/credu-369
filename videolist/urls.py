from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.CreateCategoryinfo, name='CreateCategoryinfo'),
    path('category1/', views.SaveCategoryinfo, name='SaveCategoryinfo'),
    path('category2/', views.Mycategoryview, name='Mycategoryview'),
    path('upload/', views.upload_v, name='upload_v'),
    path('upload1/', views.upload_video, name='upload_video'),
    path('update/', views.UpdateCategoryname, name='UpdateCategoryname'),
    path('update1/', views.UpdateCategoryname1, name='UpdateCategoryname1'),
    path('delete/', views.DeleteCategory, name='DeleteCategory'),
    path('delete1/', views.DeleteCategory1, name='DeleteCategory1'),
]
