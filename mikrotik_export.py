import telnetlib
import time

sw_ip = "10.194.7.8"
user = "infomedia"
pas  = "infomediaok"
perintah = "sh run"

def telnet_send(sw_ip, perintah):
    perintah_cli = bytes(perintah, encoding='ASCII')
    cek_telnet.write(perintah_cli + b'\n')
    time.sleep(1)
    return(cek_telnet.read_very_eager())


cek_telnet = telnetlib.Telnet()
cek_telnet.open(sw_ip, 23, timeout=1)
cek_telnet.read_very_lazy()
cek_telnet.read_until(b"Login: ", timeout=1)
cek_telnet.write("infomedia".encode('ascii') + b"\n")
time.sleep(1)
cek_telnet.read_until(b'Password: ', 5)
cek_telnet.write("infomediaok".encode('ascii') + b"\n")
time.sleep(1)

output_1 = telnet_send(sw_ip, '/ppp active print')
#output_2 = telnet_send(sw_ip, 'sh run')
print(output_1.decode('ascii'))

cek_telnet.close