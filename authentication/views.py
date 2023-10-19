from django.shortcuts import render, redirect, HttpResponse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from .utils import send_verification_mail, token_generator, send_reset_link
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use choose another one'}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use choose another one'}, status=409)
        return JsonResponse({'username_valid': True})
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        Firstname = request.POST["Firstname"]
        Lastname = request.POST["Lastname"]

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.first_name = Firstname
                user.last_name = Lastname
                user.is_active=False
                user.save()
                
                # path_to_view
                # -getting domain we are on
                # -relative url to verification
                # -encode uid
                # -token
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64':uidb64, 'token':token_generator.make_token(user)
                })
                activate_url = 'http://'+domain+link
                
                email_body = 'Hi '+user.first_name + " " + user.last_name +  \
                    ' Please use this link to verify your account\n' +activate_url    
                send_verification_mail(email, email_body)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html', context)

        return render(request, 'authentication/register.html')
    
class VerificationView(View):
    def get(self, request, uidb64, token):
        print("---Verifying----")
        try:
            print("---in try block---")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                print("--in check token--")
                messages.success(request, 'Account already activated')
                return redirect('login')
            
            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            print("---sending message---")
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        
        except Exception as ex:
            print(ex)
            return HttpResponse('Error occurred during activation')
        
        return redirect('login')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user=auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, '+user.username+' you are now logged in')
                    return redirect('expenses')
                
                messages.error(request, 'Account is not active, please check your email.')
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials, please try again.')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please fill all the fields.')
        return render(request, 'authentication/login.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render (request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST["email"]
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, 'Please provide a valid email')
            return render (request, 'authentication/reset-password.html')
        
        user = User.objects.filter(email=email)
        if user.exists():
            user = user[0]
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            token = PasswordResetTokenGenerator().make_token(user)
            link = reverse('reset-user-password', kwargs={
                'uidb64':uidb64, 'token': token
            })
            reset_url = 'http://'+domain+link
            
            email_body = 'Hi there, Please click the link below to reset your password  \n'+ reset_url    
            send_reset_link(email, email_body)
            messages.success(request, 'reset link sent')
            return render(request, 'authentication/reset-password.html', context)

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password reset link is invalid, please request a new one')
                return render(request, 'authentication/reset-password.html', context)
        except Exception as identifier: 
            pass

        return render(request, 'authentication/set-new-password.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set-new-password.html', context)
        
        if len(password) <6 :
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set-new-password.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfully, you can login now with your new password')
            return redirect('login')
        except Exception as ex:
            print(ex)
            messages.info(request, 'Something went wrong, try again')
            return render(request, 'authentication/set-new-password.html', context)
    
        # return render(request, 'authentication/set-new-password.html', context)