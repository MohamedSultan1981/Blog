from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm
# Create your views here.
class PostListView(ListView):
    """
    Alternative post list view
    """
    # model = Post
    queryset = Post.published.all() # we could have specified model = Post and Django would have built the generic Post.objects.all() QuerySet
    context_object_name = 'posts' # The default variable is object_list if you don’t specify any context_object_name.
    paginate_by = 3 # Django’s ListView generic view passes the page requested in a variable called page_obj
    template_name = 'blog/post/list.html'# If you don’t set a default template, ListView will use blog/post_list.html by default.
def post_list(request):
    post_list=Post.published.all()
    paginator=Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
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
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Form fields passed validation
            cd = form.cleaned_data
        # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form})