"""
Smart personalized notifications in Hindi/Hinglish
"""

from datetime import datetime, timedelta

def get_days_since_planting(planting_date):
    """Calculate days since planting"""
    planting = datetime.fromisoformat(planting_date)
    days = (datetime.now() - planting).days
    return max(0, days)

def get_hindi_day_description(days):
    """Convert days to Hindi description"""
    if days == 0:
        return "aaj"
    elif days == 1:
        return "kal"
    elif days == 2:
        return "parson"
    elif days == 3:
        return "3 din pehle"
    elif days == 7:
        return "ek hafte pehle"
    elif days <= 30:
        return f"{days} din pehle"
    elif days <= 90:
        weeks = days // 7
        return f"{weeks} hafte pehle"
    else:
        months = days // 30
        return f"{months} mahine pehle"

def generate_personalized_reminder(farmer_name, crop_name, task, days_elapsed, planting_date):
    """Generate personalized reminder message in Hindi/Hinglish"""
    
    days_since = get_days_since_planting(planting_date)
    day_desc = get_hindi_day_description(days_since)
    
    crop_hindi = {
        'moong': 'moong',
        'rice': 'chawal',
        'wheat': 'gehun',
        'maize': 'makka',
        'cotton': 'kapas',
        'potato': 'aloo',
        'tomato': 'tamatar'
    }
    
    crop_name_hindi = crop_hindi.get(crop_name.lower(), crop_name)
    
    # Task-specific messages
    task_messages = {
        'irrigation': {
            'hi': f"{farmer_name} ji, aapne {day_desc} {crop_name_hindi} lagayi thi. Aaj halka paani dena zaroori hai.",
            'en': f"{farmer_name}, you planted {crop_name} {day_desc}. Water your crop today."
        },
        'weeding': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} ab thik se badh gayi hogi. Aaj nindai (weeding) kar dena zaroori hai.",
            'en': f"{farmer_name}, your {crop_name} has grown well. Time to remove weeds today."
        },
        'fertilizer': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} ko ab khad ki zaroorat hai. Aaj nitrogen khad daal dena.",
            'en': f"{farmer_name}, your {crop_name} needs fertilizer. Apply nitrogen today."
        },
        'monitoring': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} ko dhyan se dekh lena. Koi bimari toh nahi hai?",
            'en': f"{farmer_name}, check your {crop_name} carefully. Look for any diseases."
        },
        'pest_control': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} mein keede aa sakte hain. Aaj spray kar dena zaroori hai.",
            'en': f"{farmer_name}, pests may attack your {crop_name}. Spray pesticide today."
        },
        'maintenance': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} ki nindai kar dena zaroori hai.",
            'en': f"{farmer_name}, remove weeds from your {crop_name} today."
        },
        'preparation': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} lagane ki tayyari kar lo.",
            'en': f"{farmer_name}, prepare to plant {crop_name}."
        },
        'harvest': {
            'hi': f"{farmer_name} ji, {crop_name_hindi} kaatne ka samay aa gaya! Badhai ho!",
            'en': f"{farmer_name}, your {crop_name} is ready to harvest! Congratulations!"
        }
    }
    
    # Get task type from task description
    task_type = 'monitoring'  # default
    if 'water' in task.lower() or 'irrigation' in task.lower():
        task_type = 'irrigation'
    elif 'weed' in task.lower():
        task_type = 'weeding'
    elif 'fertilizer' in task.lower() or 'khad' in task.lower():
        task_type = 'fertilizer'
    elif 'pest' in task.lower() or 'spray' in task.lower():
        task_type = 'pest_control'
    elif 'harvest' in task.lower():
        task_type = 'harvest'
    elif 'check' in task.lower() or 'monitor' in task.lower():
        task_type = 'monitoring'
    elif 'prepare' in task.lower() or 'sow' in task.lower():
        task_type = 'preparation'
    elif 'pruning' in task.lower() or 'earthing' in task.lower():
        task_type = 'maintenance'
    
    message = task_messages.get(task_type, {})
    
    return {
        'hindi': message.get('hi', f"{farmer_name} ji, {task} karna zaroori hai."),
        'english': message.get('en', f"{farmer_name}, {task} is important today."),
        'task_type': task_type,
        'days_since_planting': days_since,
        'day_description': day_desc
    }

def generate_crop_stage_message(farmer_name, crop_name, days_elapsed):
    """Generate message about current crop stage"""
    
    crop_stages = {
        'moong': {
            (0, 7): {
                'hi': f"{farmer_name} ji, {crop_name} abhi germination stage mein hai. Thandi rakhna.",
                'en': f"{farmer_name}, {crop_name} is in germination stage. Keep it cool.",
                'stage': 'Germination'
            },
            (7, 21): {
                'hi': f"{farmer_name} ji, {crop_name} seedling stage mein hai. Nindai kar dena.",
                'en': f"{farmer_name}, {crop_name} is in seedling stage. Remove weeds.",
                'stage': 'Seedling'
            },
            (21, 45): {
                'hi': f"{farmer_name} ji, {crop_name} vegetative stage mein hai. Khad daal dena.",
                'en': f"{farmer_name}, {crop_name} is in vegetative stage. Apply fertilizer.",
                'stage': 'Vegetative'
            },
            (45, 75): {
                'hi': f"{farmer_name} ji, {crop_name} flowering stage mein hai. Dhyan se dekh lena.",
                'en': f"{farmer_name}, {crop_name} is flowering. Monitor closely.",
                'stage': 'Flowering'
            },
            (75, 90): {
                'hi': f"{farmer_name} ji, {crop_name} pod maturation stage mein hai. Jaldi hi kaatne ka samay aa jayega.",
                'en': f"{farmer_name}, {crop_name} is maturing. Harvest will be soon.",
                'stage': 'Pod Maturation'
            }
        },
        'rice': {
            (0, 10): {
                'hi': f"{farmer_name} ji, chawal abhi germination stage mein hai.",
                'en': f"{farmer_name}, rice is germinating.",
                'stage': 'Germination'
            },
            (10, 30): {
                'hi': f"{farmer_name} ji, chawal seedling stage mein hai. Nindai kar dena.",
                'en': f"{farmer_name}, rice is in seedling stage.",
                'stage': 'Seedling'
            },
            (30, 60): {
                'hi': f"{farmer_name} ji, chawal vegetative stage mein hai.",
                'en': f"{farmer_name}, rice is in vegetative stage.",
                'stage': 'Vegetative'
            },
            (60, 90): {
                'hi': f"{farmer_name} ji, chawal panicle stage mein hai. Bahut zaroori stage hai!",
                'en': f"{farmer_name}, rice is in panicle stage. Critical stage!",
                'stage': 'Panicle'
            },
            (90, 120): {
                'hi': f"{farmer_name} ji, chawal grain filling stage mein hai.",
                'en': f"{farmer_name}, rice is in grain filling stage.",
                'stage': 'Grain Filling'
            }
        }
    }
    
    crop_lower = crop_name.lower()
    stages = crop_stages.get(crop_lower, {})
    
    for (start, end), stage_info in stages.items():
        if start <= days_elapsed < end:
            return stage_info
    
    return {
        'hi': f"{farmer_name} ji, {crop_name} ab kaatne ke liye tayyar hai!",
        'en': f"{farmer_name}, {crop_name} is ready to harvest!",
        'stage': 'Harvest Ready'
    }

def generate_alert_message(farmer_name, alert_type, crop_name, severity):
    """Generate alert messages"""
    
    alerts = {
        'heat': {
            'hi': f"{farmer_name} ji, bahut garmi hai! {crop_name} ko zyada paani dena padega.",
            'en': f"{farmer_name}, it's very hot! Water your {crop_name} more frequently."
        },
        'cold': {
            'hi': f"{farmer_name} ji, bahut sardi hai! {crop_name} ko dhyan se dekh lena.",
            'en': f"{farmer_name}, it's very cold! Monitor your {crop_name} carefully."
        },
        'rain': {
            'hi': f"{farmer_name} ji, bahut barish aa rahi hai! {crop_name} ke liye drainage theek kar dena.",
            'en': f"{farmer_name}, heavy rain is coming! Check drainage for your {crop_name}."
        },
        'drought': {
            'hi': f"{farmer_name} ji, barish nahi ho rahi. {crop_name} ko paani dena zaroori hai.",
            'en': f"{farmer_name}, no rain expected. Water your {crop_name} regularly."
        },
        'humidity': {
            'hi': f"{farmer_name} ji, bahut nammi hai. {crop_name} mein bimari aa sakti hai. Spray kar dena.",
            'en': f"{farmer_name}, high humidity. Disease risk for {crop_name}. Spray fungicide."
        },
        'pest': {
            'hi': f"{farmer_name} ji, keede aa sakte hain. {crop_name} ko spray kar dena.",
            'en': f"{farmer_name}, pests may attack. Spray your {crop_name}."
        }
    }
    
    message = alerts.get(alert_type, {})
    
    return {
        'hindi': message.get('hi', f"{farmer_name} ji, {crop_name} ka dhyan rakhna."),
        'english': message.get('en', f"{farmer_name}, take care of your {crop_name}."),
        'alert_type': alert_type,
        'severity': severity
    }

def generate_encouragement_message(farmer_name, crop_name, progress_percentage):
    """Generate encouragement messages based on progress"""
    
    if progress_percentage < 25:
        messages = [
            f"{farmer_name} ji, {crop_name} abhi shuru hi hui hai. Mehnat karte raho!",
            f"{farmer_name}, your {crop_name} journey has just started. Keep going!"
        ]
    elif progress_percentage < 50:
        messages = [
            f"{farmer_name} ji, {crop_name} achhi tarah badh rahi hai. Shukriya mehnat ke liye!",
            f"{farmer_name}, your {crop_name} is growing well. Great work!"
        ]
    elif progress_percentage < 75:
        messages = [
            f"{farmer_name} ji, {crop_name} ab aadhi tarah tayyar ho gayi. Thoda aur mehnat!",
            f"{farmer_name}, your {crop_name} is halfway there. Almost done!"
        ]
    elif progress_percentage < 100:
        messages = [
            f"{farmer_name} ji, {crop_name} ab kaatne ke liye bilkul tayyar hai! Badhai ho!",
            f"{farmer_name}, your {crop_name} is almost ready to harvest! Congratulations!"
        ]
    else:
        messages = [
            f"{farmer_name} ji, {crop_name} kaatne ka samay aa gaya! Badhai ho!",
            f"{farmer_name}, harvest time for your {crop_name}! Well done!"
        ]
    
    return {
        'hindi': messages[0],
        'english': messages[1],
        'progress': progress_percentage
    }

def format_notification(reminder_data, farmer_name, crop_name):
    """Format complete notification with all details"""
    
    notification = generate_personalized_reminder(
        farmer_name,
        crop_name,
        reminder_data.get('task', ''),
        reminder_data.get('day', 0),
        reminder_data.get('scheduled_date', '')
    )
    
    return {
        'title_hi': f"📅 {reminder_data.get('task', 'Task')}",
        'title_en': f"📅 {reminder_data.get('task', 'Task')}",
        'message_hi': notification['hindi'],
        'message_en': notification['english'],
        'scheduled_date': reminder_data.get('scheduled_date', ''),
        'priority': reminder_data.get('priority', 'medium'),
        'task_type': notification['task_type'],
        'days_since_planting': notification['days_since_planting'],
        'day_description': notification['day_description']
    }
