from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.

def register(request):
    # check to see if POST or GET
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            # FOR NOW just redirect back to the register page
            # eventually want to change this to base.html or something 
            # or index.html 
            return redirect('register')
    
    else:
        f = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': f})

