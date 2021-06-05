from django.urls import path
from . import views

app_name = "posts"
# view나 template에서 해당 이름을 이용해 url에 요청을 보낼 수 있다.

# 이건 뭐징.... app_name을 바꿔주니까 에러가 사라지네...

# app_name과 path의 name속성으로 views.py에서 return redirct("posts:index")을 이용한다.
# redirect("<urls.py의 app_name>:<urls.py의 name속성>")

urlpatterns = [
    path('index/', views.index, name="index"),
]
