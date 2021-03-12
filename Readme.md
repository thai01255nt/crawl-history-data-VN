# CDP

## Build for dev environment

- **Create `dev.ini` config file in `/internal/configs` .**
- ```docker build -t crawl-history-data-vn:latest .```
- ```docker run -e FLASK_ENV=dev -e FLASK_DEBUG=1 -p 5000:5000 -d crawl-history-data-vn:latest```

`FLASK_ENV=dev` is active dev environment

`FLASK_DEBUG=1` is active response debug message

## Build for staging environment

- **Create `staging.ini` config file in `/internal/configs` .**
- ```docker build -t crawl-history-data-vn:latest .```
- ```docker run -e FLASK_ENV=staging -e FLASK_DEBUG=0 -p 5000:5000 -d crawl-history-data-vn:latest```

`FLASK_ENV=staging` is active staging environment

`FLASK_DEBUG=0` is deactive response debug message