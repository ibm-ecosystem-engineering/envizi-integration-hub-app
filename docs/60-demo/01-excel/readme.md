
# Demo Script - Excel Data Processing

Here is the demo script for the Excel Integration of the Integration Hub.

## Steps

### Excel Mappings list

1. Click on the menu `Excel`. 

It will show the Excel Mappings list as given below.

2. Click on the `C-Corp Travel Data` link to open the mapping details page.

<img src="images/image11.png">

### Excel Mapping Detail

Here is the mapping details page. If you want, you can change the mapping as per your need here and save.

Here is the detail about the mapping

- **Organization :** This column is hard coded with the `IBM APAC` text.
- **Location :** This column is mapped to the `Places` column of the excel.
- **Account Number :** This column is mapped to the `Subject Name` column of the excel.
- **Total cost (incl. Tax) in local currency :** This column is mapped to the sum of `Cost A` + `Cost B` + `Cost C` columns of the excel.


<img src="images/image12-1.png">
<img src="images/image12-2.png">
<img src="images/image12-3.png">



### Upload Excel

3. Click on the `Choose file` button to upload your excel file.

<img src="images/image13.png">

4. Select the file [TravelData.xlsx](./files/TravelData.xlsx) available in this repo.

<img src="images/image14.png">

The content of the excel file is like this.

<img src="images/image15.png">


### Load Source Data

After loading the Excel file, its columns are added to the dropdown lists of the mapping section. 

5. Click on the `Load Source Data` button to load the excel file columns into the mapping section.

<img src="images/image16.png">

6. The excel file columns are loaded. You can see the columns in the drop down list.

<img src="images/image17.png">

7. You can change the mapping as per your need here and `Save`.

### Preview

8. Click on the `Preview` button to to see how the Excel data is converted in the Envizi POC template format based on the mapping.

<img src="images/image18.png">

The preview data is displayed here.

<img src="images/image19.png">


### Ingest to Envizi

9. Click on the `Ingest to Envizi` button to push the converted Excel data into Envizi.

<img src="images/image20.png">

The data is pushed to Envizi.

<img src="images/image21.png">