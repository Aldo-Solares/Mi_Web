from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea
    
class Crearcuenta(FormView):
    template_name = "base/Registro.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tareas")
    
    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(Crearcuenta, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tareas")
        return super(Crearcuenta, self).get(*args, **kwargs)
    
class Logueo(LoginView):
    template_name = "base/login.html"
    field = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy("tareas")

class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = "tareas"
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["tareas"] = contexto["tareas"].filter(usuario=self.request.user)
        contexto["count"] = contexto["tareas"].filter(completo=False).count()
        
        valor_buscado = self.request.GET.get("buscador") or  ""
        if valor_buscado:
            contexto["tareas"] = contexto["tareas"].filter(titulo__icontains  = valor_buscado)
        contexto["valor_buscado"] = valor_buscado
        
        return contexto
    
class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = "tareas_d"
    template_name = "base/Detalle_tareas.html"
    
class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo','descripcion', 'completo']
    success_url = reverse_lazy("tareas")
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)
    
class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo','descripcion', 'completo']
    success_url = reverse_lazy("tareas")
    
class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = "tareas"
    success_url = reverse_lazy("tareas")
