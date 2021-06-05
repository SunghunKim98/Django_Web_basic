from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from django.contrib.auth.forms import UserChangeForm
from .models import Profile
from django.db import models


class CustomUserCreationForm(UserCreationForm):
	# UserCreationForm을 상속받아 CustomUserCreationForm을 만든다.
	username = forms.CharField(
		label="",
		widget=forms.TextInput(attrs={
			"placeholder": "사용자 이름",
		})
	)
	password1 = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={
			"placeholder": "비밀번호(8자 이상)",
		})
	)
	password2 = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={
			"placeholder": "비밀번호 확인",
		})
	)
	class Meta:
		model = get_user_model() # 이 폼이 적용될 모델을 지정한다.
		fields = ['username', 'password1', 'password2',]
		# 이 폼에서 입력 받을 필드명을 지정한다.

class CustomUserChangeForm(UserChangeForm):
	password = None
	# UserChangeForm에서는 password를 수정할 수 없다.
	# 하지만 이렇게 None 값으로 지정해주지 않으면 password를 변경할 수 없다는 설명이 화면에 표현된다.
	class Meta:
		model = get_user_model()
		fields = ['email', 'first_name', 'last_name',]


# 여기에 조금 문제가 있었다.
# models.Model이 아니라, forms.ModelForm으로 바꿔야 한다.
# models.Model vs forms.ModelForm
# -> 애초에 models.Model은 Model을 만들 때 쓰는 거고, forms.ModelForm은 form을 만들 때 써야 하지 않냐?

class ProfileForm(forms.ModelForm):
	nickname = forms.CharField(label="별명", required=False)
	description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())
	image = forms.ImageField(label="이미지", required=False)
   	# 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
	class Meta:
		model = Profile
		fields = ['nickname', 'description', 'image',]
