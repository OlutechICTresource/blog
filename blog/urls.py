from django.urls import path
from .views import  *
# from .views import  post_list, post_detail, like_post, star_post, applaud_post,home , create_post, about

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('post/create/', create_post, name='create_post'),
    path('post/', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('post/<int:pk>/star/', star_post, name='star_post'),
    path('post/<int:pk>/applaud/', applaud_post, name='applaud_post'),
    path('post/<int:pk>/comment/', create_comment, name='create_comment'),
]
