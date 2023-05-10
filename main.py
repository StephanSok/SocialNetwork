import uvicorn
from fastapi import FastAPI
from backend.routers import user, auth, chat


app = FastAPI()


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     print(json.dumps(dict(request.headers), indent=4))
#     if 'Authenticate' in request.cookies:
#         print(request.cookies['Authenticate'])
#         new_header = MutableHeaders(request._headers)
#         new_header['authorization'] = request.cookies["Authenticate"]
#         request._headers = new_header
#     print(json.dumps(dict(request.headers), indent=4))
#     authorization = request.headers.get("Authorization")
#     scheme, param = get_authorization_scheme_param(authorization)
#     response = await call_next(request)
#     return response

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
