# actionsheets-streamlit
Streamlit front-end for the [actionsheets package](https://github.com/niekdt/actionsheets).
The app features a large collection of detailed cheatsheets for Python and R that I’ve created over the years. 
The name “actionsheets” comes from the way the sheets are structured: code snippets are indexed in terms of a desired action, and are grouped in sections.

What separates this app from typical cheatsheet websites is that the sheets are dynamically rendered from a data source. 
This enables search functions for sheets and snippets, and generating filtered sheets.

![dashboard](https://github.com/user-attachments/assets/c5ff5472-a80e-4228-af1f-fea9f55c024a)

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
poetry export --without-hashes -f requirements.txt > requirements.txt
```
