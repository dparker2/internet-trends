from time import sleep

print("PRINTING STUFF")
print("SLEEPING")
sleep(1)
print("MAKING FILE")
with open("newfile.txte", "w") as f:
    f.write("Weee")
print("DONE")
