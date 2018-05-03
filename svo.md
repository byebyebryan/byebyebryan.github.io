# Sparse Voxel Octree and Global Effects

The problem with the brick engine is that each brick is still somewhat separated from other bricks. This prevent us from doing stuff such as shooting shadow rays.

The way we get to the bricks is pretty much building a Octree anyway, it's unthinkable not to do a full Octree implementation.

This naturally leads to Sparse Voxel Octree. Sparse in the sense that we don't store the empty nodes.

Using SVO not only help with memory footprint but also means we have a accelerated structure for storing the global information regarding the volume.
Not only we can cast primary rays more efficiently but also we can cast secondary rays for things like shadows and reflections.

The advantage of having a proper accelerated global data structure is that it allowed us to do fancy effects such as proper reflections, map-less shadows, global space AO and other GI stuff
