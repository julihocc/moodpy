def tagImg(nom_graf, alt="imagen", width="600", height="400"):
    code = """<p>
    <img src=\"@@PLUGINFILE@@/{}\" alt=\"{}\" width=\"{}\" height=\"{}\" />
    </p>""".format(nom_graf,alt,width,height)
    return code

def fileImg(nom_graf, cod_graf):
    code = """
    <file name=\"{}\" path=\"/\" encoding=\"base64\">{}</file>
    """.format(nom_graf, cod_graf)
    return code

def encodePlot(*args):
    plt.plot(*args)
    tiempo=str(time.time())
    filename=tiempo+".png"
    foldername="./temp"
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    folderFile = os.path.join(foldername, filename)
    plt.savefig(folderFile)
    plt.close()
    with open(folderFile, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    return filename, encoded

def encodeGraf(graf):
    #plt.plot(*args)
    tiempo=str(time.time())
    filename=tiempo+".png"
    foldername="./temp"
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    folderFile = os.path.join(foldername, filename)
    graf.save(folderFile)
    with open(folderFile, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    return filename, encoded
