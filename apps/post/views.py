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
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView, UpdateView,DetailView
from apps.user_profile.models import Doctor



class UserIndexView(View):
	index_template="partial/index.html"  
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
class SearchListView(ListView):
    model=Doctor
    paginate_by=10
    template_name="post/home_search.html"
    context_object_name="searches"

    def get_queryset(self):
        keywords=self.request.GET.get("q")
        qs = Doctor.objects.all() if keywords else Doctor.objects.none()

        if keywords:
            query= SearchQuery(keywords)
            name_vector=SearchVector("user__username",weight="A")
            department_vector=SearchVector("department__department_name",weight="B")
            firstname_vector=SearchVector("user__first_name",weight="C")
            lastname_vector=SearchVector("user__last_name",weight="D")
            vectors=name_vector + department_vector + firstname_vector + lastname_vector
            qs=qs.annotate(search=vectors).filter(search=query)
            qs=qs.annotate(rank=SearchRank(vectors,query)).order_by("education")

        return qs