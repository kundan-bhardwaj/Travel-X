from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('book/',book,name='book'),
    path('post-book/',postBook,name='post-book'),
    path('cancel/',cancel,name='cancel')
]