import psycopg2
import os
from datetime import datetime

# Replace these with your actual database credentials
dbname = "db"
user = "postgres"
password = "postgres"
host = "localhost"  # or your host IP address if different

def fetch_param_type_id(cursor, parameter_name):
    try:
        cursor.execute('SELECT "IdParametertype" FROM "tblParametertype" WHERE "ParameterName" = %s', (parameter_name,))
        result = cursor.fetchone()
        if result:
            print(f"Fetched IdParametertype for {parameter_name}: {result[0]}")
            return result[0]
        else:
            print(f"No IdParametertype found for {parameter_name}")
            return None
    except psycopg2.DatabaseError as error:
        print(f"Error fetching IdParametertype for {parameter_name}: {error}")
        return None

def fetch_device_id(cursor, device_name):
    try:
        cursor.execute('SELECT "Deviceid" FROM "tblNsDeviceData" WHERE "DeviceName" = %s', (device_name,))
        result = cursor.fetchone()
        if result:
            print(f"Fetched Deviceid for {device_name}: {result[0]}")
            return result[0]
        else:
            print(f"No Deviceid found for {device_name}")
            return None
    except psycopg2.DatabaseError as error:
        print(f"Error fetching Deviceid for {device_name}: {error}")
        return None

def convert_timestamp(timestamp_str):
    try:
        return datetime.strptime(timestamp_str, '%Y:%m:%d-%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Error converting timestamp: {e}")
        return None

def main():
    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()

        humidity_type_id = fetch_param_type_id(cursor, 'Humidity')
        temperature_type_id = fetch_param_type_id(cursor, 'Temperature(K)')
        pressure_type_id = fetch_param_type_id(cursor, 'Pressure(hPa)')
        
        if not humidity_type_id or not temperature_type_id or not pressure_type_id:
            raise ValueError("One or more parameter types could not be found in the database.")

        device_id = fetch_device_id(cursor, 'Geoffry')  # Update with the correct device name
        if not device_id:
            raise ValueError("Device ID could not be found in the database.")

        file_path = r'C:\Users\HP\Desktop\Dummy\geoffry\20240502\2300\aa24.txt'
        print("Attempting to open file at:", file_path)
        
        if os.path.isfile(file_path):
            print("File exists.")
            with open(file_path, 'r') as file:
                next(file)  # Skip the header line
                for line in file:
                    if line.startswith("Position(m)"):
                        continue  # Skip the position line
                        
                    parts = line.strip().split('\t')
                    if len(parts) != 4:
                        print(f"Skipping malformed line: {line.strip()}")
                        continue  # Skip malformed lines

                    timestamp_str = parts[0]
                    humidity = float(parts[1])
                    temperature = float(parts[2])
                    pressure = float(parts[3])

                    timestamp = convert_timestamp(timestamp_str)
                    if timestamp is None:
                        print(f"Skipping row with invalid timestamp: {timestamp_str}")
                        continue  # Skip rows with invalid timestamps

                    # Insert data into tblParameters
                    try:
                        # Insert humidity
                        cursor.execute('INSERT INTO "tblParameters" ("IdParametertype", "Deviceid", "Timestamp", "Value") VALUES (%s, %s, %s, %s)', (humidity_type_id, device_id, timestamp, humidity))
                        # Insert temperature
                        cursor.execute('INSERT INTO "tblParameters" ("IdParametertype", "Deviceid", "Timestamp", "Value") VALUES (%s, %s, %s, %s)', (temperature_type_id, device_id, timestamp, temperature))
                        # Insert pressure
                        cursor.execute('INSERT INTO "tblParameters" ("IdParametertype", "Deviceid", "Timestamp", "Value") VALUES (%s, %s, %s, %s)', (pressure_type_id, device_id, timestamp, pressure))
                    except psycopg2.Error as e:
                        print(f"Error inserting data into tblParameters: {e}")
                        conn.rollback()
                    else:
                        conn.commit()

            print("Records inserted successfully into tblParameters table")

        else:
            print(f"File not found: {file_path}")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL or executing SQL:", error)
    
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    main()
