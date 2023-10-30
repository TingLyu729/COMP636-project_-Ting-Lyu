 

# Web Application Structure

## 1. Route: `/` (Home Page)
- **Template**: `base.html`
- **Data Passed from Route**: None
- **Description**: The home page serves as the main landing page of the web application. It contains the title and main menus of the web app. No specific data is passed to this template as it serves as an entry point.

## 2. Route: `/listdrivers` (List Drivers)
- **Template**: `driverlist.html`
- **Data Passed from Route**: List of drivers (`driver_list`) containing driver information like driver ID, first name, surname, date of birth, age, caregiver, car model, and drive class.
- **Description**: This route is responsible for listing all drivers and their associated car information. The `listdrivers()` function queries the database for driver details and passes this data to the `driverlist.html` template for rendering. Users can view a list of drivers and their basic information.

## 3. Route: `/listcourses` (List Courses)
- **Template**: `courselist.html`
- **Data Passed from Route**: List of courses (`course_list`) containing course details.
- **Description**: This route lists all available courses for the users. The `listcourses()` function queries the database to retrieve course details and passes this information to the `courselist.html` template, and the template retrieves courses images from the static folder, allowing users to see a list of courses.

## 4. Route: `/selectadriver` (Select a Driver)
- **Template**: `selectadriver.html`. The template takes a selected driver id from the user and sends the driver id to another Route: `/showrundetails` (Show Run Details).
- **Data Passed from Route**: List of drivers (`drivers`) for selection.
- **Description**: This route enables users to select a driver from a dropdown list. The function retrieves a list of drivers from the database and passes it to the `selectadriver.html` template. Users can choose a driver from the list.

## 5. Route: `/showrundetails` (Show Run Details)
- **Template**: `showrundetails.html`
- **Data Passed to Route**: A driver ID is passed to the route when users choose a driver from the dropdown list on the web page.
- **Data Passed from Route**: The detailed run information (`rundetails`) of this driver, including run details, driver name, car model, drive class, course name, and run total, is passed from the Route.
- **Description**: Users can choose a driver from the dropdown list and view the driver’s detailed information about a specific driver's runs. The route retrieves the relevant data from the database and passes it to the `showrundetails.html` template for rendering.

## 6. Route: `/getrundetails` (Get Run Details)
- **Template**: `getrundetails.html`
- **Data Passed to Route**: A driver id is passed to the route through the URL when users click on a driver’s name.
- **Data Passed from Route**: The detailed run information (`rundetails`) of this chosen driver, including run details, driver name, car model, drive class, course name, and run total, is then passed again to the template.
- **Description**: Similar to the "Show Run Details” route, this route allows users to view detailed information about a specific driver's runs. It receives input of a driver id from the URL and retrieves run details data from the database and passes it to the `getrundetails.html` template for rendering.

## 7. Route: `/graph` (Show Graph)
- **Template**: `top5graph.html`
- **Data Passed from Route**: Lists (`name_list` and `value_list`) for rendering the top 5 drivers in a graph.
- **Description**: Users can view a graph displaying the top 5 drivers based on their performance. The route retrieves data about the top drivers and their results and passes it to the `top5graph.html` template for graph visualization.

## 8. Route: `/overallresults` (Overall Results)
- **Template**: `overallresults.html`
- **Data Passed from Route**: List of overall results (`results`) sorted by total time.
- **Description**: This route provides an overview of the overall results for all drivers. It retrieves comprehensive results from the database and passes them to the `overallresults.html` template for display.

## 9. Route: `/administrator` (Administrator)
- **Template**: `administrator.html`
- **Data Passed from Route**: None
- **Description**: This route is dedicated to administrative functionalities and includes features accessible to administrators. It serves as a control panel for administrative tasks.

## 10. Route: `/listjuniordrivers` (List Junior Drivers)
- **Template**: `juniordriverslist.html`
- **Data Passed from Route**: List of junior drivers (`junior_drivers`) including driver ID, first name, surname, date of birth, age, caregiver, car model, and drive class.
- **Description**: Users can view a list of junior drivers in this route. It queries the database for junior driver data and passes it to the `juniordriverslist.html` template for display.

## 11. Route: `/searchdriver` (Search Driver)
- **Template**: `searchdriver.html`, the template allows users to input the search term and also render results related to the search term.
- **Data Passed to Route**: A search term is passed from the template to the route through the `search_drivers()` function when users input the search term on the webpage.
- **Data Passed from Route**:
  - Search results (`results`) containing driver details through `search_drivers(search_term)` function.
- **Description**: This route allows users to search for drivers by their first name or surname. The `searchdriver()` function handles the search query and passes the search results and the search term to the `searchdriver.html` template.

## 12. Route: `/editruns` (Edit Runs)
- **Templates**:
  - `editruns.html`, this template allows users to select a driver, a course, and a run number. It also displays the original seconds, cones, and wd and provides a form for editing them.
  - `editrunssuccess.html`, this template notifies the user that editing is successful.
  - `editrunsfail.html`, this template notifies the user that editing is not successful and informs possible reasons.
- **Data Passed from template to Route**:
  - Driver ID, course ID, and run number are passed from the template to the route when users make choices.
  - The edited run data is sent to the route when users submit the edited run information.
- **Data Passed from Route**:
  - Run details (`runs`) based on selected filter criteria.
- **Data Passed from Route to Database**:
  - New run details data is passed to the database.
- **Description**: Users can edit run details for drivers in this route. The route provides options to filter runs by driver, course, and run number. It retrieves the relevant data and passes it to the `editruns.html` template for editing. It then updates the database.

## 13. Route: `/adddriver` (Add Driver)

- **Template**:
  - `adddriver.html`
  - `adddriversuccess.html`: Provides a success message after successfully adding a driver.
  - `adddriverfail.html`: If there is an issue while adding a driver, this route displays a failure message including possible causes of failure.

- **Data Passed from Route to Template**:
  - Lists of cars and caregivers for dropdown selection.

- **Data Passed from Template to Route**:
  - New driver’s first name, surname, selected car number.
  - Junior driver’s date of birth and caregiver.

- **Data Passed from Route to Database**:
  - Driver’s info including name, care, age, and caregiver, and empty value for run details for the eight runs.

- **Description**: Users can add new drivers through this route. It offers a form for adding driver information, including the driver's name, car, age for junior driver, and caregiver for junior drivers under 16. It provides dropdowns for car selection and caregiver selection. It then creates a new driver and eight runs with empty run data for this driver in the database.

# Assumptions and design decisions

## Assumptions
    - It is assumed that the MySQL database exists with the required tables (driver, car, course, and run) and their fields.
    - All existing data in the database are valid.
    - The database structure is assumed to be consistent with the code and template requirements.
    - The connect module contains valid database connection information.
    - There is some sort of implementation of authorization to restrict access to the administrator interface.
    - Application is secure against common web vulnerabilities, such as SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF).
    - Drivers are all over 12 years old.
    - For junior drivers, caregivers are assigned based on age and are assumed to be 16 years or older.

## Design Decisions
    - Use of Flask: Flask was chosen as the web framework for its simplicity and flexibility.
    - Database Structure: The application uses a relational database to store information about drivers, cars, courses, and runs.
    - SQL Queries: Direct SQL queries are used to retrieve data from the database, but parameterized queries should be used for security.
    - Templates: HTML templates are used to separate the presentation layer from the logic.
    - Data Flow: Data is fetched from the database in route functions and passed to templates for rendering.
    - Junior Drivers: Drivers are categorized as junior if their age is under 18. Caregivers are assigned based on age.
    - Web Forms: Forms are used for adding drivers and editing run details.
    - Error Handling: Basic error handling is implemented, but more robust error handling and validation should be added.


*Database Questions*
**What SQL statement creates the car table and defines its three fields/columns? (Copy and paste the relevant lines of SQL.)**

CREATE TABLE IF NOT EXISTS car
(
car_num INT PRIMARY KEY NOT NULL,
model VARCHAR(20) NOT NULL,
drive_class VARCHAR(3) NOT NULL
);

**Which line of SQL code sets up the relationship between the car and driver tables?**
FOREIGN KEY (car) REFERENCES car(car_num)


**Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?**

INSERT INTO car VALUES
(11,'Mini','FWD'),
(17,'GR Yaris','4WD'),

**Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)**
We just need to set a default value of 'RWD' for the drive_class field in the car tableHere's the modified SQL statement:
CREATE TABLE IF NOT EXISTS car
(
car_num INT PRIMARY KEY NOT NULL,
model VARCHAR(20) NOT NULL,
drive_class VARCHAR(3) DEFAULT ‘RWD’ NOT NULL
);


**Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.**

It is important for drivers and the club admin to access different routes in a web application for several reasons:

1. ***Data Integrity***: Club admins are responsible for maintaining the integrity of the data in the system, including race results, driver profiles, and course information. By segregating routes, the admin can ensure that data remains accurate and reliable. Allowing drivers to access admin routes could lead to accidental or intentional data manipulation, leading to inaccurate records. 
2. ***Accountability***: Separating routes and controlling access helps in maintaining accountability. If all facilities were available to everyone, it would be challenging to identify who made specific changes or performed certain actions within the web application. By assigning specific routes to different user roles, it becomes easier to track and audit user activities.

3. ***Compliance***: In certain industries and applications, there may be legal or regulatory requirements that mandate separation of duties and data access. Compliance with these regulations is essential to avoid legal issues and fines.



