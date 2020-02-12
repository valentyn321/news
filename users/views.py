from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .tasks import sleepy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = f"Підтвердіть свій email на FreshNews"
            message = render_to_string('users/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            sender = "valentyncherkasov24@gmail.com"
            recipients = [form.cleaned_data.get('email')]
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Error!')
            return render(request, 'users/confirm_send.html', {})
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


    # if request.method == 'POST':
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         messages.success(request, f'Акаунт успішно створено! Будь ласка, перевірте Вашу пошту, та перейдіть за посиланням, для того, щоб підтвердити її.')
    #         subject = f"Підтвердіть свій email на FreshNews"
    #         message = "Перейдіть за посиланням та Підтвердіть свій email"
    #         sender = "valentyncherkasov24@gmail.com"
    #         recipients = [form.cleaned_data.get('email')]
    #         try:
    #             send_mail(subject, message, sender, recipients, fail_silently=True)
    #         except BadHeaderError:
    #             return HttpResponse('Dont work!')
    #         return redirect('login')
    # else:
    #     form = UserRegisterForm()

    # return render(request, 'users/register.html', {'form': form})
    

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Інформацію оновлено!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)    

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('/')
        return render(request, 'users/confirm_send.html', {})
    else:
        return render(request, 'users/error_mail.html', {})
