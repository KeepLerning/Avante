# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import CustomUserCreationForm, CustomAuthenticationForm
# from django.contrib.auth import logout
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.urls import reverse
# from django.contrib import messages


# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_decode
# from .models import CustomUser
# from allauth.account.forms import LoginForm
# from Avante.views import home


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=password)
#             login(request, user)
#             send_activation_email(request, user)
#             messages.success(request, 'Please check your email to activate your account.')
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('home') # Ganti 'home' dengan nama halaman utama Anda
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def user_logout(request):
#     logout(request)
#     return redirect('home')


# def send_activation_email(request, user):
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
#     subject = 'Activate Your Account'
#     message = render_to_string('activation_email.html', {'activation_link': activation_link})
#     from_email = 'noreply@example.com'
#     recipient_list = [user.email]
#     send_mail(subject, message, from_email, recipient_list)

# @login_required
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         messages.success(request, 'Your account has been activated.')
#         return redirect('home')
#     else:
#         messages.error(request, 'Activation link is invalid or has expired.')
#         return redirect('login')
