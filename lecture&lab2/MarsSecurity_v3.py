"""
API文档: https://api.nasa.gov/ (Mars Rover Photos栏中)

申请API KEY: https://api.nasa.gov/

在火星探测车的照片中，"sol" 是一个用来表示火星上一天的概念，也就是火星的自转周期。
火星的一 sol 大约是24小时39分钟，比地球上的一天略长。
在火星探测车的数据中，"sol" 用来计数火星车在火星表面的天数，从它着陆的那一天开始算起。
"""
import requests
import gradio as gr



# Function to fetch Mars Rover photos
def fetch_mars_rover_photos(api_key, sol=1000, camera='CHEMCAM', page=1):
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    
    params = {
        'api_key': api_key,
        'sol': sol,
        'camera': camera,
        'page': page
    }
    print(params)
    
    response = requests.get(base_url, params=params)
    # 发起一个post请求
    response = requests.post(base_url, data=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Gradio interface setup
def mars_rover_photo_interface(sol,camera,page):
    """
    本函数主要是处理API请求得到的JSON数据，提取出图片的URL并返回
    
    通常一个API文档要说清楚它的输入参数和输出数据格式, 但NASA这个API文档没说清楚输出数据格式
    我们可以通过把返回的数据打印出来，分析它的JSON结构，用Key作为索引，提取出我们需要的数据
    关于JSON: https://www.runoob.com/json/json-syntax.html
    """



    api_key = "KKDMzTTxJzgLJBkaMqw0ZfMAyTBtLdKUmneFbPD8" 
    data = fetch_mars_rover_photos(api_key, sol=sol, camera=camera, page=page)
    # 把data保存到文件中
    with open('data.json', 'w') as f:
        f.write(str(data))
    print(data)
    if data:
        photos = data.get('photos', [])
        photo_urls = [photo['img_src'] for photo in photos]
        print(photo_urls)
        return photo_urls
    else:
        return []

# Define the input components for the Gradio interface
sol_input = gr.Number(label="Martian Sol", value=1000)
camera_input = gr.Dropdown(label="Camera Type",choices=["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM", "PANCAM", "MINITES"])
page_input = gr.Number(label="Page", value=1)

# Create the Gradio interface
gr.Interface(fn=mars_rover_photo_interface, 
        inputs=[sol_input, camera_input, page_input], 
        outputs=gr.Gallery(label="Mars Rover Photos")).launch()
