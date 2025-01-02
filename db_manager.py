import psycopg2
import json
import time

def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config


def connect():
    config = load_config()
    connection = psycopg2.connect(
        dbname=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )
    return connection

def save_report(report):
    RESULT = None
    try:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO reports (report, created_at) VALUES (%s, %s) RETURNING id;",
                (report, int(time.time()))
            )
            conn.commit()
            RESULT = cur.fetchone()[0]
        conn.close()
        return RESULT
    except Exception as e:
        print(f"Error al guardar el reporte: {e}")
        return None

def save_institution(institution):
    RESULT = None
    try:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO institutions (name, created_at) VALUES (%s, %s) RETURNING id;",
                (institution, int(time.time()))
            )
            conn.commit()
            RESULT = cur.fetchone()[0]
        conn.close()
        return RESULT
    except Exception as e:
        print(f"Error al guardar la institución: {e}")
        return None

def save_image(name, image, report_id, institution_id):
    RESULT = None
    try:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO images (name, image, report_id, institution_id, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (name, image, report_id, institution_id, int(time.time()))
            )
            conn.commit()
            RESULT = cur.fetchone()[0]
        conn.close()
        return RESULT
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None