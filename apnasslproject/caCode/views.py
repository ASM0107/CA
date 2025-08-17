from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm, LoginForm, CSRUploadForm
from .models import CertificateRequest
import secrets
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm, LoginForm, CSRUploadForm
from .models import CertificateRequest
import secrets, io, zipfile, datetime

@csrf_exempt
def generate_csr(request):
    if request.method == "POST":
        common_name = request.POST.get("commonName")
        org = request.POST.get("organization")
        org_unit = request.POST.get("orgUnit")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        email = request.POST.get("email")
        san_input = request.POST.get("san")  # comma-separated domains
        algorithm = request.POST.get("algorithm")
        key_size = request.POST.get("keySize")

        # Generate private key
        if algorithm == "RSA":
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=int(key_size)
            )
        else:  # EC
            curve = ec.SECP256R1() if key_size == "256" else ec.SECP384R1()
            private_key = ec.generate_private_key(curve)

        # Build subject (only include non-empty fields)
        subject_attrs = [x509.NameAttribute(NameOID.COMMON_NAME, common_name)]
        if org: subject_attrs.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, org))
        if org_unit: subject_attrs.append(x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, org_unit))
        if city: subject_attrs.append(x509.NameAttribute(NameOID.LOCALITY_NAME, city))
        if state: subject_attrs.append(x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state))
        if country: subject_attrs.append(x509.NameAttribute(NameOID.COUNTRY_NAME, country))
        if email: subject_attrs.append(x509.NameAttribute(NameOID.EMAIL_ADDRESS, email))

        subject = x509.Name(subject_attrs)

        # Start CSR builder
        csr_builder = x509.CertificateSigningRequestBuilder().subject_name(subject)

        # Add SAN extension if provided (support DNS and email)
        san_names = []
        if san_input:
            san_list = [x.strip() for x in san_input.split(",") if x.strip()]
            for entry in san_list:
                if "@" in entry:
                    san_names.append(x509.RFC822Name(entry))
                else:
                    san_names.append(x509.DNSName(entry))
        # Add email to SAN if provided and not already present
        if email:
            if not any(isinstance(n, x509.RFC822Name) and n.value == email for n in san_names):
                san_names.append(x509.RFC822Name(email))
        if san_names:
            csr_builder = csr_builder.add_extension(
                x509.SubjectAlternativeName(san_names),
                critical=False
            )

        # Sign CSR
        csr = csr_builder.sign(private_key, hashes.SHA256())
        csr_pem = csr.public_bytes(serialization.Encoding.PEM)

        # Export private key PEM
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Save CSR PEM to database for the user
        if request.user.is_authenticated:
            # Save CSR PEM to a file with a name
            from django.core.files.base import ContentFile
            csr_filename = f"{common_name}_csr.pem"
            csr_file = ContentFile(csr_pem, name=csr_filename)
            cert_request = CertificateRequest.objects.create(
                user=request.user,
                domain=common_name,
                dns_token=secrets.token_urlsafe(32),
                status='pending',
                verified=False
            )
            cert_request.csr.save(csr_filename, csr_file)
        # Package CSR + private key into a ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            zip_file.writestr("certificate.csr", csr_pem)
            zip_file.writestr("private.key", private_key_pem)

        response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="csr_bundle.zip"'
        return response

    return HttpResponse("Invalid request", status=400)

def homepage(request):
    return render(request, 'caCode/homepage.html')

def about(request):
    return render(request, 'caCode/about.html')

def dashboard(request):
    if request.user.is_authenticated:
        certificates = CertificateRequest.objects.filter(user=request.user)
    else:
        certificates = []
    return render(request, 'caCode/dashboard.html', {'certificates': certificates})

def support(request):
    return render(request, 'caCode/support.html')

def auto_renewal(request):
    return render(request, 'caCode/auto-renewal.html')

def certificate_generator(request):
    return render(request, 'caCode/certificate-generator.html')

@login_required(login_url='login')
def certificates(request):
    return render(request, 'caCode/certificates.html')

from django.views.decorators.http import require_POST
import dns.resolver

def domain_verification(request):
    # Show all certificate requests for the logged-in user (or all if admin)
    if request.user.is_superuser:
        certificates = CertificateRequest.objects.all()
    else:
        certificates = CertificateRequest.objects.filter(user=request.user)
    return render(request, 'caCode/dns-verification.html', {'certificates': certificates})

@require_POST
def verify_dns(request, cert_id):
    from django.shortcuts import get_object_or_404
    cert = get_object_or_404(CertificateRequest, id=cert_id, user=request.user)
    txt_name = cert.dns_record_name()
    try:
        answers = dns.resolver.resolve(txt_name, 'TXT')
        for rdata in answers:
            # rdata.to_text() returns the TXT value as a string (may be quoted)
            txt_value = rdata.to_text().strip('"')
            if cert.dns_token == txt_value:
                cert.verified = True
                cert.status = 'valid'
                cert.save()
                break
    except Exception:
        pass
    return redirect('domain_verification')

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
