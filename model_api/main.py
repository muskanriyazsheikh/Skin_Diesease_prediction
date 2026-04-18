from fastapi import FastAPI, File, UploadFile
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

app = FastAPI()

# ✅ model sirf ek baar load hoga (IMPORTANT)
model = load_model("model.h5")

@app.get("/")
def home():
    return {"message": "Model API running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file).resize((224, 224))
    img = np.array(image) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    result = int(np.argmax(pred))

    return {"prediction": result}