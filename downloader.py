import requests
 
url = "https://elecciones.registraduria.gov.co/e14_elec_2015//e14_divulgacion/64/013/000/ALC/E14_ALC_X_64_013_000_XX_00_006_X_XXX.pdf"
myfile=requests.get(url)
open('/Users/andalval/Downloads/E14_ALC_X_64_013_000_XX_00_006_X_XXX.pdf','wb').write(myfile.content)
print('Done')