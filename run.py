from flask_ngrok import run_with_ngrok
from medium_scraper import create_app

app = create_app()

if __name__ == '__main__':
    app.debug = True

    if not app.debug:
        run_with_ngrok(app)
    app.run()