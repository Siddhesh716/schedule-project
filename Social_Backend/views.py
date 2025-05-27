from django.shortcuts import render, redirect
from datetime import datetime, timedelta

def home(request):
    return render(request, "home.html")

def schedule_view(request):
    if 'all_schedules' not in request.session:
        request.session['all_schedules'] = []
    all_schedules = request.session.get('all_schedules', [])

    if request.method == 'POST' and 'delete_index' in request.POST:
        delete_index = int(request.POST.get('delete_index'))
        if 0 <= delete_index < len(all_schedules):
            all_schedules.pop(delete_index)
            request.session['all_schedules'] = all_schedules
        return redirect('schedule_view')

    if request.method == 'POST' and 'delete_index' not in request.POST:
        staff = request.POST.get('staff')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        slot_minutes = int(request.POST.get('slot_minutes'))
        time_format = '%H:%M'
        start_dt = datetime.strptime(start_time, time_format)
        end_dt = datetime.strptime(end_time, time_format)

        start_time_12 = datetime.strptime(start_time, time_format).strftime('%I:%M %p')
        end_time_12 = datetime.strptime(end_time, time_format).strftime('%I:%M %p')

        slots = []
        while start_dt + timedelta(minutes=slot_minutes) <= end_dt:
            slot_end = start_dt + timedelta(minutes=slot_minutes)
            slots.append(f"{start_dt.strftime('%I:%M %p')} to {slot_end.strftime('%I:%M %p')}")
            start_dt = slot_end
        all_schedules.append({
            'staff': staff,
            'date': date,
            'start_time': start_time_12,
            'end_time': end_time_12,
            'slot_minutes': slot_minutes,
            'slots': slots
        })
        request.session['all_schedules'] = all_schedules
        return redirect('schedule_view')
    return render(request, 'Events.html', {'schedules': all_schedules})