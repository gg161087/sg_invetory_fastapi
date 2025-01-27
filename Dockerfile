FROM python:3.12-slim

WORKDIR /sg_inventory_fastapi

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]