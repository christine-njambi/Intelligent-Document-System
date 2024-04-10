from django.urls import path

from . import views

urlpatterns = [

    path('', views.homepage, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('create-class', views.create_class, name='create_class'),

    path('fetch-class', views.display_class_data, name='display_class_data'),

    path('create-student', views.create_student, name='create_student'),

    path('fetch-student', views.display_student_data, name='display_student_data'),

    path('create-transaction', views.create_transaction, name='create_transaction'),

    path('fetch-transaction', views.display_transaction_data, name='display_transaction_data'),

    path('upload-image', views.upload_image, name='upload_image'),
    
]










