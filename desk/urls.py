from django.urls import path, re_path
from .views import PostList, PostDetail, main_redirect, PostAdd, UserDetail, UserPrivatePage, agree, disagree

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('filter/', UserPrivatePage.as_view(), name='posts_filter'),
    re_path(r'^filter/agree/(?P<response_id>\d+)/$', agree, name='agree'),
    re_path(r'^filter/disagree/(?P<response_id>\d+)/$', disagree, name='disagree'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('post/add/', PostAdd.as_view(), name='post_add'),
    path('post/', main_redirect, name='main_red'),
    path('user/<int:pk>', UserDetail.as_view(), name='user_detail'),
]