# actionsheets-streamlit
Streamlit front-end for the [actionsheets package](https://github.com/niekdt/actionsheets).
The app features a large collection of detailed cheatsheets for Python and R that I’ve created over the years. 
The name “actionsheets” comes from the way the sheets are structured: code snippets are indexed in terms of a desired action, and are grouped in sections.

What separates this app from typical cheatsheet websites is that the sheets are dynamically rendered from a data source. 
This enables search functions for sheets and snippets, and generating filtered sheets.

![afbeelding](https://github.com/user-attachments/assets/8999e0c0-f7d5-4c16-9f19-6768000f4ec4)


### Quick search for snippets
![afbeelding](https://github.com/user-attachments/assets/8e8fe91f-99a1-439e-9128-8e35559ee378)



## Usage
To start the dashboard locally, run:
```shell
streamlit run app.py
```

## Development
This project uses Poetry to manage dependencies. To install the dependencies, run:
```shell
poetry install
```

To update dependencies, run:

```shell
poetry update
```
