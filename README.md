# Data Onboarding - transformer builder
## Sample, transform, map and simplify you data exchanges


> **IMPORTANT**
These project is evolving from learning about Dash to building an application using Dash for the UI component. The original project can be found in this [branch](https://github.com/marcelonyc/xformer-builder/tree/dash-learning)

Enable your customers and partners to upload CSV/XLS files and transform them to match your internal data schemas. The platform provides the infrastructure and components to generate data transformers and unique URLs for users to upload their data. 

Documentation: [Documentation](https://marcelonyc.github.io/xformer-builder)

Questions: [Ask Here](https://github.com/marcelonyc/xformer-builder/labels/question)

Do you want to run this in Docker?: [Docker Image](https://hub.docker.com/repository/docker/marcelonyc/xformer/general) 


## Features

- Upload CSV/XLS file: Users can easily upload their desired CSV/XLS file through the user interface.
- Column transformers: The project allows users to create transformers for each column using the ACE code editor.
- Restricted Python: The data transformer utilizes restricted Python to ensure secure and controlled data manipulation.
- Share a unique URL to upload/download files
- Trigger Webhook when a file is processed

![Application Flow](assets/ApplicationFlow.drawio.png)


## Getting Started

To get started with Xformer Builder, follow these steps:

1. Clone the repository: `git clone https://github.com/marcelonyc/xformer-builder`
2. Run setup.sh 
    - Requires Python > 3.10
3. Note: a linux module is required and not installed by pip
    - Install libmagic in your environment (`apk add libmagic` `apt-get install libmagic` )
4. In one terminal run: `start-dev-dataplane.sh`
5. In another terminal run: `start-dev-controlplane.sh`
6. Access the application through your web browser at `http://localhost:8050`


<div style="margin: auto; width: 80%;"><div class="table-responsive"><table class="table table-striped table-bordered table-hover"><tbody><tr><td><a href="https://xformer.marcelonyc.com/register">
<img source="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/1.svg", width=30, heigth=30>
</a></td><td><a href="https://xformer.marcelonyc.com/register"><i class="fa-solid fa-cash-register fa-xl"></i></a></td><td>Register for an Account. You will get a token to login.</td></tr><tr><td><a href="https://xformer.marcelonyc.com/xformer-builder"><i class="fa-solid fa-2 fa-xl"></i></a></td><td><a href="https://xformer.marcelonyc.com/xformer-builder"><i class="fa-solid fa-arrow-right-arrow-left fa-xl"></i></a></td><td>Create a transformer with a sample of the CSV/XLS file you want to transform.You can later associate one or more file uploads with this transformer.</td></tr><tr><td><a href="https://xformer.marcelonyc.com/edit-xformer"><i class="fa-solid fa-3 fa-xl"></i></a></td><td><a href="https://xformer.marcelonyc.com/edit-xformer"><i class="fa-solid fa-pen-to-square fa-xl"></i></a></td><td>Edit and existing transformer.</td></tr><tr><td><a href="https://xformer.marcelonyc.com/associate-xformer"><i class="fa-solid fa-4 fa-xl"></i></a></td><td><a href="https://xformer.marcelonyc.com/associate-xformer"><i class="fa-solid fa-link fa-xl"></i></a></td><td>Associate a transformer with a file upload. This steps generastes a unique URL for the file upload</td></tr><tr><td><a href="https://xformer.marcelonyc.com/"><i class="fa-solid fa-5 fa-xl"></i></a></td><td><a href="https://xformer.marcelonyc.com/"><i class="fa-solid fa-share-from-square fa-xl"></i></a></td><td>Share the unique URL with the user who will upload the file</td></tr><tr><td><a href="https://xformer.marcelonyc.com/download"><i class="fa-solid fa-6 fa-xl"></i></a></td><td><a href="https://xformer.marcelonyc.com/download"><i class="fa-solid fa-download fa-xl"></i></a></td><td>When a user uploads a file, a unique URL will be generated for the file download. As an administrator you can also list the files available for download</td></tr></tbody></table></div></div>

Suggestions for deployment architecture: [Here](https://marcelonyc.github.io/xformer-builder/ArchitectureSuggestions/)


## Create a transformer

1. Upload CSV/XLS file: Click on "Upload Sample CSV/XLS file" and select the desired CSV/XLS file from your local machine.
2. Create transformers: Use the ACE code editor to create transformers for each column. Ensure that the code adheres to the restricted Python guidelines.
    - Use `data` as the variable containing the source data.
    - Use the dictionary `columns[]` to get values from other columns
    - Examples:
        - `data / 1000`
        - `data.split("-")`
        - `data * columns['other_data']`
3. Test transformations: Once the transformers are created, click on the "Test" button to execute the transformations.
    - The result displays on the column's row. You need to [expand](#expand-row-to-see-transformation-resutls) it.
    - Any errors will display in the column's row
4. When you are finished, Name the transformer
5. Test all the transformers from the navigation bar
6. Save transformers
    - The output goes to the console

The transformer is saved into multiple lists. Right now is just a print to the console. The actual code is base64 encoded.

## Application Configuration
To customize the application configuration, review the [CONFIG.INI](https://marcelonyc.github.io/xformer-builder/CONFIG/) document

## Contributing

Contributions are welcome! If you would like to contribute to Xformer Builder, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## Screenshots

Here are some screenshots of the Xformer Builder application:

![Screenshot 1](/controlplane/src/assets/images/Screenshot%202024-07-13%20at%2012.52.17 PM.png)
---
![Screenshot 1](/controlplane/src/assets/images/Screenshot%202024-07-13%20at%201.08.00 PM.png)
---
### Expand row to see transformation resutls
<a name="expandit"></a>
![Screenshot 1](/controlplane/src/assets/images/Screenshot%202024-07-13%20at%202.56.21 PM.png)

## Technologies and tools in this project

Build a data transformer using restricted Python with a Web UI using [Dash](https://dash.plotly.com/). The transformer is designed to manipulate data in columns from a CSV/XLS file. The project provides a user interface (UI) that allows users to upload the CSV/XLS file and create transformers for each column using the [ACE code editor](http://ace.c9.io/).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
