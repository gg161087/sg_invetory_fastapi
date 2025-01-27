## Para probar localmente:
  crear .env:
    SECRET_KEY=ThisIsNotSecret
    for sqlite:
      SQLALCHEMY_DATABASE_URL=sqlite:///./sql_stocker.db
    for mysql server:
      SQLALCHEMY_DATABASE_URL=mysql+pymysql://USER:PWD@IP_DB:3306/DB_NAME
  python -m venv venv
  .\venv\Scripts\activate
  pip install --no-cache-dir -r requirements.txt
  python main.py; uvicorn main:app --host 0.0.0.0 --port 4000 --reload