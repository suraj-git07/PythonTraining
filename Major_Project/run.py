from app import create_app  # Importing the app factory function

app = create_app()  # Flask app instance

if __name__ == "__main__":
    app.run(debug=True)  # Running app in debug mode
