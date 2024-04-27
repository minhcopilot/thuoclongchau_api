from fastapi import FastAPI
from app.routes import user_routes
from app.routes import auth_routes
from app.config.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware
app=FastAPI()
app.include_router(user_routes.router)
app.include_router(user_routes.user_router)
app.include_router(auth_routes.auth_router)
app.include_router(auth_routes.router)

# add Middleware
app.add_middleware(AuthenticationMiddleware,backend=JWTAuth())

@app.get("/")
def index():
    return {"title": "Hello app is running :)"}