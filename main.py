from website import create_app
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=False)
