from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from exercise.models import Exercise, MuscleGroup

def list_exercises(request):
    name = request.GET.get('name')
    force = request.GET.get('force')
    level = request.GET.get('level')
    mechanic = request.GET.get('mechanic')
    equipment = request.GET.get('equipment')
    muscle = request.GET.get('muscle')
    category = request.GET.get('category')

    exercises = Exercise.objects.all()

    if name:
        exercises = exercises.filter(name__icontains=name)
    if force:
        exercises = exercises.filter(force__icontains=force)
    if level:
        exercises = exercises.filter(level__icontains=level)
    if mechanic:
        exercises = exercises.filter(mechanic__icontains=mechanic)
    if equipment:
        exercises = exercises.filter(equipment__icontains=equipment)
    if category:
        exercises = exercises.filter(category__icontains=category)
    if muscle:
        if MuscleGroup.objects.filter(name=muscle).exists():
            exercises = exercises.filter(primaryMuscle__name__icontains=muscle) | \
                    exercises.filter(secondaryMuscle__name__icontains=muscle)
    
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

    return render(request, 'exercise/exercise_list.html', {'exercises': exercises, 'current_page_number': current_page_number, 'page_range': page_range, 'num_pages': num_pages})