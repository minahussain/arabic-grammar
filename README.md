# Arabic Grammar App - Mina Hussain

## 👑  Description 

![Screenshot of App](/public/screenshot1.PNG)

A Flask + React app that processes a user input sentence in Arabic and displays the parts of speech for each word.
* Uses [camel-tools](https://github.com/CAMeL-Lab/camel_tools) to process Arabic sentence
* Referenced [Supriyo Biswas' parser](https://www.notion.so/Arabic-Grammar-Project-cdb44e57b3014af08dc1b95c2ab6cca5#e5b75ac4afb2434ab68d27566505cf0d) to build this one
* Created the pomegranate logo by building off an existing logo from Logo Creator in Figma

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## ✏️ Todo 

* Write tests
* Process definite articles
* Process verbal sentences
* Add Arabic<->English translations
    * such as: Prep (حرف جر)

## ⚙️ Installation

This program has been run and tested with Python 3.9 so please use that version 😊

Follow instructions from [python](https://www.python.org/downloads/) to install if you do not already have Python3 on your machine.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install camel-tools
```

## ⌛ Run

Using two separate terminals, run the commands:

```bash
yarn start
```

```bash
yarn start-api
```

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

## 🛠️ Test

Run the test with the following command

```bash
pytest <>.py
```

Use the -s flag to see the program's printed output

```bash
pytest -s <>.py
```