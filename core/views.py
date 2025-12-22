from django.shortcuts import render,redirect
from .forms import IssueForm
from .models import Issue
import random
from django.utils import timezone
from datetime import timedelta




def home(request):
    return render(request, 'core/index.html')

def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)

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

def public_issues(request):
    issues = Issue.objects.all()

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
