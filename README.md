# cobra-knee

This repository contains software that was used to analyze experimental walking data in the following publication:

Anthony J. Anderson, Yuri F. Hudak, Kira A. Gauthier, Brittney C. Muir, and Patrick M. Aubin. Design and Evaluation of a Knee Flexion Assistance Exoskeleton for People with Transtibial Amputation. *Proceedings of the International Conference on Rehabilitation Robotics (ICORR).* Rotterdam, The Netherlands. July 2022.

Unfortunately, I'm not able to share the raw data for administrative/privacy reasons, but I stil thought it would be cool to share the code.

<h3>Overview</h3>

For this paper, we built and tested a knee flexion assistance exoskeleton to assist people with transtibial amputation. The exoskeleton is controlled and actuated with a custom offboard robotic actuation system called COBRA:

!['This is an image of the knee exoskeleton cart setup'](/img/experimental_setup.png "experimental setup")

The paper, which you can find in the docs/ folder, describes the design and control of the device, as well as the results of a simple walking experiment where we tested the mechatronic performance of the exoskeleton. We tested the exoskeleton's ability to apply a variety of torque profiles to one participant with limb loss at a steady walking speed. We assess torque tracking error, peak torque, and exoskeleton range of motion across four conditions. The code here carries out the full analysis required to create all figures and tables in the results section of the paper.

!['This is an image of the subject walking in the exoskeleton'](/img/walking_subplots.png "walking and signals")

<h3>Notes on Software Layout</h3>

The primary analysis pipeline script is scripts/main_gait_pipeline.py. The main pipeline script calls functions from packages in the src/ folder, including low pass filtering, gait cycle segmentation, and other computations. The main gait pipeline script crunches data and writes an intermediate pickle file to the results/ folder. Other scripts that make figures load the data they need from the pickle file. 

The setup.py file in the root directory allows for me to pip-install my custom packages in src/ and import them into the main pipeline script even though they are in a different folder. The environment.yml file allows for someone to recreate the exact Python environment I used to run this analysis in a virtual environment. I setup this repository using practices described the [Good Research Code Handbook](https://goodresearch.dev/).
