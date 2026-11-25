from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print('\nГоловна сторінка: http://127.0.0.1:5001/\n', flush=True)

    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True,
        use_reloader=False
    )