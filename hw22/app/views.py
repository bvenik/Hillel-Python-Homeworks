from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import ProjectTaskForm, CustomUserCreationForm
from rest_framework import generics, permissions
from .serializers import ProjectTaskSerializer
from .models import ProjectTask


class TaskListView(ListView):
    model = ProjectTask
    template_name = 'app/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ProjectTask.objects.none()

        query = "SELECT * FROM app_projecttask WHERE user_id = %s ORDER BY created_at DESC"
        return ProjectTask.objects.raw(query, [self.request.user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['stats'] = ProjectTask.get_user_statistics(self.request.user)
        return context


class TaskCreateView(CreateView):
    model = ProjectTask
    form_class = ProjectTaskForm
    template_name = 'app/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class ProjectTaskAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        queryset = ProjectTask.objects.all()

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status_code=status_param.upper())

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
