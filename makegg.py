import gamegenie
import os
try:
    while True:
        line = input()
        [address, old, new] = line.split()
        address = int(address)
        new = int(new, 8)
        old = int(old, 8)
        address -= 17
        address += 0x8000
        print("{:04X} {:02X} {:02X} \t {}".format(address, old, new, gamegenie.encode(address, new, altcode=True)))
        #print(os.popen("gamegenie/gamegenie -e 0x{:04X} 0x{:02X}".format(address, new)).read())
except Exception as e:
    #print(e)
    pass
