
from django.urls import path, include
from . import views 

urlpatterns = [
    
    path('', views.tasklist), 
    path('task/<int:id>', views.taskview), 
    path('novatask/', views.novatask),
    path('edit/<int:id>', views.edittask),
    path('delete/<int:id>', views.deletetask),
    path('accounts/', include('django.contrib.auth.urls') ),
]
