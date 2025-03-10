"""Email router."""

from datetime import datetime, UTC

from fastapi import APIRouter, Body, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from auth.models.user import User
from auth.jwt import access_security, user_from_token
from auth.util.mail import send_verification_email


router = APIRouter(prefix="/mail", tags=["Mail"])


async def request_verification_email(
    email: EmailStr = Body(..., embed=True),
) -> Response:
    """Send the user a verification email."""
    user = await User.by_email(email)
    if user is None:
        raise HTTPException(404, "No user found with that email")
    if user.email_confirmed_at is not None:
        raise HTTPException(400, "Email is already verified")
    if user.disabled:
        raise HTTPException(400, "Your account is disabled")
    token = access_security.create_access_token(user.jwt_subject)
    await send_verification_email(email, token)
    return JSONResponse(status_code=200,content={"message": "Verification email sent"})


@router.get("/verify/{token}")
async def verify_email(token: str) -> Response:
    """Verify the user's email with the supplied token."""
    user = await user_from_token(token)
    if user is None:
        raise HTTPException(404, "No user found with that email")
    if user.email_confirmed_at is not None:
        raise HTTPException(400, "Email is already verified")
    if user.disabled:
        raise HTTPException(400, "Your account is disabled")
    user.email_confirmed_at = datetime.now(tz=UTC)
    await user.save()
    return JSONResponse(status_code=200,content={"message": "Email verified"})
