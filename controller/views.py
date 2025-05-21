from django.shortcuts import render
from .drone import takeoff
import threading

# গ্লোবাল ভেরিয়েবল স্ট্যাটাস লগের জন্য
status_log = []
takeoff_thread = None

def run_takeoff():
    global status_log
    status_log = takeoff()

def control_view(request):
    global takeoff_thread, status_log
    if 'takeoff' in request.GET and (takeoff_thread is None or not takeoff_thread.is_alive()):
        takeoff_thread = threading.Thread(target=run_takeoff)
        takeoff_thread.start()

    parsed_status = []
    for line in status_log:
        if ':' in line:
            key, val = line.split(':', 1)
            parsed_status.append((key.strip(), val.strip()))
        else:
            # কোলন না থাকলে পুরো লাইন ভ্যালু হিসেবে রাখুন
            parsed_status.append(('', line))

    return render(request, 'control.html', {
        'status_log': parsed_status,
        'in_progress': takeoff_thread.is_alive() if takeoff_thread else False
    })

