import sqlite3
connection = sqlite3.connect("hospital.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctor_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_name TEXT,
    diagnosis TEXT,
    required_tests TEXT,
    prescription TEXT,
    doctor_notes TEXT,
    visit_date TEXT,
    consultation_status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctor_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_name TEXT,
    diagnosis TEXT,
    prescription TEXT,
    doctor_notes TEXT,
    visit_date TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_name TEXT,
    appointment_date TEXT,
    appointment_time TEXT,
    status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS lab_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    test_name TEXT,
    test_result TEXT,
    technician_name TEXT,
    report_date TEXT,
    status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS billing (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    consultation_fee REAL,
    lab_fee REAL,
    medicine_fee REAL,
    total_amount REAL,
    payment_status TEXT,
    billing_date TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    predicted_disease TEXT,
    confidence REAL,
    risk_level TEXT,
    recommendation TEXT,
    prediction_date TEXT
)
""")

connection.commit()



def add_patient(
    patient_name,
    phone_number,
    email,
    age,
    gender,
    residence,
    purpose_of_visit,
    current_symptoms
):
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT patient_id
    FROM patients
    WHERE phone_number = ? OR email = ?
    """, (phone_number, email))
    existing_patient = cursor.fetchone()

    if existing_patient:
        connection.close()
        return False

    cursor.execute("""
                
    INSERT INTO patients
    (
        patient_name,
        phone_number,
        email,
        age,
        gender,
        residence,
        purpose_of_visit,
        current_symptoms
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        patient_name,
        phone_number,
        email,
        age,
        gender,
        residence,
        purpose_of_visit,
        current_symptoms
    ))

    connection.commit()
    connection.close()
    return True

def search_patient(patient_id):
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    connection.close()

    return patient

def add_doctor_record(
    patient_id,
    doctor_name,
    diagnosis,
    required_tests,
    prescription,
    doctor_notes,
    visit_date,
    consultation_status
):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO doctor_records
    (
        patient_id,
        doctor_name,
        diagnosis,
        required_tests,
        prescription,
        doctor_notes,
        visit_date,
        consultation_status
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        patient_id,
        doctor_name,
        diagnosis,
        required_tests,
        prescription,
        doctor_notes,
        visit_date,
        consultation_status
    ))

    connection.commit()
    connection.close()

def add_appointment(patient_id, doctor_name, appointment_date, appointment_time, status):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO appointments
    (patient_id, doctor_name, appointment_date, appointment_time, status)

    VALUES (?, ?, ?, ?, ?)
    """,
    (
        patient_id,
        doctor_name,
        appointment_date,
        appointment_time,
        status
    ))

    connection.commit()
    connection.close()

def get_total_patients():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_total_doctor_records():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM doctor_records")

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_total_appointments():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM appointments")

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_recent_appointments():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM appointments
    ORDER BY appointment_id DESC
    LIMIT 5
    """)

    appointments = cursor.fetchall()

    connection.close()

    return appointments

def get_latest_lab_report(patient_id):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM lab_reports
        WHERE patient_id = ?
        ORDER BY report_id DESC
        LIMIT 1
    """, (patient_id,))

    lab = cursor.fetchone()

    connection.close()

    return lab

def add_bill(patient_id, consultation_fee, lab_fee, medicine_fee,
             total_amount, payment_status, billing_date):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO billing
    (patient_id, consultation_fee, lab_fee, medicine_fee,
     total_amount, payment_status, billing_date)

    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        patient_id,
        consultation_fee,
        lab_fee,
        medicine_fee,
        total_amount,
        payment_status,
        billing_date
    ))

    connection.commit()
    connection.close()

def get_all_bills():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM billing
    ORDER BY bill_id DESC
    """)

    bills = cursor.fetchall()

    connection.close()

    return bills

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

def generate_bill_pdf(
    patient_id,
    patient_name,
    age,
    gender,
    residence,
    consultation_fee,
    lab_fee,
    medicine_fee,
    total_amount,
    payment_status,
    billing_date
):

    filename = f"Bill_{patient_id}.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # Title

    story.append(
        Paragraph("<b><font size=22>HyperCare AI Hospital</font></b>",
        styles["Title"])
    )
    story.append(
    Paragraph(
        "<font size=11>"
        "Srinagar, Jammu & Kashmir<br/>"
        "Phone : +91 98765 43210<br/>"
        "Email : support@hypercareai.com"
        "</font>",
        styles["Normal"]
    )
)

    story.append(
        Paragraph(
            "<font size=14><b>OFFICIAL BILL RECEIPT</b></font>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.30 * inch))

    # Invoice Details

    story.append(
        Paragraph(f"<b>Invoice No :</b> HC-{patient_id:04d}",
        styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Patient ID :</b> {patient_id}",
        styles["Normal"])
    )
    story.append(
    Paragraph(f"<b>Patient Name :</b> {patient_name}",
    styles["Normal"])
)

    story.append(
        Paragraph(f"<b>Age :</b> {age}",
        styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Gender :</b> {gender}",
        styles["Normal"])
    )
    story.append(
    Paragraph(
        f"<b>Residence :</b> {residence}",
        styles["Normal"]
    )
)

    story.append(
            Paragraph(f"<b>Date :</b> {billing_date}",
            styles["Normal"])
        )

    story.append(Spacer(1, 0.25 * inch))

    # Fees Table

    data = [

        ["Description", "Amount (Rs.)"],

        ["Consultation Fee", consultation_fee],

        ["Lab Fee", lab_fee],

        ["Medicine Fee", medicine_fee],

        ["TOTAL", total_amount]

    ]

    table = Table(data, colWidths=[250,150])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-2),colors.beige),

        ("BACKGROUND",(0,-1),(-1,-1),colors.lightgrey),

        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),

        ("ALIGN",(1,1),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

    ]))

    story.append(table)

    story.append(Spacer(1,0.30*inch))

    status = " [PAID]" if payment_status == "Paid" else "⏳ PENDING"

    story.append(
    Paragraph(
        f"<b>Payment Status :</b> {status}",
        styles["Heading3"]
    )
)

    story.append(Spacer(1,0.3*inch))

    story.append(
    Paragraph(
        "<b>Thank you for choosing HyperCare AI Hospital.</b>",
        styles["Heading2"]
    )
)

    story.append(
    Paragraph(
        "Get Well Soon!",
        styles["Heading3"]
    )
)

    story.append(Spacer(1,0.2*inch))

    story.append(
    Paragraph(
        "-----------------------------------------------------------",
        styles["Normal"]
    )
)

    story.append(
    Paragraph(
        "This is a computer-generated receipt.",
        styles["Normal"]
    )
)

    story.append(
    Paragraph(
        "No signature is required.",
        styles["Normal"]
    )
)

    pdf.build(story)

    return filename


def add_ai_prediction(
    patient_id,
    predicted_disease,
    confidence,
    risk_level,
    recommendation,
    prediction_date
):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO ai_predictions
    (
        patient_id,
        predicted_disease,
        confidence,
        risk_level,
        recommendation,
        prediction_date
    )

    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        patient_id,
        predicted_disease,
        confidence,
        risk_level,
        recommendation,
        prediction_date
    ))

    connection.commit()
    connection.close()

def get_latest_lab_report(patient_id):

    cursor.execute("""
        SELECT *
        FROM lab_reports
        WHERE patient_id = ?
        ORDER BY report_id DESC
        LIMIT 1
    """, (patient_id,))

    return cursor.fetchone()

def get_latest_ai_prediction(patient_id):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM ai_predictions
        WHERE patient_id = ?
        ORDER BY prediction_id DESC
        LIMIT 1
    """, (patient_id,))

    prediction = cursor.fetchone()

    connection.close()

    return prediction   

def get_all_ai_predictions(patient_id):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM ai_predictions
        WHERE patient_id = ?
        ORDER BY prediction_id DESC
    """, (patient_id,))

    all_predictions = cursor.fetchall()

    connection.close()

    latest_predictions = {}
    
    for prediction in all_predictions:
        disease = prediction[2]

        if disease not in latest_predictions:
            latest_predictions[disease] = prediction

    return list(latest_predictions.values())


def get_total_appointments():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM appointments")
    total = cursor.fetchone()[0]

    connection.close()
    return total


def get_total_lab_reports():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM lab_reports")
    total = cursor.fetchone()[0]

    connection.close()
    return total


def get_total_doctor_records():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM doctor_records")
    total = cursor.fetchone()[0]

    connection.close()
    return total


def get_total_ai_predictions():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM ai_predictions")
    total = cursor.fetchone()[0]

    connection.close()
    return total


def get_total_revenue():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(total_amount) FROM billing")
    total = cursor.fetchone()[0]

    connection.close()

    if total is None:
        return 0

    return total

def get_recent_patients():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT patient_name,
               age,
               gender,
               purpose_of_visit
        FROM patients
        ORDER BY patient_id DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def get_recent_appointments():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT patient_id,
               doctor_name,
               appointment_date,
               appointment_time,
               status
        FROM appointments
        ORDER BY appointment_id DESC
        LIMIT 5
    """)

    appointments = cursor.fetchall()

    connection.close()

    return appointments

def get_disease_statistics():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT predicted_disease, COUNT(*)
        FROM ai_predictions
        WHERE prediction_id IN (
            SELECT MAX(prediction_id)
            FROM ai_predictions
            GROUP BY patient_id
        )
        GROUP BY predicted_disease
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def get_revenue_data():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT billing_date,
               SUM(total_amount)
        FROM billing
        GROUP BY billing_date
        ORDER BY billing_date
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def add_lab_report(
    patient_id,
    test_name,
    test_result,
    technician_name,
    report_date,
    status
):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO lab_reports
        (
            patient_id,
            test_name,
            test_result,
            technician_name,
            report_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        test_name,
        test_result,
        technician_name,
        report_date,
        status
    ))

    connection.commit()
    connection.close()   

def generate_prescription_pdf(
    patient_id,
    doctor_name,
    visit_date,
    diagnosis,
    prescription,
    doctor_notes
):
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Get Patient Information
    cursor.execute("""
        SELECT patient_name, age, gender, residence, email
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    # Get Latest AI Prediction
    cursor.execute("""
        SELECT predicted_disease, confidence, risk_level
        FROM ai_predictions
        WHERE patient_id = ?
        ORDER BY prediction_id DESC
        LIMIT 1
    """, (patient_id,))

    prediction = cursor.fetchone()

    connection.close()

    if patient is None:
        return None
def get_pending_lab_requests():

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        p.patient_id,
        p.patient_name,
        p.age,
        p.gender,
        d.doctor_name,
        d.diagnosis,
        d.required_tests
    FROM patients p
    JOIN doctor_records d
        ON p.patient_id = d.patient_id
    WHERE d.consultation_status = 'Pending'
    ORDER BY d.record_id DESC
    """)

    requests = cursor.fetchall()

    connection.close()

    return requests    
def get_latest_doctor_record(patient_id):

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM doctor_records
        WHERE patient_id = ?
        ORDER BY record_id DESC
        LIMIT 1
    """, (patient_id,))

    record = cursor.fetchone()

    connection.close()

    return record
