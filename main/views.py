from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from child.models import child
from django.db.models import Q ,Count
from patients.models import *
from django.db.models.functions import TruncMonth

# Create your views here.


@login_required
def dashboard(request):
    data = {

        'totalpatients': patient.objects.all().count,
        'totalchildren':child.objects.all().count,
        'lowsurvival':child.objects.filter(heartrate__lte = 1).count(),
        'lowsurvivalq':child.objects.filter(heartrate__lte = 1),

       'a': child.objects
    .annotate(month=TruncMonth('Dob'))  # Truncate to month and add to select list
    .values('month')                          # Group By month
    .annotate(c=Count('id'))                  # Select the count of the grouping
    .values('month', 'c') 
	# 'my_books' : books.objects.filter(category = categoryid),
	# 'category_name':category.objects.get(id=categoryid),
	# #'count':books.objects.filter(category=categoryid).count()
	#  'count' :books.objects.values('category').annotate(count=Count('category'))



	}
    return render(request, 'main/dashboard.html',data)



