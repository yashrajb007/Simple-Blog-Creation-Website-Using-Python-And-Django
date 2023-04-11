from django.shortcuts import render
from .models import Post
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.
'''def home(request):
    data={
        'posts':Post.objects.all()
    }
    return render(request,'home.html',data)'''

class PostListView(ListView):
    model=Post
    template_name= 'home.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=2

class PostDetailView(DetailView):
    model=Post
    template_name='post_detail.html' #<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='login'
    model=Post
    template_name='post_form.html'
    fields=['title','content']
    # success_url='{% id %}'
    
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
        
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):  
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']  

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(DeleteView,LoginRequiredMixin,UserPassesTestMixin):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Post
    template_name = 'post_confirm.html'
    success_url='/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    