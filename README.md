
# PDF Reader Backend

## Overview

This is the backend for the PDF Reader/Viewer application, built with FastAPI. It processes PDF files by converting each page into an image format using [pdf2image](https://pypi.org/project/pdf2image/).

### Links to Related Repositories:

- PDF Reader frontend: [https://github.com/Raghav1909/pdfreader-frontend](https://github.com/Raghav1909/pdfreader-frontend)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Raghav1909/pdfreader-backend.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd pdfreader-backend
   ```

3. **Install dependencies using a Virtual Environment:**

   a. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

   b. Activate the virtual environment:

   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

   c. Install the required dependencies:

   > ⚠️ **Warning:** This requires **Poppler** to be installed first. Please refer to the [pdf2image documentation](https://pypi.org/project/pdf2image/) for installation instructions.

   ```bash
   pip install -r requirements.txt
   ```

## Initialize the Database

Before starting the server, initialize the database:

   ```bash
   python init_script.py
   ```

## Run the backend server

1. Start the server using Uvicorn:

   ```bash
   fastapi dev
   ```

## API Documentation

The API documentation can be accessed at: `http://localhost:8000/docs`
