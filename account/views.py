from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView 
from django.views.generic import(
	ListView,
	CreateView,
	UpdateView,
	DeleteView,
)
from .mixins import (
	FieldMixins,
	FormValid,
	AuthorAccessMixin,
	SuperUserAccessMixin,
	AuthorsAccessMixin
)
from django.shortcuts import render, redirect
from blog.models import Article
from django.urls import reverse_lazy
from .models import User
from blog.forms import ProfileForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from blog.forms import SignUpForm
from .tokens import account_activation_token

# Create your views here.

class ArticleList(AuthorsAccessMixin, ListView):

	template_name = "registration/home.html"
	def get_queryset(self):
		if self.request.user.is_superuser:
			return Article.objects.all()
		else : 
			return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldMixins, FormValid, CreateView):
	model = Article
	template_name = "registration/article-create-update.html"


class ArticleUpdate(AuthorAccessMixin, FieldMixins, FormValid, UpdateView):
	model = Article
	template_name = "registration/article-create-update.html"


class ArticleDelete(SuperUserAccessMixin, DeleteView):
	template_name = "registration/article_confirm_delete.html"
	model = Article
	success_url = reverse_lazy('account:home')


class Profile(LoginRequiredMixin ,UpdateView):
	model = User
	form_class = ProfileForm 
	template_name = "registration/profile.html"
	success_url = reverse_lazy('account:profile')

	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)

	def get_form_kwargs(self):
		kwargs = super(Profile, self).get_form_kwargs()
		kwargs.update({
			"user" : self.request.user,
		})
		return kwargs


class login(LoginView):
	def get_success_url(self):
		user = self.request.user

		if user.is_superuser or user.is_author :
			return reverse_lazy('account:home')
		else :
			return reverse_lazy('account:profile')


class signup(CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'Activate your account.'
		message = render_to_string('registration/active_acount.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': default_token_generator.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
			mail_subject, message, to=[to_email]
		)
		email.send()
		return render(self.request, 'registration/register_success.html')


UserModel = get_user_model()
def activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = UserModel._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		return render(request, 'registration/register_conferm_html.html')
	else:
		return render(request, 'registration/register_not_valid.html') 