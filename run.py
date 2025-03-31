from app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)


# migration steps
# flask db init
# flask db migrate -m "update user"
# flask db upgrade
