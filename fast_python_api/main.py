from fastapi import FastAPI, Depends, Response
from starlette.responses import JSONResponse
from typing import Annotated
from fast_python_api.chemas.user_db import UserInDB
from fast_python_api.auth.user_auth import get_current_user
from fast_python_api.chemas.user_crud import UserPublic
from fast_python_api.settings import settings
from fast_python_api.services import routes as external_api
from fast_python_api.auth import routes as auth_routes
from fast_python_api.core import routes as users_router


app = FastAPI(
    title="Fast Python API",
    description="This API integrates external data sources, "
                "supports user management, and JWT authentication. "
                "For detailed documentation, visit /docs.",
    version=settings.APP_VERSION
)

app.include_router(external_api.router)
app.include_router(auth_routes.router)
app.include_router(users_router.router)


@app.get(
    '/',
    tags=["Root"],
    description="Get information about the service",
    responses={
        200: {"description": "Successful response"},
        500: {"description": "Internal server error"}
    }
)
async def homepage():
    """
    Returns a welcome message and API version.
    Returns:
        JSONResponse: A JSON response containing a welcome message,
        API version, and documentation link.
    Raises:
        HTTPException: 500 Internal Server Error if the service
        encounters an unexpected issue.
    Example:
        curl -X GET http://localhost:8000/
    """
    return JSONResponse({
        'message': 'Welcome to My FastAPI Service!',
        'version': settings.APP_VERSION,
        'documentation': '/docs'
    })


@app.head("/", include_in_schema=False)
async def homepage_head():
    return Response(status_code=200)


@app.get(
    "/me",
    tags=["Current User"],
    description="Get information about the current user",
    responses={
        200: {
            "description": "Successful retrieval of user information",
            "content": {
                "application/json": {
                    "example": {
                        "name": {
                            "title": "Mr",
                            "first_name": "John",
                            "last_name": "Doe"
                        },
                        "login": {
                            "username": "johndoe",
                            "role": "admin",
                            "uuid": "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a"
                        },
                        "dob": "1995-05-20",
                        "city": "New York",
                        "email": "testuser@example.com",
                        "created_at": "2025-02-04T21:00:00Z"
                    }
                }
            }
        },
        401: {"description": "Unauthorized, invalid or missing credentials"},
        500: {"description": "Internal server error"}
    }
)
async def read_users_me(
        current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserPublic:
    """
    Retrieve the current user's public information.

    Args:
        current_user (UserInDB): The currently authenticated user.

    Returns:
        UserPublic: The public representation of the current user.

    Raises:
        HTTPException: 401 Unauthorized if the user is not authenticated.
        HTTPException: 500 Internal Server Error if the
        service encounters an unexpected issue.

    Example:
        curl -X GET http://localhost:8000/me -H "Authorization: Bearer <token>"
    """
    return UserPublic(**current_user.model_dump())
