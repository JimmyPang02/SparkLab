# FASTAPI写一个接口，接口地址为 /nasa，
# 接收参数 query_type, sol, earth_date, camera, page
# 返回数据类型为 List[str]

@app.get("/nasa")
def nasa(query_type: str, sol: int = 1000, earth_date: str = None, camera: str = 'CHEMCAM', page: int = 1):
    
