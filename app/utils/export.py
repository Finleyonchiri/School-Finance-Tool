import csv
import io
import json
from app.db import Receipt


def generate_csv(receipts: list[Receipt]) -> str:
    """Generate CSV string from a list of receipts."""
    if not receipts:
        return ""
    output = io.StringIO()
    writer = csv.writer(output)
    headers = [
        "Reference ID",
        "Date",
        "Student Name",
        "Admission Number",
        "Class",
        "Amount",
        "Payment Method",
        "Payer Name",
        "Notes",
    ]
    writer.writerow(headers)
    for r in receipts:
        writer.writerow(
            [
                r.reference_id,
                r.date,
                r.student_name,
                r.admission_number,
                r.class_grade,
                r.amount,
                r.payment_method,
                r.payer_name,
                r.notes,
            ]
        )
    return output.getvalue()


def generate_json_backup(receipts: list[Receipt], settings: dict) -> str:
    """Generate JSON string for full data backup."""
    data = {
        "version": "1.0",
        "timestamp": "",
        "settings": settings,
        "receipts": [r.dict() for r in receipts],
    }
    return json.dumps(data, indent=2)