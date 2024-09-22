import requests
import gradio as gr
from datetime import date

# Function to fetch Mars Rover photos by Sol or Earth date
def fetch_mars_rover_photos(api_key, query_type, sol=1000, earth_date=None, camera='CHEMCAM', page=1):
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {
        'api_key': api_key,
        'camera': camera,
        'page': page
    }
    
    if query_type == 'sol':
        params['sol'] = sol
    elif query_type == 'date':
        params['earth_date'] = earth_date
    
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

# Gradio interface function that decides which type of query to use
def mars_rover_photo_interface(query_type, sol, earth_date, camera, page):
    api_key = "Your_NASA_API_Key_Here"
    data = fetch_mars_rover_photos(api_key, query_type, sol, earth_date, camera, page)
    
    if data:
        photos = data.get('photos', [])
        return [photo['img_src'] for photo in photos]
    return []

# Interface components
query_type_input = gr.Radio(label="Query Type", choices=['sol', 'date'], value='sol')
sol_input = gr.Number(label="Martian Sol", value=1000)
earth_date_input = gr.DateTime(label="Earth Date", value=str(date.today()))
camera_input = gr.Dropdown(label="Camera Type", choices=["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM", "PANCAM", "MINITES"])
page_input = gr.Number(label="Page", value=1)

# Create the Gradio interface
interface = gr.Interface(
    fn=mars_rover_photo_interface,
    inputs=[query_type_input, sol_input, earth_date_input, camera_input, page_input],
    outputs=gr.Gallery(label="Mars Rover Photos")
)

interface.launch(share=True)


