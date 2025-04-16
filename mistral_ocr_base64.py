import requests
import base64
import json


def create_markdown_file(ocr_response, output_filename = "OCR_output.md"):
  with open(output_filename, "wt") as f:
    for page in ocr_response.get("pages", []):
      f.write(page.get("markdown", "No Markdown content found"))


url = "https://mistral-ocr-2503-qlnma.eastus.models.ai.azure.com/v1/ocr"

# Define the file URL
file_url = "https://arxiv.org/pdf/2201.04234"  # Replace with your file URL
image_url = "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
# image_url = "https://circedesign.com/cdn/shop/files/Prendre_soin_de_soi.png"
image_url = "https://www.mykomela.com/images/aides/2021/mykomela-edition-ticket-caisse1-500-c.jpg"

# Download the file from the URL
file_response = requests.get(image_url)
if file_response.status_code == 200:
    # Encode the file content in Base64
    base64_content = base64.b64encode(file_response.content).decode("utf-8")
    base64_content = "data:application/pdf;base64," + base64_content
else:
    print(f"Failed to download file. Status Code: {file_response.status_code}")
    exit()

payload = {
    "model": "mistral-ocr-2503",
    "document": {
        "type": "document_url",
        "document_url": base64_content,
    }
}

# Set the headers (if needed)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ***"  # Replace with your API key
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the response
if response.status_code == 200:
    print("Success:", response.json())
elif response.status_code == 422:
    print("Validation Error:", response.json())
else:
    print("Error:", response.status_code, response.text)

# Save response to a JSON file
with open("OCR_output.json", "w", encoding="utf-8") as file:
    json.dump(response.json(), file, ensure_ascii=False, indent=4)
print("Response saved to 'OCR_output.json'")

# Extract JSON data
response_data = response.json()

pages = response_data.get("pages", [])
print(f"Number of pages: {len(pages)}")

create_markdown_file(response_data, "OCR_output.md")
print("Markdown file created: 'OCR_output.md'")

# Access the Markdown content of the first page (if available)
if pages:
    print(pages[0].get("markdown", "No Markdown content found"))
