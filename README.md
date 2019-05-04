# Ingredients Label Application

This is the group project for CPSC 462.

Group Members:
* Phoebe Shieh
* Don Vu
* Henry Ho
* Gabriel Varela
* Liang Leon Zhao

# Quick start
To access the application server:

1. Navigate to the URL: http://thinkhealthy.ggvarela.com
2. Click on the Upload Image tab on the top right to be taken to the image upload feature
3. Choose a photo of an ingredients label to upload to the server
4. The application will then display a table of unhealthy ingredients contained in the label


To install:

1. Download the code to a directory 
2. Start up the virtual environment of your choice
3. In the directory, open a terminal and install the libraries required with this command: 
    ```
    pip install -r requirements.txt
    ```
4. Install Tesseract with this command:
    ```
    sudo apt-get install tesseract-ocr
    ```
5. Run the application with these commands in the parent folder of ingredients-label folder:
    ```
    export FLASK_APP=ingredients-label
    flask run
    ```
6. Open a web browser and navigate to the ip address displayed in the terminal e.g:
   ```
   127.0.0.1:5000
   ```
7. A set of tested ingredients labels are available in the Labels folder. Choose one of those images for the application to process and it will return the results of the analysis.
