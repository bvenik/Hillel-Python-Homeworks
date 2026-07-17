from django.contrib import admin
from .models import (
    APIToken, Task, Product, CartItem, Order, OrderItem,
    Genre, Movie, Review, Tag, Post, Comment,
    Server, MetricLog, Notification, Book, Rental,
    Student, Course, Enrollment, ExamResult
)

# Auth Token admin


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__username', 'token')

# 1. Task Manager


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_completed', 'created_at', 'due_date')
    list_filter = ('is_completed', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'user__username')

# 2. E-commerce


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name', 'description')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

# 3. Movie Collection


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')
    list_filter = ('release_date',)
    search_fields = ('title', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'comment')

# 4. Blog Platform


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'author__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'author__username', 'content')

# 5. Server Monitoring


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'ip_address', 'is_online')
    list_filter = ('is_online',)
    search_fields = ('name', 'ip_address', 'user__username')


@admin.register(MetricLog)
class MetricLogAdmin(admin.ModelAdmin):
    list_display = ('server', 'cpu_load', 'memory_usage',
                    'disk_usage', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('server__name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('server', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('server__name', 'message')

# 6. Book Library


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'is_available')
    list_filter = ('is_available', 'genre')
    search_fields = ('title', 'author', 'genre')


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rented_at', 'return_due', 'returned_at')
    list_filter = ('rented_at', 'return_due', 'returned_at')
    search_fields = ('user__username', 'book__title')

# 7. Student Course Management


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('enrolled_at',)
    search_fields = ('student__first_name',
                     'student__last_name', 'course__name')


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'exam_date')
    list_filter = ('exam_date',)
    search_fields = ('student__first_name',
                     'student__last_name', 'course__name')
