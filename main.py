from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import pytesseract



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/annotate_receipt", response_class=HTMLResponse)
async def annotate_receipt(
    request: Request,
    photo: UploadFile = File(...),
    tax_rate: float = Form(...)
):
    image_bytes = await photo.read()
    image = Image.open(io.BytesIO(image_bytes))

    # OCR: extract text from image
    text = pytesseract.image_to_string(image)
    amount_before_tax = 0.0

    for line in text.splitlines():
        if any(key in line.lower() for key in ["sub", "taxable", "total before tax", "amount"]):
            try:
                amount_before_tax = float(line.split()[-1].replace("$", "").strip())
                break
            except:
                continue

    if amount_before_tax == 0.0:
        return HTMLResponse("<h3>Error: Could not detect subtotal in image.</h3>", status_code=400)

    new_total = round(amount_before_tax * (1 + tax_rate / 100), 2)

    # Annotate image with yellow box and large red text
    draw = ImageDraw.Draw(image)
    message = f"If tax were {tax_rate}%, the total amount would be ${new_total}"

    try:
        # ✅ Use bundled font file with increased size
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 21)
    except Exception as e:
        print("⚠️ Font load failed:", e)
        font = ImageFont.load_default()

    draw.rectangle([(0, image.height - 70), (image.width, image.height)], fill="yellow")
    draw.text((10, image.height - 60), message, fill="red", font=font)

    # Convert image to base64
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_data": base64_image,
        "amount_before_tax": amount_before_tax
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
