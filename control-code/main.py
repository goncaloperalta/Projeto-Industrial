from api import app
import uvicorn

def start_api():
    uvicorn.run(app, host='0.0.0.0', port=8000)

def main():
    start_api()

if __name__ == '__main__':
    main()