# Containerization

We use containerization to fulfil the need of reproducibility. This is a short introduction to how to create containers, export them, and use them in a 'semi HPC' context.

## Getting familiar with docker

In the following, we use docker. Convenient as Fenics images are released as docker.

- First, make sure Docker is well installed:

https://docs.docker.com/get-started/

You should be able to run the *hello_world* stuff.

- Second, get just a bit of idea of how docker works. The main ideas to be clear about are:

-- difference image vs. container

-- how to manage images (push, remove)

-- how to start containers / issue commands in containers / stop containers

-- how to create an image from a container

For this, I recommend to take a look at (for me looking at the resources in this order helped a lot, as official documentation is not too helpful the first time one looks at docker in my opinion):

-- this stackoverflow discussion: https://stackoverflow.com/questions/21498832/in-docker-whats-the-difference-between-a-container-and-an-image

-- the Fenics explanation: https://fenics.readthedocs.io/projects/containers/en/latest/work_flows.html

-- a couple of tutorials: https://docker-curriculum.com/

-- Tormod has a bit of explanations on why singularity is being developed while we already have docker: http://folk.uio.no/tormodla/singularity/

After all of this, I feel I have a good enough idea of the general picture in order to get useful help from the documentation / googling around.

## How I created the docker image

This illustrates how I created an old image for docker. The newer image is a bit different. But this should give you an idea of how things work.

- I created a container that allows to run the code with the socketing.  How I created the container:

### docker pull fenics image: quay.io/fenicsproject/stable:latest

```
~$ docker pull quay.io/fenicsproject/stable:latest
latest: Pulling from fenicsproject/stable
c64513b74145: Pull complete 
01b8b12bad90: Pull complete 
c5d85cf7a05f: Pull complete 
b6b268720157: Pull complete 
e12192999ff1: Pull complete 
d39ece66b667: Pull complete 
65599be66378: Pull complete 
53880516d245: Pull complete 
ef4ec9d0264b: Pull complete 
b2d5b1537063: Pull complete 
1f16c78bf2dd: Pull complete 
37809e2fe5c5: Pull complete 
7ca1537156dc: Pull complete 
229092075e42: Pull complete 
8ca02d6ffa0d: Pull complete 
6bdd2975a90a: Pull complete 
8673b8078197: Pull complete 
d8c80ffcbcbd: Pull complete 
4cb31cf71f67: Pull complete 
d7f9d7b47238: Pull complete 
332f6ff1ebae: Pull complete 
6f9a1649bb61: Pull complete 
687412b8eb60: Pull complete 
dbfd133bfdf2: Pull complete 
e145e158c72d: Pull complete 
de74b6837d0c: Pull complete 
eed8dd3aade7: Pull complete 
Digest: sha256:9904c2e114b0c12fc7cb2ac74d004abd5558d37f8c988b0c37d3d8cb55861131
Status: Downloaded newer image for quay.io/fenicsproject/stable:latest
```

### docker create a container from the image: docker run -ti --name project_parallel_training quay.io/fenicsproject/stable

```
:~$ docker run -ti --name project_parallel_training quay.io/fenicsproject/stable
^[# FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
fenics@63e1fec1e840:~$ exit
exit

~$ docker container list --all
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS                      PORTS               NAMES
63e1fec1e840        quay.io/fenicsproject/stable   "/sbin/my_init --qui…"   23 seconds ago      Exited (0) 11 seconds ago                       project_parallel_training
```

this creates the project_parallel_training image, 

If I want to share the PWD, I can add ```-v $(pwd):/home/fenics/shared ```. I do not do it here, because I want it to be self contained to share.

### Then, I can start the container (this just starts the container, in the background):

```
~$ docker start project_parallel_training 
project_parallel_training
```

The container is now running:

```
~$ docker ps
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS               NAMES
63e1fec1e840        quay.io/fenicsproject/stable   "/sbin/my_init --qui…"   4 minutes ago       Up 3 minutes                            project_parallel_training
```

### Now I can open as many terminals inside the container as I want:

```
~$ docker exec -ti -u fenics project_parallel_training /bin/bash -l
 FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
fenics@63e1fec1e840:~$ 
```

### At this point, I installed the packages I wanted inside the container:

NOTE: be careful to install it in the container, not the shared folder, so that the new installed material does not disappear...

NOTE: do not use the -u fencis, otherwise use an unpriviledged user and rights problem.

NOTE: in all the following, I do not care about becoming an user instead of root; anyway, this is a container, I can spin it back to a previous version if anything bad happens. This is probably a (limited) security risk for my machine, though.

-- installing tensorforce through pip to make sure the right version of tensorflow is used

```
~$ docker exec -ti project_parallel_training /bin/bash -l                                                     
root@63e1fec1e840:/home/fenics# ls
WELCOME  demo  fenics.env.conf  local  shared
root@63e1fec1e840:/home/fenics# cd local/
root@63e1fec1e840:/home/fenics/local# pip install tensorforce[tf]
Collecting tensorforce[tf]
...
You are using pip version 19.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

-- upgrading tensorforce by cloning the repo and using the *setup.py*:

```
root@63e1fec1e840:/home/fenics/local# git clone https://github.com/tensorforce/tensorforce.git
Cloning into 'tensorforce'...
...
Successfully installed Tensorforce certifi-2019.3.9 chardet-3.0.4 future-0.17.1 gym-0.12.1 idna-2.8 pyglet-1.3.2 requests-2.21.0 tqdm-4.31.1
```

Now tensorforce is happy:

```
root@63e1fec1e840:/home/fenics/local/tensorforce# python3
Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorforce
>>> tensorforce.__version__
'0.5.0'
>>> exit()
```

And this container was chosen as, precisely, it contains the fenics package in the right version; so we are ready to go. Now I exit, and I will continue as a user.

```
root@63e1fec1e840:/home/fenics/local# exit
logout
```

### cloning the repo inside the container

- Now I can get a terminal on the container as a 'normal' user:

```
~$ docker exec  -ti -u fenics project_parallel_training /bin/bash -l                                          
 FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
```

- And I can clone the repo:

```
fenics@63e1fec1e840:~$ cd local/
fenics@63e1fec1e840:~/local$ git clone https://github.com/jerabaul29/Cylinder2DFlowControlWithRL_collaboration_Jonathan.git
Cloning into 'Cylinder2DFlowControlWithRL_collaboration_Jonathan'...
Username for 'https://github.com': jerabaul29
Password for 'https://jerabaul29@github.com': 
remote: Enumerating objects: 95, done.
remote: Counting objects: 100% (95/95), done.
remote: Compressing objects: 100% (67/67), done.
remote: Total 597 (delta 52), reused 64 (delta 27), pack-reused 502
Receiving objects: 100% (597/597), 64.52 MiB | 682.00 KiB/s, done.
Resolving deltas: 100% (372/372), done.
```

### At this poing, I am ready to play around:

- Open a new terminal in the container, and start the servers connected to the simulations. -n is the number of simulations. -p is the first port to use (put a random number; if one of the ports is used, try another random number). The first time, a bit of JIT compilation is happening (this will not happen again as I did it once):

```
~$ docker exec -ti -u fenics project_parallel_training /bin/bash -l
# FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
fenics@63e1fec1e840:~$ cd /home/fenics/local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning
fenics@63e1fec1e840:~/local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning$ git checkout socket-metaclass-2 
Switched to branch 'socket-metaclass-2'
Your branch is up to date with 'origin/socket-metaclass-2'.
fenics@63e1fec1e840:~/local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning$ ls
README.md   env.py                       launch_servers.py  mesh                 saved_models      start_client_learning.py           start_server.py    start_server_2.py
best_model  launch_parallel_training.py  make_mesh.py       perform_learning.py  single_runner.py  start_client_learning_2servers.py  start_server_1.py
fenics@63e1fec1e840:~/local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning$ python3 launch_servers.py -n 2 -p 43643
iUFL can be obtained from https://github.com/MiroK/ufl-interpreter
host 63e1fec1e840 on port 43643 is AVAIL
host 63e1fec1e840 on port 43644 is AVAIL
Calling FFC just-in-time (JIT) compiler, this may take some time.
dump rarely
dump often
```

Now, the servers are listening on the corresponding ports and ready to serve CFD data to the parallel learning.

- Open a new terminal in the container, to launch the training. The -n and -p options should be compatible with the servers command (that is to say, the new n should be lesser of equal, and all the ports (ie from -p to -p + -n)) should be available. Then, training in parallel starts :)

```
~$ docker exec -ti -u fenics project_parallel_training /bin/bash -l
# FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
fenics@63e1fec1e840:~$ cd /home/fenics/local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning
fenics@63e1fec1e840:~/local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning$ python3 launch_parallel_training.py -n 2 -p 43643
iUFL can be obtained from https://github.com/MiroK/ufl-interpreter
-0.2 0.21
WARNING:tensorflow:From /usr/local/lib/python3.6/dist-packages/tensorflow/python/ops/resource_variable_ops.py:435: colocate_with (from tensorflow.python.framework.ops) is deprecated and will be removed in a future version.
Instructions for updating:
Colocations handled automatically by placer.
WARNING:tensorflow:From /usr/local/lib/python3.6/dist-packages/tensorflow/python/ops/math_ops.py:3066: to_int32 (from tensorflow.python.ops.math_ops) is deprecated and will be removed in a future version.
Instructions for updating:
Use tf.cast instead.
2019-04-16 11:10:58.374712: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019-04-16 11:10:58.378502: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2593925000 Hz
2019-04-16 11:10:58.378744: I tensorflow/compiler/xla/service/service.cc:150] XLA service 0x10a76a0 executing computations on platform Host. Devices:
2019-04-16 11:10:58.378771: I tensorflow/compiler/xla/service/service.cc:158]   StreamExecutor device (0): <undefined>, <undefined>
Episodes:   0%|                                                                              | 0/2000 [00:00<?, ?it/s, mean_reward=0.00]
```

This is now tested, and works nicely.

### committing the container with all its content to a new image, that I share with you

At this stage, all I need is commit the container to an image, and share it with you to allow reproducibility.

-- stop the training (the usual CTRL-C) and the servers in the container.

-- note the unique has in the bash prompt; in our case: 63e1fec1e840. This can also be seen from the docker ps command:

```
~$ docker ps
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS               NAMES
63e1fec1e840        quay.io/fenicsproject/stable   "/sbin/my_init --qui…"   About an hour ago   Up About an hour                        project_parallel_training
```

-- exit the container terminals (with exit command from within each container terminal), WITHOUT stopping the container.

-- commit the container with the right hash id and tag the new image:

```
~$ docker commit 63e1fec
sha256:118c58303986dc2483def76a4b59e3b7f651c5f565a28a605fc2317877273cb7
~$ docker tag 118c58 project_parallel_training:all_installed_ok
~$ docker images
REPOSITORY                     TAG                 IMAGE ID            CREATED              SIZE
project_parallel_training      all_installed_ok    118c58303986        About a minute ago   2.77GB
quay.io/fenicsproject/stable   latest              63faf75ea38b        8 weeks ago          1.88GB
hello-world                    latest              fce289e99eb9        3 months ago         1.84kB
```

As you can see, we have one new image with all the new files (see its size).

-- At this point, I can stop the container, I was working on, clean it:

```
~$ docker ps
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS               NAMES
63e1fec1e840        quay.io/fenicsproject/stable   "/sbin/my_init --qui…"   About an hour ago   Up About an hour                        project_parallel_training
(VE_P2) jrlab@jrlab-T150s:~$ docker stop project_parallel_training 
project_parallel_training
(VE_P2) jrlab@jrlab-T150s:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

~$ docker container ls --all
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS                      PORTS               NAMES
63e1fec1e840        quay.io/fenicsproject/stable   "/sbin/my_init --qui…"   About an hour ago   Exited (2) 46 seconds ago                       project_parallel_training
(VE_P2) jrlab@jrlab-T150s:~$ docker rm 63e1
63e1
(VE_P2) jrlab@jrlab-T150s:~$ docker container ls --all
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

-- Following this, I can spin up a new container from the image:

```
~$ docker run -ti --name spinup_1 project_parallel_training:all_installed_ok 
# FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
fenics@17d7c3813988:~$ exit
~$ docker container ls --all
CONTAINER ID        IMAGE                                        COMMAND                  CREATED             STATUS                      PORTS               NAMES
17d7c3813988        project_parallel_training:all_installed_ok   "/sbin/my_init --qui…"   2 minutes ago       Exited (0) 17 seconds ago                       spinup_1
```

-- And now, I can start the new container and open terminals in it:

```
:~$ docker start spinup_1 
spinup_1
~$ docker exec -ti -u fenics spinup_1 /bin/bash -l                
# FEniCS stable version image

Welcome to FEniCS/stable!

This image provides a full-featured and optimized build of the stable
release of FEniCS.

To help you get started this image contains a number of demo
programs. Explore the demos by entering the 'demo' directory, for
example:

    cd ~/demo/python/documented/poisson
    python3 demo_poisson.py
fenics@17d7c3813988:~$ 
```

Opening one terminal in the container for the servers and one for the parallel trainer I can resume training. Now we have reproducibility and no more problems with versions / software stacks :)

### At this point, I export the image to a .zip so that you can load it back:

-- I export (careful, this is a bit of space):

```
~/Desktop/Current$ docker save project_parallel_training:all_installed_ok > fenics_tensorforce_parallel_training.tar
~/Desktop/Current$ ls -lh fenics_tensorforce_parallel_training.tar
-rw-rw-r-- 1 jrlab jrlab 2,7G april 16 13:38 fenics_tensorforce_parallel_training.tar
```

You should be able to 'load' this image to your docker by doing:

```
docker load < fenics_tensorforce_parallel_training.tar
```

And then you also can spin containers out of it.

I put my .tar image here: **https://folk.uio.no/jeanra/Informatics/fenics_tensorforce_parallel_training.tar**. You can check its integrity:

```
~/Desktop/Current$ sha256sum fenics_tensorforce_parallel_training.tar 
66113f3d56fa2e49fcb1cba59f26de3e872fc1cec48235424cff999a742d4fd0  fenics_tensorforce_parallel_training.tar
```

# One or two more notes

REMEMBER that each time you spin up a new container from an image, you are potentially using a lot of space... So clean up both your images (should not happen too ofter) and your containers (could happen more ofter) when necessary. If you sping again and again a container, you should find each each time in the state you left if last time.
