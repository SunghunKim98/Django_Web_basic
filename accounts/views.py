# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as user_login
from django.contrib.auth.forms import UserCreationForm
# Django 프레임워크가 구현해 놓은 회원가입 폼을 import 한다.

from django.contrib.auth import logout as user_logout
from django.contrib.auth.forms import AuthenticationForm
# django내에 구현된 로그인 폼

from django.shortcuts import get_object_or_404
from .models import Profile

# Customized Form을 가져오기
from .forms import CustomUserCreationForm

# Profile을 위해
from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile

from django.contrib.auth import get_user_model


def signup(request): # urls.py에 views.signup이 이 함수를 가리킨다.
	# 이미 로그인이 된 상태면 홈으로 보낸다.
	if request.user.is_authenticated:
		# return redirect("posts:index")
		# return render(request, "posts/main.html", {'user': request.session['user']})
		return redirect('posts:index')

	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)

		if form.is_valid(): # 회원가입 폼에서 적어 보낸 요청이 유효한지 검사한다.
			user = form.save() # 유효한 내용이면 이 회원 정보를 데이터베이스에 저장한다. 그 유저 정보를 리턴한다.
			print("Success to register")
			# print(request.path)
			user_login(request, user) # 유저 정보를 이용해 로그인한다. 이때 sessionid가 주어진다.
			# print(user) -> user name이 return 된다.
			request.session['user'] = user.username # session을 통해 user_name이라는 key에 user를 저장
			# print(type(user)) == <class 'django.contrib.auth.models.User'>
			# print(user.username) == username
			# return render(request, "posts/main.html", {'user': request.session['user']})
			return redirect('posts:index')
		print("Fail to register")
		return redirect('accounts:signup')
		# redirect 시 urls.py의 <app_name>:<name>으로 요청을 보낸다.
	else:
		form = CustomUserCreationForm() # 비어있는 회원가입 폼을 생성한다.
		return render(request, 'accounts/form.html', {'form': form})
		# forms.html 파일을 렌더한다. 이때 위에서 생성한 회원가입 폼을 'form'이라는 이름으로 함께 보낸다.(딕셔너리)


def login(request):
	# 이미 로그인이 된 상태면 홈으로 보낸다.
	if request.user.is_authenticated:
		# return redirect("posts:index")
		# return render(request, "posts/main.html", {'user': str(request.session['user'])})
		return redirect('posts:index')

	if request.method == 'POST':
		form = AuthenticationForm(request, request.POST)
		# 회원가입과 다르게 맨 앞의 인자로 request가 들어간다.
		if form.is_valid():
			user_login(request, form.get_user())
			print("Success to log in")
			# print(form.get_user()) -> user name이 return 된다.
			# print(request.session.session_key)
			# print(type(form.get_user())) -> form.get_user()는 class형태로 return

			request.session['user'] = str(form.get_user()) # session을 통해 user_name이라는 key에 user를 저장

			# return redirect('posts:index') # posts라는 App의 index 페이지로 이동.
#			return render(request, "posts/main.html", {'user': str(request.session['user'])})

			return redirect('posts:index')

		return redirect('accounts:login') # accounts라는 App의 login 페이지로 이동.
	else:
		form = AuthenticationForm()
		return render(request, 'accounts/form.html', {'form': form, 'user': ''})


def logout(request):

	user_logout(request) # sessionid를 반환(?) or 해지(?)

	# print(str(request.session['user'])) # -> 걍 KeyError에러가 남.

	# return render(request, "posts/main.html", {'user': ''})
	return redirect('posts:index')

def show_profile(request):
	person = get_object_or_404(get_user_model(), username=request.user)
	return render(request, 'accounts/people.html', {'person': person})

def people(request, username): # urls.py에서 넘겨준 인자를 username으로 받는다.
	person = get_object_or_404(get_user_model(), username=username)
	return render(request, 'accounts/people.html', {'person': person})

def profile(request):
	# Login이 되어 있지 않으면, login창으로 보낸다.
	if not request.user.is_authenticated:
		return redirect("accounts:login")

	if request.method == 'POST':
		user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_change_form.is_valid() and profile_form.is_valid():
			user = user_change_form.save()
			profile_form.save()
			print(user.username)
			return redirect('people', user.username) # ??? redirect를 통해 함수를 호출 ???
		return redirect('accounts:profile')
	else:
		user_change_form = CustomUserChangeForm(instance=request.user)
		# 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
		# 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
		profile, create = Profile.objects.get_or_create(user=request.user)
		# Profile 모델은 User 모델과 1:1 매칭이 되어있지만
		# User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
		# 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
		profile_form = ProfileForm(instance=profile)
		return render(request, 'accounts/profile.html', {
			'user_change_form': user_change_form,
			'profile_form': profile_form
		})
