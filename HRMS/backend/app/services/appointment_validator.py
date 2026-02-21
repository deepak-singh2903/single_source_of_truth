from datetime import datetime


DATE_FORMAT = "%d-%b-%Y"  # 26-Jan-2026


class AppointmentValidationError(Exception):
    pass


def parse_date(date_str: str, field_name: str):
    try:
        return datetime.strptime(date_str, DATE_FORMAT).date()
    except Exception:
        raise AppointmentValidationError(
            f"Invalid date format for {field_name}. Expected DD-MMM-YYYY (e.g. 26-Jan-2026)"
        )


def validate_appointment_payload(payload: dict):
    required_blocks = [
        "employment_details",
        "salary_details",
        "payroll_config",
        "statutory_details",
        "payroll_flags",
        "dates"
    ]

    for block in required_blocks:
        if block not in payload:
            raise AppointmentValidationError(f"Missing block: {block}")

    # ---- Dates ----
    dates = payload["dates"]

    dob = parse_date(dates.get("date_of_birth"), "date_of_birth")
    doj = parse_date(dates.get("date_of_joining"), "date_of_joining")
    effective = parse_date(dates.get("appointment_effective_from"), "appointment_effective_from")

    if effective < doj:
        raise AppointmentValidationError(
            "appointment_effective_from cannot be earlier than date_of_joining"
        )

    # ---- Statutory rules ----
    statutory = payload["statutory_details"]

    if statutory.get("is_pf_applicable") and not statutory.get("pf_number"):
        raise AppointmentValidationError("PF number required when PF is applicable")

    if statutory.get("is_esi_applicable") and not statutory.get("esi_number"):
        raise AppointmentValidationError("ESI number required when ESI is applicable")

    # ---- Payroll flags vs statutory ----
    payroll_flags = payload["payroll_flags"]

    if not statutory.get("is_pf_applicable") and payroll_flags.get("is_pf_deduction_applicable"):
        raise AppointmentValidationError(
            "PF deduction cannot be enabled if PF is not applicable"
        )

    if not statutory.get("is_esi_applicable") and payroll_flags.get("is_esi_deduction_applicable"):
        raise AppointmentValidationError(
            "ESI deduction cannot be enabled if ESI is not applicable"
        )

    # ---- Salary ----
    salary = payload["salary_details"]

    if salary.get("basic_amount") is None:
        raise AppointmentValidationError("basic_amount is mandatory")

    if salary.get("ctc_amount") is None:
        raise AppointmentValidationError("ctc_amount is mandatory")

    # ---- Payroll config ----
    payroll_config = payload["payroll_config"]
    allowed_commissions = {"6CPC", "7CPC", "8CPC"}

    if payroll_config.get("pay_commission") not in allowed_commissions:
        raise AppointmentValidationError(
            "pay_commission must be one of: 6CPC, 7CPC, 8CPC"
        )

    return {
        "date_of_birth": dob,
        "date_of_joining": doj,
        "appointment_effective_from": effective
    }
