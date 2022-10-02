from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Post
# Create your views here.
def post_list(request):
    posts=Post.published.all()
    return render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request, year,month,day,post):
    post = get_object_or_404(Post.published,
    #status=Post.Status.PUBLISHED,
    slug=post,
    publish__year=year,
    publish__month=month,
    publish__day=day
    )
    return render(request,'blog/post/detail.html',{'post': post})
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Form fields passed validation
            cd = form.cleaned_data
    # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
      
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'zickler2004@gmail.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form})