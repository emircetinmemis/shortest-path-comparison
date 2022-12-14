import  os
import  shutil

from Constants import SAFE_CACHED_FOLDERS, SAFE_PRE_EXISTING_CHECKLIST

def safeStart() :

    for path in SAFE_PRE_EXISTING_CHECKLIST :
        if not os.path.exists(path) :
            if os.path.splitext(path)[1] == "" :
                os.mkdir(path)
            else :
                with open(path, "w") as f :
                    f.write("")

def safeStop() :

    projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for folder in SAFE_CACHED_FOLDERS :
        folderPath = os.path.join(projectDir, folder)
        for root, dirs, files in os.walk(folderPath):
            for dir in dirs :
                if dir == "__pycache__" :
                    shutil.rmtree(os.path.join(root, dir))

    exit()