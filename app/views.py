from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .rfq_cleaner import process_rfq_file

# Demo credentials
DEMO_USERNAME = 'pratikakhare@'
DEMO_PASSWORD = 'Shipco@123'


def login_view(request):
    """Handle user login with demo credentials."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Verify credentials
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            # Set session to mark user as logged in
            request.session['user_logged_in'] = True
            request.session['username'] = username
            request.session.set_expiry(3600)  # 1 hour session
            return redirect('index')
        else:
            context = {'error': 'Invalid username or password. Please try again.'}
            return render(request, 'app/login.html', context)
    
    # Redirect to index if already logged in
    if request.session.get('user_logged_in'):
        return redirect('index')
    
    return render(request, 'app/login.html')


def logout_view(request):
    """Handle user logout."""
    request.session.flush()
    return redirect('login')


def check_login(view_func):
    """Decorator to check if user is logged in."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_logged_in'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_http_methods(['GET', 'POST'])
@check_login
def index(request):
    context = {
        'username': request.session.get('username', 'User')
    }
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            context['error'] = 'Please upload an Excel file.'
            return render(request, 'app/index.html', context)
        try:
            file_content = process_rfq_file(uploaded_file)
            response = HttpResponse(
                file_content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=cleaned_rfq.xlsx'
            return response
        except Exception as exc:
            context['error'] = str(exc)
    return render(request, 'app/index.html', context)
