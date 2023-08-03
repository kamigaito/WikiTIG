
def is_skip(file_path):
    if file_path.startswith("User~"):
        return True
    if file_path.startswith("Image~"):
        return True
    if file_path.startswith("Talk~"):
        return True
    if file_path.startswith("Category~"):
        return True
    if file_path.startswith("Template~"):
        return True
    if file_path.startswith("Wikipedia~"):
        return True
    if file_path.startswith("User_talk~"):
        return True
    if file_path.startswith("Image_talk~"):
        return True
    if file_path.startswith("Talk_talk~"):
        return True
    if file_path.startswith("Category_talk~"):
        return True
    if file_path.startswith("Template_talk~"):
        return True
    if file_path.startswith("Wikipedia_talk~"):
        return True
    return False

with open("./data/html.lst") as f_in, open("extracted/pages.lst", "w") as f_out:
    line = f_in.readline()
    for line in f_in:
        line = line.strip()
        if is_skip(line.split("/")[5]):
            continue
        print(line)
        f_out.write(line + "\n")
        
