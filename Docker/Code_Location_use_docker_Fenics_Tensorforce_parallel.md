# How to use the docker

- The docker is here: https://folk.uio.no/jeanra/Informatics/cylinder-drl-parallel-release-mrf-v1.tar

- Once inside the docker, one can run the code through (be familiar with tmux first; indentation means that the commands are run inside the tmux window):

```
sudo docker load -i cylinder-drl-parallel-release-mrf-v1.tar
sudo docker run -ti --name project_parallel_training cylinder-drl-parallel-release-mrf-v1
  exit
sudo docker start project_parallel_training
tmux new -s servers
  sudo docker exec -ti -u fenics project_parallel_training /bin/bash -l
  cd local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning/
  python3 launch_servers.py -n 6 -p 4252
tmux new -s training
  sudo docker exec -ti -u fenics project_parallel_training /bin/bash -l
  cd local/Cylinder2DFlowControlWithRL_collaboration_Jonathan/Cylinder2DFlowControlWithRL/ANN_controlled_flow_learning/
  python3 launch_parallel_training.py -n 6 -p 4252
```
