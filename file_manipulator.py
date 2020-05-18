#basic helper functions 

def read_file(file_name):
    try:
        file=open(file_name, "r")
        lines=file.readlines()
        file.close()
        return lines
    except:
        return None

def write_file(file_name,lines,method):
    try:
        file=open(file_name,method)
        file.writelines(lines)
        file.close()
    except:
        return None