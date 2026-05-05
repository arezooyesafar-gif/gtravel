from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-post', CreatePost, name='create-post'),
    path('update-post/<int:id>', UpdatePost, name='update-post'),
    path('delete-post/<int:id>', DeletePost, name='delete-post'),
    path('create-post-category', CreatePostCategory, name='create-post-category'),
    path('update-post-category/<int:id>', UpdatePostCategory, name='update-post-category'),
    path('delet-post-category/<int:id>', DeletPostCategory, name='delet-post-category'),
    path('post-category-list', PostCategoryList, name='post-category-list'),
    path('post-list', ListPost, name='post-list'),
    path('add_related_post/<int:id>', add_related_post, name='add_related_post'),
    path('update_related_post/<int:id>', update_related_post, name='update_related_post'),
    path('delete_related_post/<int:id>', delete_related_post, name='delete_related_post'),
    path('comments_list', comments_list, name='comments_list'),
    path('update_comment/<int:id>', update_comment, name='update_comment'),
    path('delete_comment/<int:id>', delete_comment, name='delete_comment'),
    path('ajax_related_pst', ajax_related_pst, name='ajax_related_pst'),
    path('publish_reply/<int:id>', publish_reply, name='publish_reply'),
    path('remove_reply/<int:id>', remove_reply, name='remove_reply'),
    path('toggle_reply_publish/<int:id>', toggle_reply_publish, name='toggle_reply_publish'),
]