from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    template_name = "posts/main.html"

    # print(request.user) -> user가 있으면 user이름이 나오고 없으면 Anoymous Name 뭐시기가 나옴

    if not request.user.is_authenticated:
        return render(request, template_name, {'user':''})
    else:
        return render(request, template_name, {'user':request.session['user']})


    # 개 같은게 request.session['user]가 없으면 걍 KeyError가 떠버려서 함수가 종료 되어버림.
    # 이런 경우에는 try except으로 조지는 수 밖에 없음.

    # try:
    #     useer = request.session['user']
    # except:
    #     useer = ""
    # return render(request, template_name, {'user':useer})

    # if request.session['user']:
    #     return render(request, template_name, {'user':request.session['user']})
    # else:
    #     return render(request, template_name, {'user':''})
