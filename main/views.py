from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from child.models import child
from patients.models import *

# Create your views here.


@login_required
def dashboard(request):
    data = {

        'totalpatients': patient.objects.all().count,
        'totalchildren':child.objects.all().count,
        'lowsurvival':child.objects.filter(heartrate__lte = 1).count(),
        'lowsurvivalq':child.objects.filter(heartrate__lte = 1)
	# 'my_books' : books.objects.filter(category = categoryid),
	# 'category_name':category.objects.get(id=categoryid),
	# #'count':books.objects.filter(category=categoryid).count()
	#  'count' :books.objects.values('category').annotate(count=Count('category'))



	}
    return render(request, 'main/dashboard.html',data)



