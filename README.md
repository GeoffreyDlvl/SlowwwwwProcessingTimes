# Slowwwww Processing Times

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#upload-an-archive">Upload an archive</a></li>
        <li><a href="#check-archive-status">Check archive status</a></li>
        <li><a href="#crack-an-archive">Crack an archive</a></li>
        <li><a href="#get-jobs-limit">Get jobs limit</a></li>
        <li><a href="#set-jobs-limit">Set jobs limit</a></li>
        <li><a href="#append-some-processing">Append some processing</a></li>
      </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project
This project is a simple back-end implementation of the following exercice: https://www.notion.so/Back-Slowwwww-processing-times-a9f751385277466ca00e5ee0b69280dc
### Built With
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* See `requirements.txt` to read about specific tools required to build and run the project.

## Getting Started
### Prerequisites
Be sure that `python 3.9.6` and `pip` are installed on your system.
All requires dependencies are listed in `requirements.txt`. See <a href="#installation">Installation</a> for detailed steps on how to create your virtual environment. 

### Installation
> Instructions displayed in this file assume you are running the app on a Windows OS. If your system is different, simply replace the commands with the corresponding Unix/macOS equivalent.
1. Clone the repo:
  ```sh
  git clone https://github.com/GeoffreyDlvl/SlowwwwwProcessingTimes.git
  ```
2. Create a new virtual environment:
  ```sh
  py -m venv env
  ```
  > The environment is named `env` and can be activated with the following command:
  > ```sh
  > .\env\Scripts\activate
  > ```
  > Leave the virtual environment with the `deactivate` command.
3. Automatically install all dependencies:
  ```sh
  py -m pip install -r requirements.txt
  ```
4. Initalize / reset database:
  ```sh
  flask init-db
  ```
6. Start the application:
  ```sh
  .\run_windows_dev.bat 
  ```
  > If you are running on a linux system, run `run_linux_dev.sh` instead.

  This will start a lightweight local development server on your machine. The application runs on `localhost:5000`. 

## Usage
This project is a back-end implementation. As a result, requests must be sent over HTTP if you want to interact with it.
To illustrate the different routes and features available, we will be using [Postman](https://www.postman.com/). It is advised to download the client to bypass web-browser limitations.

### Upload an archive
![Upload_archive](/docs/upload-archive.png?raw=true)
* Route: http://127.0.0.1:5000/archive/upload
* Method: POST
* Body: multipart/form-data

### Check archive status
![Info_archive](/docs/info-archive.png?raw=true)
* Route: http://127.0.0.1:5000/archive/info
* Method: POST
* Enctype: application/json
  * key: filename
  * value: name of the archive (extension included)

### Crack an archive
![Crack_archive](/docs/crack-archive.png?raw=true)
* Route: http://127.0.0.1:5000/crack/
* Method: POST
* Enctype: application/json
  * key: filename
  * value: name of the archive (extension included)
> Mock behavior: waits for 10 seconds

### Get jobs limit
![Get_jobs_limit](/docs/get-jobs-limit.png?raw=true)
* Route: http://127.0.0.1:5000/crack/jobs
* Method: GET

### Set jobs limit
![Set_jobs_limit](/docs/set-jobs-limit.png?raw=true)
* Route: http://127.0.0.1:5000/crack/jobs
* Method: POST
* Enctype: application/json
  * key: jobs_limit
  * value: the new jobs limit

### Append some processing
![Some_processing](/docs/some-processing.png?raw=true)
* Route: http://127.0.0.1:5000/processing/some_processing
* Method: POST
* Enctype: application/json
  * key: filename
  * value: name of the archive (extension included)
> Mock behavior: waits for 10 seconds. \
> Multiple processing operations can be added in a queue.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Geoffrey Delval \<geoffrey.dlvl@gmail.com\> \
Project Link: [https://github.com/GeoffreyDlvl/SlowwwwwProcessingTimes](https://github.com/GeoffreyDlvl/SlowwwwwProcessingTimes)
