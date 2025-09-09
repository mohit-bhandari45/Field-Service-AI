# 📤 Upload API Documentation

This document describes the **Upload API** endpoint of the Field Service AI project. The endpoint allows users to upload an image file, generate an embedding, and store the vector with metadata in the TiDB database.

---

## 🔹 Endpoint Details

**Method:** `POST`
**Endpoint:** `/upload/`

### 📥 Request

#### Headers

* `Content-Type: multipart/form-data`

#### Body (Form Data)

* `file` (required): The image file to upload.

Example form-data:

```
Key: file
Value: sample_image.png
```

---

### 📤 Response

#### Success Response (200)

```json
{
  "filename": "sample_image.png",
  "vector_length": 512
}
```

* `filename`: The name of the uploaded file.
* `vector_length`: Length of the generated embedding vector.

#### Error Response (400/500)

```json
{
  "detail": "Invalid file format or processing error"
}
```

---

## 🖥️ Example Usage

### 1️⃣ Using **curl**

```bash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_image.png"
```

### 2️⃣ Using **Python requests**

```python
import requests

url = "http://127.0.0.1:8000/upload/"
files = {"file": open("sample_image.png", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## ✅ Expected Behavior

* The API reads the uploaded image.
* Generates an embedding vector.
* Stores the embedding + metadata in the TiDB database.
* Returns the uploaded filename and vector length.
