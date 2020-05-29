# tunneling_between_machines

A simple explanation of how to use tunneling between machines using sockets and ssh. In all the following, we want to get a server and a client to talk to each other.

## using sockets locally

Open 2 terminals, server and client.

- in the server terminal:

``` nc -kl localhost 3000```

- in the client terminal:

```nc localhost 3000```

Now, anything typed in one terminal ends up in the other too.

Thanks to the ```-kl```, deconnecting the client does not kill the server.

## using sockets remotely through ssh tunnel

Make 2 computers talk to each other through ssh piping.

- make sure that both computers can ssh into each other (NOTE: 1 way should be enough). For this, best to set up ssh keys (see any tutorial online).

- start nc on the server (in my case a VM at IP 158.39.75.55):

```nc -kl localhost 3000```

- perform port forwarding on the client to the host (in my case a VM at IP 158.39.75.10): all connections from port 3000 on the local loop are now forwarded to port 3000 on the server. This command must remain active to keep the pipe alive.

```ssh -N -L 3000:127.0.0.1:3000 -v ubuntu@158.39.75.55```

- now in a separate terminal on the client, use the socket:

```nc localhost 3000```

Everything typed there will end up on the server (and vice-versa, communication is two ways). The socket is piped through ssh and a tunneling is done between the machines.

This way, sockets can communicate between machines through the internet, and everything is encrypted thanks to ssh.

## different ports

Can use different ports on client and server:

- server:

```nc -kl localhost 4000```

- client

```ssh -N -L 5000:localhost:4000 -v ubuntu@158.39.75.55```

```nc localhost 5000```
