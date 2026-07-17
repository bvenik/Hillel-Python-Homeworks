from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.utils import timezone
from ninja.errors import HttpError
from ..models import Student, Course, Enrollment, ExamResult
from ..schemas import (
    StudentIn, StudentOut, CourseIn, CourseOut,
    EnrollmentOut, ExamResultIn, ExamResultOut, CourseAverageOut
)
from ..auth import bearer_auth

router = Router()


@router.get("/students", response=List[StudentOut], auth=bearer_auth)
def list_students(request):
    """
    Retrieves the list of all registered students.
    :param request: standard Django HTTP request object
    :return: list of Student instances
    """
    return Student.objects.all()


@router.get("/students/{student_id}", response=StudentOut, auth=bearer_auth)
def get_student(request, student_id: int):
    """
    Retrieves a single student's details by their ID.
    :param request: standard Django HTTP request object
    :param student_id: unique integer identifier of the student
    :return: Student instance or raises 404 Not Found
    """
    return get_object_or_404(Student, id=student_id)


@router.post("/students", response={201: StudentOut}, auth=bearer_auth)
def create_student(request, data: StudentIn):
    """
    Registers a new student.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing student name and email
    :return: tuple of HTTP status code 201 and the created Student instance
    """
    student = Student.objects.create(**data.dict())
    return 201, student


@router.put("/students/{student_id}", response=StudentOut, auth=bearer_auth)
def update_student(request, student_id: int, data: StudentIn):
    """
    Updates details of an existing student.
    :param request: standard Django HTTP request object
    :param student_id: unique integer identifier of the student to update
    :param data: Pydantic schema containing updated student details
    :return: updated Student instance
    """
    student = get_object_or_404(Student, id=student_id)
    for attr, value in data.dict().items():
        setattr(student, attr, value)
    student.save()
    return student


@router.delete("/students/{student_id}", response={204: None}, auth=bearer_auth)
def delete_student(request, student_id: int):
    """
    Deletes a student registration from the system.
    :param request: standard Django HTTP request object
    :param student_id: unique integer identifier of the student to delete
    :return: tuple of HTTP status code 204 and None
    """
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return 204, None


@router.get("/courses", response=List[CourseOut], auth=bearer_auth)
def list_courses(request):
    """
    Retrieves the list of all registered courses.
    :param request: standard Django HTTP request object
    :return: list of Course instances
    """
    return Course.objects.all()


@router.get("/courses/{course_id}", response=CourseOut, auth=bearer_auth)
def get_course(request, course_id: int):
    """
    Retrieves details for a single course by its ID.
    :param request: standard Django HTTP request object
    :param course_id: unique integer identifier of the course
    :return: Course instance or raises 404 Not Found
    """
    return get_object_or_404(Course, id=course_id)


@router.post("/courses", response={201: CourseOut}, auth=bearer_auth)
def create_course(request, data: CourseIn):
    """
    Creates a new course entry in the database.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing course name and description
    :return: tuple of HTTP status code 201 and the created Course instance
    """
    course = Course.objects.create(**data.dict())
    return 201, course


@router.put("/courses/{course_id}", response=CourseOut, auth=bearer_auth)
def update_course(request, course_id: int, data: CourseIn):
    """
    Updates details of an existing course.
    :param request: standard Django HTTP request object
    :param course_id: unique integer identifier of the course to update
    :param data: Pydantic schema containing updated course details
    :return: updated Course instance
    """
    course = get_object_or_404(Course, id=course_id)
    for attr, value in data.dict().items():
        setattr(course, attr, value)
    course.save()
    return course


@router.delete("/courses/{course_id}", response={204: None}, auth=bearer_auth)
def delete_course(request, course_id: int):
    """
    Deletes a course entry from the database.
    :param request: standard Django HTTP request object
    :param course_id: unique integer identifier of the course to delete
    :return: tuple of HTTP status code 204 and None
    """
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None


@router.post("/courses/{course_id}/enroll", response={201: EnrollmentOut}, auth=bearer_auth)
def enroll_student(request, course_id: int, student_id: int):
    """
    Enrolls a student into a specific course.
    :param request: standard Django HTTP request object
    :param course_id: unique integer identifier of the course
    :param student_id: unique integer identifier of the student
    :return: tuple of HTTP status code 201 and the Enrollment instance
    """
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=student,
        course=course
    )
    return 201, enrollment


@router.get("/courses/{course_id}/enrollments", response=List[EnrollmentOut], auth=bearer_auth)
def list_course_enrollments(request, course_id: int):
    """
    Retrieves all student enrollments associated with a specific course.
    :param request: standard Django HTTP request object
    :param course_id: unique integer identifier of the course
    :return: list of Enrollment instances with prefetched student and course info
    """
    course = get_object_or_404(Course, id=course_id)
    return Enrollment.objects.filter(course=course).select_related('student', 'course')


@router.post("/grades", response={201: ExamResultOut}, auth=bearer_auth)
def record_grade(request, data: ExamResultIn):
    """
    Records an exam grade for a student in a specific course. The student must be enrolled in the course.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing student ID, course ID, grade, and optional exam date
    :return: tuple of HTTP status code 201 and formatted ExamResult details
    """
    student = get_object_or_404(Student, id=data.student_id)
    course = get_object_or_404(Course, id=data.course_id)

    if not Enrollment.objects.filter(student=student, course=course).exists():
        raise HttpError(
            400, "Student must be enrolled in the course before recording a grade.")

    exam_date = data.exam_date or timezone.now().date()
    exam_result = ExamResult.objects.create(
        student=student,
        course=course,
        grade=data.grade,
        exam_date=exam_date
    )

    return 201, {
        "id": exam_result.id,
        "student_name": f"{student.first_name} {student.last_name}",
        "course_name": course.name,
        "grade": exam_result.grade,
        "exam_date": exam_result.exam_date
    }


@router.get("/courses/{course_id}/average-grade", response=CourseAverageOut, auth=bearer_auth)
def get_course_average_grade(request, course_id: int):
    """
    Calculates and returns the average exam grade for all students graded in a specific course.
    :param request: standard Django HTTP request object
    :param course_id: unique integer identifier of the course
    :return: dictionary containing course name and calculated average grade
    """
    course = get_object_or_404(Course, id=course_id)
    average = ExamResult.objects.filter(course=course).aggregate(
        avg_grade=Avg('grade'))['avg_grade']
    return {
        "course_name": course.name,
        "average_grade": round(average, 2) if average is not None else None
    }
