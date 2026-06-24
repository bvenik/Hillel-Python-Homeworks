from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import ProjectTask
from .forms import ProjectTaskForm, CustomUserCreationForm


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
