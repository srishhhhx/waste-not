from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

# Add these imports at the top of the file
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
import uuid

# In your Item model, add these fields and methods
class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50)
    location = models.CharField(max_length=500)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_items')
    received_at = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    pickup_code = models.CharField(max_length=36, blank=True, null=True, unique=True)
    
    def save(self, *args, **kwargs):
        # Generate a unique pickup code if it doesn't exist
        if not self.pickup_code:
            self.pickup_code = str(uuid.uuid4())
            
        # Generate QR code if it doesn't exist and the item has an ID
        if not self.qr_code and self.id:
            self.generate_qr_code()
            
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        # URL for scanning the QR code
        pickup_url = reverse('confirm_pickup', args=[self.pickup_code])
        absolute_url = f"{settings.BASE_URL}{pickup_url}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(absolute_url)
        qr.make(fit=True)
        
        # Create image from QR code - this is the corrected line
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code image
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"qr_code_{self.id}.png", ContentFile(buffer.getvalue()), save=False)

    def __str__(self):
        return self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.item.title}"

class ExchangeSchedule(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='schedules')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_schedules')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_schedules')
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Exchange for {self.item.title} on {self.scheduled_date}"

    def send_notification(self, subject, message):
        """Send email notification to both donor and recipient"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.donor.email, self.recipient.email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Send initial notification
            subject = f"New Exchange Scheduled: {self.item.title}"
            message = f"""
            A new exchange has been scheduled:
            
            Item: {self.item.title}
            Date: {self.scheduled_date}
            Location: {self.location}
            
            Please confirm the details and contact the other party if needed.
            """
            self.send_notification(subject, message)
        elif self.status == 'confirmed':
            # Send confirmation notification
            subject = f"Exchange Confirmed: {self.item.title}"
            message = f"""
            The exchange has been confirmed:
            
            Item: {self.item.title}
            Date: {self.scheduled_date}
            Location: {self.location}
            
            Please make sure to be at the location on time.
            """
            self.send_notification(subject, message)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    exchange_schedule = models.ForeignKey(ExchangeSchedule, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(upload_to='message_attachments/', null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    def send_notification(self):
        """Send email notification to recipient"""
        send_mail(
            f"New Message: {self.subject}",
            f"""
            You have received a new message from {self.sender.username}:
            
            {self.content}
            
            View the message at: {settings.SITE_URL}/messages/{self.id}/
            """,
            settings.DEFAULT_FROM_EMAIL,
            [self.recipient.email],
            fail_silently=False,
        )

    def can_send_message(self, sender, recipient):
        """Check if users can message each other based on confirmed exchange schedule"""
        if not sender.is_authenticated or not recipient.is_authenticated:
            return False
            
        # Check if there's a confirmed exchange schedule between the users
        confirmed_exchange = ExchangeSchedule.objects.filter(
            (Q(donor=sender, recipient=recipient) | Q(donor=recipient, recipient=sender)),
            status='confirmed'  # Only allow messages for confirmed exchanges
        ).exists()
        
        return confirmed_exchange
