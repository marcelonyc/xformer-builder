# Run in Docker

## Build the image

Run these commands from the project's root directory

```bash
docker build -t xformer/services -f docker/images/services.Dockerfile  .
```

## Run in Docker

Run all services in a single Docker container.

### Configuration
1. Make a copy of config.ini and secrets.txt
    - Clone the GitHub repository or download config.ini and secrets.txt from the repo
2. Change the dataplane_token secret (in secrets.txt)
3. Create a directory for the database
4. Create a directory to save your files
5. Review the [Config](https://marcelonyc.github.io/xformer-builder/CONFIG/) documentation and change any required values
   - Change app_cfg - db_url to **db_url=sqlite+aiosqlite:////app/db/data.db**
   - Change fileprovider - path to /app/data
### Run from local build

Replace {PATH TO} with the location of your files and db directory

```bash
docker run --rm -v {PATH TO}/config.ini:/app/config.ini \
-v {PATH TO}/secrets.txt:/app/secrets.txt \
-v {PATH TO}/db:/app/db/ \
-p 9000:9000 \
-p 8050:8050 \
-e APP_CONFIG_FILE=/app/config.ini \
-e SERVICE=both \
xformer/services
``` 

### Run from release build

- Replace {PATH TO} with the location of your files and db directory
- Replace {TAG} with the image tag

```bash
docker run --rm -v {PATH TO}/config.ini:/app/config.ini \
-v {PATH TO}/secrets.txt:/app/secrets.txt \
-v {PATH TO}/db:/app/db/ \
-v {PATH TO}/data:/app/data \
-p 9000:9000 \
-p 8050:8050 \
-e APP_CONFIG_FILE=/app/config.ini \
-e SERVICE=both \
marcelonyc/xformer:{TAG}
```

## NOTES

- Forwarding port 9000 is optional. That port is for the dataplane.
- After starting the container, got to http://localhost:8050 