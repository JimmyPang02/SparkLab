from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# 增加一个名字的请求参数
@app.get("/api/hello")
def get_data(name: str):

    data = {"message": f"Hello, {name}!"}
    return JSONResponse(content=data)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
