import socket

verbose = 10
buffer_size = 262144

host = socket.gethostname()

port_receive = 3500
port_forward = 3000

socket_receive = socket.socket()
socket_receive.bind(('localhost', port_receive))
socket_receive.listen(1)

socket_forward = socket.socket()
socket_forward.connect((host, port_forward))

connection_receive = None

while True:
    if connection_receive is None:
        if verbose > 1:
            print('[Waiting for connection...]')
        connection_receive, address_receive = socket_receive.accept()
        if verbose > 1:
            print('Got connection from {}'.format(address_receive))
    else:
        if verbose > 2:
            print('[Waiting for request...]')

        message_receive = connection_receive.recv(buffer_size)

        if verbose > 2:
            print('Received request: {}'.format(message_receive))
            print('Forward request')

        socket_forward.send(message_receive)

        if verbose > 2:
            print('[Waiting for answer...]')

        message_answer = socket_forward.recv(buffer_size)

        if verbose > 2:
            print('Received answer: {}'.format(message_answer))
            print('Forward answer')

        socket_receive.send(message_answer)

        if verbose > 2:
            print('[... Successfull request]')
        

# TODO: do we really get here? Should we clean the while True loop somehow to allow to stop completely?
socket_receive.close()