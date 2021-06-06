from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import redirect, get_object_or_404
from .forms import PostForm
from .models import Post

from .models import Comment
from .forms import CommentForm


from django.core.paginator import Paginator

# def index(request):
#     template_name = "posts/main.html"

#     # print(request.user) -> user가 있으면 user이름이 나오고 없으면 Anoymous Name 뭐시기가 나옴

#     if not request.user.is_authenticated:
#         return render(request, template_name, {'user':''})
#     else:
#         return render(request, template_name, {'user':request.session['user']})


#     # 개 같은게 request.session['user]가 없으면 걍 KeyError가 떠버려서 함수가 종료 되어버림.
#     # 이런 경우에는 try except으로 조지는 수 밖에 없음.

#     # try:
#     #     useer = request.session['user']
#     # except:
#     #     useer = ""
#     # return render(request, template_name, {'user':useer})

#     # if request.session['user']:
#     #     return render(request, template_name, {'user':request.session['user']})
#     # else:
#     #     return render(request, template_name, {'user':''})

def index(request):

    posts = Post.objects.all()
    # Post 모델을 기반으로 생성된 테이블의 모든 데이터를 가져온다.
    form = CommentForm()

    page = request.GET.get('page', '1')
    print(page)
    paginator = Paginator(posts, 10)
    # page_obj = paginator.get_page(page)
    page_obj = paginator.get_page(page)

    print(page_obj)
    print(page_obj.paginator.count)
    print(page_obj.number)
    print("---")
    print(type(page_obj))

    # for i in page_obj:
    #     print(type(i)) -> 여기 i에 <class 'posts.models.Post'>가 들어있네.
    #     print(i)

    return render(request, 'posts/index.html', {'posts': posts, 'form': form, 'page': page, 'page_list': page_obj})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # commit=False일 경우 실제 DB에는 적용하지 않는다.
            # 아직 작성자 정보가 담겨있지 않기 때문에 실제 DB에 적용하는 것을 지연시키고,
            # 작성자 정보를 넣어준 후 DB에 적용한다.

            # print(type(post.user))
            print(type(request.user))
            post.user = request.user
            post.save()

            print(post.id)
            print(post)
            # print(post.post_id)

            return redirect('posts:index')
        return redirect('posts:create_post')
    else:
        form = PostForm()
        title = '새 글'
        return render(request, 'posts/form.html', {'form': form, 'title': title})

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:index')
            return redirect('posts:edit_post')
        else:
            form = PostForm(instance=post)
            return render(request, 'posts/form.html', {'form': form})
    return redirect('posts:index')

@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('posts:index')


# 댓글 관련된 Method

@require_POST
@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():

        # print(request.POST)
        # print(post_id) # -> post_id가 출력
        # print(post) # -> "post_id: Post의 내용"이 출력
        # print(type(post))

        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()

        # print(f"typeof comment: {type(comment)}")
        # print(f"comment: {comment}")

    return redirect('posts:specific_page', post_id) # @@@ 이게 이렇게 된다!!
#    return redirect('posts:specific_page')

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:specific_page', post_id)

@login_required
def specific_page(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()

    print(type(post))
    print(post)

    template_name = "posts/specific.html"
    context = {
        'post': post,
        'form': form
    }

    return render(request, template_name, context)
