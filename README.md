# Local Bot Builder

 <p align="center">
   <img src="frontend/logo.png" alt="Logo" width="300" />
 </p>


 **Local Bot Builder** is an intuitive platform designed to make AI bot creation accessible to everyone—whether you're a beginner or an expert. Users can easily create custom AI bots by providing a name, tone, and system prompt, and even upload files to index for smarter, context-aware responses. While the platform is simple enough for beginners, it also provides advanced features for experts.

 ### Key Features:
 - **Simple and Expert Mode**: When registering, users fill out a questionnaire to determine their expertise level, ensuring a tailored experience.
 - **Bot Creation**: Users can create bots by defining a name, tone, and system prompt. They can also upload files to index for more intelligent responses.
 - **Predefined Tone Templates**: Choose from a variety of tone templates like **Friendly**, **Motivational**, **Professional**, and more.
 - **AI Model Integration**: Local Bot Builder leverages **Llama**, **Phi**, and other AI models for smart responses.
 - **File Indexing**: Upload files to be indexed using **LlamaIndex**, which enhances the bot's ability to answer questions based on those files.

 ## Table of Contents
 - [Features](#features)
 - [Installation](#installation)
 - [Usage](#usage)
   - [Create a Bot](#create-a-bot)
   - [View Bot History](#view-bot-history)
   - [Download Bot](#download-bot)
 - [API Endpoints](#api-endpoints)
 - [Docker Setup](#docker-setup)
 - [License](#license)

 ## Installation

 ### Prerequisites
 To run **Local Bot Builder** locally, you will need the following:
 - Python 3.7+
 - Node.js 18+ (for the frontend)
 - Docker and Docker Compose

 ### Clone the Repository

 ```bash
 git clone https://github.com/yourusername/local-bot-builder.git
 cd local-bot-builder
 ```

 ### Install Backend Dependencies
 Create a virtual environment and install the Python dependencies.

 ```bash
 python -m venv venv
 source venv/bin/activate  # For Windows: venv\Scripts\activate
 pip install -r backend/requirements.txt
 ```
 ### Install Frontend Dependencies
 Change to the frontend directory and install the necessary dependencies.

 ```bash
 cd frontend
 npm install
 ```
  ### Setup Environment Variables
 Create a .env file in the root directory of your project and set the following variables:

 ```bash
 DATABASE_URL=sqlite:///app/data/history.db
 OLLAMA_BASE_URL=http://ollama:11434
 SECRET_KEY=your-secret-key
 GENERATED_FOLDER=./app/generated_bots
 UPLOAD_FOLDER=./app/uploaded_files
 INDEX_FOLDER=./app/index_storage
 ```
 ### Run Database Migrations
 To set up the database, run the following commands:

 ```bash
 cd backend
 flask db init
 flask db migrate
 flask db upgrade
 ```
 ### Docker Setup
 This project uses Docker and Docker Compose for easy setup and deployment. The configuration includes the backend, frontend, and the Ollama AI model server.       

 Build and Run Docker Containers:

 ```bash
 docker-compose up --build
 ```
 This will build and run the containers for the backend (bot_creator), frontend, and Ollama. The frontend will be available on port 5173 and the backend will be available on port 5001.

 Stop the Containers:

 ```bash
 docker-compose down
 ```
 ### Usage
 Create a Bot
 Register: Fill out a registration form where you'll provide your name, email, password, and select your expertise level.

 Create a Bot: After logging in, you can create a new bot:

 Choose a bot name.

 Select a tone (e.g., Friendly, Motivational).

 Provide a system prompt to guide the bot's responses.

 Optionally, upload a file to be indexed (like lesson plans or documents).

 Download: After creating the bot, you can download a ZIP package containing the bot's model and indexed data.

 ### View Bot History
 Once logged in, you can view a list of all the bots you've created, with details like bot name, model, tone, and system prompt.

 ### Download Bot
 You can download any of the bots you've created as a ZIP file, which includes the model and any indexed files used by the bot.

 ## API Endpoints
 POST /api/register

 Description: Register a new user.

 Body:

 ```bash
 {
   "name": "User Name",
   "email": "user@example.com",
   "password": "password123"
 }
 ```
 POST /api/login

 Description: Log in an existing user.

 Body:

 ```bash
 {
   "email": "user@example.com",
   "password": "password123"
 }
 ```
 POST /api/logout

 Description: Log out the current user.

 POST /api/create

 Description: Create a new bot.

 Body (Form Data):

 ```bash
 {
   "bot_name": "My Bot",
   "model_name": "gpt-3.5",
   "system_prompt": "Please help with my tasks",
   "tone": "Friendly"
 }
 ```
 GET /api/history

 Description: Get a list of all bots created by the current user.

 GET /api/download/<bot_name>

 Description: Download a bot as a ZIP file containing its model and indexed data.

 ## Docker Setup
 This project includes a Docker Compose setup with three main services:

 bot_creator: The backend service running Flask and managing the creation of bots.

 frontend: The Vue.js frontend for interacting with the bot creator.

 ollama: The Ollama AI model server.

 ### Docker Compose Configuration:
 ```bash
 version: '3.9'

 services:
   bot_creator:
     build:
       context: .
       dockerfile: Dockerfile.app
     ports:
       - "5001:5000"
     volumes:
       - ./backend:/app
     depends_on:
       - ollama
     environment:
       - OLLAMA_BASE_URL=http://ollama:11434

   frontend:
     build:
       context: ./frontend
       dockerfile: Dockerfile.frontend
     ports:
       - "5173:5173"
     volumes:
       - ./frontend:/app
       - /app/node_modules
     working_dir: /app
     command: npm run dev -- --host

   ollama:
     image: ollama/ollama
     ports:
       - "11434:11434"
     volumes:
       - ollama_data:/root/.ollama
 volumes:
   ollama_data:
 ```
 ### Dockerfiles:
 Dockerfile for Backend:

 ```bash
 FROM python:3.10-slim

 ENV PYTHONDONTWRITEBYTECODE=1 \
     PYTHONUNBUFFERED=1 \
     PIP_NO_CACHE_DIR=1

 RUN apt-get update && apt-get install -y --no-install-recommends \
     git curl bash libssl-dev libstdc++6 ca-certificates \
  && rm -rf /var/lib/apt/lists/*

 WORKDIR /app

 COPY backend/requirements.txt .

 RUN pip install --upgrade pip \
  && pip install -r requirements.txt

 COPY backend/ .

 CMD ["python", "run.py"]
 ```
 Dockerfile for Frontend:

 ```bash
 FROM node:18

 WORKDIR /app

 COPY package.json package-lock.json ./

 RUN npm install

 COPY . .

 CMD ["npm", "run", "dev"]
 ```
 ### License
 See the LICENSE file for details.
