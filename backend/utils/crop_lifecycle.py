"""
Crop lifecycle management - defines tasks and reminders for each crop
"""

CROP_LIFECYCLE = {
    'rice': {
        'duration_days': 120,
        'season': 'Monsoon/Winter',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and sow seeds', 'type': 'preparation', 'priority': 'high'},
            {'day': 3, 'task': 'Water the field', 'type': 'irrigation', 'priority': 'high'},
            {'day': 7, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 14, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 21, 'task': 'Second weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 30, 'task': 'Check for pests and diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 35, 'task': 'Apply phosphorus fertilizer', 'type': 'fertilizer', 'priority': 'medium'},
            {'day': 45, 'task': 'Spray pesticide if needed', 'type': 'pest_control', 'priority': 'medium'},
            {'day': 60, 'task': 'Panicle initiation - monitor closely', 'type': 'monitoring', 'priority': 'high'},
            {'day': 75, 'task': 'Flowering stage - ensure adequate water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 90, 'task': 'Grain filling stage - reduce water', 'type': 'irrigation', 'priority': 'medium'},
            {'day': 110, 'task': 'Prepare for harvest', 'type': 'preparation', 'priority': 'high'},
            {'day': 120, 'task': 'Harvest ready', 'type': 'harvest', 'priority': 'high'},
        ]
    },
    'wheat': {
        'duration_days': 150,
        'season': 'Winter',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and sow seeds', 'type': 'preparation', 'priority': 'high'},
            {'day': 5, 'task': 'Light irrigation', 'type': 'irrigation', 'priority': 'medium'},
            {'day': 15, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 25, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 35, 'task': 'Second weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 45, 'task': 'Check for diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 60, 'task': 'Tillering stage - ensure moisture', 'type': 'irrigation', 'priority': 'high'},
            {'day': 75, 'task': 'Stem elongation - monitor pests', 'type': 'monitoring', 'priority': 'high'},
            {'day': 90, 'task': 'Heading stage - critical monitoring', 'type': 'monitoring', 'priority': 'high'},
            {'day': 105, 'task': 'Flowering - ensure adequate water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 120, 'task': 'Grain filling - reduce irrigation', 'type': 'irrigation', 'priority': 'medium'},
            {'day': 140, 'task': 'Prepare for harvest', 'type': 'preparation', 'priority': 'high'},
            {'day': 150, 'task': 'Harvest ready', 'type': 'harvest', 'priority': 'high'},
        ]
    },
    'moong': {
        'duration_days': 90,
        'season': 'Summer/Monsoon',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and sow seeds', 'type': 'preparation', 'priority': 'high'},
            {'day': 3, 'task': 'Water the field', 'type': 'irrigation', 'priority': 'high'},
            {'day': 7, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 14, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 21, 'task': 'Second weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 30, 'task': 'Check for pests and diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 35, 'task': 'Spray pesticide if needed', 'type': 'pest_control', 'priority': 'medium'},
            {'day': 45, 'task': 'Flowering stage - monitor closely', 'type': 'monitoring', 'priority': 'high'},
            {'day': 60, 'task': 'Pod formation - ensure water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 75, 'task': 'Pod maturation - reduce water', 'type': 'irrigation', 'priority': 'medium'},
            {'day': 85, 'task': 'Prepare for harvest', 'type': 'preparation', 'priority': 'high'},
            {'day': 90, 'task': 'Harvest ready', 'type': 'harvest', 'priority': 'high'},
        ]
    },
    'maize': {
        'duration_days': 120,
        'season': 'Summer/Monsoon',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and sow seeds', 'type': 'preparation', 'priority': 'high'},
            {'day': 3, 'task': 'Water the field', 'type': 'irrigation', 'priority': 'high'},
            {'day': 10, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 20, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 30, 'task': 'Second weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 40, 'task': 'Check for pests and diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 50, 'task': 'Spray pesticide if needed', 'type': 'pest_control', 'priority': 'medium'},
            {'day': 60, 'task': 'Tasseling stage - critical monitoring', 'type': 'monitoring', 'priority': 'high'},
            {'day': 75, 'task': 'Silking stage - ensure water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 90, 'task': 'Grain filling - monitor closely', 'type': 'monitoring', 'priority': 'high'},
            {'day': 110, 'task': 'Prepare for harvest', 'type': 'preparation', 'priority': 'high'},
            {'day': 120, 'task': 'Harvest ready', 'type': 'harvest', 'priority': 'high'},
        ]
    },
    'cotton': {
        'duration_days': 180,
        'season': 'Summer',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and sow seeds', 'type': 'preparation', 'priority': 'high'},
            {'day': 5, 'task': 'Light irrigation', 'type': 'irrigation', 'priority': 'medium'},
            {'day': 20, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 35, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 50, 'task': 'Second weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 60, 'task': 'Check for pests and diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 75, 'task': 'Spray pesticide if needed', 'type': 'pest_control', 'priority': 'high'},
            {'day': 90, 'task': 'Flowering stage - monitor closely', 'type': 'monitoring', 'priority': 'high'},
            {'day': 120, 'task': 'Boll formation - ensure water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 150, 'task': 'Boll maturation - reduce water', 'type': 'irrigation', 'priority': 'medium'},
            {'day': 170, 'task': 'Prepare for harvest', 'type': 'preparation', 'priority': 'high'},
            {'day': 180, 'task': 'Harvest ready', 'type': 'harvest', 'priority': 'high'},
        ]
    },
    'potato': {
        'duration_days': 90,
        'season': 'Winter',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and plant seed potatoes', 'type': 'preparation', 'priority': 'high'},
            {'day': 3, 'task': 'Water the field', 'type': 'irrigation', 'priority': 'high'},
            {'day': 10, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 20, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 30, 'task': 'Earthing up - cover plants with soil', 'type': 'maintenance', 'priority': 'high'},
            {'day': 40, 'task': 'Check for pests and diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 50, 'task': 'Spray pesticide if needed', 'type': 'pest_control', 'priority': 'medium'},
            {'day': 60, 'task': 'Tuber formation - monitor closely', 'type': 'monitoring', 'priority': 'high'},
            {'day': 75, 'task': 'Tuber bulking - ensure water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 85, 'task': 'Prepare for harvest', 'type': 'preparation', 'priority': 'high'},
            {'day': 90, 'task': 'Harvest ready', 'type': 'harvest', 'priority': 'high'},
        ]
    },
    'tomato': {
        'duration_days': 120,
        'season': 'Summer/Winter',
        'tasks': [
            {'day': 0, 'task': 'Prepare field and transplant seedlings', 'type': 'preparation', 'priority': 'high'},
            {'day': 3, 'task': 'Water the field', 'type': 'irrigation', 'priority': 'high'},
            {'day': 7, 'task': 'First weeding', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 14, 'task': 'Apply nitrogen fertilizer', 'type': 'fertilizer', 'priority': 'high'},
            {'day': 21, 'task': 'Pruning and staking', 'type': 'maintenance', 'priority': 'medium'},
            {'day': 30, 'task': 'Check for pests and diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 40, 'task': 'Spray pesticide if needed', 'type': 'pest_control', 'priority': 'high'},
            {'day': 50, 'task': 'Flowering stage - monitor closely', 'type': 'monitoring', 'priority': 'high'},
            {'day': 65, 'task': 'Fruit setting - ensure water', 'type': 'irrigation', 'priority': 'high'},
            {'day': 80, 'task': 'Fruit development - monitor for diseases', 'type': 'monitoring', 'priority': 'high'},
            {'day': 100, 'task': 'Fruit ripening - start harvesting', 'type': 'harvest', 'priority': 'high'},
            {'day': 120, 'task': 'Final harvest', 'type': 'harvest', 'priority': 'high'},
        ]
    },
}

def get_crop_lifecycle(crop_name):
    """Get lifecycle for a specific crop"""
    crop_lower = crop_name.lower()
    return CROP_LIFECYCLE.get(crop_lower, None)

def get_all_crops_with_lifecycle():
    """Get all crops that have lifecycle defined"""
    return list(CROP_LIFECYCLE.keys())

def get_tasks_for_crop(crop_name):
    """Get all tasks for a crop"""
    lifecycle = get_crop_lifecycle(crop_name)
    if lifecycle:
        return lifecycle['tasks']
    return []

def get_task_by_day(crop_name, day):
    """Get task for a specific day"""
    tasks = get_tasks_for_crop(crop_name)
    for task in tasks:
        if task['day'] == day:
            return task
    return None

def get_upcoming_tasks(crop_name, current_day, days_ahead=7):
    """Get upcoming tasks for the next N days"""
    tasks = get_tasks_for_crop(crop_name)
    upcoming = []
    for task in tasks:
        if current_day < task['day'] <= current_day + days_ahead:
            upcoming.append(task)
    return upcoming

def get_task_type_description(task_type):
    """Get description for task type"""
    descriptions = {
        'preparation': '🌱 Preparation',
        'irrigation': '💧 Irrigation',
        'maintenance': '🔧 Maintenance',
        'fertilizer': '🧪 Fertilizer',
        'monitoring': '👁️ Monitoring',
        'pest_control': '🐛 Pest Control',
        'harvest': '🌾 Harvest',
    }
    return descriptions.get(task_type, task_type)

def get_priority_color(priority):
    """Get color for priority level"""
    colors = {
        'high': 'red',
        'medium': 'yellow',
        'low': 'blue',
    }
    return colors.get(priority, 'gray')
