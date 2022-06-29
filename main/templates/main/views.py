import io
import csv
from django import forms
from django.urls import reverse
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q ,Count
from django.core.mail import send_mail
from datetime import datetime ,timedelta
from .forms import AddBookForm ,issuebookform
from uzlibrary.settings import EMAIL_HOST_USER
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect ,HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.views.generic import ListView,DetailView,FormView,UpdateView ,DeleteView
from .models import books,author,category,issuedbooks,User,reservedbooks,issuebookhistory ,searchedcontent

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse

	

#function for searching boook using title/serial number /category /author and description
@login_required
def searched_books(request):
	if request.method == 'POST':
		searchedq = request.POST.get('searchedbook')
		
		post = searchedcontent()
		post.userid = request.user
		post.searchedinfo = searchedq
		post.save()
		
						
		searchedbook = books.objects.filter(
			Q(title__contains = searchedq) |
			Q(serialno__contains = searchedq) |
			Q(description__contains = searchedq) |
			Q(category__category_name__contains = searchedq) |
			Q(author__lastname__contains = searchedq)
			)
		return render(request,'library/searched_books.html',{'searchedbook':searchedbook})
	else:
		return render(request,'library/books.html')

@login_required
def searched_user_issued_books(request):
	if request.method == 'POST':
		searcheduser = request.POST.get('searcheduser')
		searcheduser = issuedbooks.objects.filter(
			Q(userid_id__last_name__contains = searcheduser)|
			Q(userid_id__first_name__contains = searcheduser)

			).distinct('userid_id__last_name')
		return render(request,'library/searched_user_issued_books.html',{'searcheduser':searcheduser})
	else:
		return render(request,'library/searched_user_issued_books.html',{'title':'Search Page'})




#a class based view used to display all books from the database 
#it is inheriting listview which will display data in a list way
#model - is the name of the table int the databse which you are queryin(you can use any table of your choice)
#template name = the html page were we will display our data
class booksView(LoginRequiredMixin, ListView):
	model = books 
	template_name = 'library/books.html'
	context_object_name = 'all_books'
	paginate_by = 5
	title = 'Books'

#function to insert books in the database
#if not request.user.is_superuse(if user is not admin they are redirected to a resticted page)

@login_required
def addbooks(request):
	if not request.user.is_superuser:
		return render(request,'library/restricted.html')
	if request.method == 'POST':
	 form = AddBookForm(request.POST)
	 if form.is_valid():
	 	form.save()
	 	messages.success(request, f'Book successfully added')
	 	return redirect('books')
	else:
		form = AddBookForm()
	return render(request,'library/addbooks.html',{'my_form':form})






class issuebooksview(LoginRequiredMixin, ListView):
	model = issuedbooks
	template_name = "library/issuedbooks.html"
	context_object_name = 'issuedbooks'
	paginate_by = 5

	def get_context_data(self, ** kwargs):
		ctx = super().get_context_data( ** kwargs)
		queryset = issuedbooks.objects.values('userid_id').annotate(count=Count('userid_id')).order_by('count')
		ctx['count'] = queryset
		ctx['today'] = timezone.now()
		return ctx

	def get_queryset(self,**kwargs):
		return issuedbooks.objects.all().distinct('userid')


class BookDetailView(LoginRequiredMixin,DetailView):
	model = books
	context_object_name = 'bookname'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category = self.get_object()
		context['category'] = category
		context['related'] = books.objects.filter(category = category.category)
		return context

class deleteBookview(PermissionRequiredMixin, LoginRequiredMixin,DeleteView):
	permission_required = 'book.delete_books'
	model =books	
	success_url= reverse_lazy('books')
	success_message = "Book Successfully Deleted"

class UpdateBookView(PermissionRequiredMixin, LoginRequiredMixin,SuccessMessageMixin,UpdateView):

	permission_required = 'books.change_books'
	model = books
	context_object_name = 'bookname'
	fields =['serialno','title','category','author','image','quantity']
	#success_url = reverse_lazy('books')
	success_message = "Book Successfully Updated"

@login_required
def  UserIssuedBooks(request,userid):
	if not request.user.is_superuser:
		return render(request,'library/restricted.html')
	context ={
		'userissuedbooks' :issuedbooks.objects.filter(userid_id = userid),
		#'userissuedname':issuedbooks.objects.filter(userid_id=userid).distinct(),
		'userissuedname':User.objects.get(id=userid),
		#'duedate' : issuedbooks.objects.get(due_date),
		'today' : timezone.now()

	}

	return render(request,'library/userIssuedBooks.html',context)


@login_required
def returnbook(request,issuebooksid):

	returnissueidbook = issuedbooks.objects.get(id=issuebooksid)
	return render(request ,'library/book_confirm_return.html',{'returnissueidbook':returnissueidbook})


@login_required
def returnissuedbook(request,issuebooksid):


	if request.method == 'POST':
		issueid = issuedbooks.objects.get(id = issuebooksid)
		bookobject = books.objects.get(id = request.POST.get('bkid'))
		bookrsvdid = reservedbooks.objects.filter(bookid_id = bookobject)
		a = reservedbooks.objects.filter(Q(bookid =issueid.booksid) & Q(bookid_id = request.POST.get('bkid') ))

		
		bookobject.quantity = bookobject.quantity + 1
		bookobject.save()
		issueid.delete()	
		protocol = 'http://'	
		host = request.get_host()		
				
		if a:
		
			for b in a:
				subject = "Returned Book - UZ Library"
				link = protocol + host + reverse('book-detail',kwargs={'pk':b.bookid_id})
				message = b.bookid.title + " Book has been Returned .login to issue it is you still need it " + link			
				recipient_list = [b.userid.email,]
				send_mail(subject, message, EMAIL_HOST_USER,recipient_list,fail_silently=False)

				print(b.userid.email)				
				print(link)
		else:
			print('its not there')
	messages.success(request,f'Book successfully returned')
	return redirect('issued-books-view')


		
def reserve_book(request,booksid):
	'''context = {
	'booksid' : booksid,
	'user':request.user,
	'date':datetime.now()
	}'''
	reservebook = books.objects.get(id=booksid)	
	return render(request,'library/reserve_confirm_book.html',{'reservebook':reservebook})

def get_reserve_book(request):
	if request.method == 'POST':
		
		rsvbook = reservedbooks()
		rsvbook.bookid_id = request.POST['bookid']
		rsvbook.userid_id = request.user.id

		if reservedbooks.objects.filter(Q(userid_id = request.user.id) & Q(bookid_id = request.POST['bookid'])):
			messages.warning(request,f'This book has been reserved for you  already.Check 	Your Reserved books below')
			return redirect('user-account')
		else:
			totalreserved = reservedbooks.objects.filter(userid_id = request.user.id).count()
			if totalreserved > 1:
					messages.info(request,f'You can Only reserve two books.')
					return redirect('user-account')
			else :
				rsvbook.save()
				messages.success(request,f'Book successfully reserved')
				return redirect('user-account')
	else:
		return HttpResponse('error')


@login_required
def issuebook(request,booksid):
	issuebook = books.objects.get(id=booksid)
	return render(request,'library/book_confirm_issue.html',{'issuebook':issuebook})

@login_required
def getissuebook(request):

	if request.method == 'POST':
		post = issuedbooks()
		issuehistory = issuebookhistory()

		#personally i dont like how i achieved this
		#this will  be added in the history tables
		#django signals wil be better to use i think, hope to learn to use them soon
		issuehistory.booksid_id = request.POST['bookid']
		issuehistory.userid_id = request.POST['userid']

		post.booksid_id = request.POST['bookid']
		post.userid_id = request.POST['userid']
		bookobject = books.objects.get(id = request.POST.get('bookid'))

		if issuedbooks.objects.filter(Q(userid_id = request.user.id) & Q(booksid_id = request.POST['bookid'])):
			messages.warning(request,f'You have issued this book already.Check 	Your Issued books below')
			return redirect('user-account')
		else:
			t = issuedbooks.objects.filter(userid_id = request.user.id).count()
			if t > 2:
				messages.info(request,f'You have reached your limit of issuedbooks books.')
				return redirect('user-account')
			else:

				bookobject.quantity = bookobject.quantity - 1
				bookobject.save()
				post.save()
				issuehistory.save()

				#for email
				returndate  =issuedbooks.objects.latest('id')			
				book_title = request.POST.get('book_title')
				subject = "Issued Book - UZ Library"
				message = book_title + ' Has been issued to You.To be returnd on ' +	' '+ str(returndate.due_date) +''			
				recipient_list = [request.user.email,]
				send_mail(subject,message,EMAIL_HOST_USER,recipient_list,fail_silently = False)
						



				messages.success(request,f'Book successfully issued')
				return redirect('user-account')
	else:
		return HttpResponse('error')
		#issuedbooks.objects.filter(userid_id = self.request.user.id)
class historyissuedbook(ListView):
	model = issuebookhistory 
	context_object_name = 'issuehistory'

			### end of books model function ####

			### Category function ####
class add_category(PermissionRequiredMixin, SuccessMessageMixin, CreateView ):
	permission_required = 'library.add_category'
	model = category
	fields =['category_name']
	success_url = reverse_lazy('Viewcategory')
	success_message = "Category Successfully Added"
	
class UpdateCategoryView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	permission_required = 'library.change_category'
	model = category
	fields = ['category_name']
	success_url = reverse_lazy('Viewcategory')
	success_message = "Category Successfully Updated"


class CategoryDetailView(LoginRequiredMixin,DetailView):
	model = category 
	queryset = category.objects.filter(category_name='technology')
		
class ListCategoryView(LoginRequiredMixin, ListView):
	model = category
	template_name = "library/category.html"
	paginate_by = 5
	context_object_name = 'category'
	

	def get_context_data(self,**kwargs):
		context = super(ListCategoryView, self).get_context_data(**kwargs)
		queryset = books.objects.values('category').annotate(count=Count('category')).order_by('count')
		context['count'] = queryset
		return context


class DeleteCategoryView(PermissionRequiredMixin, LoginRequiredMixin,SuccessMessageMixin,DeleteView):
	permission_required = 'library.change_category'
	model = category
	success_url = reverse_lazy('Viewcategory')
	success_message = "Category Successfully Deleted"


class search_historyview(LoginRequiredMixin,ListView):
		model = searchedcontent
		context_object_name = 'searchedcontent'
		template_name = 'library/search_history.html'
		paginate_by = 5

		def get_queryset(self,**kwargs):
    			return searchedcontent.objects.filter(userid_id = self.request.user.id)

		 			


@login_required
def viewCategory(request,categoryid):
	categoryid = categoryid
	data = {

	'my_books' : books.objects.filter(category = categoryid),
	'category_name':category.objects.get(id=categoryid),
	#'count':books.objects.filter(category=categoryid).count()
	 'count' :books.objects.values('category').annotate(count=Count('category'))



	}
	return render(request,'library/category_list.html',data)


def export_csv(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition']=  'attachment; filename=librarybooks.csv'
	writer =csv.writer(response)
	writer.writerow(['title','category'])
	objbooks = books.objects.all()

	for objb in objbooks:
		writer.writerow([objb.title,objb.category]),
	return response


def export_pdf(request):
	buf = io.BytesIO()
	c = canvas.Canvas(buf,pagesize=letter,bottomup=0)


	textob = c.beginText()
	#textob.setTextOrigin(inch,inch)
	textob.setFont("Helvetica",14)
	objbooks = books.objects.all()
	lines = []
	for objb in objbooks:
		lines.append(objb.title)
		lines.append(objb.quantity)	



	for line in lines:
		textob.textLine(line)
	
	c.drawText(textob)
	c.showPage()
	c.save()	
	buf.seek(0)
	return FileResponse(buf, as_attachment=True, filename='books.pdf')



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 2, 3, 12, 2]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)