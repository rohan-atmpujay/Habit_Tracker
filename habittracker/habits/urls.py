from django.urls import path

from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add/',views.habit_add,name='habit_add'),
    path('edit/<int:id>',views.habit_edit,name='habit_edit'),
    path('delete/<int:id>',views.habit_delete,name='habit_delete'),
    # path('accounts/login/', views.login_view, name='login'),
    path('done/<int:id>', views.mark_done, name='mark_done'),
    path('habit/<int:id>', views.habit_detail, name='habit_detail'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

]