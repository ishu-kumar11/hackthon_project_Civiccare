from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.conf import settings





class Issue(models.Model):



    STATE_CHOICES = [
    ('AN', 'Andaman and Nicobar Islands'),
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CH', 'Chandigarh'),
    ('CT', 'Chhattisgarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('LA', 'Ladakh'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
]

    state = models.CharField(max_length=5, choices=STATE_CHOICES)


    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )



    CATEGORY_CHOICES = [
        ('road', 'Road & Potholes'),
        ('water', 'Water Supply'),
        ('electricity', 'Electricity'),
        ('garbage', 'Garbage & Sanitation'),
        ('street', 'Street Lights'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='issues',
    null=True,        
    blank=True
)

    complaint_id = models.CharField(max_length=20, unique=True, blank=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    pincode = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='issues/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_public = models.BooleanField(default=True)  

    phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid 10-digit Indian mobile number."
)

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[phone_validator])

    is_verified = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    # ===============================
    # AUTHORITY CONTROL FIELDS
    # ===============================

    is_fake = models.BooleanField(default=False)

    fake_marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fake_marked_issues'
    )

    fake_marked_at = models.DateTimeField(null=True, blank=True)

    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authority_updates'
    )

    updated_at = models.DateTimeField(auto_now=True)





    def save(self, *args, **kwargs):
        if not self.complaint_id:
            year = timezone.now().year
            last_issue = Issue.objects.order_by('id').last()
            next_id = 1 if not last_issue else last_issue.id + 1
            self.complaint_id = f"CC-{year}-{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.complaint_id







# USER PROFILE MODEL

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  

    def __str__(self):
        return self.user.username



# SIGNALS (AUTO CREATE PROFILE)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)





class IssueVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    vote = models.BooleanField()  # True = Real, False = Fake
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'issue')  # one vote per user per issue

    def __str__(self):
        return f"{self.user.username} - {self.issue.title}"



class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('MARK_FAKE', 'Marked as Fake'),
        ('STATUS_UPDATE', 'Status Updated'),
        ('EDIT', 'Issue Edited'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    issue = models.ForeignKey(
        Issue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    remarks = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
