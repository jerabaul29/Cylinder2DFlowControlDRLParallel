# Cylinder2DFlowControlDRLParallel

This repository contains the code corresponding to our manuscript, "Accelerating Deep Reinforcement Learning strategies of Flow Control through a multi-environment approach", Rabault and Kuhnle, Physics of Fluids (2019), preprint accessible at https://arxiv.org/abs/1906.10382.

This is a further improvement on the work published in "Artificial Neural Networks trained through Deep Reinforcement Learning discover control strategies for active flow control", Rabault et. al., Journal of Fluid Mechanics (2019), preprint accessible at https://arxiv.org/pdf/1808.07664.pdf, code available at https://github.com/jerabaul29/Cylinder2DFlowControlDRL.

In the present repository, we offer code that allows to perform parallel training of the active flow control of the Karman wake behind a circular cylinder, which leads in our case to speedups of up to a factor of 60 compared with the serial code previously released.

If you find this work useful and / or use it in your own research, please cite our works:

```
Rabault, J., Kuhnle, A (2019).
Accelerating Deep Reinforcement Leaning strategies of Flow Control through a
multi-environment approach.
Physics of Fluids.

Rabault, J., Kuchta, M., Jensen, A., Réglade, U., & Cerardi, N. (2019).
Artificial neural networks trained through deep reinforcement learning discover
control strategies for active flow control.
Journal of Fluid Mechanics, 865, 281-302. doi:10.1017/jfm.2019.62
```

## Getting started

The main code is located in **Cylinder2DFlowControlWithRL**. There, the simulation template to be run is in the **simulation_base** folder. If you want to run different simulations, this is where your modified files will have to go (see the section under for more details about user-defined cases).

The main script for launching trainings is the **script_launch_parallel.sh** script. It takes care of both launching simulation servers, and launching the parallel training. Launching the scripts takes a few minutes, be a bit patient with it :) .

The recommended method of execution is with the docker container, provided in the ```container``` folder as a series of segments tracked with ```git-lfs```. This will make sure that all packages are available in the right versions. To re-create the container locally:

```
> cat cylinder2dflowcontrol_Parallel_v1.tar_part.?? > cylinder2dflowcontrol_Parallel_v1.tar
> sha256sum cylinder2dflowcontrol_Parallel_v1.tar
d33140ad84630c657177867646a8322261cb82fc052067484c52df578a868de7  cylinder2dflowcontrol_Parallel_v1.tar
```

Remember to check your assembled container integrity with the checksum!

**A note here**: while git-lfs should allow to download sucessfully all segments upon cloning the repository, it seems that some users have a problem, either with github serving the git-lfs files, or with git checking out the large files. If this is the case, to get all the fragments, you may have to use the github web GUI, i.e. to 1) go to the right folder (```https://github.com/jerabaul29/Cylinder2DFlowControlDRLParallel/tree/master/container```) 2) for each fragment there, to click on the filename and use the download button to start downloading directly from your browser.

Docker explanations are available in the **Docker** folder. See **README_container.md** for a simple, general introduction to docker. See the **Code_Location_use_docker_Fenics_Tensorforce_parallel.md** file for explanations on how to get the docker container, and run the code inside of it. Once you are familiar with how the code works, you should use the **script_launch_parallel.sh** to launch the servers and clients for you automatically.

If you encounter problems, please:

- look for help in the .md readme files of this repo
- look for help on the github repo of the JFM paper used for serial training
- if this is not enough to get your problem solved, feel free to open an issue and ask for help.

## Main scripts

- **script_launch_parallel.sh**: automatically launch the training in parallel (use the -h option to get help).
- **python3 single_runner.py**: evaluate the latest saved policy.

## CFD simulation fenics, and user-defined user cases

For more details about the CFD simulation and how to build your own user-defined cases, please consult the Readme of the JFM code, availalbe at https://github.com/jerabaul29/Cylinder2DFlowControlDRL.

## Video of the lecture at IFAIME: learning about DRL for flow control

I was recently invited to give a guest lecture about DRL for flow control at IFAIME; the recording is available at: https://www.youtube.com/watch?v=SfbajZPvGoM .

[![IFAIME guest lecture: DRL for flow control](https://github.com/jerabaul29/Cylinder2DFlowControlDRL/blob/master/assets/image_ifaime_youtube_2.png)](https://www.youtube.com/watch?v=SfbajZPvGoM)
