import requests

URL = "http://localhost:8000"


def add_book(data):
    url = URL
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print("Data posted successfully:", response.json())
        return response.json()

    except requests.RequestException as e:
        print("Error posting data:", e)
        return None


def add_pdf_book(book_id: int, pdf_path: str):
    url = f"http://localhost:8000/{book_id}/pdf"

    with open(pdf_path, "rb") as pdf_file:
        files = {"pdf_file": (pdf_path, pdf_file, "application/pdf")}

        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            print("PDF uploaded successfully:", response.json())
            return response.json()

        except requests.RequestException as e:
            print("Error posting PDF:", e)
            return None


book_data = {
    "name": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "no_of_pages": 285,
}
add_book(book_data)

pdf_path = "./data/test.pdf"
add_pdf_book(1, pdf_path)  # Assuming `1` is the ID of the created book
