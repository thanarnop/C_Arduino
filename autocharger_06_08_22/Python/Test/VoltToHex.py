import time
def s1():
    time.sleep(0.1)
v = 1

while v <= 50 :
    o = " "
    _v = (hex(v * 1024)).split(o)    
    _a = (hex(v * 16)).split(o)
    print("Volt",v,":",_v,"|", "AMP",v,":",_a)
    v = v + 1
    s1()
print("end")