"""Script para verificar la conexión y el estado de la base de datos"""
import pymysql
from pymysql import Error

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'cc5002',
    'password': 'programacionweb',
    'database': 'tarea2',
    'port': 3306
}

def verificar_conexion():
    """Verifica la conexión a MySQL"""
    print("=" * 60)
    print("VERIFICACIÓN DE BASE DE DATOS MYSQL - TAREA 2")
    print("=" * 60)
    
    try:
        # Intentar conectar sin especificar la base de datos primero
        print("\n1️⃣  Verificando conexión al servidor MySQL...")
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        print("   ✅ Conexión al servidor MySQL exitosa")
        print(f"   Usuario: {DB_CONFIG['user']}")
        print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        
        cursor = conn.cursor()
        
        # Verificar si existe la base de datos
        print("\n2️⃣  Verificando existencia de base de datos 'tarea2'...")
        cursor.execute("SHOW DATABASES LIKE 'tarea2'")
        result = cursor.fetchone()
        
        if result:
            print("   ✅ Base de datos 'tarea2' existe")
        else:
            print("   ❌ Base de datos 'tarea2' NO existe")
            print("\n   💡 Solución: Ejecuta los siguientes comandos SQL:")
            print("      1. Abre MySQL Workbench o la consola de MySQL")
            print("      2. Ejecuta el archivo db/tarea2.sql")
            print("      3. Ejecuta el archivo db/region-comuna.sql")
            conn.close()
            return False
        
        conn.close()
        
        # Conectar a la base de datos específica
        print("\n3️⃣  Conectando a la base de datos 'tarea2'...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("   ✅ Conexión exitosa a la base de datos 'tarea2'")
        
        # Verificar tablas
        print("\n4️⃣  Verificando tablas en la base de datos...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        tablas_esperadas = ['region', 'comuna', 'aviso_adopcion', 'foto', 'contactar_por']
        tablas_encontradas = [table[0] for table in tables]
        
        print(f"   Tablas encontradas: {len(tablas_encontradas)}")
        
        for tabla in tablas_esperadas:
            if tabla in tablas_encontradas:
                print(f"   ✅ {tabla}")
            else:
                print(f"   ❌ {tabla} (FALTA)")
        
        if len(tablas_encontradas) != len(tablas_esperadas):
            print("\n   ⚠️  Faltan tablas. Ejecuta el archivo db/tarea2.sql")
            conn.close()
            return False
        
        # Verificar datos en tablas importantes
        print("\n5️⃣  Verificando datos en las tablas...")
        
        cursor.execute("SELECT COUNT(*) FROM region")
        count_regiones = cursor.fetchone()[0]
        print(f"   Regiones: {count_regiones} registros", end="")
        if count_regiones == 16:
            print(" ✅")
        elif count_regiones == 0:
            print(" ❌ (Ejecuta db/region-comuna.sql)")
        else:
            print(f" ⚠️  (Se esperaban 16)")
        
        cursor.execute("SELECT COUNT(*) FROM comuna")
        count_comunas = cursor.fetchone()[0]
        print(f"   Comunas: {count_comunas} registros", end="")
        if count_comunas == 346:
            print(" ✅")
        elif count_comunas == 0:
            print(" ❌ (Ejecuta db/region-comuna.sql)")
        else:
            print(f" ⚠️  (Se esperaban 346)")
        
        cursor.execute("SELECT COUNT(*) FROM aviso_adopcion")
        count_avisos = cursor.fetchone()[0]
        print(f"   Avisos de adopción: {count_avisos} registros")
        
        cursor.execute("SELECT COUNT(*) FROM foto")
        count_fotos = cursor.fetchone()[0]
        print(f"   Fotos: {count_fotos} registros")
        
        # Resumen final
        print("\n" + "=" * 60)
        if count_regiones == 16 and count_comunas == 346:
            print("✅ BASE DE DATOS CONFIGURADA CORRECTAMENTE")
            print("   Puedes ejecutar tu aplicación Flask con: python app.py")
        elif count_regiones > 0 and count_comunas > 0:
            print("⚠️  BASE DE DATOS CONFIGURADA PERO CON ADVERTENCIAS")
            print("   La aplicación debería funcionar, pero verifica los datos")
        else:
            print("❌ BASE DE DATOS INCOMPLETA")
            print("\n   📋 PASOS PARA COMPLETAR LA CONFIGURACIÓN:")
            print("   1. Abre MySQL Workbench")
            print("   2. Conéctate con usuario: cc5002, contraseña: programacionweb")
            print("   3. Ejecuta: db/tarea2.sql (crea las tablas)")
            print("   4. Ejecuta: db/region-comuna.sql (inserta regiones y comunas)")
        print("=" * 60)
        
        conn.close()
        return True
        
    except Error as e:
        print(f"\n❌ ERROR al conectar a MySQL:")
        print(f"   {e}")
        print("\n   💡 Posibles soluciones:")
        print("   1. Verifica que MySQL esté ejecutándose")
        print("   2. Verifica que el usuario 'cc5002' exista")
        print("   3. Verifica la contraseña 'programacionweb'")
        print("   4. Verifica que el puerto 3306 esté disponible")
        return False
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        return False

if __name__ == "__main__":
    verificar_conexion()
