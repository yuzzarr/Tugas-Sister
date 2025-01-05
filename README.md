# REST - SOAP API Implementation

S1 Informatika FATISDA UNS  
Program Studi Informatika

## Members
- Yuzzar Rizky Mahendra (M0521082)
- Rizki Dwi Rahmawan (M0521066)

## Prerequisite
- Python 3.10.10
> Download Python 3.10.10 [Here](https://www.python.org/downloads/release/python-31010/)
>
- python path is declared in system environment
> Refer to tutorial [Here](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))

> Path to add (refer to your installation path)
>
>"D:\Program Files\Python310\" & "C:\Program Files\Tesseract-OCR" 

## Installation REST API

Run REST Server
```bash
  py app.py
```


## Installation SOAP API

Install Dependencies and Create Virtual Environment

```bash
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
```
    
Run SOAP Server 
```bash
  py soap_server.py
```

Run Python Program to Call SOAP API
```bash
  py pythonsoap.py
```
