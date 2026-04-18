"""
Database management for crop reminders and tracking
Uses JSON files for simple storage (can be upgraded to SQLite/PostgreSQL)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Database directory
DB_DIR = 'data/reminders'
Path(DB_DIR).mkdir(parents=True, exist_ok=True)

CROPS_FILE = os.path.join(DB_DIR, 'crops.json')
REMINDERS_FILE = os.path.join(DB_DIR, 'reminders.json')
PHOTOS_FILE = os.path.join(DB_DIR, 'photos.json')

def _load_json(filepath):
    """Load JSON file"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def _save_json(filepath, data):
    """Save JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== CROP MANAGEMENT ====================

def add_crop(farmer_id, crop_name, planting_date, field_name=None, area_acres=None):
    """Add a new crop for a farmer"""
    crops = _load_json(CROPS_FILE)
    
    if farmer_id not in crops:
        crops[farmer_id] = []
    
    crop_id = f"{farmer_id}_{crop_name}_{datetime.now().timestamp()}"
    
    crop = {
        'id': crop_id,
        'farmer_id': farmer_id,
        'crop_name': crop_name.lower(),
        'planting_date': planting_date,
        'field_name': field_name or 'Field 1',
        'area_acres': area_acres or 1,
        'status': 'active',
        'created_at': datetime.now().isoformat(),
        'days_elapsed': 0,
        'completed_tasks': [],
        'photos': []
    }
    
    crops[farmer_id].append(crop)
    _save_json(CROPS_FILE, crops)
    
    return crop

def get_farmer_crops(farmer_id):
    """Get all crops for a farmer"""
    crops = _load_json(CROPS_FILE)
    return crops.get(farmer_id, [])

def get_crop_by_id(crop_id):
    """Get a specific crop"""
    crops = _load_json(CROPS_FILE)
    for farmer_crops in crops.values():
        for crop in farmer_crops:
            if crop['id'] == crop_id:
                return crop
    return None

def update_crop_status(crop_id, status):
    """Update crop status (active, completed, abandoned)"""
    crops = _load_json(CROPS_FILE)
    for farmer_crops in crops.values():
        for crop in farmer_crops:
            if crop['id'] == crop_id:
                crop['status'] = status
                _save_json(CROPS_FILE, crops)
                return crop
    return None

def get_days_elapsed(crop_id):
    """Calculate days elapsed since planting"""
    crop = get_crop_by_id(crop_id)
    if crop:
        planting_date = datetime.fromisoformat(crop['planting_date'])
        days = (datetime.now() - planting_date).days
        return max(0, days)
    return 0

# ==================== REMINDER MANAGEMENT ====================

def create_reminders_for_crop(crop_id, tasks):
    """Create reminders for all tasks of a crop"""
    crop = get_crop_by_id(crop_id)
    if not crop:
        return []
    
    reminders = _load_json(REMINDERS_FILE)
    if crop_id not in reminders:
        reminders[crop_id] = []
    
    planting_date = datetime.fromisoformat(crop['planting_date'])
    
    for task in tasks:
        reminder_date = planting_date + timedelta(days=task['day'])
        
        reminder = {
            'id': f"{crop_id}_task_{task['day']}",
            'crop_id': crop_id,
            'task': task['task'],
            'task_type': task['type'],
            'priority': task['priority'],
            'scheduled_date': reminder_date.isoformat(),
            'day': task['day'],
            'completed': False,
            'completed_date': None,
            'notes': '',
            'created_at': datetime.now().isoformat()
        }
        
        reminders[crop_id].append(reminder)
    
    _save_json(REMINDERS_FILE, reminders)
    return reminders[crop_id]

def get_crop_reminders(crop_id):
    """Get all reminders for a crop"""
    reminders = _load_json(REMINDERS_FILE)
    return reminders.get(crop_id, [])

def get_pending_reminders(crop_id):
    """Get pending (not completed) reminders for a crop"""
    reminders = get_crop_reminders(crop_id)
    return [r for r in reminders if not r['completed']]

def get_today_reminders(crop_id):
    """Get reminders due today"""
    reminders = get_crop_reminders(crop_id)
    today = datetime.now().date()
    
    today_reminders = []
    for reminder in reminders:
        if not reminder['completed']:
            scheduled_date = datetime.fromisoformat(reminder['scheduled_date']).date()
            if scheduled_date == today:
                today_reminders.append(reminder)
    
    return today_reminders

def get_upcoming_reminders(crop_id, days_ahead=7):
    """Get reminders for the next N days"""
    reminders = get_crop_reminders(crop_id)
    today = datetime.now().date()
    future_date = today + timedelta(days=days_ahead)
    
    upcoming = []
    for reminder in reminders:
        if not reminder['completed']:
            scheduled_date = datetime.fromisoformat(reminder['scheduled_date']).date()
            if today <= scheduled_date <= future_date:
                upcoming.append(reminder)
    
    return sorted(upcoming, key=lambda x: x['scheduled_date'])

def mark_reminder_complete(reminder_id, notes=''):
    """Mark a reminder as completed"""
    reminders = _load_json(REMINDERS_FILE)
    
    for crop_reminders in reminders.values():
        for reminder in crop_reminders:
            if reminder['id'] == reminder_id:
                reminder['completed'] = True
                reminder['completed_date'] = datetime.now().isoformat()
                reminder['notes'] = notes
                _save_json(REMINDERS_FILE, reminders)
                return reminder
    
    return None

def get_reminder_progress(crop_id):
    """Get completion progress for a crop"""
    reminders = get_crop_reminders(crop_id)
    if not reminders:
        return {'total': 0, 'completed': 0, 'percentage': 0}
    
    total = len(reminders)
    completed = len([r for r in reminders if r['completed']])
    percentage = (completed / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'completed': completed,
        'percentage': round(percentage, 1)
    }

# ==================== PHOTO MANAGEMENT ====================

def add_photo(crop_id, photo_filename, photo_data, notes=''):
    """Add a photo for crop monitoring"""
    photos = _load_json(PHOTOS_FILE)
    
    if crop_id not in photos:
        photos[crop_id] = []
    
    photo = {
        'id': f"{crop_id}_photo_{datetime.now().timestamp()}",
        'crop_id': crop_id,
        'filename': photo_filename,
        'data': photo_data,
        'notes': notes,
        'uploaded_at': datetime.now().isoformat(),
        'analysis': None
    }
    
    photos[crop_id].append(photo)
    _save_json(PHOTOS_FILE, photos)
    
    return photo

def get_crop_photos(crop_id):
    """Get all photos for a crop"""
    photos = _load_json(PHOTOS_FILE)
    return photos.get(crop_id, [])

def update_photo_analysis(photo_id, analysis):
    """Update photo analysis (disease detection, health status)"""
    photos = _load_json(PHOTOS_FILE)
    
    for crop_photos in photos.values():
        for photo in crop_photos:
            if photo['id'] == photo_id:
                photo['analysis'] = analysis
                _save_json(PHOTOS_FILE, photos)
                return photo
    
    return None

def get_photo_timeline(crop_id):
    """Get photos in chronological order"""
    photos = get_crop_photos(crop_id)
    return sorted(photos, key=lambda x: x['uploaded_at'])

# ==================== STATISTICS ====================

def get_crop_statistics(crop_id):
    """Get statistics for a crop"""
    crop = get_crop_by_id(crop_id)
    if not crop:
        return None
    
    days_elapsed = get_days_elapsed(crop_id)
    progress = get_reminder_progress(crop_id)
    photos = get_crop_photos(crop_id)
    
    return {
        'crop_name': crop['crop_name'],
        'field_name': crop['field_name'],
        'area_acres': crop['area_acres'],
        'planting_date': crop['planting_date'],
        'days_elapsed': days_elapsed,
        'status': crop['status'],
        'reminders': progress,
        'photos_count': len(photos),
        'created_at': crop['created_at']
    }
