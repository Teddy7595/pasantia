import psycopg2
import time

# Configuración de conexión a PostgreSQL
DB_CONFIG = {
    'dbname': 'pasantia_db',
    'user': 'root',
    'password': 'taspl7595',
    'host': 'localhost',
    'port': 5432
}

def connect_to_db():
    """Conectar a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def create_tables(conn):
    """Crear las tablas necesarias: imagenes, reporte, institucion."""
    create_institucion_table = """
    CREATE TABLE IF NOT EXISTS institutions (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        created_at BIGINT NOT NULL  -- Usar UNIX time (segundos)
    );
    """

    create_reporte_table = """
    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        report TEXT NOT NULL,
        created_at BIGINT NOT NULL  -- Usar UNIX time (segundos)
    );
    """

    create_imagen_table = """
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        image TEXT NOT NULL,
        report_id INT REFERENCES reports(id),
        institution_id INT REFERENCES institutions(id),
        created_at BIGINT NOT NULL  -- Usar UNIX time (segundos)
    );
    """

    try:
        with conn.cursor() as cur:
            # Crear las tablas si no existen
            cur.execute(create_institucion_table)
            cur.execute(create_reporte_table)
            cur.execute(create_imagen_table)
            conn.commit()
            print("Tablas creadas correctamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        conn.rollback()

def seed_data(conn):
    """Insertar datos iniciales en las tablas."""
    try:
        with conn.cursor() as cur:
            # Insertar datos en la tabla institucion
            institucion_data = [
                ("Institucion A", int(time.time())),  # Unix timestamp
            ]
            cur.executemany(
                "INSERT INTO institutions (name, created_at) VALUES (%s, %s);", 
                institucion_data
            )

            # Insertar datos en la tabla reporte
            reporte_data = [
                ("Reporte 1", int(time.time())),  # Unix timestamp
            ]
            cur.executemany(
                "INSERT INTO reports (report, created_at) VALUES (%s, %s);", 
                reporte_data
            )

            # Insertar datos en la tabla imagen (usa fechas UNIX actuales)
            imagen_data = [
                ("Image1.jpg","Image1.jpg", 1, 1, int(time.time())),  # Unix timestamp
            ]
            cur.executemany(
                "INSERT INTO images (name, image, report_id, institution_id, created_at) VALUES (%s, %s, %s, %s, %s);", 
                imagen_data
            )

            conn.commit()
            print("Datos iniciales insertados correctamente.")
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        conn.rollback()

def main():
    # Conectar a la base de datos
    conn = connect_to_db()
    if conn:
        try:
            # Crear tablas si no existen
            create_tables(conn)

            # Insertar datos iniciales
            seed_data(conn)
        finally:
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    main()
