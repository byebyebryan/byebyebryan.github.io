# The Hierarchical Evaluator and The Brick Renderer

The idea is that instead of looking at one edit at a time, what if we consider the whole list of edits at once.

Assume a volume of 1024^3 voxels, and a big list of 100k volumes, that sum up to 100 trillion evaluations and it is way too much.

Instead we took a hierarchical approach:
- start with a coarse grid of 2x2x2 nodes, check all the edits that overlap each node
- split each node into 2x2x2 children nodes, only check the edits overlap the parent node
- repeat until at leaf nodes

At each step we cull away a significant amount of edits for each node, and also we have less and less nodes to deal with since we can mark the nodes that are empty or solid.

For actually check overlaps between nodes and edits:

AABB is one way to do it but it would be way too conservative, eg we will get a lot of empty bricks intersecting with the AABB but not the actual surface.

A slightly better way to deal with this is sphere culling.
Instead of think the bricks as cubes we will consider them as spheres since it's much eaiser to calculate distance.
Calcualte the distance from the center of the cube/sphere to the surface of the edit.

If the distance > radius of the sphere then we know for sure this bricks won't intersect with the surface.
If distance < - radius then we know this brick is surely encapsulated by the edit, so we change the status of the whole brick rather then do a detail computation.

This is essentially build a Octree, only difference is that I ping-pong between two buffers of input-output nodes without worrying about storing the tree structure. Also instead of doing a 2x2x2 split at each step it's actually 4x4x4. It reduce the number of steps required to reach the bottom level and maps better to the 32/64 wide warps on Nvidia/AMD GPUs.

Also at the bottom level, instead of leafs contain single voxels, it is small bricks of 8x8x8 points. We wasted a small amount of memory but gain the advantage of hardware interpolation within each brick.

Now that we have a list of bricks of SDFs, there is a very simple way to render the result:
- use instancing/geometry shaders to render a cube for each brick
- for each fragment, ray march into the brick to find the surface

I call this the brick renderer.

It's very fast since for each 8x8x8 cubes we only need to march a small number of steps before it reaches the surface or exit the brick
Also we get some free LOD since the rasterizer would naturally generate fewer rays on a smaller cube

The only caviar here is that we don't have a way to turn on early-z for culling the cubes and we have to render all of them
There is no guarantee that a brick will fully block another brick simply because it's in the front because it might be empty or only contain a partial surface

Still the rendering performance is high enough and was used for quite a while.
It run >100 fps even when an additional pass was used to render into the shadow map.

The hybrid ray marcher

The brick engine is so performant that I can afford to think about trading some performance for better accuracy/visuals.

One of the biggest problem so far is that since we are using a discrete grid to estimate a continuous surface, there are always loss of details.

This becomes especially bad at sharp edges or intersections between shapes.

One way to solve this problem is to use the distance functions rather then the calculate SDF for ray marching.

The problem is that ray marching is efficient because at each step along the way it just a interpolation between 8 corners, and that's what the texture unit are designed to do.

Now at each step we need to fetch from device memory all the overlapping edits and do a somewhat lengthy calculation of the result distance, and the penalty is simply too big.

Instead I consider a hybrid approach. We start with fetch from the SDF which is very fast, and switch to calculate using the distance function once we are near the surface.

This yield significantly cleaner lines with manageable performance loss.
