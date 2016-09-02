from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import timedelta
from .models import CheckInCheckOut, CustomUser, TimeEntryLog
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from .forms import TimeEntryForm, NewTimeEntryForm

def index(request):
    context = {}
    if request.user.is_authenticated:
        now = timezone.now()
        
        # Weekly hours
        start_of_week = now.date() - timedelta(days=now.weekday())
        weekly_checkins = CheckInCheckOut.objects.filter(
            user=request.user,
            check_in_time__date__gte=start_of_week,
            check_out_time__isnull=False
        )
        weekly_hours = sum(((ci.check_out_time - ci.check_in_time) for ci in weekly_checkins), timedelta())
        context['weekly_hours'] = weekly_hours.total_seconds() / 3600

        # Monthly hours
        start_of_month = now.date().replace(day=1)
        monthly_checkins = CheckInCheckOut.objects.filter(
            user=request.user,
            check_in_time__date__gte=start_of_month,
            check_out_time__isnull=False
        )
        monthly_hours = sum(((ci.check_out_time - ci.check_in_time) for ci in monthly_checkins), timedelta())
        context['monthly_hours'] = monthly_hours.total_seconds() / 3600
        
    return render(request, 'tracker/index.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def time_history(request):
    checkin_list = CheckInCheckOut.objects.filter(user=request.user).order_by('-check_in_time')
    paginator = Paginator(checkin_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tracker/time_history.html', {'page_obj': page_obj})

@login_required
def team_timesheet(request):
    if not request.user.is_manager:
        return redirect('index')

    managed_users = request.user.managed_users
    
    now = timezone.now()
    start_of_week = now.date() - timedelta(days=now.weekday())

    timesheet_data = []
    for user in managed_users:
        weekly_checkins = CheckInCheckOut.objects.filter(
            user=user,
            check_in_time__date__gte=start_of_week,
            check_out_time__isnull=False
        )
        weekly_hours = sum(((ci.check_out_time - ci.check_in_time) for ci in weekly_checkins), timedelta())
        timesheet_data.append({
            'user': user,
            'weekly_hours': weekly_hours.total_seconds() / 3600
        })

    return render(request, 'tracker/team_timesheet.html', {'timesheet_data': timesheet_data})

@login_required
def export_monthly_timesheet(request):
    if not request.user.is_staff:
        return redirect('index')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monthly_timesheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Total Hours'])

    now = timezone.now()
    start_of_month = now.date().replace(day=1)
    
    if now.month == 12:
        start_of_next_month = now.date().replace(year=now.year + 1, month=1, day=1)
    else:
        start_of_next_month = now.date().replace(month=now.month + 1, day=1)

    users = CustomUser.objects.all()
    for user in users:
        monthly_checkins = CheckInCheckOut.objects.filter(
            user=user,
            check_in_time__date__gte=start_of_month,
            check_in_time__date__lt=start_of_next_month,
            check_out_time__isnull=False
        )
        monthly_hours = sum(((ci.check_out_time - ci.check_in_time) for ci in monthly_checkins), timedelta())
        writer.writerow([user.username, f"{monthly_hours.total_seconds() / 3600:.2f}"])

    return response

@login_required
def view_user_timesheet(request, user_id):
    if not request.user.is_manager:
        return redirect('index')
    
    managed_user = get_object_or_404(CustomUser, id=user_id)
    if managed_user not in request.user.managed_users.all():
        return redirect('team_timesheet')

    checkin_list = CheckInCheckOut.objects.filter(user=managed_user).order_by('-check_in_time')
    paginator = Paginator(checkin_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'managed_user': managed_user,
        'page_obj': page_obj
    }
    return render(request, 'tracker/view_user_timesheet.html', context)

@login_required
def edit_time_entry(request, entry_id):
    if not request.user.is_manager:
        return redirect('index')

    entry = get_object_or_404(CheckInCheckOut, id=entry_id)
    managed_user = entry.user

    if managed_user not in request.user.managed_users.all():
        return redirect('team_timesheet')

    if request.method == 'POST':
        old_entry = get_object_or_404(CheckInCheckOut, id=entry_id)
        old_check_in = old_entry.check_in_time
        old_check_out = old_entry.check_out_time

        form = TimeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            new_entry = form.save() # Save the form first to update the entry object
            
            TimeEntryLog.objects.create(
                entry=new_entry,
                edited_by=request.user,
                old_check_in=old_check_in,
                new_check_in=new_entry.check_in_time,
                old_check_out=old_check_out,
                new_check_out=new_entry.check_out_time
            )
            
            return redirect('view_user_timesheet', user_id=managed_user.id)
    else:
        form = TimeEntryForm(instance=entry)

    context = {
        'form': form,
        'entry': entry
    }
    return render(request, 'tracker/edit_time_entry.html', context)

@login_required
def add_time_entry(request):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        form = NewTimeEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewTimeEntryForm()

    return render(request, 'tracker/add_time_entry.html', {'form': form})