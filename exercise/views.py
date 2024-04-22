from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from exercise.models import Exercise, MuscleGroup

def list_exercises(request):
    name = request.GET.get('exercise_name')
    level = request.GET.get('exercise_level')
    equipment = request.GET.get('exercise_equipment')
    muscle = request.GET.get('exercise_muscle')
    category = request.GET.get('exercise_category')

    exercises = Exercise.objects.all()

    if name:
        exercises = exercises.filter(name__icontains=name)
    if level and level != 'none':
        exercises = exercises.filter(level__icontains=level)
    if equipment and equipment != 'none':
        exercises = exercises.filter(equipment__icontains=equipment)
    if category and category != 'none':
        exercises = exercises.filter(category__icontains=category)
    if muscle and muscle != 'none':
        if MuscleGroup.objects.filter(name=muscle).exists():
            exercises = exercises.filter(primaryMuscles__name__icontains=muscle) | \
                    exercises.filter(secondaryMuscles__name__icontains=muscle)
    
    filter_dict = {
        "name": name if name else "",
        "level": level if level else "none",
        "equipment": equipment if equipment else "none",
        "category": category if category else "none",
        "muscle": muscle if muscle else "none"
    }
    
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided
    paginator = Paginator(exercises, 10)
    
    try:
        exercises = paginator.page(page_number)
    except PageNotAnInteger:
        exercises = paginator.page(1)
    except EmptyPage:
        exercises = paginator.page(paginator.num_pages)

    current_page_number = exercises.number
    page_range = paginator.page_range
    num_pages = paginator.num_pages

    return render(request, 'exercise/exercise_list.html', {'exercises': exercises, 'filter_dict': filter_dict, 'current_page_number': current_page_number, 'page_range': page_range, 'num_pages': num_pages})