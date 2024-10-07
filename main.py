import argparse

import uvicorn


def start_server(app: str, host: str, port: int, reload: bool) -> None:
    uvicorn.run(app, host=host, port=port, reload=reload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="Host", default="127.0.0.1")
    parser.add_argument("-P", "--port", help="Port", default=8000, type=int)
    parser.add_argument("-R", "--reload", help="Reload", default=True, type=bool)

    args = parser.parse_args()

    start_server("routes:app", args.host, args.port, args.reload)


if __name__ == "__main__":
    main()
