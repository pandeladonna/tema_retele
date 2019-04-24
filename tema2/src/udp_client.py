# UDP client
import socket
import logging
import argparse

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

def calculeaza_checksum(mesaj_binar):
	checksum = 0 
	length = len(mesaj_binar)
	if(lenght % 2) ==1:
		lenght +=1
	mesaj_binar += struct.pack('!B', 0)
	
	for i in range (0,len(mesaj_binar),2):
		mesaj = (ord(mesaj_binar[i]) << 8) + ord(mesaj_binar[i+1])
		checksum += mesaj
	
	checksum = (checksum >>16)+(checksum & 0xFFFF)
	checksum =~checksum & 0xFFFF
	return checksum

def send_message(address, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        logging.info('Trimitem mesajul "%s" catre %s:%d', message, address[0], address[1])
        sock.sendto(message.encode('utf-8'), address)

        logging.info('Asteptam un raspuns...')
        data, server = sock.recvfrom(4096)
	logging.info("Am primit %s octeti de la %s", len(data),address)
		logging.info('Content primit: "%s" ',data)
	sock.connect(server)
	client = sock.getsockname()
	mesaj_binar = construieste_mesaj_raw(server[0],client[0],server[1],client[1],data)
	valoare_numerica = calculeaza_checksum(mesaj_binar)
	valoare = hex(valoare_numerica)
        logging.info('Content primit: "%s"', str(valoare))

    finally:
        logging.info('closing socket')
        sock.close()


def main():
    parser = argparse.ArgumentParser(description='Client UDP',
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--server', '-s', dest='server', action='store',
                        required=True, help='Adresa IP a serverului')
    parser.add_argument('--port', '-p', dest='port', action='store', type=int,
                        required=True, help='Portul serverului.')
    parser.add_argument('--mesaj', '-m', dest='mesaj', action='store',
                        default="", help='Mesaj de trimis prin UDP')
    args = parser.parse_args()
    server_address = (args.server, args.port)

    send_message(server_address, args.mesaj)


if __name__ == '__main__':
    main()