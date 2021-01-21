import os

way_list = list()
for root, dirs, files in os.walk( "../_test", topdown=False ):
    print( root , 465)
    print( dirs )
    print(files)
    print(0)
    for file in files:
        # print(file)
        if file.endswith(".kt"):
            way_list.append(os.path.join(root, file))
            # print(os.path.join(root, file))

print(way_list)

with open(way_list[0]) as file:
    array = [row.strip() for row in file]
    print(array)




