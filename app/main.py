from fastapi import FastAPI


app = FastAPI(title="TaskListAPI")


@app.get("/health")
async def health():
    return {"ok": True}
