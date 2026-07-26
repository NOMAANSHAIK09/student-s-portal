from django.shortcuts import render, redirect

from .models import UserInfo
# Create your views here.
# from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')



def signup(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        roll_no=request.POST.get('roll_no')
        branch=request.POST.get('branch')
        semester=request.POST.get('semester')
        password=request.POST.get('password')
        
        user=UserInfo(
            name=name,
            email=email,
            roll_no=roll_no,
            branch=branch,
            semester=semester,
            password=password
        )
        user.save()
        
        request.session['user_id'] = user.id  # Store the user ID in the session
        return redirect('dashboard')
        
        

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user = UserInfo.objects.get(email=email)
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('dashboard')
                # return render(request, 'dashboard.html' )
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except UserInfo.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
    
    return render(request, 'login.html')


def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    userinfo = UserInfo.objects.get(id=user_id)
    return render(request, 'dashboard.html', {'userinfo': userinfo})

def logout(request):
    request.session.flush()
    return redirect('login')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def exampaper(request):
    return render(request, 'exampaper.html')


        
    # return render(request, 'dashboard.html')

