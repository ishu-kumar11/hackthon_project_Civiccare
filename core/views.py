from django.shortcuts import render,redirect
from .forms import IssueForm
from .models import Issue
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import UserProfile


from django.http import JsonResponse
from .models import Issue, IssueVote


def home(request):
    return render(request, 'core/index.html')


@login_required(login_url='login')
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user

            issue.otp = generate_otp()
            issue.otp_created_at = timezone.now()
            issue.is_verified = False

            issue.save()

            print("DEV OTP:", issue.otp)

            return redirect('verify_otp', issue_id=issue.id)
    else:
        form = IssueForm()

    return render(request, 'core/report_issue.html', {'form': form})


def success(request, complaint_id):
    return render(request, 'core/success.html', {
        'complaint_id': complaint_id
    })




@login_required(login_url='login')
def track_issue(request):
    issue = None
    error = None

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')

        try:
            issue = Issue.objects.get(complaint_id=complaint_id)
        except Issue.DoesNotExist:
            error = "No issue found with this Complaint ID."

    return render(request, 'core/track_issue.html', {
        'issue': issue,
        'error': error
    })

from django.db.models import Count, Q

def public_issues(request):

    # Base queryset with vote counts
    issues = Issue.objects.annotate(
        real_votes=Count('issuevote', filter=Q(issuevote__vote=True)),
        fake_votes=Count('issuevote', filter=Q(issuevote__vote=False)),
    )

    # Filters
    category = request.GET.get('category')
    status = request.GET.get('status')

    if category:
        issues = issues.filter(category=category)

    if status:
        issues = issues.filter(status=status)

    return render(request, 'core/public_issues.html', {
        'issues': issues
    })


def generate_otp():
    return str(random.randint(100000, 999999))



def verify_otp(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    error = None

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if issue.otp != entered_otp:
            error = "Invalid OTP"
        else:
            issue.is_verified = True
            issue.otp = None
            issue.save()

            return redirect('success', complaint_id=issue.complaint_id)

    return render(request, 'core/verify_otp.html', {
        'issue': issue,
        'error': error
    })



from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'core/login.html')


from django.contrib.auth.models import User


from django.contrib.auth import login
import re

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        district = request.POST.get('district')
        location = request.POST.get('location')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password match check
        if password1 != password2:
            return render(request, 'core/register.html', {
                'error': 'Passwords do not match'
            })

        # Phone validation
        if not phone or not phone.isdigit() or len(phone) != 10:
            return render(request, 'core/register.html', {
                'error': 'Phone number must be exactly 10 digits'
            })

        # Username exists
        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {
                'error': 'Username already exists'
            })

        # Phone exists
        if UserProfile.objects.filter(phone=phone).exists():
            return render(request, 'core/register.html', {
                'error': 'Phone number already registered'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password1
        )

        # ✅ CREATE profile properly
        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.phone = phone
        profile.state = state
        profile.district = district
        profile.location = location.strip().lower()
        profile.pincode = pincode
        profile.save()

        login(request, user)
        return redirect('home')

    return render(request, 'core/register.html')


@login_required
def vote_issue(request, issue_id):

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        issue = Issue.objects.get(id=issue_id)
        user = request.user

        # Ensure profile exists
        user_profile, _ = UserProfile.objects.get_or_create(user=user)

        vote_type = request.POST.get('vote')

        if vote_type not in ['real', 'fake']:
            return JsonResponse({'error': 'Invalid vote'}, status=400)

        # Area safety check
        if not user_profile.location or not issue.location:
            return JsonResponse({'error': 'Area not set'}, status=400)

        # Area comparison
        if user_profile.location.strip().lower() != issue.location.strip().lower():
            return JsonResponse({'error': 'Only people from this area can vote'}, status=403)

        vote_value = True if vote_type == 'real' else False

        IssueVote.objects.update_or_create(
            user=user,
            issue=issue,
            defaults={'vote': vote_value}
        )

        real_count = IssueVote.objects.filter(issue=issue, vote=True).count()
        fake_count = IssueVote.objects.filter(issue=issue, vote=False).count()

        return JsonResponse({
            'real': real_count,
            'fake': fake_count
        })

    except Exception as e:
        print("VOTE ERROR:", e)  # 👈 VERY IMPORTANT
        return JsonResponse({'error': 'Server error'}, status=500)



import requests


def pincode_lookup(request):
    pincode = request.GET.get('pincode')

    if not pincode or len(pincode) != 6:
        return JsonResponse({'error': 'Invalid pincode'}, status=400)

    url = f"https://api.postalpincode.in/pincode/{pincode}"

    try:
        response = requests.get(
            url,
            timeout=5,   # 👈 VERY IMPORTANT
            headers={
                "User-Agent": "CivicCare/1.0"
            }
        )

        data = response.json()

        if data[0]['Status'] != 'Success':
            return JsonResponse({'error': 'Pincode not found'}, status=404)

        po = data[0]['PostOffice']

        return JsonResponse({
            'state': po[0]['State'],
            'district': po[0]['District'],
            'areas': [p['Name'] for p in po]
        })

    except requests.exceptions.RequestException as e:
        print("PINCODE API ERROR:", e)  # 👈 for debugging
        return JsonResponse(
            {'error': 'Pincode service temporarily unavailable'},
            status=503
        )



@login_required
def user_dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    my_issues = Issue.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        # Update allowed fields only
        profile.phone = phone
        profile.location = location.strip().lower()
        profile.save()

    context = {
        'profile': profile,
        'issues': my_issues
    }

    return render(request, 'core/dashboard.html', context)






