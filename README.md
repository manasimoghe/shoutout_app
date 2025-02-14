This is a simple Shoutout App with a REST API built using Flask and SQLite. It allows users to create shoutouts, like them, and delete them. The app features a front-end UI built with HTML, JavaScript, and integrates with a Flask backend API for handling data operations (create, read, update, delete).

Features:
Create Shoutouts: Users can submit text-based shoutouts.
Like Shoutouts: Users can like a shoutout, which increments its like count.
Delete Shoutouts: Users can delete shoutouts.

Persistence: Uses in-memory Uses an in-memory SQLite database, shared across API requests. Every new invocation of flask app older data is lost
Requirements
    Python 3.x
    Flask
    Flask-CORS
    SQLite

Steps
------
1. Clone the repo
        git clone https://github.com/<your-repo>/shoutout-app.git
        cd shoutout-app
2. Create a virtual env (optional but recommended)
      python3 -m venv ~/shoutout  #name of env: shoutout
      source ~/shoutout/bin/activate  #
3. Install dependencies
       pip install -r requirements.txt
4. sqlite3 comes with python. But in case you need to install it use
        brew install sqlite   #for macOS
        apt-get install sqlite3 libsqlite3-dev
4. Run the app
       python app.py
   
    If all goes well your app would be running at http://localhost:3000.

  Frontend/UI
  ------------
  The front-end allows users to interact with the Flask API and perform CRUD operations.
  HTML Structure (index.html):
   * It contains a form to accept text input for shoutout
   * A table to display the shoutouts with Like and Delete button
   app.js:
       Javascript code to create/update, delete and list shoutouts
       It contacts python Flask REST server using http requests
    

Usage
------
1. Start flask backend server using
     python app.py

2. Open frontend/UI in brower
     1. You can either navigate to index.html in your brower OR
     2. serve it using a local server (for example, with Python's built-in HTTP server):
            python -m http.server
     3. Use "http://localhost:8000" in your brower to see your page

    
