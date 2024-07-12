

# Clinical Users Database

This repository contains the source code for a Clinical Users Database application. The application is designed to manage and store information about clinical users efficiently.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Clinical Users Database application is built to help manage information about clinical users. It includes a graphical user interface created using Qt Designer, which allows users to interact with the database easily.

## Features

- **User-friendly Interface:** Designed with Qt Designer to provide an intuitive and easy-to-use interface.
- **Database Management:** Efficiently stores and retrieves clinical user information.
- **Cross-Platform Compatibility:** Can be run on various operating systems.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- PyQt5
- MySQL

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/MaximilianoAntonio/clinical-users-database.git
   cd clinical-users-database
   ```

2. Install the required Python packages:

   ```sh
   pip install PyQt5 mysql-connector-python
   ```

## Database Setup

Follow these steps to set up the MySQL database:

1. Open your MySQL command line or use a database management tool like phpMyAdmin.

2. Create a new database:

   ```sql
   CREATE DATABASE clinical_users_db;
   ```

3. Switch to the new database:

   ```sql
   USE clinical_users_db;
   ```

4. Create the `pacientes` table:

   ```sql
   CREATE TABLE pacientes (
       id_paciente INT AUTO_INCREMENT PRIMARY KEY,
       nombres VARCHAR(255) NOT NULL,
       apellidos VARCHAR(255) NOT NULL,
       rut VARCHAR(20) NOT NULL,
       direccion VARCHAR(255) NOT NULL,
       edad INT NOT NULL,
       fecha_ingreso DATE NOT NULL,
       correo VARCHAR(255) NOT NULL
   );
   ```

5. Create the `examenes` table:

   ```sql
   CREATE TABLE examenes (
       id_examen INT AUTO_INCREMENT PRIMARY KEY,
       id_paciente INT,
       examen VARCHAR(255) NOT NULL,
       resultado VARCHAR(255) NOT NULL,
       FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
   );
   ```

## Usage

1. Open the `Interfaz.ui` file using Qt Designer to view or edit the GUI.

2. Run the main Python script to start the application:

   ```sh
   python Codigo\ qt.py
   ```

3. Use the following SQL query to retrieve patient information along with their exams:

   ```sql
   SELECT p.*, e.examen, e.resultado
   FROM pacientes p
   LEFT JOIN examenes e ON p.id_paciente = e.id_paciente
   WHERE p.id_paciente = %s;
   ```

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create an issue or submit a pull request. Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
