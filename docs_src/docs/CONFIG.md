# CONFIG.INI

The application reads the provided config.ini file to initialize the application. You can provide the location of this file (full path and name) to the `start-..` scripts.

When values in the config.ini require secrets from the vault provider use the syntax ${vault:<vault key>}. The values are replaced when the config file is parsed.

## Sections documentation

### appcfg
General application settings

[appcfg]

`title`: Application title to display on the Navigation bar
> Example <span style="color: green;">**title=Data Transformer**</span>

`db_url`: Url to connect to the database
> Example <span style="color: green;">**db_url=sqlite+aiosqlite:////tmp/data.db**</span>

`max_file_size`: Max size for a single file in bytes
> Example <span style="color: green;">**max_file_size=10000000**</span>

`max_storage_size`: Max total size of files in bytes per account
> Example <span style="color: green;">**max_storage_size=100000000**</span> 

`webhook_domain_whitelist`: Comma separated list of domains allowed for webhooks
> Example <span style="color: green;">**webhook_domain_whitelist=webhook.site, webhook-test.com**</span>

`debug`: Not implemented
> Example <span style="color: green;">**debug=false**</span>

`file_ttl`: Hours before deleting a file. No automation is implemented yet. You can delete by invoking the API call to /platform/delete-expired-files 
> Example <span style="color: green;">**file_ttl=72**</span>

**TODO**

> require_email_verification=false

> allow_plus_in_email=false

> enable_announcements=true

> log_level=info



### vaultprovider
Secrets provider configuration. Classes for each provider are defined in the application. Current implementation support an environment file

[vaultprovider]

`type`: Provider class. Options: envfile
> Example <span style="color: green;">**type=envfile**</span>

**ENVFILE options**

path=../../   <span style="color: green;"># Path to locate file</span>

file=secrets.txt <span style="color: green;"># File name</span>

### fileprovider
File storage provider. Classes for each provider type are defined in the application. Currently local filesystem is support. S3 is next.

[fileprovider]

`type`: Provider class. Options: localfs, s3

**LOCALFS options**

path=/tmp/data <span style="color: green;"># Path to store files</span>

**S3 options**

bucket=s3://mybucket  <span style="color: green;"># S3 Bucket name</span>

endpoint_url=http://localhost:9000  <span style="color: green;"># Set if not using a standard AWS endpoint</span>

region=us-west-1  <span style="color: green;"># Required for some providers</span>

access_key_id=${vault:access_key_id}  <span style="color: green;"># Access Key stored in a vault provider</span>

secret_access_key=${vault:secret_access_key}  <span style="color: green;"># Secret stored in a vault provider</span>

### dataplane
Endpoint url for dataplane
[dataplane]
url=http://localhost:9000 <span style="color: green;"># Endpoint where data plane is listening</span>

### controlplane
Endpoint url for dataplane
[controlplane]
url=http://localhost:8050 <span style="color: green;"># URL of controlplane. We use this to contruct urls from the dataplane (like password reset url)</span>

### background provider

Background tasks execution provider. A class is defined in the application to handle background tasks. Currently, only FastApi Backgroundtasks is implemented

[backgroundprovider]

type=fastapi