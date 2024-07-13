# Xformer Builder

This project is for learning purposes only and aims to demonstrate how to build a data transformer using restricted Python with a Web UI using [Dash](https://dash.plotly.com/). The transformer is designed to manipulate data in columns from a CSV file. The project provides a user interface (UI) that allows users to upload the CSV file and create transformers for each column using the [ACE code editor](http://ace.c9.io/).

Questions: [Ask Here](https://github.com/marcelonyc/xformer-builder/labels/question)
## Features

- Upload CSV file: Users can easily upload their desired CSV file through the user interface.
- Column transformers: The project allows users to create transformers for each column using the ACE code editor.
- Restricted Python: The data transformer utilizes restricted Python to ensure secure and controlled data manipulation.


## Getting Started

To get started with Xformer Builder, follow these steps:

1. Clone the repository: `git clone https://github.com/marcelonyc/xformer-builder`
2. Run setup.sh 
    - Requires Python > 3.10 
3. cd to the `coding` directory
4. Run `python dash_app.py`
4. Access the application through your web browser at `http://localhost:8050`

## Usage

1. Upload CSV file: Click on "Upload Sample CSV file" and select the desired CSV file from your local machine.
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

## Contributing

Contributions are welcome! If you would like to contribute to Xformer Builder, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## Screensghots
## Screenshots

Here are some screenshots of the Xformer Builder application:

![Screenshot 1](/coding/assets/images/Screenshot%202024-07-13%20at%2012.52.17 PM.png)
---
![Screenshot 1](/coding/assets/images/Screenshot%202024-07-13%20at%201.08.00 PM.png)
---
### Expand row to see transformation resutls
<a name="expandit"></a>
![Screenshot 1](/coding/assets/images/Screenshot%202024-07-13%20at%202.56.21 PM.png)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
