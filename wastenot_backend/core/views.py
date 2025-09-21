from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
import base64
from django.contrib import messages
# Add this import for the User model
from django.contrib.auth.models import User

from .models import Category, Item, ItemImage, ExchangeSchedule, Message
from .serializers import CategorySerializer, ItemSerializer, ItemImageSerializer
from .forms import ExchangeScheduleForm, MessageForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    # Get items posted by the current user
    posted_items = Item.objects.filter(donor=request.user).order_by('-created_at')
    
    # Get available items (excluding user's own items)
    available_items = Item.objects.filter(
        is_available=True
    ).exclude(
        donor=request.user
    ).order_by('-created_at')[:6]
    
    # Get exchanges where user is either donor or recipient
    exchanges = ExchangeSchedule.objects.filter(
        Q(donor=request.user) | Q(recipient=request.user)
    ).order_by('-created_at')
    
    return render(request, 'dashboard.html', {
        'posted_items': posted_items,
        'available_items': available_items,
        'exchanges': exchanges,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def post_item(request):
    if request.method == 'POST':
        # Handle item creation
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        category_id = request.POST.get('category')
        condition = request.POST.get('condition')

        # Handle image uploads
        images = request.FILES.getlist('images')
        if not images:
            messages.error(request, 'Please upload at least one image.')
            categories = Category.objects.all()
            conditions = Item.CONDITION_CHOICES
            return render(request, 'post_item.html', {
                'categories': categories,
                'conditions': conditions,
                'title': title,
                'description': description,
                'location': location,
                'category_id': category_id,
                'condition': condition,
            })

        # Create the item
        item = Item.objects.create(
            title=title,
            description=description,
            location=location,
            category_id=category_id,
            condition=condition,
            donor=request.user
        )

        for idx, image in enumerate(images):
            ItemImage.objects.create(
                item=item,
                image=image,
                is_primary=(idx == 0)
            )

        messages.success(request, 'Item posted successfully!')
        return redirect('dashboard')

    categories = Category.objects.all()
    conditions = Item.CONDITION_CHOICES
    return render(request, 'post_item.html', {
        'categories': categories,
        'conditions': conditions
    })

def browse_items(request):
    # Get filter parameters
    category = request.GET.get('category')
    search = request.GET.get('search')
    location = request.GET.get('location')
    
    # Start with all available items
    items = Item.objects.filter(is_available=True)
    
    # Apply filters
    if category:
        items = items.filter(category_id=category)
    if search:
        items = items.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    if location:
        items = items.filter(location__icontains=location)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all()
    
    # Prefetch related images and annotate primary image
    for item in items:
        primary_images = item.images.filter(is_primary=True)
        item.primary_image = primary_images.first() if primary_images.exists() else None
    
    context = {
        'items': items,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
        'location_query': location,
    }
    return render(request, 'browse_items.html', context)

# Create your views here.

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['POST'])
    def create_with_images(self, request):
        try:
            item_data = request.data.copy()
            images_data = item_data.pop('images', [])
            
            item_serializer = self.get_serializer(data=item_data)
            if item_serializer.is_valid():
                item = item_serializer.save(owner=request.user)
                
                for idx, image_data in enumerate(images_data):
                    if isinstance(image_data, str) and image_data.startswith('data:image'):
                        format, imgstr = image_data.split(';base64,')
                        ext = format.split('/')[-1]
                        data = ContentFile(base64.b64decode(imgstr), 
                                        name=f'item_{item.id}_{idx}.{ext}')
                        
                        ItemImage.objects.create(
                            item=item,
                            image=data,
                            is_primary=(idx == 0)
                        )
                
                return Response(item_serializer.data, status=status.HTTP_201_CREATED)
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@login_required
def schedule_exchange(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = ExchangeScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.item = item
            schedule.donor = item.donor
            schedule.recipient = request.user
            schedule.save()
            
            messages.success(request, 'Exchange scheduled successfully!')
            return redirect('item_detail', item_id=item.id)
    else:
        form = ExchangeScheduleForm(initial={'location': item.location})
    
    return render(request, 'schedule_exchange.html', {
        'form': form,
        'item': item
    })

@login_required
def confirm_exchange(request, schedule_id):
    schedule = get_object_or_404(ExchangeSchedule, id=schedule_id)
    
    # Only allow the donor to confirm exchanges
    if request.user != schedule.donor:
        messages.error(request, 'Only the item donor can confirm exchanges.')
        return redirect('dashboard')
    
    schedule.status = 'confirmed'
    schedule.save()
    
    messages.success(request, 'Exchange confirmed successfully!')
    return redirect('dashboard')

@login_required
def cancel_exchange(request, schedule_id):
    schedule = get_object_or_404(ExchangeSchedule, id=schedule_id)
    
    if request.user not in [schedule.donor, schedule.recipient]:
        messages.error(request, 'You are not authorized to cancel this exchange.')
        return redirect('dashboard')
    
    schedule.status = 'cancelled'
    schedule.save()
    
    messages.success(request, 'Exchange cancelled successfully!')
    return redirect('dashboard')

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {'item': item})

@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    return render(request, 'messages/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Only allow sender or recipient to view message
    if request.user not in [message.sender, message.recipient]:
        messages.error(request, 'You are not authorized to view this message.')
        return redirect('inbox')
    
    # Mark as read if recipient is viewing
    if request.user == message.recipient:
        message.is_read = True
        message.save()
    
    # Determine the other party in the conversation
    reply_to = message.sender if request.user == message.recipient else message.recipient
    
    return render(request, 'messages/view_message.html', {
        'message': message,
        'reply_to': reply_to,
    })

@login_required
def send_message(request, recipient_id=None, item_id=None):
    recipient = None
    item = None
    
    if recipient_id:
        recipient = get_object_or_404(User, id=recipient_id)
    if item_id:
        item = get_object_or_404(Item, id=item_id)
        if not recipient:
            recipient = item.donor
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, initial={'user': request.user})
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if recipient:
                message.recipient = recipient
            message.item = item
            message.save()
            
            # Send email notification
            message.send_notification()
            
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')
    else:
        initial = {'user': request.user}
        if recipient:
            initial['recipient'] = recipient
        if item:
            initial['subject'] = f"Regarding: {item.title}"
        form = MessageForm(initial=initial)
    
    return render(request, 'messages/send_message.html', {
        'form': form,
        'recipient': recipient,
        'item': item,
    })

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Message.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'All messages marked as read.')
    return redirect('inbox')

@login_required
def item_qr_code(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Only allow the donor to view the QR code
    if request.user != item.donor:
        messages.error(request, 'Only the item donor can view the QR code.')
        return redirect('dashboard')
    
    # Generate QR code if it doesn't exist
    if not item.qr_code:
        item.generate_qr_code()
        item.save()
    
    return render(request, 'qr_code.html', {'item': item})

@login_required
def confirm_pickup(request, pickup_code):
    item = get_object_or_404(Item, pickup_code=pickup_code)
    
    # Check if the user is the recipient of an exchange for this item
    exchanges = ExchangeSchedule.objects.filter(
        item=item,
        recipient=request.user,
        status='confirmed'
    )
    
    if not exchanges.exists():
        messages.error(request, 'You are not authorized to confirm pickup for this item.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Update item status
        item.is_available = False
        item.save()
        
        # Update exchange status
        exchange = exchanges.first()
        exchange.status = 'completed'
        exchange.save()
        
        messages.success(request, 'Item pickup confirmed successfully!')
        
        # Send a thank you message to the donor
        Message.objects.create(
            sender=request.user,
            recipient=item.donor,
            subject=f"Thank you for {item.title}",
            content=f"I've received the {item.title}. Thank you for your generosity!",
            item=item
        )
        
        return redirect('dashboard')
    
    return render(request, 'confirm_pickup.html', {
        'item': item,
    })


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Only allow the donor to delete the item
    if request.user != item.donor:
        messages.error(request, 'You can only delete items that you have posted.')
        return redirect('dashboard')
    
    # Check if there are any confirmed exchanges
    if item.schedules.filter(status='confirmed').exists():
        messages.error(request, 'Cannot delete item with confirmed exchanges.')
        return redirect('item_detail', item_id=item.id)
    
    # Delete the item
    item_title = item.title
    item.delete()
    
    messages.success(request, f'Item "{item_title}" has been deleted successfully.')
    return redirect('dashboard')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from google.cloud import vision
import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\skand\Downloads\dk\gcloud-key.json"

@csrf_exempt
def analyze_item_condition(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        content = image_file.read()

        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)

        # Label detection
        label_response = client.label_detection(image=image)
        labels = label_response.label_annotations

        # Object detection
        object_response = client.object_localization(image=image)
        objects = object_response.localized_object_annotations

        # Web detection (for additional context)
        web_response = client.web_detection(image=image)
        web_entities = getattr(web_response.web_detection, 'web_entities', [])

        # Image properties detection (for color analysis)
        properties_response = client.image_properties(image=image)
        props = properties_response.image_properties_annotation
        dominant_colors = []
        yellowed_flag = False
        dark_flag = False
        if props and props.dominant_colors:
            for color_info in props.dominant_colors.colors:
                rgb = (color_info.color.red, color_info.color.green, color_info.color.blue)
                dominant_colors.append({
                    'rgb': rgb,
                    'score': color_info.score,
                    'pixel_fraction': color_info.pixel_fraction
                })
                # Check for yellowed (old paper) - high red and green, lower blue
                if color_info.color.red > 180 and color_info.color.green > 140 and color_info.color.blue < 100 and color_info.score > 0.2:
                    yellowed_flag = True
                # Check for dark images - all channels low
                if color_info.color.red < 60 and color_info.color.green < 60 and color_info.color.blue < 60 and color_info.score > 0.2:
                    dark_flag = True
            # Debug: Print dominant colors
            print("DOMINANT COLORS:")
            for color in dominant_colors:
                print(f"  RGB: {color['rgb']}, Score: {color['score']}, Pixel Fraction: {color['pixel_fraction']}")
            print(f"Yellowed flag: {yellowed_flag}, Dark flag: {dark_flag}")

        # Debug: Print Vision API results
        print("LABELS:")
        for label in labels:
            print(f"  {label.description} ({label.score})")
        print("OBJECTS:")
        for obj in objects:
            print(f"  {obj.name} ({obj.score})")
        print("WEB ENTITIES:")
        for entity in web_entities:
            if entity.description:
                print(f"  {entity.description} ({entity.score})")

        # Prepare results for frontend display
        results = [
            {'description': label.description, 'score': label.score}
            for label in labels
        ]
        object_results = [
            {'name': obj.name, 'score': obj.score}
            for obj in objects
        ]
        web_results = [
            {'description': entity.description, 'score': entity.score}
            for entity in web_entities if entity.description
        ]

        # Define keywords for each condition
        good_labels = {'new', 'clean', 'good', 'intact', 'pristine', 'perfect', 'excellent', 'shiny', 'spotless'}
        poor_labels = {
            'damaged', 'broken', 'dirty', 'torn', 'cracked', 'old', 'rusty', 'worn', 'poor', 'stained', 'scratched',
            'antique', 'yellowed', 'aged', 'vintage', 'discolored', 'faded', 'worn out', 'brittle', 'foxing',
            'musty', 'fragile', 'tattered', 'dog-eared', 'dog eared', 'mildew', 'moldy', 'water damage', 'warped'
        }
        old_labels = {
            'old', 'antique', 'vintage', 'aged', 'historic', 'ancient', 'retro', 'classic', 'weathered', 'patina',
            'yellowed', 'discolored', 'faded', 'brittle', 'worn out', 'tattered', 'foxing', 'fragile', 'dog-eared', 'dog eared'
        }
        fair_labels = {'used', 'average', 'fair', 'acceptable', 'functional', 'working', 'chair', 'table', 'furniture', 'natural material', 'wood', 'garden furniture', 'stool'}

        # Aggregate all descriptions from labels, objects, and web entities
        all_descriptions = [label.description.lower() for label in labels]
        all_descriptions += [obj.name.lower() for obj in objects]
        all_descriptions += [entity.description.lower() for entity in web_entities if entity.description]

        # Old item detection logic
        old_score = sum(label.score for label in labels if label.description.lower() in old_labels)
        old_score += sum(obj.score * 0.7 for obj in objects if obj.name.lower() in old_labels)
        old_score += sum(entity.score * 0.5 for entity in web_entities if entity.description and entity.description.lower() in old_labels)

        # Scoring system (lowered threshold to 0.3)
        good_score = sum(label.score for label in labels if label.description.lower() in good_labels)
        good_score += sum(obj.score * 0.7 for obj in objects if obj.name.lower() in good_labels)
        good_score += sum(entity.score * 0.5 for entity in web_entities if entity.description and entity.description.lower() in good_labels)

        poor_score = sum(label.score for label in labels if label.description.lower() in poor_labels)
        poor_score += sum(obj.score * 0.7 for obj in objects if obj.name.lower() in poor_labels)
        poor_score += sum(entity.score * 0.5 for entity in web_entities if entity.description and entity.description.lower() in poor_labels)

        fair_score = sum(label.score for label in labels if label.description.lower() in fair_labels)
        fair_score += sum(obj.score * 0.7 for obj in objects if obj.name.lower() in fair_labels)
        fair_score += sum(entity.score * 0.5 for entity in web_entities if entity.description and entity.description.lower() in fair_labels)

        # Decision logic: pick the highest score, but if any poor label is present with high confidence, prioritize "Poor"
        high_conf_poor = any(
            (label.description.lower() in poor_labels and label.score > 0.7)
            for label in labels
        ) or any(
            (obj.name.lower() in poor_labels and obj.score > 0.7)
            for obj in objects
        )

        # Flag as poor if yellowed or dark or old detected with moderate confidence
        if high_conf_poor or yellowed_flag or dark_flag or old_score > 0.3:
            condition = "Poor"
        elif good_score >= poor_score and good_score >= fair_score and good_score > 0.3:
            condition = "Good"
        elif fair_score >= good_score and fair_score >= poor_score and fair_score > 0.3:
            condition = "Fair"
        elif poor_score > 0.3:
            condition = "Poor"
        else:
            return JsonResponse({
                'condition': None,
                'labels': results,
                'objects': object_results,
                'web_entities': web_results,
                'dominant_colors': dominant_colors,
                'message': 'Could not determine condition from image. Please try a clearer photo.'
            })

        return JsonResponse({
            'condition': condition,
            'labels': results,
            'objects': object_results,
            'web_entities': web_results,
            'dominant_colors': dominant_colors
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
