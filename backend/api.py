import datetime

import fastapi
from fastapi import responses, templating
from services import jwt_service, otp_service

app = fastapi.FastAPI()
templates = templating.Jinja2Templates(directory="templates")

_canonical_url = "http://localhost:8000"


@app.get("/", response_class=responses.HTMLResponse)
async def render_codes(request: fastapi.Request):
    token = jwt_service.encode_dict(
        {
            "name": f"this is a name, now is {datetime.datetime.utcnow()}",
            "id": "some-id",
        },
        expiration_in_secs=120,  # valid for 2mins
    )
    validate_url = f"{_canonical_url}/validate/{token}"

    return templates.TemplateResponse(
        "display.html",
        {
            "request": request,
            "validate_url": validate_url,
            "code": otp_service.get_otp_time_code(),
        },
    )


@app.get("/validate/{token}", response_class=responses.HTMLResponse)
async def validate_render(request: fastapi.Request, token: str):

    data = jwt_service.decode_dict(token)
    if not data:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": "Invalid Token",
            },
        )

    return templates.TemplateResponse(
        "validate.html",
        {
            "request": request,
            "name": data["name"],
            "id": data["id"],
        },
    )


@app.post("/validate/{token}", response_class=responses.HTMLResponse)
async def validate_code(
    request: fastapi.Request, token: str, code: str = fastapi.Form()
):

    data = jwt_service.decode_dict(token)
    if not data:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": "Invalid Token",
            },
        )

    if not otp_service.verify_otp_time_code(code):
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": "Bad veridication code",
            },
        )

    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "msg": "Token is valid and the code is also valid",
        },
    )
