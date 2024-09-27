# Data Onboarding - transformer builder
## Sample, transform, map and simplify you data exchanges

Enable your customers and partners to upload CSV/XLS files and transform them to match your internal data schemas. The platform provides the infrastructure and components to generate data transformers and unique URLs for users to upload their data.

![Flow](https://marcelonyc.github.io/xformer-builder/assets/ApplicationFlow.drawio.png)

Please read the [documentation](https://marcelonyc.github.io/xformer-builder) for more details 

Clone the [GitHub](https://github.com/marcelonyc/xformer-builder) repository for additional capabilities and the latest dev versions. 


## Configuration
1. Make a copy of config.ini and secrets.txt
    - Clone the GitHub repository or download config.ini and secrets.txt from the repo
2. Change the dataplane_token secret (in secrets.txt)
3. Create a directory for the database
4. Create a directory to save your files
5. Review the [Config](https://marcelonyc.github.io/xformer-builder/CONFIG/) documentation and change any required values
   - Change app_cfg - db_url to **db_url=sqlite+aiosqlite:////app/db/data.db**
   - Change fileprovider - path to /app/data



## Run both services in one container
- Change {PATH TO} to the path of your files. You must set, config, secrets, db and data locations. 
- Set the {TAG} to the version you want to deploy (Check the Github repository to release notes)

```bash
docker run --rm -v {PATH TO}/config.ini:/app/config.ini \
-v {PATH TO}/secrets.txt:/app/secrets.txt \
-v {PATH TO}/db:/app/db/ \
-v {PATH TO}/data:/app/data \
-p 9000:9000 \
-p 8050:8050 \
-e APP_CONFIG_FILE=/app/config.ini \
-e SERVICE=both \
quay.io/marcelonyc/xformer:{TAG}
``` 

---
**Note:**

9000 is the dataplane port. It is optional to expose it

---

If the services start successfully, go to http://localhost:8050 on your browser.