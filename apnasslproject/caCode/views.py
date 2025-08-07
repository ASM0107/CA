from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm, LoginForm, CSRUploadForm
from .models import CertificateRequest
import secrets



def homepage(request):
    return render(request, 'caCode/homepage.html')

def about(request):
    return render(request, 'caCode/about.html')

def support(request):
    return render(request, 'caCode/support.html')

def auto_renewal(request):
    return render(request, 'caCode/auto-renewal.html')

def certificate_generator(request):
    return render(request, 'caCode/certificate-generator.html')

def certificates(request):
    return render(request, 'caCode/certificates.html')

def domain_verification(request):
    return render(request, 'caCode/domain-verification.html')

def installation_guides(request):
    return render(request, 'caCode/installation-guides.html')

def key_generator(request):
    return render(request, 'caCode/key-generator.html')

def organization_validation(request):
    return render(request, 'caCode/organization-validation.html')

def revocation(request):
    return render(request, 'caCode/revocation.html')


# Auth views
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Form invalid.')
    else:
        form = SignUpForm()
    return render(request, 'caCode/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('certificates')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'caCode/login.html')


def upload_csr(request):
    if request.method == 'POST':
        form = CSRUploadForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            csr = form.cleaned_data['csr']
            token = secrets.token_urlsafe(16)

            CertificateRequest.objects.create(
                user=request.user,
                domain=domain,
                csr=csr,
                dns_token=token
            )
            return redirect('dns_verification_list')
    else:
        form = CSRUploadForm()
    return render(request, 'upload_csr.html', {'form': form})
