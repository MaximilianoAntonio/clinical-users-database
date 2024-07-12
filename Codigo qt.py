import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
import mysql.connector as mysql

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Interfaz.ui", self)
        self.ingresar_paciente.clicked.connect(self.Ingreso_Pacientes)
        self.ingresar_paciente.clicked.connect(self.tabla)

        self.ingresar_examen.clicked.connect(self.Ingresar_Examen)
        self.ingresar_examen.clicked.connect(self.tabla)

        self.Buscar_boton.clicked.connect(self.Buscar_Paciente)

        self.tabla()


    def Ingreso_Pacientes(self):
        try:
            con = mysql.connect(host="localhost", user="root", database="laboratorio_clinico")
            cur = con.cursor()

            Ingreso_id_paciente = self.Ingreso_id_paciente.text()
            Ingreso_nombres = self.Ingreso_nombres.text()
            Ingreso_apellidos = self.Ingreso_apellidos.text()
            Ingreso_rut = self.Ingreso_rut.text()
            Ingreso_direccion = self.Ingreso_direccion.text()
            Ingreso_edad = self.Ingreso_edad.text()
            Ingreso_correo = self.Ingreso_correo.text()
            Ingreso_calendario = self.Ingreso_calendario.selectedDate().toString("yyyy-MM-dd")

            if not (Ingreso_id_paciente and Ingreso_nombres and Ingreso_apellidos and Ingreso_rut and Ingreso_direccion and Ingreso_edad and Ingreso_correo and Ingreso_calendario):
                QMessageBox.about(self, 'Error', 'Todos los campos son obligatorios.')
                return

            cur.execute("SELECT COUNT(*) FROM pacientes WHERE id_paciente = %s", (Ingreso_id_paciente,))
            if cur.fetchone()[0] > 0:
                QMessageBox.about(self, 'Error', 'El ID del paciente ya existe.')
                return

            query = """
            INSERT INTO pacientes 
            (id_paciente, nombres, apellidos, rut, direccion, edad, fecha_ingreso, correo) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (Ingreso_id_paciente, Ingreso_nombres, Ingreso_apellidos, Ingreso_rut, Ingreso_direccion, Ingreso_edad, Ingreso_calendario, Ingreso_correo))

            con.commit()
            QMessageBox.about(self, 'Conexión', 'Paciente ingresado correctamente')
        except mysql.Error as e:
            QMessageBox.about(self, 'Conexión', f'Error al ingrear al paciente: {e}')
        finally:
            if con.is_connected():
                cur.close()
                con.close()

    def Ingresar_Examen(self):
        try:
            con = mysql.connect(host="localhost", user="root", database="laboratorio_clinico")
            cur = con.cursor()

            Ingreso_id_paciente = self.Ingreso_id_paciente_2.text()
            Ingreso_examen = self.Box_examenes.currentText()
            Ingreso_resultado = self.Ingreso_resultado.toPlainText()

            if not (Ingreso_id_paciente and Ingreso_examen and Ingreso_resultado):
                QMessageBox.about(self, 'Error', 'Todos los campos son obligatorios.')
                return
            
            cur.execute("SELECT COUNT(*) FROM pacientes WHERE id_paciente = %s", (Ingreso_id_paciente,))
            resultado = cur.fetchone()

            if resultado[0] == 0:
                QMessageBox.about(self, 'Error', 'El ID del paciente no existe.')
                return
            
            query = "INSERT INTO examenes (id_paciente, examen, resultado) VALUES (%s, %s, %s)"
            cur.execute(query, (Ingreso_id_paciente, Ingreso_examen, Ingreso_resultado))
            
            con.commit()
            QMessageBox.about(self, 'Conexión', 'Examen ingresado correctamente')
        except mysql.Error as e:
            QMessageBox.about(self, 'Conexión', f'Error al insertar examen: {e}')
        finally:
            if con.is_connected():
                cur.close()
                con.close()

    def Buscar_Paciente(self):
        id_paciente = self.Buscar_paciente.text()
        self.tabla(id_paciente)

    def tabla(self, id_paciente=None):
        try:
            con = mysql.connect(host="localhost", user="root", database="laboratorio_clinico")
            cur = con.cursor()
            
            if id_paciente:
                query = """
                    SELECT p.*, e.examen, e.resultado
                    FROM pacientes p
                    LEFT JOIN examenes e ON p.id_paciente = e.id_paciente
                    WHERE p.id_paciente = %s
                    ORDER BY p.id_paciente
                """
                cur.execute(query, (id_paciente,))
            else:
                query = """
                    SELECT p.*, e.examen, e.resultado
                    FROM pacientes p
                    LEFT JOIN examenes e ON p.id_paciente = e.id_paciente
                    ORDER BY p.id_paciente
                """
                cur.execute(query)

            records = cur.fetchall()

            if records:
                num_columns = len(records[0])
                self.Tabla.setRowCount(len(records))
                self.Tabla.setColumnCount(num_columns)

                for i, row in enumerate(records):
                    for j, col in enumerate(row):
                        self.Tabla.setItem(i, j, QTableWidgetItem(str(col)))
            else:
                self.Tabla.setRowCount(0)
                self.Tabla.setColumnCount(0)

        except mysql.Error as e:
            QMessageBox.about(self, 'Conexión', f'Error al recuperar datos: {e}')
        finally:
            if con.is_connected():
                cur.close()
                con.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
