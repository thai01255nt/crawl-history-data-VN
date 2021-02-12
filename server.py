from internal.app import app

if __name__ == '__main__':
    app.run('0.0.0.0', app.config["SYS"]["port"]["port"])
