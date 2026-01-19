from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q
from core.models import Issue, AuditLog   # 👈 IMPORTANT (app name change)
from django.contrib.auth.decorators import login_required


# =========================
# Authority Permission
# =========================
def authority_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized")
    return wrapper


# =========================
# Dashboard
# =========================
@authority_required
def authority_dashboard(request):

    issues = Issue.objects.all().order_by('-created_at')

    stats = {
        'pending': Issue.objects.filter(status='pending', is_fake=False).count(),
        'in_progress': Issue.objects.filter(status='in_progress', is_fake=False).count(),
        'resolved': Issue.objects.filter(status='resolved', is_fake=False).count(),
        'fake': Issue.objects.filter(is_fake=True).count(),
    }

    return render(request, 'authority/dashboard.html', {
        'issues': issues,
        'stats': stats
    })


# =========================
# Issue List + Filters
# =========================
@authority_required
def authority_issue_list(request):

    query = request.GET.get('q')
    status = request.GET.get('status')
    category = request.GET.get('category')

    issues = Issue.objects.all()

    if query:
        issues = issues.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(complaint_id__icontains=query)
        )

    if status:
        issues = issues.filter(status=status)

    if category:
        issues = issues.filter(category=category)

    issues = issues.order_by('-created_at')

    return render(request, 'authority/issue_list.html', {
        'issues': issues
    })


# =========================
# Mark Issue Fake
# =========================
@authority_required
def mark_issue_fake(request, issue_id):

    issue = Issue.objects.get(id=issue_id)

    issue.is_fake = True
    issue.status = 'pending'
    issue.fake_marked_by = request.user
    issue.fake_marked_at = timezone.now()
    issue.last_updated_by = request.user
    issue.save()

    AuditLog.objects.create(
        user=request.user,
        issue=issue,
        action='MARK_FAKE',
        remarks='Marked as fake by authority'
    )

    return redirect('authority_dashboard')


# =========================
# Update Issue Status
# =========================
@authority_required
def update_issue_status(request, issue_id):

    issue = Issue.objects.get(id=issue_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status not in ['pending', 'in_progress', 'resolved']:
            return HttpResponseForbidden("Invalid status")

        issue.status = new_status
        issue.last_updated_by = request.user
        issue.save()

        AuditLog.objects.create(
            user=request.user,
            issue=issue,
            action='STATUS_UPDATE',
            remarks=f"Status changed to {new_status}"
        )

        return redirect('authority_dashboard')

    return render(request, 'authority/update_status.html', {
        'issue': issue
    })


# =========================
# Audit Logs
# =========================
@authority_required
def audit_logs(request):

    logs = AuditLog.objects.select_related('user', 'issue').order_by('-timestamp')

    return render(request, 'authority/audit_logs.html', {
        'logs': logs
    })
