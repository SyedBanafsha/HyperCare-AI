from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def generate_prescription_pdf(
    filename,
    patient_id,
    patient_name,
    age,
    gender,
    doctor_name,
    diagnosis,
    prescription,
    doctor_notes,
    visit_date
):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        spaceAfter=4,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
    )

    story = []

    # Header
    story.append(
        Paragraph(
            "HyperCare AI Hospital",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Digital Healthcare Management System",
            subtitle_style
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            spaceAfter=10
        )
    )

    # Patient and doctor information
    info_data = [
        [
            Paragraph("<b>Prescription ID</b>", small_style),
            Paragraph(f"HC-{patient_id:04d}", small_style),
            Paragraph("<b>Patient ID</b>", small_style),
            Paragraph(str(patient_id), small_style)
        ],
        [
            Paragraph("<b>Patient Name</b>", small_style),
            Paragraph(str(patient_name), small_style),
            Paragraph("<b>Age</b>", small_style),
            Paragraph(str(age), small_style)
        ],
        [
            Paragraph("<b>Gender</b>", small_style),
            Paragraph(str(gender), small_style),
            Paragraph("<b>Doctor</b>", small_style),
            Paragraph(str(doctor_name), small_style)
        ],
        [
            Paragraph("<b>Visit Date</b>", small_style),
            Paragraph(str(visit_date), small_style),
            Paragraph("", small_style),
            Paragraph("", small_style)
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            30 * mm,
            60 * mm,
            28 * mm,
            52 * mm
        ]
    )

    info_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
        ])
    )

    story.append(info_table)

    # Diagnosis
    story.append(
        Paragraph(
            "Diagnosis",
            section_style
        )
    )

    story.append(
        Paragraph(
            str(diagnosis).replace("\n", "<br/>"),
            body_style
        )
    )

    # Prescription
    story.append(
        Paragraph(
            "Prescription",
            section_style
        )
    )

    for line in str(prescription).split("\n"):

        if line.strip():

            story.append(
                Paragraph(
                    f"• {line}",
                    body_style
                )
            )

    # Doctor Notes
    story.append(
        Paragraph(
            "Doctor Notes",
            section_style
        )
    )

    story.append(
        Paragraph(
            str(doctor_notes).replace("\n", "<br/>"),
            body_style
        )
    )

    # Doctor Signature
    story.append(
        Spacer(
            1,
            18 * mm
        )
    )

    signature_data = [
        ["", "____________________________"],
        ["", "Doctor Signature"],
        ["", str(doctor_name)],
    ]

    signature_table = Table(
        signature_data,
        colWidths=[
            105 * mm,
            65 * mm
        ]
    )

    signature_table.setStyle(
        TableStyle([
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("FONTNAME", (1, 1), (1, 1), "Helvetica-Oblique"),
            ("FONTSIZE", (1, 1), (1, 2), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ])
    )

    story.append(signature_table)

    story.append(
        Spacer(
            1,
            10 * mm
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            spaceAfter=8
        )
    )

    # Disclaimer
    story.append(
        Paragraph(
            "This prescription was generated electronically by HyperCare AI.<br/>"
            "AI-assisted screening is for clinical decision support only. "
            "Final diagnosis and treatment decisions remain with the doctor.",
            footer_style,
        )
    )

    doc.build(story)