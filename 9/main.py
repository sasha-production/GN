import subprocess

from fastapi import FastAPI, Header, HTTPException, Response, status

app = FastAPI(title="Simple API")


@app.post("/")
def hello_world(test: str | None = Header(default=None, alias="Test")):
    if test == "Hello":
        return "Hello, World!"
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@app.get("/health")
def health():
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", "77.88.8.8"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        return Response(content="OK", status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unavailable")
