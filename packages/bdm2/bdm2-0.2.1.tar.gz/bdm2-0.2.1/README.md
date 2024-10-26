# birdoo_data_manager_2

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)

[comment]: <> (![Build Status]&#40;https://img.shields.io/travis/com/username/repository&#41;)

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Installation](#Installation)


## Project Description

**Birdoo Data Manager 2** is a project aimed at maintaining and validating the Birdoo system. The project focuses on two primary areas:

1. **Data Validation, Processing, and Generation**: This aspect of the project ensures that all data related to the Birdoo system is accurate, consistent, and up-to-date. It includes various tools and processes for validating incoming data, processing it for use within the system, and generating new data as needed.

2. **Release Management System**: This component of the project manages the release process for the Birdoo system. It includes tools and workflows for preparing, testing, and deploying new releases, ensuring that updates are delivered smoothly and efficiently.

By addressing these two key areas, Birdoo Data Manager 2 aims to enhance the reliability and performance of the Birdoo system, providing a robust framework for ongoing development and maintenance.






## Features

### Data Validation, Processing, and Generation
- **Data Validation**: Ensures accuracy and consistency of incoming data.
- **Data Processing**: Efficiently processes data for integration into the Birdoo system.
- **Data Generation**: Generates new data as needed for various system requirements.

### Release Management System
- **Release Preparation**: Tools and workflows for preparing new releases.
- **Testing**: Comprehensive testing tools to ensure the quality and stability of releases.
- **Deployment**: Streamlined deployment processes for smooth and efficient updates.

### Additional Features
- **Configurable Settings**: Customize various aspects of data validation and release management to suit different needs.
- **Scalability**: Designed to handle growing data and system demands.
- **Robust Logging**: Detailed logging for tracking data processing and release activities.
- **User-Friendly Interface**: Intuitive interface for managing data and releases.

## Installation

### Prerequisites


- [Python 3.9+](https://www.python.org/downloads/)
- [poetry](https://python-poetry.org/docs/)
- [pip](https://pip.pypa.io/en/stable/installation/)
### Steps
 **Initial installation and configuration of poetry**

skip this part if you've installed poetry.

How to implement it: 
Install Poetry in the conda base environment.
```
pip install poetry
```
Specify the directory containing Poetry's conda environments as the default environments folder.
```
poetry configuration virtualenvs.path C:\Users\Your_user\anaconda3\envs
```

Explain that you do not need to create the environment yourself 
```
poetry config virtualenvs.create false
```
1. **Clone the repository**
```
   git clone https://<token_name>:<token>@kgitlab.knexinc.com/pawlin_birdoo/birdoo-data-manager.git -b feature/full_refactor
```
2.  **Creating an Environment | installing dependencies**
  ``` 
conda create <env name> python=<3.9>
conda activate <env name> 
cd <project dir>
pip install poetry 

poetry install
  ```
3. **get .env file from server and set environment variable**
- get .env file from \\Datasets\chikens\configs\credentials\BDM2\.env
- set on your machine environment_variable "BIRDOO_CREDS_PATH" to your .env copied to project root or path to file on server
