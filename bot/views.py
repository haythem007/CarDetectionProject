from django.shortcuts import render, redirect, reverse
from .forms import UserForm, EditProfileForm, ContactUsForm, SUBJECT_CHOICES, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.template import loader
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, User
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
import os


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashbord')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def index(request):
   
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
   
    return render(request, 'index.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
              
                return redirect('dashbord')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

 

def bott(request):
   bot = ChatBot('Bot')
   bot.set_trainer(ListTrainer)
   for files in os.listdir('C:/djangopro/chatterbot-corpus-master\chatterbot_corpus\data\spanish/'):
        data = open('C:/djangopro/chatterbot-corpus-master\chatterbot_corpus\data\spanish/' + files , 'r').readlines()
        bot.train(data)
   message = request.GET.get('message')
   
   if message:
        reply = bot.get_response(message)
        return HttpResponse (reply)  
   return render(request, 'home.html',{'reply':"" , 'message': ""})  
   if message.strip() == 'tchaw':
        return HttpResponse (message)    

def dashbord(request):
    return render(request, 'dashbord.html')        

def home(request):
    return render(request, 'home.html')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('dashbord'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'profile.html', args)        


class ContactUsView(FormView):
    template_name = 'contact.html'
    email_template_name = 'contact_notification_email.txt'
    form_class = ContactUsForm
    success_url = "success/"
    subject = "Contact Us Request"

    def get_initial(self):
        initial = super(ContactUsView, self).get_initial()
        if not self.request.user.is_anonymous:
            initial['name'] = self.request.user.get_full_name()
            initial['email'] = self.request.user.email
            initial['subject'] = '-----'

        return initial

    def form_valid(self, form):
        form_data = form.cleaned_data

        if not self.request.user.is_anonymous:
            form_data['username'] = self.request.user.username

        form_data['subject'] = dict(SUBJECT_CHOICES)[form_data['subject']]

        # POST to the support email
        if form.is_valid():
            subject = form.cleaned_data['subject']
            #from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['description']
           
            try:
                send_mail(subject, message, self.request.user.email, ['haythemmarouani@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

        return super(ContactUsView, self).form_valid(form)    

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST or None)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
           
            try:
                send_mail(subject, message, from_email, ['haythemmarouani@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')   
def success(request):
    return render(request, 'success.html')     

def about(request):
    return render(request, 'about.html')


def bott1(request):
   bot = ChatBot('Bot')
   bot.set_trainer(ListTrainer)
   for files in os.listdir('C:/djangopro/chatterbot-corpus-master\chatterbot_corpus\data\english/'):
        data = open('C:/djangopro/chatterbot-corpus-master\chatterbot_corpus\data\english/' + files , 'r').readlines()
        bot.train(data)
   message = request.GET.get('message')
   
   if message:
        reply = bot.get_response(message)
        return HttpResponse (reply)  
   return render(request, 'home.html',{'reply':"" , 'message': ""})  
   if message.strip() == 'tchaw':
        return HttpResponse (message)     