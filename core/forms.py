from django import forms
from django.core.exceptions import ValidationError
from .models import Issue

class IssueForm(forms.ModelForm):

    MAX_VIDEO_MB = 20
    MAX_PHOTO_MB = 5

    class Meta:
        model = Issue
        fields = [
            'full_name',
            'phone',
            'category',
            'urgency',
            'title',
            'description',
            'state',
            'district',
            'location',
            'pincode',
            'photo',
            'video'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '10-digit mobile number',
                'maxlength': '10'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        urgency = cleaned_data.get("urgency")
        photo = cleaned_data.get("photo")
        video = cleaned_data.get("video")

        # ✅ PHOTO SIZE CHECK
        if photo:
            if photo.size > self.MAX_PHOTO_MB * 1024 * 1024:
                raise ValidationError(f"Photo must be under {self.MAX_PHOTO_MB} MB.")

        # ✅ VIDEO SIZE CHECK + FORMAT CHECK
        if video:
            if video.size > self.MAX_VIDEO_MB * 1024 * 1024:
                raise ValidationError(f"Video must be under {self.MAX_VIDEO_MB} MB.")

            # allow only mp4 (best for web)
            if not video.name.lower().endswith(".mp4"):
                raise ValidationError("Only MP4 videos are allowed.")

        # ✅ URGENCY RULES
        # low => photo optional + video optional
        if urgency == "low":
            return cleaned_data

        # medium => photo mandatory
        if urgency == "medium" and not photo:
            raise ValidationError("Photo is required when urgency is Medium.")

        # high => photo + video mandatory
        if urgency == "high":
            if not photo:
                raise ValidationError("Photo is required when urgency is High.")
            if not video:
                raise ValidationError("Video is required when urgency is High.")

        return cleaned_data
