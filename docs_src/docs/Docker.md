# Run in Docker

## Build the image

Run this commands from the project's root directory

```bash
docker build -t xformer/services -f docker/images/services.Dockerfile  .
```

## Run in Docker

Run all services in a single Docker container.

### Configuration
1. Make a copy of config.ini and secrets.txt
   - Make note of the location of these files
2. Create a directory to store the database
3. Change the value of `dataplane_token` in secrets.txt
4. Review the [Config](CONFIG.md) documentation and change any required values
   - At least, you must change db_url to **db_url=sqlite+aiosqlite:////app/data.db**

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
-p 9000:9000 \
-p 8050:8050 \
-e APP_CONFIG_FILE=/app/config.ini \
-e SERVICE=both \
marcelonyc/xformer:{TAG}
```