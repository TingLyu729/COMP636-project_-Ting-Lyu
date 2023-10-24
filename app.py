from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/listdrivers")
def listdrivers():
    connection = getCursor()
    # Select necessary data from driver and car tables and join them
    query = """
    SELECT driver.driver_id, driver.first_name, driver.surname, driver.date_of_birth,
           driver.age, driver.caregiver, car.model, car.drive_class
    FROM driver
    INNER JOIN car ON driver.car = car.car_num
    ORDER BY driver.surname, driver.first_name
    """ 
    connection.execute(query)
    driverList = connection.fetchall()
    return render_template("driverlist.html", driver_list = driverList)    

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("courselist.html", course_list = courseList)
    
@app.route("/selectadriver")
def selectadriver():
    connection = getCursor()
    # Fetch the driver's details from the database using the provided driver_id                 
    query = """
    SELECT * FROM driver
    """
    connection.execute(query)
    drivers = connection.fetchall()
    print(drivers)


    # Pass the drivers list to the template
    return render_template('selectadriver.html', drivers = drivers)


@app.route("/showrundetails", methods=["POST"])
def showrundetails():
    driverid = request.form.get("driver_id")
    if driverid:
        print("Selected driver ID:", driverid)
        connection = getCursor()
        query = """
        SELECT run.*, 
        driver.first_name,
        driver.surname,
        car.model, 
        car.drive_class,
        course.name,
        ROUND((run.seconds + (COALESCE(run.cones, 0) * 5) + (run.wd * 10)), 2) AS run_total

        FROM run
        INNER JOIN course ON run.crs_id = course.course_id
        INNER JOIN driver ON run.dr_id = driver.driver_id
        INNER JOIN car ON driver.car = car.car_num
        WHERE dr_id = %s;
        """
        parameters = (driverid,)
        connection.execute(query, parameters)
        run_Details = connection.fetchall()
        return render_template("showrundetails.html", rundetails = run_Details)

@app.route("/getrundetails", methods=["GET"])
def getrundetails():
    driverid = request.args.get("driver_id")
    if driverid:
        print("Selected driver ID:", driverid)
        connection = getCursor()
        query = """
        SELECT run.*, 
        driver.first_name,
        driver.surname,
        car.model, 
        car.drive_class,
        course.name,
        ROUND((run.seconds + (COALESCE(run.cones, 0) * 5) + (run.wd * 10)), 2) AS run_total

        FROM run
        INNER JOIN course ON run.crs_id = course.course_id
        INNER JOIN driver ON run.dr_id = driver.driver_id
        INNER JOIN car ON driver.car = car.car_num
        WHERE dr_id = %s;
        """
        parameters = (driverid,)
        connection.execute(query, parameters)
        run_Details = connection.fetchall()
        return render_template("getrundetails.html", rundetails = run_Details)

@app.route("/graph")
def showgraph():
    connection = getCursor()
    # Insert code to get top 5 drivers overall, ordered by their final results.
    # Use that to construct 2 lists: bestDriverList containing the names, resultsList containing the final result values
    # Names should include their ID and a trailing space, eg '133 Oliver Ngatai '
    query = """
    WITH RankedRuns AS (
    SELECT
        driver.driver_id,
        CASE WHEN driver.age <= 18 THEN CONCAT(driver.first_name, ' ', driver.surname, ' (J)') ELSE CONCAT(driver.first_name, ' ', driver.surname) END AS driver_name,
        car.model,
        course.name AS course_name,
        COALESCE(
            CASE
                WHEN run1.seconds IS NULL AND run2.seconds IS NULL THEN NULL  -- 'dnf' if both runs are NULL
                WHEN run1.seconds IS NULL THEN run2.seconds + (COALESCE(run2.cones, 0) * 5) + (run2.wd * 10)  -- Use the second run if the first is NULL
                WHEN run2.seconds IS NULL THEN run1.seconds + (COALESCE(run1.cones, 0) * 5) + (run1.wd * 10)  -- Use the first run if the second is NULL
                ELSE LEAST(
                    run1.seconds + (COALESCE(run1.cones, 0) * 5) + (run1.wd * 10),
                    run2.seconds + (COALESCE(run2.cones, 0) * 5) + (run2.wd * 10)
                )
            END, 'dnf'
        ) AS course_time
    FROM
        run
        INNER JOIN course ON run.crs_id = course.course_id
        INNER JOIN driver ON run.dr_id = driver.driver_id
        INNER JOIN car ON driver.car = car.car_num
        LEFT JOIN run AS run1 ON driver.driver_id = run1.dr_id AND course.course_id = run1.crs_id AND run1.run_num = 1
        LEFT JOIN run AS run2 ON driver.driver_id = run2.dr_id AND course.course_id = run2.crs_id AND run2.run_num = 2
    )
    SELECT
        driver_id,
        driver_name,
        model,
        MIN(CASE WHEN course_name = 'Cracked Fluorescent' THEN ROUND(course_time, 2) END) AS 'Cracked Fluorescent Course time',
        MIN(CASE WHEN course_name = 'Going Loopy' THEN ROUND(course_time, 2) END) AS 'Going Loopy Course time',
        MIN(CASE WHEN course_name = 'Hamburger' THEN ROUND(course_time, 2) END) AS 'Hamburger Course time',
        MIN(CASE WHEN course_name = "Mum's Favourite" THEN ROUND(course_time, 2) END) AS "Mum's Favourite Course time",
        MIN(CASE WHEN course_name = 'Shoulders Back' THEN ROUND(course_time, 2) END) AS 'Shoulders Back Course time',
        MIN(CASE WHEN course_name = 'Walnut' THEN ROUND(course_time, 2) END) AS 'Walnut Course time',
        CASE
            WHEN COUNT(DISTINCT course_name) < 6 OR SUM(CASE WHEN course_time = 0 THEN 1 ELSE 0 END) > 0 THEN 'NQ'
            ELSE ROUND(SUM(course_time) / 2, 2)
            END AS total_time
        FROM RankedRuns
        GROUP BY driver_id, driver_name, model
        ORDER BY total_time;
    """
    connection.execute(query)
    overall_results = connection.fetchall()
    bestDriverList = []
    resultsList = []
    for i in range(5):
        bestDriverList.append(f"{ overall_results[i][0]}  {overall_results[i][1]} ")
        resultsList.append(overall_results[i][-1])
    bestDriverList.reverse()
    resultsList.reverse()
    return render_template("top5graph.html", name_list = bestDriverList, value_list = resultsList)

@app.route("/overallresults")
def overallresults():
    connection = getCursor()
    query = """
    WITH RankedRuns AS (
    SELECT
        driver.driver_id,
        CASE WHEN driver.age <= 18 THEN CONCAT(driver.first_name, ' ', driver.surname, ' (J)') ELSE CONCAT(driver.first_name, ' ', driver.surname) END AS driver_name,
        car.model,
        course.name AS course_name,
        COALESCE(
            CASE
                WHEN run1.seconds IS NULL AND run2.seconds IS NULL THEN NULL  
                WHEN run1.seconds IS NULL THEN ROUND(run2.seconds + (COALESCE(run2.cones, 0) * 5) + (run2.wd * 10),2)  -- Use the second run if the first is NULL
                WHEN run2.seconds IS NULL THEN ROUND(run1.seconds + (COALESCE(run1.cones, 0) * 5) + (run1.wd * 10),2)  -- Use the first run if the second is NULL
                ELSE ROUND(LEAST(
                    run1.seconds + (COALESCE(run1.cones, 0) * 5) + (run1.wd * 10),
                    run2.seconds + (COALESCE(run2.cones, 0) * 5) + (run2.wd * 10)
                ),2)
            END, 'dnf'
        ) AS course_time
    FROM
        run
        INNER JOIN course ON run.crs_id = course.course_id
        INNER JOIN driver ON run.dr_id = driver.driver_id
        INNER JOIN car ON driver.car = car.car_num
        LEFT JOIN run AS run1 ON driver.driver_id = run1.dr_id AND course.course_id = run1.crs_id AND run1.run_num = 1
        LEFT JOIN run AS run2 ON driver.driver_id = run2.dr_id AND course.course_id = run2.crs_id AND run2.run_num = 2
    )
    SELECT
        driver_id,
        driver_name,
        model,
        MIN(CASE WHEN course_name = 'Cracked Fluorescent' THEN course_time END) AS 'Cracked Fluorescent Course time',
        MIN(CASE WHEN course_name = 'Going Loopy' THEN course_time END) AS 'Going Loopy Course time',
        MIN(CASE WHEN course_name = 'Hamburger' THEN course_time END) AS 'Hamburger Course time',
        MIN(CASE WHEN course_name = "Mum's Favourite" THEN course_time END) AS "Mum's Favourite Course time",
        MIN(CASE WHEN course_name = 'Shoulders Back' THEN course_time END) AS 'Shoulders Back Course time',
        MIN(CASE WHEN course_name = 'Walnut' THEN course_time END) AS 'Walnut Course time',
        CASE
            WHEN COUNT(DISTINCT course_name) < 6 OR SUM(CASE WHEN course_time = 0 THEN 1 ELSE 0 END) > 0 THEN 'NQ'
            ELSE ROUND(SUM(course_time) / 2, 2)
            END AS total_time
        FROM RankedRuns
        GROUP BY driver_id, driver_name, model
        ORDER BY total_time;
    """
    connection.execute(query)
    overall_results = connection.fetchall()
    new_results = []
    for i, result in enumerate(overall_results):
        result_with_index = result + (i,) 
        new_results.append(result_with_index)  
    print(new_results)
                          
    return render_template("overallresults.html", results = new_results)

@app.route("/administrator")
def administrator():
    return render_template("administrator.html")

@app.route("/listjuniordrivers")
def listjuniordrivers():
    connection = getCursor()
    
    # Select junior drivers including any caregiver names and order them by age, then by surname.
    query = """
    SELECT
    junior.driver_id AS junior_driver_id,
    junior.first_name AS junior_first_name,
    junior.surname AS junior_surname,
    junior.date_of_birth AS junior_date_of_birth,
    junior.age AS junior_age,
    junior.caregiver AS caregiver_id,
    caregiver.first_name AS caregiver_first_name,
    caregiver.surname AS caregiver_surname,
    car.model,
    car.drive_class
    FROM driver AS junior
    INNER JOIN car ON junior.car = car.car_num
    LEFT JOIN driver AS caregiver ON junior.caregiver = caregiver.driver_id
    WHERE junior.age >= 12 AND junior.age <= 25
    ORDER BY junior.age DESC, junior.surname ASC
    """
    connection.execute(query)
    junior_drivers = connection.fetchall()
    print(junior_drivers)
    return render_template("juniordriverslist.html", junior_drivers=junior_drivers)



@app.route("/searchdriver", methods=["GET", "POST"])
def searchdriver():
    if request.method == "POST":
        # Handle the search form submission
        search_term = request.form.get("search_term")
        results = search_drivers(search_term)
        return render_template("searchdriver.html", results=results, search_term=search_term)
    else:
        # Display the search form
        return render_template("searchdriver.html")
    
def search_drivers(search_term):
    connection = getCursor()
    # Perform a search for drivers with a partial text match in first name or surname
    query = """
    SELECT driver.driver_id, driver.first_name, driver.surname, driver.date_of_birth,
    driver.age, driver.caregiver, car.model, car.drive_class
    FROM driver
    INNER JOIN car ON driver.car = car.car_num 
    WHERE first_name LIKE %s OR surname LIKE %s
    ORDER BY driver.surname, driver.first_name
    """
    parameters = (f"%{search_term}%", f"%{search_term}%")
    connection.execute(query, parameters)
    search_results = connection.fetchall()

    return search_results



@app.route("/editruns", methods=["GET", "POST"])
def editruns():
    connection = getCursor()
    connection.execute("SELECT driver_id, first_name, surname FROM driver")
    drivers = connection.fetchall()
    connection = getCursor()
    connection.execute("SELECT course_id, name FROM course")
    courses = connection.fetchall()
    run_nums = [1,2]
 
    driver_id = request.args.get("driver_id")
    course_id = request.args.get("course_id")
    run_num = request.args.get("run_num")
    

    
    if driver_id and course_id and run_num:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE dr_id = %s AND crs_id = %s AND run_num = %s"
        connection.execute(query, (driver_id, course_id, run_num))
        runs =connection.fetchall()
        print(runs)

    elif driver_id and course_id:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE dr_id = %s AND crs_id = %s"
        connection.execute(query, (driver_id, course_id),)
        runs =connection.fetchall()
        print(runs)
        
    elif driver_id and run_num:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE dr_id = %s AND run_num = %s"
        connection.execute(query, (driver_id, run_num),)
        runs =connection.fetchall()

    elif course_id and run_num:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE crs_id = %s AND run_num = %s"
        connection.execute(query, (course_id, run_num),)
        runs =connection.fetchall()
       
    elif driver_id:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE dr_id = %s"
        connection.execute(query, (driver_id,))
        runs =connection.fetchall()

    elif course_id:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE crs_id = %s"
        connection.execute(query, (course_id,))
        runs =connection.fetchall()

    elif run_num:
        connection = getCursor()
        query = "SELECT run.*, course.name, driver.first_name, driver.surname " \
        "FROM run " \
        "INNER JOIN course ON run.crs_id = course.course_id " \
        "INNER JOIN driver ON run.dr_id = driver.driver_id " \
        "WHERE run_num = %s"
        connection.execute(query, (run_num,))
        runs =connection.fetchall()
    else:
        runs = []

    if request.method == "POST":
        # Get and update run information
        dr_id = request.form.get("dr_id")
        crs_id = request.form.get("crs_id")
        run_num = request.form.get("run_num")
        seconds = request.form.get("seconds")
        cones = cones if request.form.get("cones") else None
        wd = 1 if request.form.get("wd") else 0

        update_query = "UPDATE run SET seconds = %s, cones = %s, wd = %s WHERE dr_id = %s AND crs_id = %s AND run_num = %s"
        connection.execute(update_query, (seconds, cones, wd, dr_id, crs_id, run_num )) 
        return render_template('editrunsuccess.html')
        # else:
        #     return render_template('editrunfail.html')   
    
    return render_template(
            "editruns.html",
            drivers=drivers,
            courses=courses,
            run_nums= run_nums,
            runs=runs,
    )
            

@app.route('/adddriver', methods=['GET', 'POST'])
def adddriver():

    connection = getCursor()
    query = "SELECT * FROM car"
    connection.execute(query)
    cars =connection.fetchall()

    connection = getCursor()
    query = "SELECT * FROM driver WHERE driver.age IS NULL"
    connection.execute(query)
    caregivers =connection.fetchall()

    if request.method == 'POST':
        is_junior = request.form.get("is_junior") == "on"
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        car_num = request.form.get('car_num')

        date_of_birth = None
        if is_junior and request.form.get('date_of_birth'):
            date_of_birth = request.form.get('date_of_birth')            

        caregiver = None
        if is_junior and request.form.get('caregiver'):
            caregiver = request.form.get('caregiver')  

        age = None
        if is_junior and date_of_birth:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
            current_date = datetime.now()
            age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
      
        if age and age < 12:
            return render_template('adddriverfail.html')
        if age and age < 16 and caregiver is None:
            return render_template('adddriverfail.html')
        else:
            try:
                connection = getCursor()
                connection.execute("INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, surname, date_of_birth, age, caregiver, car_num))
            except:
                return render_template('adddriverfail.html')

# Retrieve the auto-generated driver_id
        driver_id = connection.lastrowid
 
        allcourseid = getallcourseid()

        for courseid in allcourseid:
            for run_num in [1,2]:
                connection = getCursor()
                connection.execute("INSERT INTO run (dr_id, crs_id, run_num, seconds,cones, wd) VALUES (%s, %s, %s, %s, %s, %s)", (driver_id, courseid, run_num, None, None, 0))


            # Redirect to a success page or display a success message
            # flash("Driver added successfully", 'success')
        return render_template('adddriversuccess.html')

    # Handle GET request (show the form)
    # Query the database to get a list of cars and caregivers for dropdowns

    return render_template('adddriver.html', cars=cars, caregivers=caregivers)

def getallcourseid():
        connection = getCursor()
        connection.execute("SELECT * from course")
        courses = connection.fetchall()
        allcourseid = []
        for course in courses:
            allcourseid.append(course[0])
        return allcourseid


    




