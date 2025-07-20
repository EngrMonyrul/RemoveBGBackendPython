from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile=File(...)):
    input_data = await file.read()
    output_data = remove(input_data)
    
    output_image = Image.open(BytesIO(output_data)).convert("RGBA")
    buffer = BytesIO()
    output_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/")
def read_root():
    return {"message": "Background remover backend running succesfully."}