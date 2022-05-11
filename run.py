from medium_scraper import create_app

app = create_app()

if __name__ == '__main__':
    app.debug = False

    if not app.debug:
        from flask_ngrok import run_with_ngrok
        run_with_ngrok(app)
    app.run()