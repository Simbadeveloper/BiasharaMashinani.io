#run.py
"""
run the app
"""
from app import app #import app from app

if __name__ == '__main__':
    app.run(debug=True) #debug false on development
