from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from trip.firebase import create_log, delete_log_fb, read_log_by_date, read_logs, read_logs_by_date_range, update_log_fb

@csrf_exempt
def add_log(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            date = data.get("date")
            logEntry = data.get("logEntry")

            if not date or not logEntry:
                return JsonResponse({"error": "logEntry and date are required"}, status=400)

            log_id = create_log(logEntry,date)
            return JsonResponse({"message": "Log added", "log_id": log_id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

def get_logs(request):
    if request.method == "GET":
        logs_data = read_logs()
        if logs_data:
            keys = logs_data.keys()
            logs = [{"id": n, **(logs_data.get(n) or {})} for n in keys]
            return JsonResponse(logs, safe=False, status=200)
        return JsonResponse({"error": "Log not found"}, status=404)
    
@csrf_exempt
def get_log(request, date):
    if request.method == "GET":
        log_data = read_log_by_date(date)
        if log_data:
            keys = log_data.keys()
            logs = [{"id": n, **(log_data.get(n) or {})} for n in keys]
            return JsonResponse(logs, safe=False,status=200)
        return JsonResponse({"error": "Log not found"}, status=404)

def get_log_by_range(request):
    if request.method == "GET":
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        logs_data = read_logs_by_date_range(start_date,end_date)
        if logs_data:
            keys = logs_data.keys()
            logs = [{"id": n, **(logs_data.get(n) or {})} for n in keys]
            return JsonResponse(logs,safe=False, status=200)
        return JsonResponse({"error": "Log not found"}, status=404)


@csrf_exempt
def update_log(request, log_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            logEntry = data.get("logEntry")

            updated = update_log_fb(log_id,logEntry)
            if updated:
                return JsonResponse({"message": "Log updated successfully"}, status=200)
            return JsonResponse({"error": "No fields to update"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@csrf_exempt
def delete_log(request, log_id):
    if request.method == "DELETE":
        deleted = delete_log_fb(log_id)
        if deleted:
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        return JsonResponse({"error": "User not found"}, status=404)

