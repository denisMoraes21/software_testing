from app.app import App


if __name__ == "__main__":
    app = App().get_app()
    app.run(debug=True)
