
from pwn import *
context(arch='amd64', os='linux')  # need to specify this for compilation

#sh = ssh("fd", "pwnable.kr", password="guest", port=2222)  # ssh connection
comms = remote("0", 9007)
#comms = remote("pwnable.kr", 9007)

print(comms.recv())  # title and rules
pars = comms.recvline().decode().split("\n")[0].split(" ")
N = int(pars[0].split("=")[1])
C = int(pars[1].split("=")[1])
fake = 0



def generate_seq(lowest, highest):
    seq = ""
    for i in range(lowest, highest + 1):
        seq += str(i)
        if i != highest:
            seq += " "
    return seq


def binary_search():
    global fake
    low = 0
    high = N - 1
    mid = int(math.ceil((low + high) / 2))
    currseq = b" "

    while True:
        if currseq.count(b" ") == 0:
            currseq = str(mid).encode()
        else:
            currseq = generate_seq(low, mid).encode()

        print(currseq.decode())
        comms.sendline(currseq)
        totweight = comms.recvline().decode().split("\n")[0]
        if not totweight.isnumeric():
            print(totweight)
            if totweight == "Wrong coin!":
                pass
                print("Failed!")
            else:
                print("Succeeded!")
                fake = mid
            break

        totweight = int(totweight)
        print(totweight)
        if totweight % 10 == 0:
            if currseq.count(b" ") == 0:
                mid += 1
            else:
                low = mid + 1
        else:
            if currseq.count(b" ") > 0:
                high = mid - 1

        if currseq.count(b" ") > 0:
            mid = int(math.ceil((low + high) / 2))


for i in range(100):
    print("\n=====BINSEARCH NUMBER " + str(i) + "=====")
    print("NC: " + str(N) + "," + str(C))
    binary_search()
    pars = comms.recvline().decode().split("\n")[0].split(" ")
    if pars.count("=") == 2 and pars.count(" ") == 1:
        N = int(pars[0].split("=")[1])
        C = int(pars[1].split("=")[1])
    else:
        print(pars)
        print(comms.recvline())
    print("\n=====BINSEARCH NUMBER " + str(i) + " END=====")

