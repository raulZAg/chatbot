# AI Dashbot

## Installation Instructions

**Important Note: You must have an existing Python installation. It's recommended to install everything inside a Virtual Environment.**

### Step 1: Clone or download the repository

Execute the following command in the shell:

```shell
git clone https://github.com/K4rlosReyes/ai-dashbot.git
```

Alternatively, you can download it from [GitHub](https://github.com/K4rlosReyes/ai-dashbot/archive/refs/heads/main.zip) and unzip the repository.

### Step 2: Set up the .env file

You need to create a `.env` file in the root folder and add the following line:

```shell
# OpenAI
OPENAI_API_KEY="copy_the_key_here"

# backend
INDEX_FOLDER = "index_folder"

DATASOURCE_FOLDER = "data_folder"

# GUI 
BACKEND_ADDRESS = 'http://localhost'

BACKEND_PORT = 8000
```

Replace `"copy_the_key_here"` with your OpenAI API key.

### Step 3: Create the documents folder.

Also, out the project folder, you need to create a new folder and name it `app-data`. This folder will store the documents to be processed.

### Step 4: Create and activate a virtual environment

#### On Windows

Run the following command in the root folder to create a new virtual environment:

```shell
python -m venv myenv
```

Activate it using:

```shell
myenv\Scripts\activate
```

#### On Linux

Run the following command in the root folder to create a new virtual environment:

```shell
python -m venv ./myenv
```

Activate it using:

```shell
source myenv/bin/activate
```

### Step 5: Install requirements

To install the project's requirements, run:

```shell
pip install -r requirements.txt
```

## Running Server

There are two backends in this app, the Chatbot and the Dashboard.
To run the Dashboard:
```shell
gunicorn -b 0.0.0.0:8050 app:server
```
To run the Chatbot
```shell
uvicorn main:app
```
To make the server more robust you should create two daemon processes using systemctl.

## Usage Instructions

**First of all**, place all the files to be processed in the `apps-data` folder.

Then run the ChatBot:

```shell
python main_view.py
```

Wait until it finishes scanning and indexing documents.

Open your web browser and go to <http://127.0.0.1:5555/>

***Start chatting***

## ToDo

- [ ] Azure Sharepoint
- [ ] Excel files
