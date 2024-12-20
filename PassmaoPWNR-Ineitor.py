import argparse
import blosc
import os
import time
import math
import threading
import psutil
from alive_progress import alive_bar

# Define functions with each action
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
#Loads the search index for the blocs
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
#The sorting of the hashes preceding the search
#-------------------------------------------------------
def ordenar_hashes_ntlm(input_file):
    if "txt" in input_file:                                         
        try:                                                                #See if the input is a hashfile or a single file
            # Read the hashes from the input file
            with open(input_file, 'r') as file:
                hashes = file.readlines()
            
            # Remove the (\n) of each line
            hashes = [hash.strip() for hash in hashes]

            # Sort the hashes in ascendant order
            hashes.sort()  

            new_hashes=[]
            for hash in hashes:
                if len(hash) > 40:
                    hash=hash.strip(':')
                    hash=hash[(len(hash)-32):]                              #NTLM hashes are 32 chars long, so this way we can extract them from the string
                    new_hashes.append(hash)
                    new_hashes = sorted(new_hashes)
                else:
                    
                    new_hashes = hashes
                    new_hashes = sorted(new_hashes)
                    new_hashes = set(new_hashes)

        except Exception as e:
            print(f"Ocurrió un error ordenando: {e}")
    else:
        new_hashes = [input_file]                                           #The single hash is put inside a list to avoid problems with the indexing and search functions
    return new_hashes
# ====================================================================================
# Search of the hashes in the blocs
# ====================================================================================
contador = 0
def busqueda_de_hashes(bloques_requeridos, hashes_buscados, archivo_resultado, pathToBlocs,bar): 
    # print('Thread_iniciado')
    bloques_requeridos, hashes_buscados = list(set(bloques_requeridos)), set(hashes_buscados)
    escribir = []  
    for archivo_bloque in bloques_requeridos:
        ruta_bloque = os.path.join(pathToBlocs, archivo_bloque)    
        
        # decompress the blocs
        with open(ruta_bloque, "rb") as f:
            datos_descomprimidos = blosc.decompress(f.read()).decode("utf-8")           
                    
        # search if the hashes of the block are in the searched files list
        
        for linea in datos_descomprimidos.splitlines():            
            hash_actual, valor = linea.split(":", 1)
            if hash_actual in hashes_buscados:
                # print(f"{hash_actual}:{valor}")                
                escribir.append(f"{hash_actual}:{valor}\n")
                global contador
                contador += 1
        bar()       
    with open(archivo_resultado, "a", encoding="utf-8") as archivo:
        archivo.writelines(escribir)                                        #The file is opened at the end to reduce interactions and increase speed

def has_live_threads(threads):
    return True in [t.is_alive() for t in threads]
#-------------------------------------------------------
#Search using Blosc
#-------------------------------------------------------

def buscar_hashes_ntlm_blosc(archivo_hashes, pathToBlocs, archivo_resultado, threads=1):
    start_time = time.time()
    # Load the hashes and the index
    print(f"[+]Ordenando hashes del archivo en:{archivo_hashes}")
    hashes_buscados = ordenar_hashes_ntlm(archivo_hashes)
    print(f"[+]Cargando hashes del archivo en:{archivo_hashes}")
    print(f"[+]Cargando indice en:{pathToBlocs}\index.txt")
    indice, comprobacion = cargar_indice(pathToBlocs+"\index.txt")
    
    
    # Set the variable to 'set' type so that it removes repetitions and orders the list
    bloques_requeridos =  set()
   
    
    
    print(f"[+]Buscando...")
    

#-------------------------------------------------------
#Single indexed search
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
#Double indexed search
#-------------------------------------------------------
    elif comprobacion == 'txt':
        tamaño_bloque = os.stat(pathToBlocs+'\\'+bloc).st_size
        for hash_buscado in hashes_buscados:
            for hash_inicio, hash_fin, index in indice:
                if hash_inicio <= hash_buscado <= hash_fin:
                    indice2, nulo = cargar_indice(pathToBlocs+"\\"+index)
                    null,null,bloc = indice2[1]
                    for hash_inicio, hash_fin, archivo_bloque in indice2:
                        if hash_inicio <= hash_buscado <= hash_fin:
                            bloques_requeridos.add(archivo_bloque)
                            break
    """
    The double index search is faster in cases where there are many blocks because the maximum number of lines to search is minimized,
    for example if there are 10000 blocks, in case of having a single index there are 10000 lines to search. On the other hand, if you 
    have an index of 100 lines with another 100 sub-indexes of 100 lines each, the maximum number of lines is reduced to 200.
    """
    bloques_requeridos=list(bloques_requeridos)
    numero_de_threads = threads                                                                                                 #If more threads more fast
    mem = psutil.virtual_memory()
    totalMem = mem.total
    if threads != 1:
        if numero_de_threads*(tamaño_bloque*1.66) > totalMem:                                                                       #Tryes stoping you from burning your house
            proceed = input("You are using to many threads and gonna fry you compunter, do you want to proceed?[Y]/[N]\nEstas usando demasiados hilos y vas a destrozar el ordenador, quieres continuar?[Y]/[N]\n")
            if proceed.upper == "Y" or proceed == 'y':
                return
            elif proceed.upper == "N" or proceed == 'n':
                quit()
            else:
                print("You didn't peek any / No has escogido ninguna")
                quit()
        threads_list = []       
        decimo = math.ceil(len(bloques_requeridos)/numero_de_threads)
        with alive_bar(len(bloques_requeridos)) as bar:                                                                                 #Stetic shit
            for i in range(numero_de_threads+1):                                                                                        #Create the threads by using a loop
                locals()[f'bloque+{i}']=bloques_requeridos[decimo*(i-1):decimo*i]
                locals()[f'thread+{i}']=threading.Thread(
                    target=busqueda_de_hashes, args=(locals()[f'bloque+{i}'], hashes_buscados, archivo_resultado, pathToBlocs,bar)      #Establish parameters for the thread function to use
                )
                locals()[f'thread+{i}'].start()                                                                                         #Start the threads secuentialy using a for loop
                threads_list.append(locals()[f'thread+{i}'])
            while has_live_threads(threads_list):
                try:
                    [t.join(1) for t in threads_list
                     if t is not None and t.is_alive()]
                except KeyboardInterrupt:
                    print ("[-] Stopping all the threads...")
                    for t in threads:
                        t.kill_received = True
                    quit()
                    
    else:
        with alive_bar(len(bloques_requeridos)) as bar:
            busqueda_de_hashes(bloques_requeridos,hashes_buscados, archivo_resultado, pathToBlocs, bar)
    time.sleep(1)
    print('\n--------------------------------------------------------------------')
    print("Se han tardado %s segundos" % (time.time() - start_time))
    print('--------------------------------------------------------------------')
    print('\x1b[0;36;40m'+f'{contador}'+'\x1b[0m'+' hashes encontrados')
    print('--------------------------------------------------------------------')
    print('Los resultados se han guardado en '+'\x1b[0;34;40m'+f'{archivo_resultado}'+'\x1b[0m')
    print('--------------------------------------------------------------------\n\n')
    print(f"[+]MALDITO SEAS PERRY EL ORNITORRINCO...")
   

#-------------------------------------------------------
#Generate diferent blocs using blosc
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

    indice = []  # creation of the diferent variables
    menor_hash = None
    mayor_hash = None
    numero_bloque = 1
    buffer = []
    tam_actual = 0
    tamaño_archivo_grande = os.stat(archivo_entrada).st_size
    cantidad_bloques = int(round(tamaño_archivo_grande/tam_bloque,0))


    with open(archivo_entrada, "r", encoding="utf-8") as archivo:
        with alive_bar(cantidad_bloques) as bar:
            for linea in archivo:
                # Divide the line in the hash and value
                hash_ntlm, valor = linea.strip().split(":", 1)
                
                # Update the lowest and highest hashes
                if menor_hash is None or hash_ntlm < menor_hash:
                    menor_hash = hash_ntlm
                if mayor_hash is None or hash_ntlm > mayor_hash:
                    mayor_hash = hash_ntlm
                
                buffer.append(linea)
                tam_actual += len(linea)

                if tam_actual >= int(tam_bloque):
                    # Create compressed block
                    nombre_bloque = os.path.join(ruta_salida, f"bloque_{numero_bloque}.blosc")
                    datos_comprimidos = blosc.compress("".join(buffer).encode("utf-8"), cname="zstd", clevel=9)
                    
                    # Write the comrpessed block into the file
                    with open(nombre_bloque, "wb") as f:
                        f.write(datos_comprimidos)
                    
                    # Register the info into the index
                    indice.append(f"{menor_hash},{mayor_hash},bloque_{numero_bloque}.blosc\n")
                    
                    # print(f"[-]Escrbiendo archivo bloque_{numero_bloque}.blosc escrito")
                    bar()                   #Just fancy graphics
                    numero_bloque += 1
                    buffer = []
                    tam_actual = 0

                    # Reset the lower and higher hash values
                    menor_hash = None
                    mayor_hash = None

            if buffer:
                # Create the last block if they are pending values
                nombre_bloque = os.path.join(ruta_salida, f"bloque_{numero_bloque}.blosc")
                datos_comprimidos = blosc.compress("".join(buffer).encode("utf-8"), cname="zstd", clevel=9)
                
                # write the last compressed block
                with open(nombre_bloque, "wb") as f:
                    f.write(datos_comprimidos)
                # print(f"[+]Archivo bloque_{numero_bloque}.blosc escrito")
                bar()
                # Register the last block into the index
                indice.append(f"{menor_hash},{mayor_hash},bloque_{numero_bloque}.blosc\n")
                bar()

    # Write the index into a file
    indice_padre=[]
    longitud = len(indice)
    len_maximo_para_subindice = 500                                         #Minimum size of an index to create a double index
#-------------------------------------------------------
#Create a double index
#-------------------------------------------------------
    if longitud >= len_maximo_para_subindice:                                                       #Create double index for faster search, fiuuuum
        tamaño_subindice=round(math.sqrt(longitud))                                                 #set the size of the index to the sqrt of the total length of the index to minimize searches
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
#Create simple indes(for slow loosers)
#-------------------------------------------------------
    else:
        ruta_index = os.path.join(ruta_salida, "index.txt")
        with open(ruta_index, "w", encoding="utf-8") as f:
            f.writelines(indice)

    print(f"[+]Archivo dividido y comprimido en {numero_bloque} bloques.")
    print(f"[+]Índice de bloques guardado en {ruta_index}")

# Create the arg parser

banner()
parser = argparse.ArgumentParser(description="Gestor de acciones")

# Main params
parser.add_argument("action", type=str, help="Selected action / Acción a realizar: search, generateBlocs, sort")
parser.add_argument("-f","--filehashesh", type=str, help="File with the hashes / Archivo con hashesh para crackear")
parser.add_argument("-H","--hash", type=str, help="Individual hash / Hash individual a encontrar")
parser.add_argument("-p","--pathblocs", type=str, help="Path to the blocs file directory / Ruta a archivos Blocs")
parser.add_argument("-of","--ouputfile", type=str, help="File to output the found hashes / Ruta archivo output")
parser.add_argument("-T","--bloctype", default="blosc", type=str, help="Blocks format is .blosc or .txt / Se ha comprimido en formato TXT o Blosc.\n Default: blosc")
parser.add_argument("-b","--brutefile", type=str, help="File with the precalculated hashes / Archivo con hashesh")
parser.add_argument("-s","--blocsize", default=100_000_000, type=int, help="Size of each block in bytes / Tamaño de cada bloque en bytes.\n Default: 100000000")
parser.add_argument("-t","--threads", default=1, type=int, help="Simultaneous threads used / Cantidad de procesos simultaneos\n Default: 1")



# Parse the args 
args = parser.parse_args()

# Set the acction depending on 'action'

#-------------------------------------------------------
# Search action
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
                    # search with blosc
                    if args.filehashesh is None:
                        buscar_hashes_ntlm_blosc(args.hash,args.pathblocs, args.ouputfile, args.threads)
                    else:
                        buscar_hashes_ntlm_blosc(args.filehashesh,args.pathblocs, args.ouputfile, args.threads)

                if args.bloctype == "txt":
                    # Search with txt
                    print("[-] Acción no implementada")
                    #buscar_hashes_ntlm_txt(args.filehashesh,args.pathblocs, args.ouputfile)
            else:
                print(f"La ruta {args.pathblocs} no existe")
        else:
            print(f"La ruta {args.filehashesh} no existe")
    else:
        print("Necessary parameters for search action / Parametros requeridos para la acción search : -f/--filehashesh, -p/--pathblocs y -of/--ouputfile")
        print("Optional parameters / Parametros Opcionales: -T/--bloctype, -t/--threads")
#-------------------------------------------------------
# GenerateBlocs action
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
        print("Optional parameters /  Parametros Opcionales: -T/--bloctype y -s/--blocsize")
#-------------------------------------------------------
# Sort action
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
