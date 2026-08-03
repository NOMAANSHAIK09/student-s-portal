from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

from .models import UserInfo, QuestionPaper
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
            password=make_password(password)
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
            if check_password(password, user.password):
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
    user_id = request.session.get('user_id')
    if not user_id:
            return redirect('login')
        
    userinfo = UserInfo.objects.get(id=user_id)
         
    return render(request, 'about.html',{'userinfo': userinfo})

def contact(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
            
    userinfo = UserInfo.objects.get(id=user_id)
    return render(request, 'contact.html',{'userinfo': userinfo})

def exampaper(request):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    userinfo = UserInfo.objects.get(id=user_id)

    subject = request.GET.get('subject', '').strip()
    branch = request.GET.get('branch', '').strip()
    semester = request.GET.get('semester', '').strip()
    year = request.GET.get('year', '').strip()

    # All papers
    papers = QuestionPaper.objects.all()

    # Apply filters
    if subject:
        papers = papers.filter(
            subject__icontains=subject
        )

    if branch:
        papers = papers.filter(
            department__iexact=branch
        )

    if semester:
        papers = papers.filter(
            semester=semester
        )

    if year:
        papers = papers.filter(
            exam_year=year
        )

    # Latest uploads
    latest_papers = QuestionPaper.objects.all().order_by('-id')[:3]
    # if latest_papers < 3:
    #     latest_papers = QuestionPaper.objects.all().order_by('-id')[:latest_papers]
    # else:
    #     latest_papers = QuestionPaper.objects.all().order_by('-id')[:3]
    
    

    return render(request, 'exampaper.html', {
        'papers': papers,
        'latest_papers': latest_papers,
        'userinfo': userinfo
    })
    
    

        
    # return render(request, 'dashboard.html')


def download_paper(request, paper_id):

    # Check login
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    # Get question paper
    paper = get_object_or_404(
        QuestionPaper,
        id=paper_id
    )

    # Download PDF from Supabase
    file_data = paper.pdf.storage.download(
        paper.pdf.name
    )

    # Create response
    response = HttpResponse(
        file_data,
        content_type='application/pdf'
    )

    # Force browser download
    filename = paper.pdf.name.split('/')[-1]

    response['Content-Disposition'] = (
        f'attachment; filename="{filename}"'
    )

    return response
