from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator




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




    def save(self, *args, **kwargs):
        if not self.complaint_id:
            year = timezone.now().year
            last_issue = Issue.objects.order_by('id').last()
            next_id = 1 if not last_issue else last_issue.id + 1
            self.complaint_id = f"CC-{year}-{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.complaint_id

