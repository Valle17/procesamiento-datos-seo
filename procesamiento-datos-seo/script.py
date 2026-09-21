import pandas as pd
import numpy as np
import re

#Abrir archivo de resultados SEO y exportar la clasificación de las muestras a otro archivo   
with open("results.txt","rb") as f:
    lines = f.readlines()
   
with open("clasificacion.txt", "wb") as g:
    for i in lines[11::]:
        g.write(i)

#Convertir el archivo en un dataframe 
df = pd.read_csv('clasificacion.txt', '|', header=None, decimal='.')
df.columns = ['NaN', 'Muestras', 'Catalogacion']

#Extrae porcentajes de cada fila según patrón y guardar en nuevas columnas
aove = df['Catalogacion'].str.extract(r'(AOVE](.....))', expand=True)
df=df.assign(AOVE=aove[1].values)
aov = df['Catalogacion'].str.extract(r'(AOV](.....))', expand=True) 
df=df.assign(AOV=aov[1].values) 
lam = df['Catalogacion'].str.extract(r'(LAM](.....))', expand=True)
df=df.assign(LAM=lam[1].values)

#Eliminar caracteres especiales
df['Muestras'] = df['Muestras'].str.replace(r'Compound=', '')
df['Muestras'] = df['Muestras'].str.strip()
df=df.replace('\(','',regex=True)
df=df.replace('\[','',regex=True).replace('\]','',regex=True) 

del(df['Catalogacion'])

df[['AOVE', 'AOV', 'LAM']] = df[['AOVE', 'AOV', 'LAM']].astype(float) # cambiar tipo de dato
#print(df.dtypes)

#La catalogación del SEO viene dada por el valor máximo de categoría
valormaximo = df[['AOVE', 'AOV', 'LAM']].idxmax(axis=1, skipna=False)
df['Catalogación'] = valormaximo
df0 = df[['Muestras', 'AOVE', 'AOV', 'LAM', 'Catalogación']] #Duplico df para exportarse, si se requiere. 
pd.options.display.max_rows = None
df['Catalogación'] = df['Catalogación'].map({'AOVE':chr(27)+"[1;32m"+'AOVE'+chr(27)+"[0m",'AOV':chr(27)+"[1;33m"+'AOV'+chr(27)+"[0m",'LAM':chr(27)+"[1;31m"+'LAM'+chr(27)+"[0m"}, na_action=None)


# tabla 2 - catalogación SEO para muestras (sin replicas, para ello se hace el promedio de los valores de cada categoría) 

lista_media_aove = []
n = 0
for i in range (0, 25):
    end = n + 3
    media_aove = df['AOVE'][n:end]
    media = np.mean(media_aove)
    lista_media_aove.append(media)
    n = n + 3

lista_media_aov = []
n = 0
for k in range (0, 25):
    end = n + 3
    media_aov = df['AOV'][n:end]
    media = np.mean(media_aov)
    lista_media_aov.append(media)
    n = n + 3

lista_media_lam = []
n = 0
for i in range (0, 25):
    end = n + 3
    media_lam = df['LAM'][n:end]
    media = np.mean(media_lam)
    lista_media_lam.append(media)
    n = n + 3

lista_muestras = []
z = 0
for j in range (0,25):
    end = z + 3
    muestras = df['Muestras'].str.replace('A', '')[z]
    lista_muestras.append(muestras)
    z = z + 3

listas = list(zip(lista_muestras, lista_media_aove, lista_media_aov, lista_media_lam))
df2 = pd.DataFrame(listas, columns = ['Muestras', 'AOVE', 'AOV', 'LAM'])

valormaximo2 = df2[['AOVE', 'AOV', 'LAM']].idxmax(axis=1, skipna=False)
df2['Catalogación'] = valormaximo2
df3 = df2[['Muestras', 'Catalogación']]
df2['Catalogación'] = df2['Catalogación'].map({'AOVE':chr(27)+"[1;32m"+'AOVE'+chr(27)+"[0m",'AOV':chr(27)+"[1;33m"+'AOV'+chr(27)+"[0m",'LAM':chr(27)+"[1;31m"+'LAM'+chr(27)+"[0m"}, na_action=None)

df2.set_index('Muestras',inplace=True) # Se establece la columna 'muestras' como index
df3.set_index('Muestras',inplace=True)
df0.set_index('Muestras',inplace=True)


print(chr(27)+"[1;36m"+'***********************************************************************************************'+chr(27)+"[0m")
print(chr(27)+"[1;36m"+'       MUESTRAS ANALIZADAS MEDIANTE EL SISTEMA ELECTRÓNICO OLFATIVO EOS835'+chr(27)+"[0m")
print(chr(27)+"[1;36m"+'***********************************************************************************************\n'+chr(27)+"[0m")
print('Este programa ha sido creado por María del Valle Ruiz Florido dentro del proyecto "Optimización\ndel entrenamiento de un sistema electrónico de olfato para la catalogación organoléptica de\naceites de oliva".\nEste programa tiene como objetivo mejorar la información obtenida por el software propio del\nsistema y su manipulación, de manera más rápida, visual e individualizada.\n')
entrada = True
while entrada == True:
    print(chr(27)+"[1;34m"+'------------------------------ESCOJA UNA OPCIÓN-----------------------------------')
    print('¿Qué necesita de este programa?:')
    print('1) Conocer la catalogacion de una muestra de aceite específica')
    print('2) Conocer la catalogacion de todas las muestras de aceite analizadas')
    print('3) Mostrar el análisis completo obtenido por el EOS835')
    print('4) Exportar el analisis completo obtenido por el EOS835 a un archivo excel')
    print('5) Cerrar el programa\n')
    print('------------------------------------------------------------------------------------' +chr(27)+"[0m")
    respuesta = input('Introduzca aquí su selección: ')
    print('\n')
    if respuesta == '1':
        print(chr(27)+"[1;35m", '\nMuestras analizadas: ', lista_muestras, chr(27)+"[0m", '\n')        
        muestra = input('¿Qué muestra quiere conocer?: ')
        if muestra in lista_muestras:
            if df3.loc[muestra, 'Catalogación'] == 'AOVE':
                print(chr(27)+"[1;32m"+'La muestra ' + muestra + " es AOVE\n\n" + chr(27)+"[0m")
            elif df3.loc[muestra, 'Catalogación'] == 'LAM':
                print(chr(27)+"[1;31m" + "La muestra " + muestra + " es lampante\n\n" + chr(27)+"[0m")
            else: 
                print(chr(27)+"[1;33m" + 'La muestra ' + muestra + ' es AOV\n\n' + chr(27)+"[0m")
        else:
            print(chr(27) + "[1;35m" + 'Esa muestra no ha sido analizada\n\n' + chr(27)+ "[0m")
    elif respuesta == '2':
        print(df2.loc[:,['Catalogación']], '\n', '\n')
    elif respuesta == '3':
        print(df, '\n', '\n')
    elif respuesta == '4':
        while True:        
            try:
                file_name = input(chr(27)+"[1;35m" + 'Introduzca un nombre para el archivo a exportar (Importante: añadir .xlsx a continuacion del nombre): ' + chr(27)+"[0m")
                df0.to_excel(file_name)            
                print(chr(27)+"[1;32m" + '\nEl análisis completo del EOS ha sido exportado con éxito al archivo Excel indicado\n' + chr(27)+"[0m")
                break
            except:
                print(chr(27)+"[1;31m" + '\nEl nombre introducido no es válido (Recuerde añadir la extensión .xlsx)\n' + chr(27)+"[0m")
    elif respuesta == '5':
        print(chr(27)+"[1;35m" + '\nGracias por usar este programa\n\n' + chr(27)+"[0m")
        entrada = False
    else:
        print(chr(27)+"[1;35m" + 'Error, no existe esa opción. Repita su selección, por favor\n\n' + chr(27)+"[0m")  
