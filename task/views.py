from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Task
from django.db.models import Q 
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page upon successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to the home page upon successful login
        else:
            # Handle invalid login credentials
            return render(request, "registration/login.html", {"error": "Invalid login credentials"})
    return render(request, "registration/login.html")

@login_required
def home(request):
    if request.method == "POST" and "logout" in request.POST:
        logout(request)
        return redirect("login")  # Redirect to the login page after logging out
    return render(request, "home.html")

# @login_required
# def home(request):
#     tasks = Task.objects.all()  # Retrieve all tasks (you can filter them as needed)
#     return render(request, "home.html", {"tasks": tasks})

@login_required
def home(request):
    tasks = Task.objects.all()

    # Search by title
    search_query = request.GET.get("search")
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Filter by creation date
    creation_date = request.GET.get("creation_date")
    if creation_date:
        tasks = tasks.filter(creation_datetime=creation_date)

    # Filter by due date
    due_date = request.GET.get("due_date")
    if due_date:
        tasks = tasks.filter(due_date=due_date)

    # Filter by priority
    priority = request.GET.get("priority")
    if priority:
        tasks = tasks.filter(priority=priority)

    # Filter by completion status
    is_complete = request.GET.get("is_complete")
    if is_complete == "true":
        tasks = tasks.filter(is_complete=True)
    elif is_complete == "false":
        tasks = tasks.filter(is_complete=False)

    return render(request, "home.html", {"tasks": tasks})


class TaskUpdateView(UpdateView):
    model = Task
    template_name = "update_task.html"
    fields = ['title', 'description', 'due_date', 'priority', 'is_complete']
    success_url = reverse_lazy('home')

def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('home')