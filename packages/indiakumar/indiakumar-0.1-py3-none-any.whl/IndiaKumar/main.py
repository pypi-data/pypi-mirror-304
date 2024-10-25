import requests
import json

Email = """
// -- npm install nodemailer

var nodemailer = require('nodemailer');

var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'youremail@gmail.com',
    pass: 'yourpassword'
  }
});

var mailOptions = {
  from: 'youremail@gmail.com',
  to: 'myfriend@yahoo.com',
  subject: 'Sending Email using Node.js',
  text: 'That was easy!'
};

transporter.sendMail(mailOptions, function(error, info){
  if (error) {
    console.log(error);
  } else {
    console.log('Email sent: ' + info.response);
  }
});


// Run the code

"""

SERVER = """
const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World!\n');
});
server.listen(3000, '127.0.0.1', () => {
  console.log('Listening on 127.0.0.1:3000');
});
"""

NOSQL = """
// -- npm install mongodb

// Database Connection
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/mydb";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  console.log("Database created!");
  db.close();
});

// -- Create Collection 
MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("mydb");
  dbo.createCollection("customers", function(err, res) {
    if (err) throw err;
    console.log("Collection created!");
    db.close();
  });
});


// -- Insert into Collection 
MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("mydb");
  var myobj = { name: "Company Inc", address: "Highway 37" };
  dbo.collection("customers").insertOne(myobj, function(err, res) {
    if (err) throw err;
    console.log("1 document inserted");
    db.close();
  });
});

// Find into Collection 

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("mydb");
  dbo.collection("customers").findOne({}, function(err, result) {
    if (err) throw err;
    console.log(result.name);
    db.close();
  });
});


// Run the code
"""

SQL = """
// --- npm install mysql

var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database:"mydb" // add after Database creation
});


// --- Create Database
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  con.query("CREATE DATABASE mydb", function (err, result) {
    if (err) throw err;
    console.log("Database created");
  });
});


// -- Create a Table
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  var sql = "CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))";
  con.query(sql, function (err, result) {
    if (err) throw err;
    console.log("Table created");
  });
});


// -- Insert data into Table
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  var sql = "INSERT INTO customers (name, address) VALUES ('Company Inc', 'Highway 37')";
  con.query(sql, function (err, result) {
    if (err) throw err;
    console.log("1 record inserted");
  });
});


// -- Select * from table
con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM customers", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});


// Run the code
"""

BOOTSTRAP = """
<!DOCTYPE html>
<html>

<head>
    <title> Bootstrap Example </title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>

<body>
    <div class="container-fluid">
        <h1>Hello World !!!</h1>
        <p>Resize browser window to see the effect</p>
        <p>The columns will automatically stack on top of each other when the screen is less than 768px wide</p>
        <div class="row">
            <div class="col-sm-4" style="background-color: red;">
                (col-sm-4-1)
            </div>
            <div class="col-sm-4" style="background-color: blue;">
                (col-sm-4-2)
            </div>
            <div class="col-sm-4" style="background-color: green;">
                (col-sm-4-3)
            </div>
        </div>
    </div>
</body>

</html>
"""

RESPOWEB = """
<!DOCTYPE html>
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
        }

        [class*="col-"] {
            float: left;
            padding: 15px;
        }

        .header {
            background-color: #9933cc;
            color: #ffffff;
            padding: 15px;
        }

        .menu ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }

        .menu li {
            padding: 8px;
            margin-bottom: 7px;
            background-color: #33b5e5;

        }

        /* For desktop: */

        .col-1 {
            width: 8.33%;
        }

        .col-2 {
            width: 16.66%;
        }

        .col-3 {
            width: 25%;
        }

        .col-4 {
            width: 33.33%;
        }

        .col-5 {
            width: 41.66%;
        }

        .col-6 {
            width: 50%;
        }

        .col-7 {
            width: 58.33%;
        }

        .col-8 {
            width: 66.66%;
        }

        .col-9 {
            width: 75%;
        }

        .col-10 {
            width: 83.33%;
        }

        .col-11 {
            width: 91.66%;
        }

        .col-12 {
            width: 100%;
        }

        @media only screen and (max-width: 768px) {

            /* For mobile phones: */

            [class*="col-"] {

                width: 100%;

            }

        }
    </style>

</head>

<body>

    <div class="header">

        <h1>Chania</h1>

    </div>


    <div class="row">

        <div class="col-3 menu">

            <ul>

                <li>The Flight</li>

                <li>The City</li>

                <li>The Island</li>

                <li>The Food</li>

            </ul>

        </div>

        <div class="col-6">

            <h1>The City</h1>

            <p>Chania is the capital of the Chania region on the island of Crete. The city can be divided in two parts,
                the old town and the modern city.</p>

        </div>

</body>

</html>
"""

FLEXGRID = """
<html lang="en">

<head>

    <title>Bootstrap Example</title>

    <meta charset="utf-8">

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>

</head>

<body>

    <div class="container mt-3">

        <h2>Horizontal Direction</h2>

        <p>Use .flex-row to make the flex items appear side by side (default):</p>

        <div class="d-flex flex-row bg-secondary mb-3">

            <div class="p-2 bg-info">Flex item 1</div>

            <div class="p-2 bg-warning">Flex item 2</div>

            <div class="p-2 bg-primary">Flex item 3</div>

        </div>

        <p>Use .flex-row-reverse to right-align the direction:</p>

        <div class="d-flex flex-row-reverse bg-secondary">

            <div class="p-2 bg-info">Flex item 1</div>

            <div class="p-2 bg-warning">Flex item 2</div>

            <div class="p-2 bg-primary">Flex item 3</div>

        </div>

    </div>

</body>

</html>
"""

HOOKER = """
import { useState , useEffect, useRef} from 'react'
import './App.css'

function App() {
  const [inputValue, setInputValue] = useState("");
  const count = useRef(0);

  useEffect(() => {
    count.current = count.current + 1;
  });

  return (
    <>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <h1>Render Count: {count.current}</h1>
    </>
  );
}
export default App

"""

def MYAI():
    url = "https://api.together.xyz/v1/chat/completions"
    api_key = "914f4a737398cdd09c79bfce5755d849f898ff613feb0a9ae88d5fd39f138275" 

    x = input("Enter your Question: ")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "microsoft/WizardLM-2-8x22B",
        "messages": [{"role": "user", "content": x}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Output the response
    response_json = response.json()

    # Access the content of the assistant's response
    assistant_message = response_json['choices'][0]['message']['content']
    print(assistant_message)


def main():
    print("""
    1. Email
    2. SERVER
    3. NOSQL
    4. SQL
    5. BOOTSTRAP
    6. RESPOWEB
    7. FLEXGRID
    8. Hooks
    9. THE SAVER OF ALL TIME
    """)

    x = int(input("Enter No.: "))

    match x:
            case 1:
                print("File Downloaded")
                with open("Email.js", "w") as f:
                    f.write(Email)
            case 2:
                print("File Downloaded")
                with open("Server.js", "w") as f:
                    f.write(SERVER)
            case 3:
                print("File Downloaded")
                with open("NoSQL.js", "w") as f:
                    f.write(NOSQL)
            case 4:
                print("File Downloaded")
                with open("SQL.js", "w") as f:
                    f.write(SQL)
            case 5:
                print("File Downloaded")
                with open("BOOTSTRAP.html", "w") as f:
                    f.write(BOOTSTRAP)
            case 6:
                print("File Downloaded")
                with open("RESPOWEB.html", "w") as f:
                    f.write(RESPOWEB)
            case 7:
                print("File Downloaded")
                with open("FLEXGRID.html", "w") as f:
                    f.write(FLEXGRID)
            case 8:
                print("File Downloaded")
                with open("HOOK.jsx",'w') as f:
                    f.write(HOOKER)
            case 9:
                MYAI()
            case _:
                print("\nNumber toh Barobar Dal\nIder Bhi Error Create kar ra hai")

