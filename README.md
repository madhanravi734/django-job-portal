# Job Portal

A full-stack job portal built with Django that provides separate workflows for candidates and recruiters. Candidates can create profiles, browse jobs, apply, and track applications, while recruiters can create and manage jobs, review applicants, and update application statuses.

## Features

### Candidate
- Candidate registration and authentication
- Candidate profile management
- Resume upload
- Browse available jobs
- View job details
- Apply for jobs
- Duplicate application prevention
- View submitted applications and statuses
- Logout

### Recruiter
- Recruiter registration and authentication
- Company profile management
- Recruiter dashboard with application statistics
- Create, edit, and delete jobs
- View recruiter-owned jobs
- View applicants for owned jobs
- View candidate resumes
- Accept/reject/pending application status management
- Logout

### Access control
- Candidate and recruiter workflows are separated
- Recruiters can manage only their own jobs and applicants
- Candidates cannot access recruiter management actions
- Duplicate candidate/job applications are prevented at the database level
- POST forms use Django CSRF protection
- Protected pages use authentication checks and cache-control protection

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite for local development
- **Authentication:** Django built-in authentication
- **ORM:** Django ORM
- **File uploads:** Django media handling

## Project Structure

```text
JobPortal/
├── JobPortal/          # Project configuration
├── accounts/           # Authentication and candidate/recruiter profiles
├── jobs/               # Job creation, browsing and management
├── applications/       # Applications and applicant status management
├── templates/          # Shared templates
├── static/
│   ├── css/
│   └── js/
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd JobPortal
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and set a strong `DJANGO_SECRET_KEY` for anything beyond local development.

For local development, the project also has a development fallback secret so it can start without extra configuration. Do **not** use that fallback in production.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Main Routes

| Area | Route |
|---|---|
| Home | `/` |
| Login | `/accounts/login/` |
| Register | `/accounts/register/` |
| Candidate Dashboard | `/accounts/candidate-dashboard/` |
| Recruiter Dashboard | `/jobs/recruiter-dashboard/` |
| Browse Jobs | `/jobs/job_list/` |
| My Jobs | `/jobs/my_jobs/` |
| My Applications | `/applications/my-applications/` |

## Data Model

The application uses four main domain models:

- **CandidateProfile** — candidate information and resume
- **RecruiterProfile** — company information
- **Job** — job postings owned by recruiters
- **Application** — links candidates to jobs and stores application status

The `Application` model enforces a unique candidate/job combination, preventing the same candidate from applying to the same job more than once.

## Candidate Workflow

```text
Register
   ↓
Candidate Profile
   ↓
Browse Jobs
   ↓
Job Details
   ↓
Apply
   ↓
My Applications
   ↓
Logout
```

## Recruiter Workflow

```text
Register
   ↓
Company Profile
   ↓
Recruiter Dashboard
   ↓
Create Job
   ↓
My Jobs
   ↓
View Applicants
   ↓
Update Status
   ↓
Edit / Delete Job
   ↓
Logout
```

## Security & Authorization

The project includes ownership and role-based access checks around recruiter and candidate workflows. Recruiters can only edit/delete their own jobs and view/update applications belonging to their own jobs. Candidates cannot access recruiter management operations.

For production deployment, additional hardening should be configured, including secure cookies, HTTPS, production `ALLOWED_HOSTS`, `DEBUG=False`, a production secret key, and a production database.

## Screenshots

Add screenshots of the main pages to a `screenshots/` directory and reference them here.

Recommended screenshots:
- Home page
- Candidate dashboard
- Job listing
- Job detail
- My applications
- Recruiter dashboard
- My jobs
- Applicants page
- Recruiter profile

## Future Improvements

- Django REST Framework API
- PostgreSQL for production
- Search and filtering
- Pagination
- Email notifications
- Password reset flow
- Recruiter/candidate role permissions using dedicated authorization classes
- Production deployment with a cloud platform
- Automated tests with broader coverage
- Improved resume/document validation

## Author

**Madhan Ravi**

Software Engineer Intern | Python | Django | React | TypeScript

## License

This project is licensed under the MIT License.
