import os
def getDirs():
    """Gets dir names in the specified or current path"""
    try:
        path = str(sys.argv[1])
    except Exception as e:
        path = os.getcwd()
    dirs = [ item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) ]
    dirs.sort()
    return path, dirs

def writeFile(path, dirs):
    """Writes the exercises down to a file"""
    output = open("output2.md", "w")
    output.flush()
    cpInfo = """```bash\n wsl gcc main.c -ansi -Wall -W -pedantic -std=c89\n``` \n"""
    text = """# Esercizi in C\n""" + cpInfo
    output.write(text)
    for dir in dirs:
        writeExercise(dir, output)
    output.close()

def writeExercise(dir, output):
    """ Writes down every main.c file for each folder present in the specified or current path"""
    try:
        code, coms = extractCode(dir+"/main.c");
    except Exception as e:
        code = str(extractCode(dir+"/main.c"));
        coms = [];
    exTitle="### Es. " + dir + " \n"
    exCode= """```c\n""" + code+"""\n```\n"""
    exSeparator = """---\n"""
    output.write(exTitle);
    for com in coms:
        output.write("- "+com.replace("\n", " ").replace(". ", ".\n").replace("\t", " ").replace("    ", " ")+"\n")
    output.write(exCode.replace("\n\n\n", "\n").replace("\n\n", "\n").strip()+"\n");
    output.write(exSeparator);


def extractCode(file):
    """Extracts the code from each specific main.c"""
    try:
        f = open(file,"r")
        lines = f.readlines()
        code, coms = removeComments(lines)
        f.close()
        return code, coms
    except Exception as e:
        pass


def removeComments(lines):
    """removes the comments present between the /* */ characters"""
    allcode =""; coms= [];
    for line in lines:
        allcode += str(line)
    try:
        split = allcode.split("/*", maxsplit=1)
        while split!=allcode:
            res = split[0]
            com =  split[1]
            newsplit = com.split("*/", maxsplit=1)
            com = newsplit[0]
            res += newsplit[1]
            coms.append(com);
            split = res.split("/*", maxsplit=1)
    except Exception as e:
        pass
    return res, coms;

if __name__ == '__main__':
    """3, 2, 1: GO!"""
    path, dirs = getDirs()
    writeFile(path, dirs)
