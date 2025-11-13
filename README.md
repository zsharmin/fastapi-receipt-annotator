# Receipt Annotation Web App (FastAPI)

This project is a FastAPI web application that allows users to upload a photo of a receipt, extract the subtotal using OCR, and automatically calculate a new total based on a custom tax rate. The app displays the updated total and returns an annotated version of the receipt image with the new amount written on it.

## Overview

The application uses:
- FastAPI for the backend web framework
- Jinja2 templates for rendering HTML pages
- Tesseract OCR (via pytesseract) to read text from uploaded receipt images
- Pillow (PIL) to draw tax annotations directly onto the image
- A simple form interface that accepts an image upload and a tax rate

Users upload a receipt photo, the system extracts the subtotal, applies the tax rate, and returns a modified image with the calculated total highlighted.

## Features

- Upload a receipt image through a web form  
- Extract subtotal using OCR  
- Automatically calculate a new total based on user-entered tax rate  
- Annotate the receipt image with a colored box and text  
- Display processed images directly in the browser  
- Includes static and template folders for a full web interface  
- Deployable to Google Cloud Run or Google App Engine

## How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
