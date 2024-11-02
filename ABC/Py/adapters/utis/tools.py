import os
import shutil
import aiohttp
import aspose.words as aw
from getpass import getuser

def Convert(filename):
    if filename:
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        builder.insert_image(filename)
        pdf_filename = filename.replace('.tif', '.pdf')
        doc.save(pdf_filename)
        return pdf_filename
    else:
        return False

async def Download(url, suministro):
    async with aiohttp.ClientSession() as session:
        try:
            filename = suministro + '.tif'
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    async with open(filename, "wb") as out_file:
                        await out_file.write(data)
                    return filename
                else:
                    return False
        except Exception as e:
            return False
        
def Remove(pdf_filename):
    try:
        if pdf_filename:
            paths = os.getcwd()
            pdf = os.path.join(paths,'pdf')
            os.makedirs(pdf,exist_ok=True)

            shutil.move(pdf_filename, os.path.join(paths, pdf_filename))
            os.remove(pdf_filename.replace('.pdf', '.tif'))
            return True

    except FileNotFoundError:
        return False
    
    except FileExistsError:
        return False
        