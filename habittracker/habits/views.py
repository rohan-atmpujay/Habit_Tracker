from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Habit, HabitRecord
from django.contrib import messages
from django.contrib.auth import login, logout
from datetime import date, timedelta


def home(request):
    return render(request, "habits/home.html")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('habit_list')
        else:
            messages.error(request, "Invalid username or password!")
    else:
        form = AuthenticationForm()

    return render(request, 'habits/login.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'habits/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = date.today()

    # mark done_today attribute for template
    for h in habits:
        h.done_today = h.habitrecord_set.filter(date=today).exists()

    return render(request, 'habits/habit_list.html', {
        'habits': habits
    })


@login_required
def habit_add(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST.get('description', '')
        Habit.objects.create(user=request.user, name=name, description=description)
        return redirect('habit_list')
    return render(request, 'habits/habit_add.html')


@login_required
def habit_edit(request, id):
    habit = get_object_or_404(Habit, id=id, user=request.user)
    if request.method == 'POST':
        habit.name = request.POST['name']
        habit.description = request.POST.get('description', '')
        habit.save()
        return redirect('habit_list')
    return render(request, "habits/habit_edit.html", {"habit": habit})


@login_required
def habit_delete(request, id):
    habit = get_object_or_404(Habit, id=id, user=request.user)
    habit.delete()
    return redirect('habit_list')


@login_required
def mark_done(request, id):
    habit = get_object_or_404(Habit, id=id, user=request.user)

    HabitRecord.objects.get_or_create(
        habit=habit,
        date=date.today(),
        defaults={'status': True}
    )

    return redirect('habit_list')


@login_required
def habit_detail(request, id):
    habit = get_object_or_404(Habit, id=id, user=request.user)
    records = HabitRecord.objects.filter(habit=habit).order_by('-date')

    # current streak
    current_streak = 0
    today = date.today()
    for r in records:
        if r.date == today - timedelta(days=current_streak):
            current_streak += 1
        else:
            break

    # longest streak
    longest_streak = 0
    streak = 0
    prev_date = None

    for r in records.order_by("date"):
        if prev_date and r.date == prev_date + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        longest_streak = max(longest_streak, streak)
        prev_date = r.date

    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'records': records,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
    })


@login_required
def dashboard(request):
    today = date.today()
    habits = Habit.objects.filter(user=request.user)

    # today status
    today_records = {
        h.id: HabitRecord.objects.filter(habit=h, date=today).exists()
        for h in habits
    }

    # last 7 days
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]

    weekly_data = []

    for h in habits:
        day_status = []
        for d in week_dates:
            done = HabitRecord.objects.filter(habit=h, date=d).exists()
            day_status.append(done)

        weekly_data.append({
            "habit": h,
            "status": day_status
        })

    return render(request, 'habits/dashboard.html', {
        'habits': habits,
        'today_records': today_records,
        'week_dates': week_dates,
        'weekly_data': weekly_data,
    })
