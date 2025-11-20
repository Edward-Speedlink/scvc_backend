from ..models.certificate import Certificate
from ..models.verification_log import VerificationLog

def dashboard_summary():
    total_certs = Certificate.query.count()
    total_valid = VerificationLog.query.filter_by(status="VALID").count()
    total_invalid = VerificationLog.query.filter_by(status="INVALID").count()

    latest_logs = VerificationLog.query.order_by(
        VerificationLog.verified_at.desc()
    ).limit(10).all()

    logs_data = [
        {
            "date": log.verified_at,
            "status": log.status,
            "ip": log.ip_address,
            "certificate_code": log.certificate.verification_code if log.certificate else None
        }
        for log in latest_logs
    ]

    return {
        "total_certificates": total_certs,
        "total_valid_verifications": total_valid,
        "total_invalid_attempts": total_invalid,
        "recent_verifications": logs_data
    }
