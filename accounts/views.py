from django.shortcuts import redirect, render
from .models import Profile
from .forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    if request.method == 'POST': #save
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('/accounts/profile')
        
    else: # display
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    profile = Profile.objects.get(user = request.user)
    return render(request, 'profile/profile.html', {'profile': profile})

def profile_edite(request):
    profile = Profile.objects.get(user = request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            myform = profile_form.save(commit=False)
            myform.user = request.user
            myform.save()
            return redirect('/accounts/profile')

    else: 
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    