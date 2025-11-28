from ..models.certificate import Certificate
from ..extensions import db
from datetime import datetime


def generate_certificate_number(course_name, issuance_date=None):
    """
    Generate certificate number with course code from first letters of words
    and batch letter (A/B) based on issuance date.
    
    Examples:
    - "Software Engineering" -> "SE"
    - "Data Analytics" -> "DA"
    - Issued in June 2025 -> "25A/" (first half)
    - Issued in July 2025 -> "25B/" (second half)
    """
    
    def get_course_code(full_course_name):
        if not full_course_name:
            return "GN"  # General as fallback
        
        words = full_course_name.split()
        code = ''.join([word[0].upper() for word in words if word])
        
        if 2 <= len(code) <= 4:
            return code
        elif len(code) > 4:
            return code[:4]
        else:
            return full_course_name[:2].upper() if len(full_course_name) >= 2 else "GN"

    def get_batch_letter(date):
        """
        Determine batch letter based on date:
        - A: January to June (first half)
        - B: July to December (second half)
        """
        if date.month <= 6:
            return "A"  # First half of year
        else:
            return "B"  # Second half of year

    course_code = get_course_code(course_name)
    
    # Use provided issuance_date or current date
    if issuance_date:
        target_date = issuance_date
    else:
        target_date = datetime.utcnow()
    
    year = target_date.year % 100   # 2025 -> 25
    batch_letter = get_batch_letter(target_date)

    prefix = f"SHSL/{year}{batch_letter}/{course_code}"

    # Count how many certificates already exist for this course+year+batch
    existing_count = Certificate.query.filter(
        Certificate.verification_code.like(f"{prefix}/%")
    ).count()

    new_number = existing_count + 1
    formatted_number = str(new_number).zfill(4)

    return f"{prefix}/{formatted_number}"










# from ..models.certificate import Certificate
# from ..extensions import db
# from datetime import datetime


# def generate_certificate_number(course_name):
#     """
#     Generate certificate number with course code from first letters of words
#     Examples:
#     - "Software Engineering" -> "SE"
#     - "Data Analytics" -> "DA"
#     - "Frontend Development" -> "FD"
#     - "Cyber Security" -> "CS"
#     """
    
#     # Extract course code from course name (first letters of each word)
#     def get_course_code(full_course_name):
#         if not full_course_name:
#             return "GN"  # General as fallback
        
#         # Split by space and take first letter of each word, then uppercase
#         words = full_course_name.split()
#         code = ''.join([word[0].upper() for word in words if word])
        
#         # If we get a reasonable code (2-4 characters), use it
#         if 2 <= len(code) <= 4:
#             return code
#         elif len(code) > 4:
#             return code[:4]  # Truncate to 4 characters if too long
#         else:
#             # If only one word or empty, use first 2 letters
#             return full_course_name[:2].upper() if len(full_course_name) >= 2 else "GN"
        

#     course_code = get_course_code(course_name)
    
#     year = datetime.utcnow().year % 100   # 2025 -> 25
#     batch_letter = "B"   # You can automate this later

#     prefix = f"SHSL/{year}{batch_letter}/{course_code}"

#     # Count how many certificates already exist for this course+year+batch
#     existing_count = Certificate.query.filter(
#         Certificate.verification_code.like(f"{prefix}/%")
#     ).count()

#     new_number = existing_count + 1
#     formatted_number = str(new_number).zfill(4)  # 0001, 0002...

#     return f"{prefix}/{formatted_number}"
