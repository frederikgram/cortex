# Entrypoint for the application


from fastapi import FastAPI
from routers import detection_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(detection_router, prefix="/api/v1/detection")



# This is the entrypoint for the application
app.get("/")(lambda: {"message": "Hello World"})


# CHANGE FOR PRODUCTION
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Adding cors rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
