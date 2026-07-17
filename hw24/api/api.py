from ninja import NinjaAPI
from .endpoints.auth import router as auth_router
from .endpoints.tasks import router as tasks_router
from .endpoints.ecommerce import router as ecommerce_router
from .endpoints.movies import router as movies_router
from .endpoints.blog import router as blog_router
from .endpoints.servers import router as servers_router
from .endpoints.books import router as books_router
from .endpoints.students import router as students_router

api = NinjaAPI(
    title="Hillel Python Homework 24 REST API",
    version="1.0.0",
    description="Unified API endpoints for Hillel Python Homework 24 containing all 7 sub-projects with Bearer Token authentication."
)

api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/tasks", tasks_router, tags=["1. Task Manager"])
api.add_router("/ecommerce", ecommerce_router, tags=["2. E-commerce"])
api.add_router("/movies", movies_router, tags=["3. Movie Collection"])
api.add_router("/blog", blog_router, tags=["4. Blog Platform"])
api.add_router("/servers", servers_router, tags=["5. Server Monitoring"])
api.add_router("/books", books_router, tags=["6. Book Library"])
api.add_router("/students", students_router,
               tags=["7. Student Course Management"])
