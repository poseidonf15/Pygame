
with open("levels data.txt", "r+") as f:
    num = int(f.readline())
    f.seek(0)
    if num < 2: f.writelines("2")