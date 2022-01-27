from django.urls import path

from  . import views

urlpatterns=[
    path('',views.landing),
    path('accounts/login/',views.authenticate_user),
    path('accounts/logout/',views.logout),
    path('accounts/login/handler/',views.loginhandler),
    path('accounts/signup/handler/',views.signuphandler),
    path('blogs/',views.explore),
    path('blog/<int:blogid>',views.readblog),
    path('blog/delete/<int:blogid>',views.deleteBlog),
    path('blogger/<str:username>',views.blogger),
    path('bloggers/',views.allusers),
    path('compose/',views.compose),
    path('compose/publish/',views.makeNewBlog),
    path('admin/',views.alladmins),
]