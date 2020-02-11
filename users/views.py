from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Акаунт успішно створено! Будь ласка, перевірте Вашу пошту, та перейдіть за посиланням, для того, щоб підтвердити її.')
            subject = f"Підтвердіть свій email на FreshNews"
            message = "Перейдіть за посиланням та Підтвердіть свій email"
            sender = "valentyncherkasov24@gmail.com"
            recipients = [form.cleaned_data.get('email')]
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Dont work!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
    

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
