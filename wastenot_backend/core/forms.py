from django import forms
from .models import Item, ExchangeSchedule, Message
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

class ExchangeScheduleForm(forms.ModelForm):
    class Meta:
        model = ExchangeSchedule
        fields = ['scheduled_date', 'location', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 3}),
        }

    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data['scheduled_date']
        if scheduled_date < timezone.now():
            raise forms.ValidationError("Scheduled date cannot be in the past.")
        return scheduled_date

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content', 'attachments']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'subject': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 4}),
            'attachments': forms.FileInput(attrs={'class': 'hidden'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users with confirmed exchanges as recipients
        if 'initial' in kwargs and 'recipient' in kwargs['initial']:
            self.fields['recipient'].initial = kwargs['initial']['recipient']
            self.fields['recipient'].widget = forms.HiddenInput()
        else:
            user = kwargs.get('initial', {}).get('user')
            if user:
                # Get users with confirmed exchanges
                confirmed_users = User.objects.filter(
                    Q(donor_schedules__recipient=user, donor_schedules__status='confirmed') |
                    Q(recipient_schedules__donor=user, recipient_schedules__status='confirmed')
                ).distinct()
                self.fields['recipient'].queryset = confirmed_users
            else:
                self.fields['recipient'].queryset = User.objects.none() 