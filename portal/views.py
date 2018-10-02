## Author: Aziz Khan
## License: GPL v3
## Copyright 2017 Aziz Khan <azez.khan__AT__gmail.com>

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Max
from .models import Factor, FactorData, Post
from itertools import chain
from .forms import SearchForm, ContactForm
import os, sys, re
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse

from unibind.settings import BASE_DIR, BIN_DIR, TEMP_DIR, TEMP_LIFE, SEND_TO_EMAIL, MAX_PAGINATION_LIMIT, PAGINATION_DEFAULT

from django.views.decorators.cache import cache_page

CACHE_TIMEOUT = 60 * 60 * 24 * 1 # cache timeout in seconds

@cache_page(60)
def index(request):
	'''
	This loads the homepage
	'''

	setattr(request, 'view', 'index')

	search_form = SearchForm()
	
	datasets = Factor.objects.all().count()

	context ={
	'search_form': search_form,
	'datasets': datasets,
	}
	context.update(_get_advanced_search_data())

	return render(request, 'portal/index.html', context)

@cache_page(CACHE_TIMEOUT)
def search(request):
	'''
	This function returns the results based the on the search query
	'''
	
	query_string = request.GET.get('q', None)
	cell_line = request.GET.get('cell_line', None)
	tf_name = request.GET.get('tf_name', None)
	model = request.GET.get('model', None)
	peak_caller = request.GET.get('peak_caller', None)
	data_source = request.GET.get('source', None)
	has_pvalue = request.GET.get('has_pvalue', None)

	setattr(request, 'view', 'search')

	#Pagination
	page = request.GET.get('page', 1)
	page_size = request.GET.get('page_size', PAGINATION_DEFAULT)
	if page_size =='' or int(page_size) > MAX_PAGINATION_LIMIT:
		page_size = PAGINATION_DEFAULT

	queryset = Factor.objects.all().order_by('tf_name')

	#filter based on tf_name
	if tf_name and tf_name !='' and tf_name !='all':
		queryset = queryset.filter(tf_name=tf_name)

	#filter based on cell_line
	if cell_line and cell_line !='' and cell_line !='all':
		queryset = queryset.filter(cell_line=cell_line)

	#filter based on data_source
	if data_source and data_source !='' and data_source !='all':
		queryset = queryset.filter(data_source=data_source)

	#filter based on query_string
	if query_string and query_string !='':
		id_query = query_string.split('.')
		if len(id_query) == 2 and id_query[0][0:2] == 'MA':
			query_string = id_query[0]
		queryset = queryset.filter(
			Q(tf_name__icontains=query_string) | 
			Q(cell_line__icontains=query_string) |
			Q(biological_condition__icontains=query_string) |
			Q(data_source__icontains=query_string) |
			Q(identifier__icontains=query_string) |
			Q(jaspar_id__icontains=query_string)
			) 

	if has_pvalue:
		folders = queryset.values_list('folder', flat=True).distinct()
		folders = FactorData.objects.values_list('folder', flat=True).filter(folder__in=folders).exclude(adj_centrimo_pvalue__in=['NS','NA']).distinct()
		queryset = queryset.filter(folder__in=folders)

	#filter based on peak caller
	if peak_caller and peak_caller !='' and peak_caller !='all':
		folders = queryset.values_list('folder', flat=True).distinct()
		folders = FactorData.objects.values_list('folder', flat=True).filter(folder__in=folders, peak_caller=peak_caller).distinct()
		queryset = queryset.filter(folder__in=folders)

	##paginate the queryset
	paginator = Paginator(queryset, page_size)
		
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
	'pages': queryset,	
	}
	context.update(_get_advanced_search_data())
	
	return render(request, 'portal/search.html', context)


@cache_page(CACHE_TIMEOUT)
def factor_detail(request, factor_id):
	'''
	This will show the details of a factor based on factor_id
	'''

	factor = Factor.objects.get(folder__iexact=factor_id)

	#factor_details = FactorData.objects.filter(folder=factor_id)
	factor_details = FactorData.objects.filter(folder__folder__iexact=factor_id)
	folder_name = factor_details.values_list('folder', flat=True)[0]


	similar_factors = Factor.objects.filter(tf_name=factor.tf_name).exclude(folder=factor_id).order_by('tf_name')

	#models = factor_details.values_list('prediction_model', flat=True).distinct().order_by('prediction_model')
	models = factor_details.values_list('prediction_model', flat=True).distinct()
	mlists = models
	#BEM, DNAshaped, DiMO, PWM, TFFM
	morder=[1,2,3,0]
	if len(morder) == len(mlists):
		models = [ mlists[i] for i in morder]
		
	peak_callers = factor_details.values_list('peak_caller', flat=True).distinct().order_by('-peak_caller')

	model_name = request.GET.get('mtrain', None)
	if model_name and model_name != '':
		#Create a zip file

		tar_file_name = 'UniBind_trained_model_'+model_name+'_'+_get_current_date()+'.tar.gz'
		tar_file_path = TEMP_DIR+'/'+tar_file_name
		target_path = BASE_DIR+'/static/data/macs/'+model_name+'/'+factor_id

		cmd = "tar -czf "+tar_file_path+" -C "+target_path+" . --exclude='"+target_path+"/*.bed' --exclude='"+target_path+"/*.fa' --exclude='"+target_path+"/*.png'"
		#cmd = "tar -czf "+tar_file_path+" "+target_path

		os.system(cmd)
	else:
		tar_file_name = None

	context = {
		'factor': factor,
		'folder_name': folder_name,
		'factor_details': factor_details,
		'models': models,
		'peak_callers': peak_callers,
		'factors': similar_factors,
		'tar_file_name': tar_file_name,
	}

	return render(request, 'portal/factor_detail.html', context)					

def _get_current_date():
	
	import datetime
	
	now = datetime.datetime.now()

	return str(str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2))


@cache_page(CACHE_TIMEOUT)
def documentation(request):
	'''
	This will show the documentation page
	'''
	setattr(request, 'view', 'docs')

	return render(request, 'portal/documentation.html')

@cache_page(CACHE_TIMEOUT)
def download_data(request):
	'''
	This will show the downloads page
	'''
	setattr(request, 'view', 'downloads')
	
	#models = FactorData.objects.all().values_list('prediction_model', flat=True).distinct().order_by('prediction_model')
	models = FactorData.objects.all().values_list('prediction_model', flat=True).distinct()
	mlists = models
	#BEM, DNAshaped, DiMO, PWM, TFFM
	morder=[1,2,3,0]
	models = [ mlists[i] for i in morder]

	peak_callers = FactorData.objects.all().values_list('peak_caller', flat=True).distinct().order_by('-peak_caller')

	context = {
	'models': models,
	'peak_callers': peak_callers,
	}

	return render(request, 'portal/downloads.html', context)


@cache_page(CACHE_TIMEOUT)
def api_documentation(request):
	'''
	This will show the api documentation page
	'''
	setattr(request, 'view', 'api-home')
	#setattr(request, 'view', 'apidocs')

	#return render(request, 'portal/api_documentation.html')
	return render(request, 'rest_framework/api_home.html')

@cache_page(CACHE_TIMEOUT)
def contact_us(request):
	'''
	Contact us and feednback page to send email
	'''
	setattr(request, 'view', 'contact_us')

	from django.core.mail import EmailMessage

	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['from_email']
			#from_name = form.cleaned_data['from_name']
			message = form.cleaned_data['message']

			email = EmailMessage(
			    subject,
			    'From: '+from_email+'\n\nMessage: '+message,
			    from_email,
			    SEND_TO_EMAIL,
			    reply_to=[from_email],
			)
			try:
				#send_mail(subject, message, from_email, SEND_TO_EMAIL)
				email.send()
			except BadHeaderError:
				context ={'message': 'Invalid header found. Your message did not went through.', 'message_type': 'error', }
				return render(request, 'portal/contact_us.html', context)

			context = {'message': 'Thank you! Your message has been sent successfully. We will get back to you shortly.', 'message_type': 'success'}

			return render(request, 'portal/contact_us.html', context)
	return render(request, 'portal/contact_us.html', {'form': form})

@cache_page(CACHE_TIMEOUT)
def faq(request):
	'''
	This will show the FAQ page
	'''

	setattr(request, 'view', 'faq')


	return render(request, 'portal/faq.html')

@cache_page(CACHE_TIMEOUT)
def changelog(request):
	'''
	This will show the changelog page
	'''

	setattr(request, 'view', 'changelog')


	return render(request, 'portal/changelog.html')

@cache_page(CACHE_TIMEOUT)
def tour_video(request):
	'''
	This will show the tour video page
	'''

	setattr(request, 'view', 'tour')


	return render(request, 'portal/tour_video.html')

@cache_page(CACHE_TIMEOUT)
def about(request):
	'''
	This will show the about page
	'''
	setattr(request, 'view', 'about')

	datasets = Factor.objects.all().count()

	context ={
	'datasets': datasets,
	}
	context.update(_get_advanced_search_data())

	return render(request, 'portal/about.html', context)

@cache_page(CACHE_TIMEOUT)
def post_details(request, year, month, day, slug):
	'''
	Show individual news/update
	'''
	post = get_object_or_404(Post, slug=slug)

	posts = Post.objects.all().order_by('-date')[:5]

	return render(request, 'portal/blog_single.html', {
        'post': post,
        'posts': posts,
    })

@cache_page(CACHE_TIMEOUT)
def post_list(request):
	'''
	List all news/updates
	'''
	posts = Post.objects.all().order_by('-date')

	return render(request, 'portal/blog.html', {
        'posts': posts,
    })


def page_not_found(request):
	'''
	Return custome 404 error page
	'''

	return render(request, '404.html', status=404)


def server_error(request):
	'''
	Return custome 500 error page
	'''
	return render(request, '500.html', status=500)


def _get_advanced_search_data():
	'''
	Return a data dictionary to create advanced search options
	'''
	tf_names = Factor.objects.all().values('tf_name').distinct().order_by('tf_name')
	cell_lines = Factor.objects.all().values('cell_line').distinct().order_by('cell_line')
	prediction_models = FactorData.objects.all().values('prediction_model').distinct().order_by('prediction_model')
	peak_callers = FactorData.objects.all().values('peak_caller').distinct().order_by('peak_caller')
	sources = Factor.objects.all().values('data_source').distinct().order_by('data_source')

	context ={
	'tf_names': tf_names,
	'cell_lines': cell_lines,
	'prediction_models': prediction_models,
	'peak_callers': peak_callers,
	'sources': sources,

	}

	return context