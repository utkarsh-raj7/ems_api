import mysql.connector
from app.common.logger.logger import get_logger
from app.common.errors.custom_errors import DatabaseOperationError
from app.application.model.employee_model import EmployeeCreate, EmployeeUpdate

logger = get_logger(__name__)

class EmployeeRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool
        
    def list(self, *, limit: int, offset: int, filters: dict):
        connection = None
        cursor = None
        try:
            connection = self.db_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            base_where = " FROM employee WHERE 1=1"
            query_params = []
            if "name" in filters:
                base_where += " AND (first_name LIKE %s OR last_name LIKE %s)"
                query_params.extend([f"%{filters['name']}%", f"%{filters['name']}"])
                
            if filters.get("department"):
                base_where += " AND department = %s"
                query_params.append(filters["department"])
                
            count_query = "SELECT COUNT(*) as total" + base_where
            cursor.execute(count_query, tuple(query_params))
            total_count = cursor.fetchone()["total"]
            
            data_query = "SELECT id, first_name, last_name, email, department, role" + base_where + " LIMIT %s OFFSET %s"
            
            data_params = query_params.copy()
            data_params.extend([limit, offset])
            
            cursor.execute(data_query, tuple(data_params))
            data = cursor.fetchall()
            
            return data, total_count
        
        except mysql.connector.Error as e:
            logger.error(f"My sql crashed during list: {e}")
            raise DatabaseOperationError(message = "Failed to retrieve employee from the database.")
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            
    def get_by_id (self, *, id: int):
        connection = None
        cursor = None
        try:
            connection = self.db_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            sql_query = "SELECT id, first_name, last_name, email, department FROM employee WHERE id = %s"
            cursor.execute(sql_query, (id,))
            row = cursor.fetchone()
            return row
        
        except mysql.connector.Error as e:
            logger.error(f"My sql crashed during get_by_id: {e}")
            raise DatabaseOperationError(message = f"Failed to retrieve employee {id}.")
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
    def get_by_email(self, *, email: str):
        connection = None
        cursor = None
        try:
            connection = self.db_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            sql_query = "SELECT id, first_name, last_name, email, department, password_hash FROM employee WHERE email = %s"
            cursor.execute(sql_query, (email,))
            row = cursor.fetchone()
            return row
        except mysql.connector.Error as e:
            logger.error(f"MySQL crashed during get_by_email: {e}")
            raise DatabaseOperationError(message = f"Failed to retrieve employee by email: {email}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            
        
    def create(self, *, data: EmployeeCreate, hashed_password: str):
        connection = None
        cursor = None
        try:
            connection = self.db_pool.get_connection()
            cursor = connection.cursor(prepared=True)
            
            sql_query ="""
            INSERT INTO employee (first_name, last_name, email, department, password_hash)
            Values (%s, %s, %s, %s, %s)
            """
        
            values = (
                data.first_name,
                data.last_name,
                data.email,
                data.department,
                hashed_password
            )

            cursor.execute(sql_query, values)
            connection.commit()
            
            new_id = cursor.lastrowid
            return new_id
        
        except mysql.connector.Error as e:
            logger.error(f"Database error while creating employee: {e}")
            raise DatabaseOperationError(message = "Failed to create employee.")
        
        finally:
            if cursor: 
                cursor.close()
            if connection:
                connection.close() 
                
    def update(self, *, id: int, data: EmployeeUpdate):
        connection = None
        cursor = None
        try:
            connection = self.db_pool.get_connection()
            cursor = connection.cursor(prepared=True)
            
            fields_to_update = data.model_dump(exclude_unset=True)
            if not fields_to_update: return
            
            set_clauses =[]
            values = []
            
            for column, value in fields_to_update.items():
                set_clauses.append(f"{column} = %s")
                values.append(value)
            
            set_string = ", ".join(set_clauses)
            values.append(id)
                
            sql_query = f"UPDATE employee SET {set_string} WHERE id = %s"
            
            cursor.execute(sql_query, tuple(values))
            connection.commit()
            
        except mysql.connector.Error as e:
            logger.error(f"MySQL  error during update: {e}")
            raise DatabaseOperationError(message = f"Failed to update employee {id}.")
        finally:
            if cursor: cursor.close()
            if connection: connection.close()
    
    def delete(self, *, id: int):
        connection = None
        cursor = None
        try:
            connection = self.db_pool.get_connection()
            cursor = connection.cursor(prepared=True)
            
            sql_query = "DELETE FROM employee WHERE id = %s"
            cursor.execute(sql_query, (id,))
            connection.commit()
            
        except mysql.connector.Error as e:
            logger.error(f"MySQL crash during delete: {e}")
            raise DatabaseOperationError(message = f"Failed to delete employee {id}.")
        finally:
            if cursor: cursor.close()
            if connection: connection.close()
        
            
            