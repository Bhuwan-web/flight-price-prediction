"""Registration router."""

from fastapi import APIRouter, Body, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from auth.models.user import User, UserAuth, UserOut
from auth.jwt import access_security, user_from_token
from auth.routes.mail import request_verification_email
from auth.util.mail import send_password_reset_email
from auth.util.password import hash_password

router = APIRouter(prefix="/register", tags=["Register"])

embed = Body(..., embed=True)


@router.post("")
async def user_registration(user_auth: UserAuth):  # type: ignore[no-untyped-def]
    """Create a new user."""
    user = await User.by_email(user_auth.email)
    if user is not None:
        raise HTTPException(409, "User with that email already exists")
    hashed = hash_password(user_auth.password)
    user = User(email=user_auth.email, password=hashed)
    await user.create()
    await request_verification_email(user_auth.email)
    return JSONResponse(status_code=201, content={"data": user.model_dump(exclude={"password","id"}),"message": "User Verification Email sent"})


@router.post("/forgot-password")
async def forgot_password(email: EmailStr = embed) -> Response:
    """Send password reset email."""
    user = await User.by_email(email)
    if user is None:
        raise HTTPException(404, "No user found with that email")
    if user.email_confirmed_at is None:
        raise HTTPException(400, "Email is not yet verified")
    if user.disabled:
        raise HTTPException(400, "Your account is disabled")
    token = access_security.create_access_token(user.jwt_subject)
    await send_password_reset_email(email, token)
    return Response(status_code=200)


@router.post("/reset-password", response_model=UserOut)
async def reset_password(token: str, password: str = Body(..., embed=True)):  # type: ignore[no-untyped-def]
    """Reset user password from token value."""
    user = await user_from_token(token)
    if user is None:
        raise HTTPException(404, "No user found with that email")
    if user.email_confirmed_at is None:
        raise HTTPException(400, "Email is not yet verified")
    if user.disabled:
        raise HTTPException(400, "Your account is disabled")
    user.password = hash_password(password)
    await user.save()
    return JSONResponse(status_code=200, content={"success": True,"message": "Password reset successful"})
