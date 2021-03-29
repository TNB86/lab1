import select
import socket

SERVER_ADDRESS = ('localhost', 80)

MAX_CONNECTIONS = 5

INPUTS = list()
OUTPUTS = list()


def get_non_blocking_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(SERVER_ADDRESS)
    server.listen(MAX_CONNECTIONS)
    return server


def handle_readables(readables, server):
    """
    Обработка появления событий на входах
    """
    for resource in readables:
        if resource is server:
            connection, client_address = resource.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
            print("new connection from {address}".format(address=client_address))
        else:
            data = ""
            try:
                data = resource.recv(1024)
            except ConnectionResetError:
                pass

            if data:
                print("getting data: {data}".format(data=str(data)))
                if resource not in OUTPUTS:
                    OUTPUTS.append(resource)
            else:
                clear_resource(resource)


def clear_resource(resource):
    """
    Метод очистки ресурсов использования сокета
    """
    if resource in OUTPUTS:
        OUTPUTS.remove(resource)
    if resource in INPUTS:
        INPUTS.remove(resource)
    resource.close()
    print('closing connection ' + str(resource))


def handle_writables(writables, c):
	f = open("Lul.txt", "rb")
	l = f.read(1024)
	for resource in writables:
		try:
			while (l):
				print ("Sending...")
				print (l)
				c.send(l)
				l = f.read(1024)
			f.close()
			print ("Done Sending")
#resource.send(bytes('You here!', encoding='UTF-8'))
		except OSError:
			clear_resource(resource)


if __name__ == '__main__':
    server_socket = get_non_blocking_server_socket()
    INPUTS.append(server_socket)

    print("server is running, please, press ctrl+c to stop")
    try:
        while INPUTS:
            readables, writables, exceptional = select.select(INPUTS, OUTPUTS, INPUTS)
            handle_readables(readables, server_socket)
            handle_writables(writables, server_socket)
    except KeyboardInterrupt:
        clear_resource(server_socket)
        print("Server stopped! Thank you for using!")
