from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal


class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    token: str
    username: str


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = ""
    is_completed: Optional[bool] = False
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductIn(BaseModel):
    name: str
    description: Optional[str] = ""
    price: Decimal
    stock: int


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock: int

    class Config:
        from_attributes = True


class CartItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: Decimal

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class GenreIn(BaseModel):
    name: str


class GenreOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieIn(BaseModel):
    title: str
    description: Optional[str] = ""
    release_date: date
    genre_ids: List[int]


class MovieOut(BaseModel):
    id: int
    title: str
    description: str
    release_date: date
    genres: List[GenreOut]

    class Config:
        from_attributes = True


class ReviewIn(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = ""


class ReviewOut(BaseModel):
    id: int
    movie_id: int
    username: str
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True


class TagIn(BaseModel):
    name: str


class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PostIn(BaseModel):
    title: str
    content: str
    tag_ids: Optional[List[int]] = []


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_username: str
    created_at: datetime
    tags: List[TagOut]

    class Config:
        from_attributes = True


class CommentIn(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    post_id: int
    author_username: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ServerIn(BaseModel):
    name: str
    ip_address: str
    is_online: Optional[bool] = True


class ServerOut(BaseModel):
    id: int
    name: str
    ip_address: str
    is_online: bool

    class Config:
        from_attributes = True


class MetricLogIn(BaseModel):
    cpu_load: float = Field(ge=0.0, le=100.0)
    memory_usage: float = Field(ge=0.0, le=100.0)
    disk_usage: float = Field(ge=0.0, le=100.0)


class MetricLogOut(BaseModel):
    id: int
    server_id: int
    cpu_load: float
    memory_usage: float
    disk_usage: float
    recorded_at: datetime

    class Config:
        from_attributes = True


class NotificationOut(BaseModel):
    id: int
    server_id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BookIn(BaseModel):
    title: str
    author: str
    genre: str
    is_available: Optional[bool] = True


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    is_available: bool

    class Config:
        from_attributes = True


class RentalIn(BaseModel):
    book_id: int
    duration_days: int = Field(gt=0, default=14)


class RentalOut(BaseModel):
    id: int
    username: str
    book: BookOut
    rented_at: datetime
    return_due: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class StudentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class CourseIn(BaseModel):
    name: str
    description: Optional[str] = ""


class CourseOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class EnrollmentOut(BaseModel):
    id: int
    student: StudentOut
    course: CourseOut
    enrolled_at: date

    class Config:
        from_attributes = True


class ExamResultIn(BaseModel):
    student_id: int
    course_id: int
    grade: float
    exam_date: Optional[date] = None


class ExamResultOut(BaseModel):
    id: int
    student_name: str
    course_name: str
    grade: float
    exam_date: date

    class Config:
        from_attributes = True


class CourseAverageOut(BaseModel):
    course_name: str
    average_grade: Optional[float] = None
