# tunneling_between_machines

A simple explanation of how to use tunneling between machines using sockets and ssh.

## using sockets locally

- in the server terminal:

``` nc -kl localhost 3000```

- in the client terminal:

```nc localhost 3000```

Now, anything typed in one terminal ends up in the other too.

Thanks to the ```-kl```, deconnecting the client does not kill the server.

## using sockets remotely through ssh tunnel

- make sure that both computers can ssh into each other (NOTE: 1 way should be enough).

- start nc on the host (here VM 158.39.75.55):

```nc -kl localhost 3000```

- allow port forwarding on the client (here VM 158.39.75.10):

```ssh -N -L 3000:127.0.0.1:3000 -v ubuntu@158.39.75.55```

- now in a separate terminal on the client, use the socket:

```nc localhost 3000```

Everything typed there will end up on the server (and vice-versa, communication is two ways).

This way, sockets can communicate between machines through the internet, and everything is encrypted thanks to ssh.

## different ports

Can use different ports on client and server:

- server:

```nc -kl localhost 4000```

- client

```ssh -N -L 5000:localhost:4000 -v ubuntu@158.39.75.55```

```nc localhost 5000```
