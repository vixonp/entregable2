import os
import pandas as pd
import subprocess

def convertir_excel_a_csv(ruta_excel="data/eventos.xlsx", ruta_csv="data/eventos.csv"):
    if not os.path.exists(ruta_excel):
        print(f"❌ Archivo {ruta_excel} no encontrado.")
        return False
    df = pd.read_excel(ruta_excel)
    df.to_csv(ruta_csv, index=False)
    print(f"✅ Archivo convertido: {ruta_csv}")
    return True

def copiar_csv_al_contenedor(nombre_contenedor="pig_container", archivo_local="data/eventos.csv", destino="/data/eventos.csv"):
    comando = ["docker", "cp", archivo_local, f"{nombre_contenedor}:{destino}"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode == 0:
        print(f"✅ CSV copiado al contenedor {nombre_contenedor}")
        return True
    else:
        print(f"❌ Error al copiar CSV al contenedor: {resultado.stderr}")
        return False

def copiar_script_pig(nombre_contenedor="pig_container", archivo_local="data/test.pig", destino="/data/test.pig"):
    comando = ["docker", "cp", archivo_local, f"{nombre_contenedor}:{destino}"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    return resultado.returncode == 0

def eliminar_output(nombre_contenedor, ruta):
    subprocess.run(["docker", "exec", nombre_contenedor, "rm", "-rf", ruta])

def copiar_resultado(nombre_contenedor, origen_contenedor, destino_local):
    if not os.path.exists("data"):
        os.makedirs("data")
    comando = ["docker", "cp", f"{nombre_contenedor}:{origen_contenedor}", destino_local]
    subprocess.run(comando, capture_output=True, text=True)

def ejecutar_pig_paralelo():
    print("\n🐷 Procesamiento distribuido con Pig en paralelo...")

    if not convertir_excel_a_csv(): return
    if not copiar_csv_al_contenedor(): return

    scripts = [
        {
            "script": "test.pig",
            "output_dir": "output_tipo_calle.csv",
            "result_file": "data/output_tipo_calle.csv",
            "columnas": ["tipo", "calle", "cantidad"]
        },
        {
            "script": "test_hora.pig",
            "output_dir": "output_por_hora.csv",
            "result_file": "data/output_por_hora.csv",
            "columnas": ["hora", "cantidad"]
        }
    ]

    procesos = []

    for cfg in scripts:
        script_path = f"/data/{cfg['script']}"
        local_script = f"data/{cfg['script']}"
        output_path = f"/data/{cfg['output_dir']}"
        log_path = f"data/{cfg['script']}.log"
        contenedor = "pig_container"

        # Copiar script y limpiar output
        if not copiar_script_pig(contenedor, archivo_local=local_script, destino=script_path):
            print(f"❌ Falló la copia del script: {cfg['script']}")
            continue

        eliminar_output(contenedor, output_path)

        # Ejecutar Pig en paralelo
        comando = [
            "docker", "exec", "-i", contenedor,
            "bash", "-c",
            f"export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 && pig -x local {script_path}"
        ]
        log_file = open(log_path, "w", encoding="utf-8")
        proc = subprocess.Popen(comando, stdout=log_file, stderr=subprocess.STDOUT, text=True)
        procesos.append((proc, log_file, cfg))

    # Esperar y procesar resultados
    for proc, log_file, cfg in procesos:
        proc.wait()
        log_file.close()
        print(f"✅ {cfg['script']} completado. Log: {log_file.name}")

        result_file = cfg["result_file"]
        columnas = cfg["columnas"]
        output_dir = cfg["output_dir"]

        copiar_resultado("pig_container", f"/data/{output_dir}/part-r-00000", result_file)

        if os.path.exists(result_file):
            try:
                df = pd.read_csv(result_file, sep=",", names=columnas)
                df.to_excel(result_file.replace(".csv", ".xlsx"), index=False)
                print(f"📁 Exportado a Excel: {result_file.replace('.csv', '.xlsx')}")
            except Exception as e:
                print(f"❌ Error exportando {cfg['script']}: {e}")
        else:
            print(f"⚠️ No se encontró output para {cfg['script']}")


def mostrar_resultado_hora():
    archivo_salida = "data/output_por_hora.csv/part-r-00000"
    archivo_xlsx = "data/output_por_hora.xlsx"

    if not os.path.exists(archivo_salida):
        print("❌ El archivo de evolución por hora aún no ha sido generado. Ejecuta Pig primero.")
        return

    try:
        df = pd.read_csv(archivo_salida, sep=",", names=["hora", "cantidad"])
        df.to_excel(archivo_xlsx, index=False)
        print(f"✅ Resultado convertido a Excel: {archivo_xlsx}\n")
        print("📊 Evolución temporal de eventos:")
        print(df)
    except Exception as e:
        print(f"❌ Error al procesar los resultados por hora: {e}")

def mostrar_resultado_pig():
    archivo_salida = "data/output_tipo_calle.csv/part-r-00000"
    archivo_xlsx = "data/output_tipo_calle.xlsx"

    if not os.path.exists(archivo_salida):
        print("❌ El archivo de resultados tipo-calle aún no ha sido generado. Ejecuta Pig primero.")
        return

    try:
        df = pd.read_csv(archivo_salida, sep=",", names=["tipo", "calle", "cantidad"])
        df.to_excel(archivo_xlsx, index=False)
        print(f"✅ Resultado convertido a Excel: {archivo_xlsx}\n")
        print("📊 Resultados tipo-calle:")
        print(df.head())
    except Exception as e:
        print(f"❌ Error al procesar los resultados tipo-calle: {e}")
