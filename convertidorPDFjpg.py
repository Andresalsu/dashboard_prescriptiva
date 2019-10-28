from pdf2image import convert_from_path
from os import listdir
from os.path import isfile, join

path = "/Users/andalval/Desktop/prueba datalicit/8. MINISTERIO DE AGRICULTURA Y DESARROLLO RURAL MADR-LP-001-2019/"
archivos = [f for f in listdir(path) if isfile(join(path, f))]
i=1
for x in archivos:
    ruta = path + x
    if ruta.endswith('.pdf'):
        pages = convert_from_path(ruta, dpi=200)
        print(x+" es un pdf")
        for page in pages:
            filename = x + "-" + str(i) + '.jpg'
            page.save(filename, 'JPEG')
            i=i+1
    else:
        print(x+" no es un PDF")
    print(i-1)