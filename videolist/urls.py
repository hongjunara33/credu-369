from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_v, name='upload_v'),
    path('category/', views.InsertCategoryinfo, name='InsertCategoryinfo'),
    path('category1/', views.SaveCategoryinfo, name='SaveCategoryinfo'),
    path('category2/', views.Mycategoryview, name='Mycategoryview'),
    path('upload1/', views.upload_video, name='upload_video'),
    path('update1/', views.UpdateCategoryname, name='UpdateCategoryname'),
    path('update2/', views.UpdateCategoryname1, name='UpdateCategoryname1'),
]
