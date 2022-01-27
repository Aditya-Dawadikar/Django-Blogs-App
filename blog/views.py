from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from blog.models import Blog
from blog.models import User as AppUser

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import auth

from datetime import date

# from django.core.paginator import Paginator

# isAdmin = False
# isLoggedin = True
# userinfo = {
#     "username":"heman",
#     "userid":"880",
#     "blog_count":"67",
# }

# blogs=[
#     {
#         "blogid":"1234",
#         "title":"some random topic",
#         "content":"Aenean a metus quis metus mollis tempor. Quisque ornare consectetur posuere. Aliquam placerat metus in lorem ornare congue. Fusce in sem in ligula porttitor faucibus sit amet lacinia mi. Aenean viverra sapien et risus vulputate vulputate. Donec placerat mi tortor, eu auctor tortor sodales in. Mauris fermentum turpis in nisl interdum scelerisque in id metus. Proin ornare tortor magna, ac porttitor nibh auctor pulvinar.",
#         "date":{
#             "day":"11",
#             "month":"January",
#             "year":"2021"
#         },
#         "author":{
#             "username":"someguy",
#             "userid":"342"
#         }
#     },{
#         "blogid":"1235",
#         "title":"some random topic",
#         "content":"Aenean a metus quis metus mollis tempor. Quisque ornare consectetur posuere. Aliquam placerat metus in lorem ornare congue. Fusce in sem in ligula porttitor faucibus sit amet lacinia mi. Aenean viverra sapien et risus vulputate vulputate. Donec placerat mi tortor, eu auctor tortor sodales in. Mauris fermentum turpis in nisl interdum scelerisque in id metus. Proin ornare tortor magna, ac porttitor nibh auctor pulvinar.",
#         "date":{
#             "day":"18",
#             "month":"January",
#             "year":"2021"
#         },
#         "author":{
#             "username":"helloyou",
#             "userid":"127"
#         }
#     },{
#         "blogid":"1236",
#         "title":"some random topic",
#         "content":"Aenean a metus quis metus mollis tempor. Quisque ornare consectetur posuere. Aliquam placerat metus in lorem ornare congue. Fusce in sem in ligula porttitor faucibus sit amet lacinia mi. Aenean viverra sapien et risus vulputate vulputate. Donec placerat mi tortor, eu auctor tortor sodales in. Mauris fermentum turpis in nisl interdum scelerisque in id metus. Proin ornare tortor magna, ac porttitor nibh auctor pulvinar.",
#         "date":{
#             "day":"20",
#             "month":"December",
#             "year":"2020"
#         },
#         "author":{
#             "username":"manhim",
#             "userid":"667"
#         }
#     },{
#         "blogid":"1237",
#         "title":"some random topic",
#         "content":"Aenean a metus quis metus mollis tempor. Quisque ornare consectetur posuere. Aliquam placerat metus in lorem ornare congue. Fusce in sem in ligula porttitor faucibus sit amet lacinia mi. Aenean viverra sapien et risus vulputate vulputate. Donec placerat mi tortor, eu auctor tortor sodales in. Mauris fermentum turpis in nisl interdum scelerisque in id metus. Proin ornare tortor magna, ac porttitor nibh auctor pulvinar.",
#         "date":{
#             "day":"26",
#             "month":"December",
#             "year":"2020"
#         },
#         "author":{
#             "username":"yeswoman",
#             "userid":"389"
#         }
#     }
# ]

# users=[
#     {
#         "username":"geekgod",
#         "userid":"112",
#         "blog_count":"20",
#     },{
#         "username":"someguy",
#         "userid":"342",
#         "blog_count":"33"
#     },{
#         "username":"helloyou",
#         "userid":"127",
#         "blog_count":"13"
#     },{
#         "username":"manhim",
#         "userid":"667",
#         "blog_count":"9"
#     },{
#         "username":"yeswoman",
#         "userid":"389",
#         "blog_count":"14"
#     },
# ]

# admins=[
#     {
#         "username":"someguy",
#         "userid":"342",
#         "blog_count":"33"
#     },{
#         "username":"helloyou",
#         "userid":"127",
#         "blog_count":"13"
#     },{
#         "username":"geekgod",
#         "userid":"112",
#         "blog_count":"20",
#     }
# ]

#utility
def getIsAdmin(request):
    currUser = AppUser.objects.filter(username=request.user)
    return currUser[0].isAdmin

def getIsLoggedIn(request):
    isLoggedin = False
    if request.user != None:
        isLoggedin=True
    return isLoggedin

#returns landing page
def landing(request):
    userinfo = request.user
    isAdmin=getIsAdmin(request)
    isLoggedin = getIsLoggedIn(request)
    return render(request,'landing.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo})

def authenticate_user(request):
    if request.user.is_authenticated: 
        return redirect('http://localhost:8000/blog/blogs')
    return render(request, 'auth.html')

def loginhandler(request):
    if request.method == 'POST':
        user = request.POST['username']
        pswd = request.POST['password']
        
        users = auth.authenticate(username = user, password = pswd)
        
        if users is not None:
            auth.login(request,users)
            return redirect('http://localhost:8000/blog/blogs/')
        else:
            return redirect('http://localhost:8000/blog/accounts/login/')
        

def signuphandler(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pswd = request.POST.get('password')
        mail = request.POST.get('email')
        
        try: 
            user = User.objects.get(username = request.POST['username'] )
            return render(request,"auth.html",{'messages' : "User has already registered"})
        except User.DoesNotExist:
            if len(request.POST['password']) <8:
                return render(request,"auth.html", {'messages':'Password should be greater than 8 characters'})
            else:
                user = User.objects.create_user(username = user, email = mail , password = pswd)
                appuser = AppUser(username = user, isAdmin=False)
                appuser.save()
                auth.login(request, user)
                return redirect('http://localhost:8000/blog/accounts/login/')

    else:
        return redirect('http://localhost:8000/blog/accounts/login/')
        
#see all blogs
def explore(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        blogs = Blog.objects.all()
        userinfo = request.user
        
        isAdmin=getIsAdmin(request)
        isLoggedin = getIsLoggedIn(request)
        
        return render(request,'blogs.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo,'blogs':blogs})

#blog page
def readblog(request,blogid):
    blogs = Blog.objects.filter(blogid=blogid)
    userinfo = request.user
    isAdmin=getIsAdmin(request)
    isLoggedin = getIsLoggedIn(request)
    return render(request,'readblog.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo,'blog':blogs[0]})

#blogger profile page
def blogger(request,username):
    blogs = Blog.objects.filter(author_id__username__contains=username)
    userinfo = request.user
    isAdmin=getIsAdmin(request)
    isLoggedin = getIsLoggedIn(request)
    return render(request,'blogger.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo,'blogs':blogs,'author':username})

#shows all users
def allusers(request):
    users = AppUser.objects.all()
    userinfo = request.user
    isAdmin=getIsAdmin(request)
    isLoggedin = getIsLoggedIn(request)
    return render(request,'users.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo,'users':users})

#returns compose page
def compose(request):
    userinfo = request.user
    isAdmin=getIsAdmin(request)
    isLoggedin = getIsLoggedIn(request)
    return render(request,'compose.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo})

#handles adding new blog
def makeNewBlog(request):
    if request.method == 'POST':

        blog_title = request.POST.get('blog_title')
        blog_content = request.POST.get('blog_content')
        blog_date = date.today()
        
        users = AppUser.objects.filter(username=request.user)
        
        author_id = users[0]
        
        blog_object = Blog(blog_title=blog_title,blog_content=blog_content,blog_date=blog_date,author_id=author_id)
        blog_object.save()
        
        newblog = Blog.objects.filter(blog_title=blog_title)
        
        return redirect('http://localhost:8000/blog/blog/'+str(newblog[0].blogid))
        
    else:
        return redirect('http://localhost:8000/blog/accounts/login/')

#handles delete blog
def deleteBlog(request,blogid):
    instance = Blog.objects.get(blogid=blogid)
    instance.delete()
    return redirect('http://localhost:8000/blog/blogger/'+str(request.user))

def alladmins(request):
    admins = AppUser.objects.filter(isAdmin=True)
    userinfo = request.user
    isAdmin=getIsAdmin(request)
    isLoggedin = getIsLoggedIn(request)
    return render(request,'adminlist.html',{'isAdmin':isAdmin,'isLoggedin':isLoggedin,'userinfo':userinfo,'admins':admins})

def logout(request):
    auth.logout(request)
    return redirect('http://localhost:8000/blog/accounts/login/')