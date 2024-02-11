# Merchant

## Table of Contents

- [Prerequisites](#Prerequisites)
- [Getting Started](#getting-started)
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Usage](#usage)

## Prerequisites

Before you get started, ensure you have the following requirements installed:

- [Python](https://www.python.org/)
- [Pipenv](https://pipenv.pypa.io/)

Install the necessary Python packages within a virtual environment using the following command:

```bash
pipenv install
```

## Getting Started

1. Navigate to the `api` folder.
2. Apply migrations to the database:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Introduction

The API provides functionality to handle loan and fund operations, including installment payments.

## Technologies

- Python
- Django

## Usage

1. Navigate to the `api` folder.

2. Ensure migrations are applied to the database:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

3. Start the server:

```bash
python3 manage.py runserver
```

Now you're ready to start utilizing the API for loan, fund, and installment operations.
