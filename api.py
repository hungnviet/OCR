from fastapi import FastAPI, UploadFile, File
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "D:\\testOCR\\tesseract.exe"
import numpy as np
import io
from PIL import Image
import subprocess
import json

app = FastAPI()
@app.post("/process_image")
async def process_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    boxes = pytesseract.image_to_data(img)
    
    results = ""
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                results += " ".join(b[11:]) + " "
    with open('output_ocr.txt', 'w') as f:
        f.write(results.strip())

    subprocess.run(["python", "extract.py"], check=True)
    with open('output_nlp.txt', 'r') as f:
        lines = f.read().split('\n')
    res = [json.loads(line) for line in lines if line]
    return {"results": res}