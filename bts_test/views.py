import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

# Default values for the OAuth configuration
DEFAULT_CLIENT_ID = "5e5ca034-a583-4f9b-bdf7-91b7613e9baa"
DEFAULT_REDIRECT_URI = "https://zabotaplus.kz/bts-test/redirect"

@csrf_exempt
def init(request):
    """
    Generate and return an OAuth link with configurable parameters
    """
    client_id = request.GET.get('client_id', DEFAULT_CLIENT_ID)
    redirect_uri = request.GET.get('redirect_uri', DEFAULT_REDIRECT_URI)
    state = request.GET.get('state', '')
    
    auth_url = (
        f"https://passport.aitu.io/oauth2/auth"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&state={state}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=selfie%20identification_document_manual"
    )
    
    return JsonResponse({'auth_url': auth_url})

@csrf_exempt
def redirect(request):
    """
    Save POST data to a file
    """
    if request.method == 'POST':
        data = request.POST.dict()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Save to redirect.log
        log_file = os.path.join(logs_dir, 'redirect.log')
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {json.dumps(data)}\n")
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'})

@csrf_exempt
def logout(request):
    """
    Save logout POST data to a file
    """
    if request.method == 'POST':
        data = request.POST.dict()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Save to logout.log
        log_file = os.path.join(logs_dir, 'logout.log')
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {json.dumps(data)}\n")
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}) 