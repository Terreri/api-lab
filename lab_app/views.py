from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from .models import Users

class MenuView(TemplateView):
    template_name = 'index.html'
    

class UserListView(ListView):
    model = Users
    template_name = 'users_list.html'
    
class UserCreateView(CreateView):
    model = Users
    fields = ['nome','email','telefone', 'user_type']
    template_name = 'users_create.html'
    def get_success_url(self):
        return reverse('UserListView')
    
class UserUpdateView(UpdateView):
    model = Users
    fields = ['nome','email','telefone', 'user_type']
    template_name = 'users_update.html'
    def get_success_url(self):
        return reverse('UserListView')
    
class UserDeleteView(DeleteView):
    model = Users
    template_name = 'users_delete.html'
    def get_success_url(self):
        return reverse('UserListView')