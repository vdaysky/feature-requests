FROM python:3.9

# install node
RUN apt-get update
RUN apt-get install -y nodejs npm

COPY ./backend /app/backend
COPY ./notionFRs /app/notionFRs

WORKDIR /app/backend
RUN pip install -r requirements.txt
WORKDIR /app/notionFRs
RUN npm install
RUN npm run build
#CMD ["npm", "run", "dev"]
WORKDIR /app/backend/src
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
