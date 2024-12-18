import argparse
import blosc
import os
import time
import math
import threading
import psutil

# Definir funciones para cada acción
def banner():
    print("""
                                     ##***####                                                        
                                      ###*******#                                                     
                                           ##*****#                                                   
                                             ##*****#                                                 
                                               #*****#      ##*#                                      
                                ##*********###  #****#  ##*****##                                     
                               #****************#**********##                                         
                             ##**************************#                                            
                            #*****##*   ####*##***************###                                     
                           #*##  ###*****************##**********#                                    
                          #     #**********#*+-::-#****####******#                                    
                               #*******##  *:::::::+*****#  #****#                                    
                               #****##   *+:::::::::+*****#   #*#                                     
                               #*##     *-:::::::::-*#*****#   #                                      
                               #       +:::::::::::+  #*****#                                         
                                      +::::::::::::*   ##                                             
                                    %%%@@#::::::::=*                                                  
                                  %%%@+:::::::::::*                                                   
                                 %%%+::::::::::::-*                                                   
                               %%%%#%#%*-::::::::=                                                    
                              %%%-.......==::::::+                                                    
                %%%%%%%%% %% %%%...  ......+:::::*                                                    
              %%%%@%:-=*%@%%@@=..  ..#:##%.+-:::-*                                                    
                 @-.  .:*:%%...    .=%#%%#+-=:::=*                                                    
                @=.   .-#%%*..     .:%%%%%.=-:::=   +=:::=*                                           
                @..   ..-#%+.       .......*::::= +:::-:::-                                           
                @=.      ..#..         ...#:::::+=:===-:::-*                                          
                  @+:..-*#=:#...   . ...=+::::::::+:+=::::+                                           
                      +==:-=:=*-....:-*=:::---::::::-+:::+                                            
                  #***===-::::::::::::-++:-*:::::::::::=*                                             
           *+=-::::::::::::::::::::-+-....#*-:::+*+*+*                                                
       *+-:::::::::::::::::::::::=+:*....:#*-:::+                                                     
     *+::::::::::::-=++=-:::::-+-..--....#**-:::+                                                     
   *=::::::::-=+***=::::::::==.....=....-#**-:::-*                                                    
 *+:::::=**       +::::::=+.............#***:::::=                                                    
+::=+*+          *-::-+*.........:=##=..-#*=::::::=+*       =#@@%+=                                   
**                +*   %....-*#+-........=*:::::::::::-==+++++%%%%#-----                              
                       @#**:............-+::::::::::::::::::::*@%%%= .:...:--                         
                    @-...+:.........=*=:::::::::::::::::::::::*@%%%+:...:.....:-                      
                   %-...::-=++++=-:::::::::::::::::::::::::::-#%%@+%#....-..   ..:-                   
              **+==--:::::::::::::::::::::::::::-=++**** -*%%%%%@+%%@-....:..   ...:-                 
             +:::::::::::::::::::::::::::-++**            =%%%@#*%%%%*.. ..:..      .:-               
              **::::::::::::::::::::-+*                  :..:+%%%%%%%%-.    : .       .-              
              *=::::::::::::::::=**                     -....#%%%%%%%@+... ..-..       .:-            
             *+:::::::::::::=+*                        -.. ..#%%%%%%%%*..   ....    .   ..-           
             +::::::::::-+*                           -..  ..#%%%%%%%%%:..  . :..         .-          
             +:::::::=*                                 :...:#%%%%%%%%%-..  .::.          ..-         
             *+===+*                                   ---..:%%%%%%%%%@=. .::..           ..:-        
 

______                                  ______ _    _ _   _ ______     _____           _ _             
| ___ \                                 | ___ \ |  | | \ | || ___ \   |_   _|         (_) |            
| |_/ /_ _ ___ ___ _ __ ___   __ _  ___ | |_/ / |  | |  \| || |_/ /_____| | _ __   ___ _| |_ ___  _ __ 
|  __/ _` / __/ __| '_ ` _ \ / _` |/ _ \|  __/| |/\| | . ` ||    /______| || '_ \ / _ \ | __/ _ \| '__|
| | | (_| \__ \__ \ | | | | | (_| | (_) | |   \  /\  / |\  || |\ \     _| || | | |  __/ | || (_) | |   
\_|  \__,_|___/___/_| |_| |_|\__,_|\___/\_|    \/  \/\_| \_/\_| \_|    \___/_| |_|\___|_|\__\___/|_|   
                                                                                                 
By pip0x & N7r3te\n\n""")
#DestruyePassGuatos-Ineitor v1.0 baino lehenagoko bertsioetan

#-------------------------------------------------------
#Carga de indice para las busquedas
#-------------------------------------------------------
def cargar_indice(pathToBlocs):
    indice = []
    # ruta_index = os.path.join(pathToBlocs, "index.txt")
    with open(pathToBlocs, "r", encoding="utf-8") as f:
        for linea in f:
            hash_inicio, hash_fin, archivo_bloque = linea.strip().split(",")
            indice.append((hash_inicio, hash_fin, archivo_bloque))
            null,comprobar = archivo_bloque.split('.')
    return indice, comprobar


#-------------------------------------------------------
#Ordenación de hashesh NTLM previo a busqueda
#-------------------------------------------------------
def ordenar_hashes_ntlm(input_file):
    if "txt" in input_file:                                         
        try:                                                                #Comprobacion de si se trata de un archivo con hashes o de un solo hash pasado por parametro
            # Leer los hashes desde el archivo de entrada
            with open(input_file, 'r') as file:
                hashes = file.readlines()
            
            # Eliminar los saltos de línea (\n) de cada hash
            hashes = [hash.strip() for hash in hashes]

            # Ordenar los hashes en orden ascendente
            hashes.sort()  # Ordena la lista de hashes directamente

            # Sobrescribir el archivo con los hashes ordenados
            # with open(input_file+'.ordenado.txt', 'w') as file:
            new_hashes=[]
            for hash in hashes:
                if len(hash) > 40:
                    hash=hash.strip(':')
                    hash=hash[(len(hash)-32):]                              #Los hash ntlm son de 32 caracteres de longitud por lo que se corta justo 
                    new_hashes.append(hash)
                    new_hashes = sorted(new_hashes)
                else:
                    
                    new_hashes = hashes
                    new_hashes = sorted(new_hashes)
                    new_hashes = set(new_hashes)

                    # file.write(f"{hash}\n")
        except Exception as e:
            print(f"Ocurrió un error ordenando: {e}")
    else:
        new_hashes = [input_file]                                           #Se introcude el hash unico como elemento de lista para evitar problemas con el resto del script
    return new_hashes
# ====================================================================================
# Busqueda de hashes en los bloques
# ====================================================================================
contador = 0
def busqueda_de_hashes(bloques_requeridos, hashes_buscados, archivo_resultado, pathToBlocs): 
    bloques_requeridos, hashes_buscados = list(set(bloques_requeridos)), set(hashes_buscados)
    escribir = []  
    for archivo_bloque in bloques_requeridos:
        ruta_bloque = os.path.join(pathToBlocs, archivo_bloque)    
        
        # Descomprimir el bloque
        with open(ruta_bloque, "rb") as f:
            datos_descomprimidos = blosc.decompress(f.read()).decode("utf-8")           
                    
        # Buscar hashes en el bloque descomprimido
        
        for linea in datos_descomprimidos.splitlines():            
            hash_actual, valor = linea.split(":", 1)
            if hash_actual in hashes_buscados:
                print(f"{hash_actual}:{valor}")
                escribir.append(f"{hash_actual}:{valor}\n")
                global contador
                contador += 1
                
    with open(archivo_resultado, "a", encoding="utf-8") as archivo:
        archivo.writelines(escribir)                                        #El archivo se abre y escribe al final para reducir la cantidad de interacciones en este y así ganar velocidad


#-------------------------------------------------------
#Bloque de busqueda mediante Blosc
#-------------------------------------------------------

def buscar_hashes_ntlm_blosc(archivo_hashes, pathToBlocs, archivo_resultado, threads):
    start_time = time.time()
    # Cargar hashes y el índice
    print(f"[+]Ordenando hashes del archivo en:{archivo_hashes}")
    hashes_buscados = ordenar_hashes_ntlm(archivo_hashes)
    print(f"[+]Cargando hashes del archivo en:{archivo_hashes}")
    # hashes_buscados = set(linea.strip() for linea in open(archivo_hashes+'.ordenado.txt', "r", encoding="utf-8"))
    print(f"[+]Cargando indice en:{pathToBlocs}\index.txt")
    indice, comprobacion = cargar_indice(pathToBlocs+"\index.txt")
    
    
    # Filtrar bloques relevantes
    bloques_requeridos =  set()
   
    
    
    print(f"[+]Buscando...")
    

#-------------------------------------------------------
#Busqueda con indice unico
#-------------------------------------------------------   
    if comprobacion != 'txt':
        null,null,bloc = indice[1]
        tamaño_bloque = os.stat(pathToBlocs+'\\'+bloc).st_size
        for hash_buscado in hashes_buscados:
            for hash_inicio, hash_fin, archivo_bloque in indice:
                if hash_inicio <= hash_buscado <= hash_fin:
                    bloques_requeridos.add(archivo_bloque)
                    break
        

#-------------------------------------------------------
#Busqueda con doble indice
#-------------------------------------------------------
    elif comprobacion == 'txt':
        null,null,bloc = indice[1][1]
        tamaño_bloque = os.stat(pathToBlocs+'\\'+bloc).st_size
        for hash_buscado in hashes_buscados:
            for hash_inicio, hash_fin, index in indice:
                if hash_inicio <= hash_buscado <= hash_fin:
                    indice2, nulo = cargar_indice(pathToBlocs+"\\"+index)
                    for hash_inicio, hash_fin, archivo_bloque in indice2:
                        if hash_inicio <= hash_buscado <= hash_fin:
                            bloques_requeridos.add(archivo_bloque)
                            break
    """
    La busqueda con doble indice es mas rapida en casos donde hay muchos bloques ya que se minimiza la cantidad maxima de lineas a buscar,
    por ejemplo si hay 10000 bloques, en caso de tener un solo indice hay 10000 lineas en las que buscar. En cambio, si se tiene un indice
    de 100 lineas con otros 100 subindices de 100 lineas cada uno la cantidad maxima de lineas se reduce a 200
    """
    bloques_requeridos=list(bloques_requeridos)
    numero_de_threads = threads
    mem = psutil.virtual_memory()
    totalMem = mem.total
    
    if numero_de_threads*(tamaño_bloque*1.66) > totalMem:
        proceed = input("You are using to many threads and gonna fry you compunter, do you want to proceed?[Y]/[N]\nEstas usando demasiados hilos y vas a destrozar el ordenador, quieres continuar?[Y]/[N]\n")
        if proceed.upper == "Y":
            return
        elif proceed.upper == "N":
            quit()
        else:
            print("You didn't peek any / No has escogido ninguna")
            quit()
            
    decimo = int(len(bloques_requeridos)/numero_de_threads)
    for i in range(numero_de_threads+1):                                                                                        #Crear los diferentes gupos de bloques y respectivos threads usando un loop for 
        locals()[f'bloque+{i}']=bloques_requeridos[decimo*(i-1):decimo*i]
        locals()[f'thread+{i}']=threading.Thread(
            target=busqueda_de_hashes, args=(locals()[f'bloque+{i}'], hashes_buscados, archivo_resultado, pathToBlocs)          #Establecer los parametros de la funcion para el thread
        )
    for i in range(numero_de_threads+1):
        locals()[f'thread+{i}'].start()                                                                                         #Iniciar los thread secuencialmente usando un for
    for i in range(numero_de_threads+1):
        locals()[f'thread+{i}'].join()                                                                                          #Juntar los thread secuencialmente
    
    print('\n--------------------------------------------------------------------')
    print("Se han tardado %s segundos" % (time.time() - start_time))
    print('--------------------------------------------------------------------')
    print(f'{contador} hashes encontrados')
    print('--------------------------------------------------------------------')
    print(f'Los resultados se han guardado en {archivo_resultado}')
    print('--------------------------------------------------------------------\n\n')
    print(f"[+]MALDITO SEAS PERRY EL ORNITORRINCO...")
   

#-------------------------------------------------------
#Generación de bloques mediante Blosc
#-------------------------------------------------------
def crear_bloques_comprimidos(archivo_entrada, ruta_salida, tam_bloque=100_000_000):
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    print(f"\n[+]Empieza lo bueno...\n")
    print(f"""Let's have a coffee break...
    (((
     )))
   _______
  ||     ||q
   \     /_/
    `---""")

    print(f"\nAmeniza la espera con un buen video: https://www.youtube.com/watch?v=jNIBs02p-Ks\n")

    indice = []  # Lista para almacenar el índice
    menor_hash = None
    mayor_hash = None
    numero_bloque = 1
    buffer = []
    tam_actual = 0

    with open(archivo_entrada, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            # Dividir la línea en hash NTLM y el valor (antes del ':')
            hash_ntlm, valor = linea.strip().split(":", 1)
            
            # Actualizar el hash menor y mayor
            if menor_hash is None or hash_ntlm < menor_hash:
                menor_hash = hash_ntlm
            if mayor_hash is None or hash_ntlm > mayor_hash:
                mayor_hash = hash_ntlm
            
            buffer.append(linea)
            tam_actual += len(linea)

            if tam_actual >= int(tam_bloque):
                # Crear bloque comprimido
                nombre_bloque = os.path.join(ruta_salida, f"bloque_{numero_bloque}.blosc")
                datos_comprimidos = blosc.compress("".join(buffer).encode("utf-8"), cname="zstd", clevel=9)
                
                # Escribir el bloque comprimido en el archivo
                with open(nombre_bloque, "wb") as f:
                    f.write(datos_comprimidos)
                
                # Registrar la información en el índice en el formato requerido
                indice.append(f"{menor_hash},{mayor_hash},bloque_{numero_bloque}.blosc\n")
                
                print(f"[-]Escrbiendo archivo bloque_{numero_bloque}.blosc escrito")
                numero_bloque += 1
                buffer = []
                tam_actual = 0

                # Resetear los valores de menor y mayor hash
                menor_hash = None
                mayor_hash = None

        if buffer:
            # Crear el último bloque comprimido si hay datos restantes
            nombre_bloque = os.path.join(ruta_salida, f"bloque_{numero_bloque}.blosc")
            datos_comprimidos = blosc.compress("".join(buffer).encode("utf-8"), cname="zstd", clevel=9)
            
            # Escribir el último bloque comprimido
            with open(nombre_bloque, "wb") as f:
                f.write(datos_comprimidos)
            print(f"[+]Archivo bloque_{numero_bloque}.blosc escrito")

            # Registrar el índice del último bloque
            indice.append(f"{menor_hash},{mayor_hash},bloque_{numero_bloque}.blosc\n")

    # Escribir el índice en un archivo
    indice_padre=[]
    longitud = len(indice)
    len_maximo_para_subindice = 500                                         #Tamaño minimo subindice para que merezca la pena hacer doble indice
#-------------------------------------------------------
#Creación de doble indice
#-------------------------------------------------------
    if longitud >= len_maximo_para_subindice:                                                       #Crear doble indice para mas velocidad, fiuuuum
        tamaño_subindice=round(math.sqrt(longitud))                                                 #Cambiar tamaño de subindice
        repeticiones = int(math.floor((longitud+tamaño_subindice)/tamaño_subindice))
        for i in range(repeticiones):
                minimo=int((i*tamaño_subindice)+1)
                maximo=int(((i+1)*tamaño_subindice)-1)
                if maximo > longitud:maximo=longitud-1
                name = str(minimo)+"-"+str(maximo+1)+".txt"
                hash_txiki,valor_nulo,valor_nulo=indice[minimo].split(',')                          
                valor_nulo,hash_haundi,valor_nulo=indice[maximo].split(',')
                indice_padre.append(f"{hash_txiki},{hash_haundi},{name}\n")
                for e in range(minimo-1,maximo+1):
                    ruta_index2 = os.path.join(ruta_salida, name)
                    with open(ruta_index2, "a", encoding="utf-8") as f:
                        f.write(indice[e])
        ruta_index = os.path.join(ruta_salida, "index.txt")
        with open(ruta_index, "w", encoding="utf-8") as f:
            f.writelines(indice_padre)
#-------------------------------------------------------
#Creación de indice simple
#-------------------------------------------------------
    else:
        ruta_index = os.path.join(ruta_salida, "index.txt")
        with open(ruta_index, "w", encoding="utf-8") as f:
            f.writelines(indice)

    print(f"[+]Archivo dividido y comprimido en {numero_bloque} bloques.")
    print(f"[+]Índice de bloques guardado en {ruta_index}")

# Crear el analizador de argumentos

banner()
parser = argparse.ArgumentParser(description="Gestor de acciones")

# Parámetros de entrada principales
parser.add_argument("action", type=str, help="Selected action / Acción a realizar: search, generateBlocs, sort")
parser.add_argument("-f","--filehashesh", type=str, help="File with the hashes / Archivo con hashesh para crackear")
parser.add_argument("-H","--hash", type=str, help="Individual hash / Hash individual a encontrar")
parser.add_argument("-p","--pathblocs", type=str, help="Path to the blocs file directory / Ruta a archivos Blocs")
parser.add_argument("-of","--ouputfile", type=str, help="File to output the found hashes / Ruta archivo output")
parser.add_argument("-T","--bloctype", default="blosc", type=str, help="Blocks format is .blosc or .txt / Se ha comprimido en formato TXT o Blosc.\n Default: blosc")
parser.add_argument("-b","--brutefile", type=str, help="File with the precalculated hashes / Archivo con hashesh")
parser.add_argument("-s","--blocsize", default=100_000_000, type=int, help="Size of each block in bytes / Tamaño de cada bloque en bytes.\n Default: 100000000")
parser.add_argument("-t","--threads", default=1, type=int, help="Simultaneous threads used / Cantidad de procesos simultaneos\n Default: 1")



# Parsear los argumentos
args = parser.parse_args()

# Asignar acción según el parámetro 'action'

#-------------------------------------------------------
# Acción de Search con sus diferentes parametros
#-------------------------------------------------------
if args.action == "search":
    if (args.filehashesh or args.hash is not None) and args.pathblocs is not None and args.ouputfile is not None:
        if args.filehashesh is None: hashpath = "C:"
        else: hashpath = args.filehashesh
        if os.path.exists(hashpath):
            if os.path.exists(args.pathblocs) or args.hash is not None:
                if args.bloctype != "blosc" and args.bloctype != "txt" :
                     print("[-] Solo se acepta los valores blosc o txt para el parametro -t/--bloctype")
                if args.bloctype == "blosc":
                    # Busqueda por blosc
                    if args.filehashesh is None:
                        buscar_hashes_ntlm_blosc(args.hash,args.pathblocs, args.ouputfile, args.threads)
                    else:
                        buscar_hashes_ntlm_blosc(args.filehashesh,args.pathblocs, args.ouputfile, args.threads)

                if args.bloctype == "txt":
                    # Busqueda por txt
                    print("[-] Acción no implementada")
                    #buscar_hashes_ntlm_txt(args.filehashesh,args.pathblocs, args.ouputfile)
            else:
                print(f"La ruta {args.pathblocs} no existe")
        else:
            print(f"La ruta {args.filehashesh} no existe")
    else:
        print("Necessary parameters for search action / Parametros requeridos para la acción search : -f/--filehashesh, -p/--pathblocs y -of/--ouputfile")
        print("Optional parameters / Parametros Opcionales: -t/--bloctype")
#-------------------------------------------------------
# Acción de generateBlocs con sus diferentes parametros
#-------------------------------------------------------

elif args.action == "generateBlocs":
    if args.bloctype is not None and args.pathblocs is not None and args.brutefile is not None and  args.blocsize is not None:
        if os.path.exists(args.brutefile):
            if os.path.exists(args.pathblocs):
                if args.bloctype != "blosc" and args.bloctype != "txt" :
                    print("[-] Solo se acepta los valores blosc o txt para el parametro -t/--bloctype")
                if args.bloctype == "blosc":                   
                    crear_bloques_comprimidos(args.brutefile, args.pathblocs,args.blocsize)
            else:
                print(f"La ruta {args.pathblocs} no existe")
        else:
            print(f"La ruta {args.brutefile} no existe")          
    else:
        print("Necessary parameters for generateBloks action / Parametros requeridos para la acción generateBlocks :  -b/--brutefile, -p/--pathblocs ")
        print("Optional parameters /  Parametros Opcionales: -t/--bloctype y -s/--blocsize")
#-------------------------------------------------------
# Acción de sort con sus diferentes parametros
#-------------------------------------------------------
elif args.action == "sort":
    if args.brutefile is None:
        print("[-] Necessary parameters for sort action / Parametros requeridos para la acción sort : -b/--brutefile ")
    else:
        with open(args.brutefile, "r") as f:
            lineas = f.readlines()
            ordenados =  []
            for i in lineas:
                orden = i.strip('\n')
                ordenados.append(orden)
        with open(args.brutefile, "w") as f:
            for i in sorted(set(ordenados)):
                f.write(f'{i}\n')
            
        print("[+] File succesfully sorted / Archivo ordenado satisfactoriamente")
#-------------------------------------------------------
else:
    print("Acción no reconocida.")