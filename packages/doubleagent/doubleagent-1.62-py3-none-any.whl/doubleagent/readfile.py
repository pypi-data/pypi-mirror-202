

def readfile(file):

    f = open(file, 'r', -1, "utf-8")
    data = f.read()
    f.close()
    return data