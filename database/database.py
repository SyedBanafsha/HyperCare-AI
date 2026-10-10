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
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    residence TEXT,
    purpose_of_visit TEXT,
    current_symptoms TEXT
)
""")
connection.commit()

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

    try:
        # Check whether this exact prediction is already saved
        cursor.execute("""
            SELECT prediction_id
            FROM ai_predictions
            WHERE patient_id = ?
              AND predicted_disease = ?
              AND confidence = ?
              AND risk_level = ?
              AND recommendation = ?
              AND prediction_date = ?
            LIMIT 1
        """, (
            patient_id,
            predicted_disease,
            confidence,
            risk_level,
            recommendation,
            prediction_date
        ))

        if cursor.fetchone():
            return False

        cursor.execute("""
            INSERT INTO ai_predictions (
                patient_id,
                predicted_disease,
                confidence,
                risk_level,
                recommendation,
                prediction_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            predicted_disease,
            confidence,
            risk_level,
            recommendation,
            prediction_date
        ))

        connection.commit()
        return True

    finally:
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

def get_appointments():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT appointment_id, patient_id, doctor_name,
               appointment_date, appointment_time, status
        FROM appointments
        ORDER BY appointment_date, appointment_time
    """)

    appointments = cursor.fetchall()
    connection.close()

    return appointments

def update_appointment_status(appointment_id, status):
    if status not in ("Confirmed", "Rejected"):
        raise ValueError("Invalid appointment status")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE appointments SET status = ? WHERE appointment_id = ?",
        (status, appointment_id)
    )

    connection.commit()
    connection.close()


def create_public_appointments_table():
    connection = sqlite3.connect("hospital.db", timeout=10)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public_appointment_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                doctor_name TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT,
                status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS unique_active_public_appointment
            ON public_appointment_requests (
                phone,
                doctor_name,
                appointment_date,
                appointment_time
            )
            WHERE status IN ('Pending', 'Confirmed')
        """)

        connection.commit()

    finally:
        connection.close()





def add_public_appointment(
    patient_name,
    phone,
    email,
    doctor_name,
    appointment_date,
    appointment_time,
    reason
):
    connection = sqlite3.connect("hospital.db", timeout=10)
    connection.execute("PRAGMA busy_timeout = 10000")
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")
        # Prevent duplicate active requests for the same slot
        cursor.execute("""
            SELECT request_id
            FROM public_appointment_requests
            WHERE phone = ?
              AND doctor_name = ?
              AND appointment_date = ?
              AND appointment_time = ?
              AND status IN ('Pending', 'Confirmed')
            LIMIT 1
        """, (
            phone,
            doctor_name,
            appointment_date,
            appointment_time
        ))

        existing = cursor.fetchone()

        if existing:
            raise ValueError(
                f"You already have an active request for this slot. "
                f"Reference number: {existing[0]}"
            )

        cursor.execute("""
            INSERT INTO public_appointment_requests
            (patient_name, phone, email, doctor_name,
             appointment_date, appointment_time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
        """, (
            patient_name,
            phone,
            email,
            doctor_name,
            appointment_date,
            appointment_time,
            reason
        ))

        request_id = cursor.lastrowid
        connection.commit()
        return request_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()



create_public_appointments_table()

def get_public_appointment_requests():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT request_id, patient_name, phone, email,
               doctor_name, appointment_date, appointment_time,
               reason, status
        FROM public_appointment_requests
        ORDER BY request_id DESC
    """)

    requests = cursor.fetchall()
    connection.close()

    return requests


def update_public_appointment_status(request_id, status):
    if status not in ("Confirmed", "Rejected"):
        raise ValueError("Invalid appointment status")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE public_appointment_requests
        SET status = ?
        WHERE request_id = ?
    """, (status, request_id))

    connection.commit()
    connection.close()

def confirm_public_request_with_patient(request_id):
    import sqlite3

    connection = sqlite3.connect("hospital.db", timeout=10)

    try:
        connection.execute("PRAGMA busy_timeout = 10000")
        cursor = connection.cursor()
        cursor.execute("BEGIN IMMEDIATE")

        # 1. Fetch the online request.
        cursor.execute("""
            SELECT patient_name, phone, doctor_name,
                   appointment_date, appointment_time, status
            FROM public_appointment_requests
            WHERE request_id = ?
        """, (request_id,))

        request = cursor.fetchone()

        if request is None:
            raise ValueError("Appointment request was not found.")

        (
            patient_name,
            phone,
            doctor_name,
            appointment_date,
            appointment_time,
            status,
        ) = request

        if status == "Confirmed":
            raise ValueError("This request has already been confirmed.")

        if status != "Pending":
            raise ValueError("Only pending requests can be confirmed.")

        # 2. Find the registered patient by mobile number.
        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE phone_number = ?
            ORDER BY patient_id DESC
            LIMIT 1
        """, (phone,))

        patient = cursor.fetchone()

        if patient is None:
            raise ValueError(
                "Patient not registered. Please register this patient "
                "using the Patient Registration page first. Then retry "
                "confirmation. The online Request ID is not a Patient ID."
            )

        patient_id = patient[0]

        # 3. Check for an existing active appointment at this slot.
        cursor.execute("""
            SELECT appointment_id
            FROM appointments
            WHERE patient_id = ?
              AND doctor_name = ?
              AND appointment_date = ?
              AND appointment_time = ?
              AND status IN ('Pending', 'Confirmed')
            LIMIT 1
        """, (
            patient_id,
            doctor_name,
            appointment_date,
            appointment_time,
        ))

        existing_appointment = cursor.fetchone()

        if existing_appointment:
            appointment_id = existing_appointment[0]
        else:
            # 4. Create the appointment if one doesn't already exist.
            cursor.execute("""
                INSERT INTO appointments (
                    patient_id,
                    doctor_name,
                    appointment_date,
                    appointment_time,
                    status
                )
                VALUES (?, ?, ?, ?, 'Confirmed')
            """, (
                patient_id,
                doctor_name,
                appointment_date,
                appointment_time,
            ))

            appointment_id = cursor.lastrowid

        # 5. Confirm the request in the same transaction.
        cursor.execute("""
            UPDATE public_appointment_requests
            SET status = 'Confirmed'
            WHERE request_id = ? AND status = 'Pending'
        """, (request_id,))

        if cursor.rowcount != 1:
            raise ValueError(
                "The request status changed. Refresh and try again."
            )

        connection.commit()
        return patient_id, appointment_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def get_patient_by_phone(phone):
    import sqlite3

    connection = sqlite3.connect("hospital.db")
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT patient_id, patient_name, phone_number, email,
                   age, gender, residence
            FROM patients
            WHERE phone_number = ?
            ORDER BY patient_id DESC
            LIMIT 1
        """, (phone.strip(),))
        return cursor.fetchone()
    finally:
        connection.close()


def register_and_confirm_public_request(
    request_id, age=None, gender=None, residence=None
):
    import sqlite3

    connection = sqlite3.connect("hospital.db", timeout=10)

    try:
        connection.execute("PRAGMA busy_timeout = 10000")
        cursor = connection.cursor()
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute("""
            SELECT patient_name, phone, email, doctor_name,
                   appointment_date, appointment_time, reason, status
            FROM public_appointment_requests
            WHERE request_id = ?
        """, (request_id,))
        request = cursor.fetchone()

        if request is None:
            raise ValueError("Appointment request not found.")

        name, phone, email, doctor, appt_date, appt_time, reason, status = request

        if status == "Confirmed":
            raise ValueError("This request is already confirmed.")
        if status != "Pending":
            raise ValueError("Only pending requests can be confirmed.")

        # Reuse a registered patient with this mobile number.
        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE phone_number = ?
            ORDER BY patient_id DESC
            LIMIT 1
        """, (phone.strip(),))
        patient = cursor.fetchone()

        if patient:
            patient_id = patient[0]
        else:
            if age is None or age < 0 or not gender or not residence or not residence.strip():
                raise ValueError(
                    "Please enter the new patient's age, gender and residence."
                )

            # Don't silently associate a different patient's email.
            if email and email.strip():
                cursor.execute("""
                    SELECT patient_id FROM patients
                    WHERE email = ?
                    LIMIT 1
                """, (email.strip(),))
                email_match = cursor.fetchone()
                if email_match:
                    raise ValueError(
                        "This email already belongs to a registered patient. "
                        "Please check the patient's details before continuing."
                    )

            cursor.execute("""
                INSERT INTO patients (
                    patient_name, phone_number, email, age, gender,
                    residence, purpose_of_visit, current_symptoms
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name.strip(),
                phone.strip(),
                (email or "").strip(),
                int(age),
                gender,
                residence.strip(),
                (reason or "Online appointment request").strip(),
                (reason or "").strip(),
            ))
            patient_id = cursor.lastrowid

        # Prevent booking a doctor who already has an active appointment
        # at the requested date and time.
        cursor.execute("""
            SELECT appointment_id
            FROM appointments
            WHERE doctor_name = ?
              AND appointment_date = ?
              AND appointment_time = ?
              AND status IN ('Pending', 'Confirmed')
            LIMIT 1
        """, (doctor, appt_date, appt_time))

        conflict = cursor.fetchone()
        if conflict:
            raise ValueError(
                "This doctor already has an active appointment at that time. "
                "Please contact the patient to arrange another slot."
            )

        cursor.execute("""
            INSERT INTO appointments (
                patient_id, doctor_name, appointment_date,
                appointment_time, status
            )
            VALUES (?, ?, ?, ?, 'Confirmed')
        """, (patient_id, doctor, appt_date, appt_time))

        appointment_id = cursor.lastrowid

        cursor.execute("""
            UPDATE public_appointment_requests
            SET status = 'Confirmed'
            WHERE request_id = ? AND status = 'Pending'
        """, (request_id,))

        if cursor.rowcount != 1:
            raise ValueError("Request status changed. Refresh and try again.")

        connection.commit()
        return patient_id, appointment_id

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# ============================================================
# PUBLIC APPOINTMENT WORKFLOW
# Add this section at the VERY BOTTOM of database/database.py
# ============================================================

import sqlite3


def _get_public_appointment_connection():
    """Open the existing hospital database and ensure the link column exists."""
    conn = sqlite3.connect("hospital.db", timeout=10)
    conn.execute("PRAGMA busy_timeout = 10000")

    # Keep a link from a public request to its hospital appointment.
    columns = {
        row[1]
        for row in conn.execute(
            "PRAGMA table_info(public_appointment_requests)"
        ).fetchall()
    }

    if not columns:
        conn.close()
        raise RuntimeError(
            "The public_appointment_requests table does not exist. "
            "Run your existing database initialization first."
        )

    if "appointment_id" not in columns:
        conn.execute(
            """
            ALTER TABLE public_appointment_requests
            ADD COLUMN appointment_id INTEGER
            """
        )
        conn.commit()

    return conn


def check_public_request_availability(request_id):
    """
    Return (available, message) for a public appointment request.
    Does not accept or confirm the request.
    """
    conn = _get_public_appointment_connection()

    try:
        request = conn.execute(
            """
            SELECT doctor_name, appointment_date, appointment_time, status
            FROM public_appointment_requests
            WHERE request_id = ?
            """,
            (request_id,),
        ).fetchone()

        if not request:
            return False, "Appointment request not found."

        doctor, date, time, status = request

        if status != "Pending":
            return False, f"This request is already {status.lower()}."

        # Check existing hospital appointments.
        existing = conn.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE LOWER(TRIM(doctor_name)) = LOWER(TRIM(?))
              AND TRIM(appointment_date) = TRIM(?)
              AND TRIM(appointment_time) = TRIM(?)
              AND LOWER(TRIM(COALESCE(status, ''))) IN
                  ('pending', 'confirmed', 'accepted', 'booked')
            LIMIT 1
            """,
            (doctor, date, time),
        ).fetchone()

        if existing:
            return False, "This doctor already has an active appointment at that time."

        # Also check other public requests already confirmed.
        other_request = conn.execute(
            """
            SELECT request_id
            FROM public_appointment_requests
            WHERE request_id != ?
              AND LOWER(TRIM(doctor_name)) = LOWER(TRIM(?))
              AND TRIM(appointment_date) = TRIM(?)
              AND TRIM(appointment_time) = TRIM(?)
              AND LOWER(TRIM(COALESCE(status, ''))) = 'confirmed'
            LIMIT 1
            """,
            (request_id, doctor, date, time),
        ).fetchone()

        if other_request:
            return False, "This time slot is already reserved."

        return True, "The requested doctor and time slot are available."

    finally:
        conn.close()


def confirm_public_request(request_id):
    """
    Accept a pending public request without requiring patient registration.
    Creates a hospital appointment with patient_id = NULL.
    Returns the new or existing appointment_id.
    """
    conn = _get_public_appointment_connection()

    try:
        conn.execute("BEGIN IMMEDIATE")

        request = conn.execute(
            """
            SELECT patient_name, phone, email, doctor_name,
                   appointment_date, appointment_time, status,
                   appointment_id
            FROM public_appointment_requests
            WHERE request_id = ?
            """,
            (request_id,),
        ).fetchone()

        if not request:
            raise ValueError("Appointment request not found.")

        (
            patient_name,
            phone,
            email,
            doctor,
            date,
            time,
            status,
            linked_appointment_id,
        ) = request

        if status == "Confirmed" and linked_appointment_id:
            conn.commit()
            return linked_appointment_id

        if status != "Pending":
            raise ValueError(
                f"This request cannot be accepted because its status is {status}."
            )

        # Recheck availability inside the transaction to reduce race conditions.
        existing = conn.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE LOWER(TRIM(doctor_name)) = LOWER(TRIM(?))
              AND TRIM(appointment_date) = TRIM(?)
              AND TRIM(appointment_time) = TRIM(?)
              AND LOWER(TRIM(COALESCE(status, ''))) IN
                  ('pending', 'confirmed', 'accepted', 'booked')
            LIMIT 1
            """,
            (doctor, date, time),
        ).fetchone()

        if existing:
            raise ValueError(
                "This doctor and time slot already has an active appointment."
            )

        # A confirmed public request for the same slot must also block booking.
        other_request = conn.execute(
            """
            SELECT request_id
            FROM public_appointment_requests
            WHERE request_id != ?
              AND LOWER(TRIM(doctor_name)) = LOWER(TRIM(?))
              AND TRIM(appointment_date) = TRIM(?)
              AND TRIM(appointment_time) = TRIM(?)
              AND LOWER(TRIM(COALESCE(status, ''))) = 'confirmed'
            LIMIT 1
            """,
            (request_id, doctor, date, time),
        ).fetchone()

        if other_request:
            raise ValueError("This time slot is already reserved.")

        # Patient is not registered yet, so patient_id is NULL.
        cursor = conn.execute(
            """
            INSERT INTO appointments
                (patient_id, doctor_name, appointment_date,
                 appointment_time, status)
            VALUES (NULL, ?, ?, ?, 'Confirmed')
            """,
            (doctor, date, time),
        )

        appointment_id = cursor.lastrowid

        conn.execute(
            """
            UPDATE public_appointment_requests
            SET status = 'Confirmed', appointment_id = ?
            WHERE request_id = ?
            """,
            (appointment_id, request_id),
        )

        conn.commit()
        return appointment_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def link_confirmed_requests_to_patient(phone, patient_id):
    """
    Link confirmed public appointments to a patient after reception
    registers them. Call this after add_patient() succeeds.
    Returns the number of appointments linked.
    """
    conn = _get_public_appointment_connection()

    try:
        conn.execute("BEGIN IMMEDIATE")

        rows = conn.execute(
            """
            SELECT appointment_id
            FROM public_appointment_requests
            WHERE TRIM(phone) = TRIM(?)
              AND status = 'Confirmed'
              AND appointment_id IS NOT NULL
            """,
            (str(phone),),
        ).fetchall()

        linked = 0

        for (appointment_id,) in rows:
            cursor = conn.execute(
                """
                UPDATE appointments
                SET patient_id = ?
                WHERE appointment_id = ?
                  AND patient_id IS NULL
                """,
                (patient_id, appointment_id),
            )
            linked += cursor.rowcount

        conn.commit()
        return linked

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
