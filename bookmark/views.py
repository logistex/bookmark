# bookmark/views.py
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy


from .models import Bookmark


class BookmarkListView(ListView):
    model = Bookmark


class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['site_name','url']
    success_url = reverse_lazy('list')  # 글쓰기를 완료했을 때 이동할 페이지
    template_name_suffix = '_create'


class BookmarkDetailView(DetailView):
    model = Bookmark
