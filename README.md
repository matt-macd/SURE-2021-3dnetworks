## Manipulation of symmetrical lattices
The goal of this project was to construct highly symmetrical lattices (cubic, hexagonal, body center cubic) and then have those lattices undergo a randomization process. This was done to determine whether or not highly symmetrical lattices could be randomized to a point where they mimic naturally occuring 3D reticulate structures. 

## The Code: 
This project is done entirely in Python. The Network class encapsulates everything done with the lattices, from their creation to randomization, then visualization of both the lattices + their node valence/angles. The Networkx library is used to manage the lattices, which are then visualized using Plotly. The randomization of the lattices uses the noise library to implement Perlin noise, which leads to a more natural randomization. Inside the Network class every method has a short description as well as the parameters. There are also comments spread throughout the file to clear up anything that might be confusing. 

There is also the buildgraph file that can take a csv file with node coordinates as input and create a Network object corresponding to that structure, which can then be easily manipulated or visualized. 

The app.py code allows the lattices to be visualized and manipulated visually. To run this app, simply run the app.py folder and put your local ip address into chrome or another browser. There, you can set different lattice symmetries and manipulate them with various parameters and see the resulting data. 

## Example:
If you wanted to generate a lattice of cubic symettry, visualize it, randomize it, refine it, then visualize it again with the corresponding data, your code would look like this:

```

import Network as nwrk

nwrk = nwrk.Network()

nwrk.setCubicSymetrry(10)
nwrk.visualizeGraph(True)

nwrk.randomize(chaosmult=0.15, minrad=0.6, maxrad=1.1)
nwrk.declutter()
nwrk.prune()
nwrk.removeKinks()
nwrk.connectNeighours()

nwrk.findAngles()
nwrk.visualizeAngles(True)
nwrk.plotDegree(True)
nwrk.visualizeGraph(True)

```

### Authors:
Natalie Reznikov, Matthew MacDonald 
