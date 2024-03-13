# Envizi Integration Hub 

Envizi Integration Hub facilitates the integration of data from various external systems into the IBM Envizi ESG Suite.

It connects to external systems, such as Turbonomic, retrieves emissions data, converts this data into the Universal Account Setup and Data Loading format (UDC), and then dispatches it to an S3 bucket configured within the IBM Envizi ESG Suite.

<img src="/docs/images/img-11-arch.png">

Note: Tririga is mentioned in the diagram is for understanding purpose. It is not integrated yet in Hub.

Here are some documentations about this Integration Hub App.

### 1. Create Data Service and Data Pipeline in Envizi

Envizi Integration Hub leverages  Envizi Data Service and Envizi Data Pipeline to integrate external systems into in Envizi. Refer the link [Create Dataservice in Envizi](./docs/01-readme_create_dataservice_in_envizi.md)

### 2. Prepare Configuration file 

Prepare Configuration file by using the link [Prepare Configuration file](./docs/02-readme_prepare_config_file.md)

### 3. Start the App

You can start the app 

Using the Docker [03-1-readme_start_app_via_docker.md](./docs/03-1-readme_start_app_via_docker.md)

or

Using the Python source code [03-2-readme_start_app_via_src.md](./docs/03-2-readme_start_app_via_src.md)

### 4. Update Configuration settings in the App

Refer [04_update_configuration_settings_in_the_app.md](./docs/04_update_configuration_settings_in_the_app.md)

### 5. Ingest Turbonomic Data into Envizi via the App

Refer [05_ingest_turbonomic_data_into_envizi_via_the_app.md](./docs/05_ingest_turbonomic_data_into_envizi_via_the_app.md)

### 6. View the Turbonomic Data in Envizi
Refer [06_view_the_turbonomic_data_in_envizi.md](./docs/06_view_the_turbonomic_data_in_envizi.md)

### 7. Copying UI (ReactJs) files to Python App
How to Copy UI (ReactJs) files to Python App. [11-readme_copying_reactjs_to_python.md](./docs/11-readme_copying_reactjs_to_python.md)

### 8. Creating Docker Image of the App
How to create Docker image for this app. [21-readme_create_docker_images.md](./docs/21-readme_create_docker_images.md)

### 9. Envizi Integration Hub - Excel Template Processing.
How to use excel template processing. [07_excel_template-processing.md](./docs/07_excel_template-processing.md)

### 10. How to extend this app 
How to extend this app for integrating with other systems like Tririga, Maximo and etc [31-how_to_extend_this_app.md](./docs/31-how_to_extend_this_app.md)