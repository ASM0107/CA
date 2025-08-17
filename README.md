
# ApnaSSL Certificate Authority (CA) Platform

A comprehensive Certificate Authority website built with Python and Django, providing digital certificate management, SSL/TLS certificate services, and a modern frontend for users and organizations.

## Features

- User Authentication and Management
- Digital Certificate Generation (CSR, Key Pair)
- SSL/TLS Certificate Issuance (DV, OV, EV)
- Domain Verification (DNS, HTTP, TXT)
- Organization Validation Workflow
- Certificate Revocation and Auto-renewal
- Database Management for Certificate Records
- Installation Guides and Support Resources
- Modern Frontend (HTML/CSS/JS) with interactive templates

## Technologies Used

- Python 3.11+
- Django Framework
- PostgreSQL Database
- HTML5, CSS3, JavaScript (Frontend)
- Cryptographic Libraries (for key/certificate generation)

## Project Structure

```
apnasslproject/
├── manage.py
├── apnasslproject/           # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── caCode/                   # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── static/
│   │   ├── images/
│   │   │   └── ApnaSSL.png
│   │   └── js/
│   │       └── homepage.js
│   └── templates/
│       └── caCode/
│           ├── about.html
│           ├── auto-renewal.html
│           ├── certificate-generator.html
│           ├── certificates.html
│           ├── dashboard.html
│           ├── Database.html
│           ├── dns-verification.html
│           ├── domain-verification.html
│           ├── homepage.html
│           ├── installation-guides.html
│           ├── key-generator.html
│           ├── login.html
│           ├── organization-validation.html
│           ├── revocation.html
│           ├── signup.html
│           └── support.html
Frontend/
├── homepage.js
LICENSE
README.md
```

## Frontend Overview

The frontend templates (in `apnasslproject/caCode/templates/caCode/`) provide:

- Certificate request and management dashboard (`dashboard.html`)
- Key and certificate generation tools (`key-generator.html`, `certificate-generator.html`)
- Domain and organization validation workflows (`domain-verification.html`, `organization-validation.html`)
- Certificate revocation and auto-renewal management (`revocation.html`, `auto-renewal.html`)
- Support and installation guides (`support.html`, `installation-guides.html`)
- User authentication (`login.html`, `signup.html`)

## Getting Started

### Prerequisites

- Python 3.11 or higher
- MySQL (or compatible database)
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ASM0107/CA.git
   cd CA
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```sh
   python manage.py migrate
   ```

5. Start the development server:
   ```sh
   python manage.py runserver
   ```

Visit [http://localhost:8000](http://localhost:8000) to access the application.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

Maintainer: [@ASM0107](https://github.com/ASM0107),[@Sauravnegiii](https://github.com/Sauravnegiii) 
Project Link: [https://github.com/ASM0107/CA](https://github.com/ASM0107/CA)
