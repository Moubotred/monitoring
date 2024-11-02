import sqlite3

def crear_conexion(nombre_bd):
    """Crea una conexión a la base de datos SQLite."""
    conexion = None
    try:
        conexion = sqlite3.connect(nombre_bd)
        print(f"Conectado a la base de datos '{nombre_bd}' exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conexion

def crear_tabla(conexion):
    """Crea la tabla usuarios si no existe."""
    try:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                numero TEXT UNIQUE NOT NULL,
                creditos INTEGER DEFAULT 0,
                intentos INTEGER DEFAULT 5
            )
        ''')
        conexion.commit()
        print("Tabla 'usuarios' creada o ya existente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

def agregar_usuario(conexion, nombre, numero, creditos=0, intentos=5):
    """Agrega un nuevo usuario a la base de datos."""
    try:
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nombre, numero, creditos, intentos)
            VALUES (?, ?, ?, ?)
        ''', (nombre, numero, creditos, intentos))
        conexion.commit()
        return 'exito'
        # print(f"Usuario '{nombre}' agregado exitosamente.")
    except sqlite3.IntegrityError:
        print(f"Error: El número '{numero}' ya está registrado.")
    except sqlite3.Error as e:
        print(f"Error al agregar el usuario: {e}")

def consultar_usuarios(conexion):
    """Consulta y muestra todos los usuarios."""
    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        if usuarios:
            print("\nLista de Usuarios:")
            print("ID | Nombre | Número | Créditos | Intentos")
            print("------------------------------------------")
            for usuario in usuarios:
                print(f"{usuario[0]} | {usuario[1]} | {usuario[2]} | {usuario[3]} | {usuario[4]}")
        else:
            print("No hay usuarios registrados.")
    except sqlite3.Error as e:
        print(f"Error al consultar usuarios: {e}")

def recargar_creditos(conexion, numero, cantidad):
    """Recarga créditos a un usuario específico."""
    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT creditos FROM usuarios WHERE numero = ?', (numero,))
        resultado = cursor.fetchone()
        if resultado:
            nuevos_creditos = resultado[0] + cantidad
            cursor.execute('UPDATE usuarios SET creditos = ? WHERE numero = ?', (nuevos_creditos, numero))
            conexion.commit()
            print(f"Créditos recargados. Nuevos créditos: {nuevos_creditos}")
        else:
            print(f"No se encontró un usuario con el número '{numero}'.")
    except sqlite3.Error as e:
        print(f"Error al recargar créditos: {e}")

def usar_credito(conexion, numero, cantidad_credito=1):
    """Usa créditos de un usuario y decrementa los intentos."""
    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT creditos, intentos FROM usuarios WHERE numero = ?', (numero,))
        resultado = cursor.fetchone()
        if resultado:
            creditos, intentos = resultado
            if intentos <= 0:
                print("Límite de intentos alcanzado. No se puede realizar la operación.")
                return
            if creditos < cantidad_credito:
                print("Créditos insuficientes. Por favor, recargue créditos.")
                return
            nuevos_creditos = creditos - cantidad_credito
            nuevos_intentos = intentos - 1
            cursor.execute('''
                UPDATE usuarios 
                SET creditos = ?, intentos = ? 
                WHERE numero = ?
            ''', (nuevos_creditos, nuevos_intentos, numero))
            conexion.commit()
            print(f"Operación realizada. Créditos restantes: {nuevos_creditos}, Intentos restantes: {nuevos_intentos}")
        else:
            print(f"No se encontró un usuario con el número '{numero}'.")
    except sqlite3.Error as e:
        print(f"Error al usar crédito: {e}")

def eliminar_usuario(conexion, numero):
    """Elimina un usuario de la base de datos."""
    try:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM usuarios WHERE numero = ?', (numero,))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"Usuario con número '{numero}' eliminado exitosamente.")
        else:
            print(f"No se encontró un usuario con el número '{numero}'.")
    except sqlite3.Error as e:
        print(f"Error al eliminar usuario: {e}")

def menu():
    print("\n=== Sistema de Suscripción ===")
    print("1. Agregar Usuario")
    print("2. Consultar Usuarios")
    print("3. Recargar Créditos")
    print("4. Usar Crédito")
    print("5. Eliminar Usuario")
    print("6. Salir")

def main():
    nombre_bd = 'suscripciones.db'
    conexion = crear_conexion(nombre_bd)
    if conexion:
        crear_tabla(conexion)
        while True:
            menu()
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                nombre = input("Ingrese el nombre del usuario: ").strip()
                numero = input("Ingrese el número de teléfono: ").strip()
                if not nombre or not numero:
                    print("Nombre y número son obligatorios.")
                    continue
                try:
                    creditos = int(input("Ingrese la cantidad inicial de créditos (opcional, default 0): ") or 0)
                except ValueError:
                    print("Cantidad de créditos inválida. Se asignarán 0 créditos por defecto.")
                    creditos = 0
                agregar_usuario(conexion, nombre, numero, creditos)
            elif opcion == '2':
                consultar_usuarios(conexion)
            elif opcion == '3':
                numero = input("Ingrese el número de teléfono del usuario: ").strip()
                if not numero:
                    print("El número es obligatorio.")
                    continue
                try:
                    cantidad = int(input("Ingrese la cantidad de créditos a recargar: "))
                    if cantidad <= 0:
                        print("La cantidad debe ser positiva.")
                        continue
                    recargar_creditos(conexion, numero, cantidad)
                except ValueError:
                    print("Cantidad inválida.")
            elif opcion == '4':
                numero = input("Ingrese el número de teléfono del usuario: ").strip()
                if not numero:
                    print("El número es obligatorio.")
                    continue
                try:
                    cantidad = int(input("Ingrese la cantidad de créditos a usar (default 1): ") or 1)
                    if cantidad <= 0:
                        print("La cantidad debe ser positiva.")
                        continue
                    usar_credito(conexion, numero, cantidad)
                except ValueError:
                    print("Cantidad inválida.")
            elif opcion == '5':
                numero = input("Ingrese el número de teléfono del usuario a eliminar: ").strip()
                if not numero:
                    print("El número es obligatorio.")
                    continue
                eliminar_usuario(conexion, numero)
            elif opcion == '6':
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")
        conexion.close()

if __name__ == '__main__':
    main()

