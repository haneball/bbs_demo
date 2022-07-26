from django.urls import path
from bbs import views


app_name = 'bbs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 板块页面
    path('plate=<int:plate_id>&page=<int:page>', views.plate, name='plate'),
    # 帖子详情页
    path('article=<int:article_id>&page=<int:page>', views.article, name='article'),
    # 发表帖子页面
    path('plate=<int:plate_id>/post', views.post, name='post'),
    # 发表回复页面
    path('article=<int:article_id>/reply', views.reply, name='reply'),
    # 用户发帖记录页面
    path('user/my_article', views.my_article, name='my_article'),
    # 用户回复记录页面
    path('user/my_comment', views.my_comment, name='my_comment'),
    # 编辑帖子页面
    path('article=<int:article_id>/edit', views.edit_article, name='edit_article'),
    # 编辑回复
    path('comment=<int:comment_id>/edit', views.edit_comment, name='edit_comment'),
    # 删除帖子页面
    path('article=<int:article_id>/delete', views.delete_article, name='delete_article'),
    # 删除回复页面
    path('comment=<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
]
