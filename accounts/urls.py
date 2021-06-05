from django.urls import path
from . import views

app_name = "accounts"
# view나 template에서 해당 이름을 이용해 url에 요청을 보낼 수 있다.

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    # "<내 URL>/accounts/signup/" 주소로 요청이 오면 views.py 안에 signup이라는 함수를 찾아 실행한다.

    path('login/', views.login, name="login"),
    # URL/accounts/login 의 url로 요청이 들어오면 views.py의 login 메소드를 수행한다.
    path('logout/', views.logout, name="logout"),

    path('profile/', views.profile, name="profile"),
    path('show_profile/', views.show_profile, name="show_profile")
]
