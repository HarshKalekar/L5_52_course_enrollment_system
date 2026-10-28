"""Manage course enrollment, tuition, and roster exports."""

import hashlib
import secrets
from pathlib import Path

COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}
ENROLLMENT_STATE = {"total_tuition": 0.0}


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Enroll a student if the course has available seats."""

    course = COURSES.get(course_id)
    if (
        course is None
        or course["is_closed"]
        or course["seats"] <= 0
        or not student_name.strip()
        or credits_registered <= 0
    ):
        return False

    if audit_trail is None:
        audit_trail = []

    course["seats"] -= 1
    if course["seats"] == 0:
        course["is_closed"] = True

    ENROLLMENT_STATE["total_tuition"] += course["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Restore a seat for an existing course."""
    course = COURSES.get(course_id)
    if course is None:
        return False

    course["seats"] += 1
    course["is_closed"] = False
    return True


def check_course_status(course_id):
    """Check whether a course is open for enrollment."""
    course = COURSES.get(course_id)
    return course is not None and not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Calculate tuition after a discount rate between zero and one."""
    course = COURSES.get(course_id)
    if course is None:
        raise ValueError(f"Unknown course ID: {course_id}")
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0 and 1.")

    return course["fee"] * (1.0 - discount_rate)


def generate_student_hash(roll_no):
    """Generate a SHA-256 digest for a roll number."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a cryptographically secure four-digit OTP."""
    return str(secrets.randbelow(9000) + 1000)


def export_course_roster(filename="course_roster.txt"):
    """Export the current course roster to a UTF-8 text file."""
    output_path = Path(filename)
    output_path.write_text(str(COURSES), encoding="utf-8")
    print(f"Course roster exported to: {output_path}")


def get_open_courses_summary(course_catalog):
    """Count courses that are open for enrollment."""
    return sum(
        not details["is_closed"]
        for details in course_catalog.values()
    )


def main():
    """Demonstrate course enrollment operations."""
    audit_trail = []

    enroll_student("CS101", "Kritika", 4, audit_trail)
    drop_course("CS202")

    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", 0.25),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())

    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    print("Audit trail:", audit_trail)
    print(
        "Total tuition collected:",
        ENROLLMENT_STATE["total_tuition"],
    )


if __name__ == "__main__":
    main()
