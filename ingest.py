from pypdf import PdfReader

from services.rag_service import add_document


# Load PDF
reader = PdfReader("mental_health_guide.pdf")


text = ""


# Extract text from all pages
for page in reader.pages:

    extracted = page.extract_text()

    if extracted:
        text += extracted


# Split into chunks
chunks = text.split(".")


# Store embeddings
for idx, chunk in enumerate(chunks):

    chunk = chunk.strip()

    if len(chunk) > 50:

        add_document(
            str(idx),
            chunk
        )


print("PDF embeddings created successfully")