# 🏥 HyperCare AI — AI-Assisted Healthcare Workflow System

HyperCare AI is a web-based healthcare workflow management prototype built using Python, Streamlit, SQLite, and Machine Learning. It aims to simplify hospital operations by bringing patient registration, appointments, laboratory records, AI-assisted screening, doctor consultations, prescriptions, and billing into one application.

**Live Demo:** https://hypercare-ai-banafsha.streamlit.app/

**GitHub Repository:** https://github.com/SyedBanafsha/HyperCare-AI

## ✨ Features

### 🔐 Role-Based Login and Access
The application includes login and role-based page access for four staff roles:

- **Admin:** Hospital management dashboard and authorized administrative information.
- **Reception:** Patient registration, patient search, appointments, billing, and billing history.
- **Doctor:** Patient information, consultations, laboratory reports, AI screening results, and prescription generation.
- **Lab Technician:** Laboratory records and AI-assisted screening workflow.

The navigation menu displays pages according to the logged-in role.

### 🧑‍⚕️ Patient Management
- Patient registration with input validation.
- Duplicate phone number and email checks.
- Patient search using the available patient records.
- Storage of patient details in an SQLite database.

### 🧪 Laboratory and AI-Assisted Screening
The prototype includes machine-learning components for screening support related to:

- Diabetes
- Hypertension
- Anemia

Predictions depend on the available input measurements and the implemented screening workflow.

### 🩺 Doctor Consultation and Prescriptions
- Doctor consultation records.
- Diagnosis and prescription entry.
- Doctor notes.
- Electronic prescription PDF generation.
- Prescription email functionality, where configured.

### 💳 Appointments and Billing
- Appointment management.
- Billing records and billing history.
- Administrative revenue information.

### 📊 Admin Dashboard
- Patient and appointment statistics.
- Laboratory and doctor-record counts.
- AI prediction statistics.
- Revenue information and dashboard visualizations.

## 🛠️ Technology Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Database:** SQLite
- **Machine Learning:** scikit-learn
- **Data Processing:** pandas
- **PDF Generation:** ReportLab
- **Development Environment:** Visual Studio Code
- **Deployment:** Streamlit Community Cloud
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
HyperCare-AI/
├── assets/
├── database/
│   └── database.py
├── datasets/
├── docs/
├── models/
├── pages/
│   ├── Admin_Dashboard.py
│   ├── Appointment.py
│   ├── Billing.py
│   ├── Billing_History.py
│   ├── Doctor_Dashboard.py
│   ├── Lab_Technician.py
│   ├── Patient_Registration.py
│   └── Search_Patient.py
├── sample_outputs/
├── screenshots/
├── Training/
├── utils/
│   ├── auth.py
│   └── pdf_generator.py
├── .env.example
├── .gitignore
├── Home.py
├── login.py
├── requirements.txt
└── README.md
```

*Note: The listed structure describes the intended project layout; filenames may vary as development continues.*

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/SyedBanafsha/HyperCare-AI.git
cd HyperCare-AI
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m streamlit run Home.py
```

The application will display a local URL in the terminal. Open that URL in your browser.

## 🔑 Demo Login Accounts

The current prototype uses demo accounts configured in `login.py`:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Doctor | `doctor` | `doctor123` |
| Lab Technician | `lab` | `lab123` |
| Reception | `reception` | `reception123` |

**Security warning:** These are demonstration credentials, not secure production credentials. Do not use them for real patient information. Replace hardcoded passwords with securely stored password hashes and implement appropriate staff account management before production use.

## 🧠 AI Safety and Limitations

HyperCare AI is an academic prototype for healthcare workflow automation and AI-assisted screening. Its predictions are not medical diagnoses and must not independently determine treatment.

- Screening results depend on the input data and model limitations.
- The diabetes model has shown low precision in testing, so its accuracy alone should not be treated as evidence of clinical reliability.
- Healthcare professionals must assess results and make final clinical decisions.
- The models have not been established as clinically validated tools.

## 🔒 Data and Deployment Limitations

The current prototype uses SQLite and demonstration authentication. Depending on the deployment environment, local database files may not provide durable, shared storage across restarts or instances.

Before real-world use, the system requires persistent shared database infrastructure, secure authentication, appropriate authorization at the data-access level, audit logging, backup and recovery, and privacy and security review.

## 🔮 Future Improvements

- Admin-managed staff accounts and password resets.
- Secure password hashing and session management.
- Role-specific navigation and finer-grained permissions.
- Persistent shared database deployment.
- Audit logs and stronger patient-data protection.
- Improved model evaluation and clinical validation.
- Automated testing and expanded documentation.

## 👩‍💻 Developer

**Syed Banafsha**

Bachelor of Science in Artificial Intelligence

Islamic University of Science and Technology (IUST), Kashmir

---

*HyperCare AI is developed as an academic project exploring healthcare workflow automation and AI-assisted screening.*
