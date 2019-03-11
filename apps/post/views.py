# from django.shortcuts import render
# from .models import Admin_post
# #from django.http import HttpResponse
# """
# importing HttpResponse
# function index handle the traffic from the home page 
# """
# # def index(request):
# #     return HttpResponse('<h1>home</h1>')

# # def about(request):
# #     return HttpResponse('<h1>About</h1>')


# def index(request):
#     context = {
#         'posts': Admin_post.objects.all()
#     }
#     return render(request, 'post/index.html', context)


# def about(request):
#     return render(request, 'about.html', {'title': 'About'})


# def services(request):
# 	template = 'services.html'
# 	return render(request, template, {'title':'Services'})

# def contact(request):
# 	template = 'contact.html'
# 	return render(request, template, {'title':'Contact'})




from django.shortcuts import render
from django.views import View
from .models import Admin_post


class UserIndexView(View):
	index_template="post/index.html"  
	def get(self,request):
		context = {
			'posts': Admin_post.objects.all()
		}
	
		return render(request, self.index_template,context)


class UserAboutView(View):
    about_template="post/about.html"
    def get(self,request):
        return render(request, self.about_template)

class UserServicesView(View):
    services_template="post/services.html"
    def get(self,request):
        return render(request, self.services_template)

class UserContactView(View):
    contact_template="post/contact.html"
    def get(self,request):
        return render(request, self.contact_template)

# def book(request):
# 	template = '#'
# 	return render(request, template, {'title':'Book_Appointment'})


# def billPayment(request):
# 	template = '#'
# 	return render(request, template, {'title':'billPay'})


# def findDoctor(request):
# 	template = '#'
# 	return render(request, template, {'title':'findDoctor'})
