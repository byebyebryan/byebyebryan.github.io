---
layout: default
---

# Project R
## From VR sculpting to 3D printing



Back when I got my hands on the HTC Vive for the first time I had this idea of using the controller for a more straight forward and intuitive 3D modeling. For the first time we have accurate and robust spatial and rotation tracking and it just makes sense to work with 3D models then using a mouse on a 2D screen.

After things have settled down a bit at the store, I picked up this project and started prototyping.

### Modeling with Distance Functions

Using simple primitives add/subtract models.

The basic idea is to model hard surfaces implicitly using distance functions, in contrast to the traditional explicit modeling via vertices.

### Marching Cubes - The First Prototype

The first prototype was based on the well studied technic of Marching Cubes. It works like this:

- one edit arrives each frame
- calculate and AABB for the edit and find all the blocks that overlap with the new edit, create new blocks if necessary
- compute the distance field for each of the affected blocks and store them in 32^3 volume textures
- extract meshes from the distance fields and rendering to screen

It's worth mentioning that although MC is one of those algorithms that are considered embarrassingly parallel, it is very much a non trivial task to implement it on GPU in practice. The tricky part is to figure out where to put the generated vertices in a vertex buffer and generate the triangles/indices compactly.

Optimization 1 - Get rid of the duplicate vertices

A vertex can be shared by up to 4 triangles, so by eliminating the duplicate vertices we can save a lot of computation and memory.
I used the multiple pass approach from GPU Gems

- for each cell generate vertex markers for edge 0, 3, 8, and triangle markers, output into two append buffers
- for each vertex marker generate a vertex into the vertex buffer, and put its index into a temporary indices lookup volume
- for each triangle buffer, output indices into the index buffer by checking the lookup volume

It's work efficient since most of the empty cells were skipped, and the append buffers took care of compacting the result VB and IB

Optimization 2 - Single pass via prefix sum

- for each cell check how many vertices will be generated for edge 0, 3, 8, and how many triangles
- do prefix sums on the number of vertices and triangles to determine the output location in VB and IB
- generate vertices into VB, output to IB the same way as the triangle pass

Optimization 3 - Histo-pyramid

The problem with the previous method is that each thread maps to each cell, and since most cells won't generate any result it leads to a lot of warps with few active threads. We can use atomics to condense the work into a few number of active warps, but they come with performance penalties.

The best way to deal with this is to figure out for the active threads its input location, without the costly atomics.

Problem with Marching Cubes

The biggest draw back of this approach is that MC generates dense meshes that contain huge number of triangles even for models consists of flat surfaces.

And since at this point the block management logic ran on the CPU it limited the potential for doing global effects since each block stores its SDF in a separate 3D texture and has no way of looking into other blocks.

One particular problem is that since the blocks are somewhat large in size (32^3), the overall voxel resolution is not that great. This resulted in some nasty jagged lines around edges and intersections.

### The Hierarchical Evaluator and The Brick Renderer

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

### Sparse Voxel Octree and Global Effects

The problem with the brick engine is that each brick is still somewhat separated from other bricks. This prevent us from doing stuff such as shooting shadow rays.

The way we get to the bricks is pretty much building a Octree anyway, it's unthinkable not to do a full Octree implementation.

This naturally leads to Sparse Voxel Octree. Sparse in the sense that we don't store the empty nodes.

Using SVO not only help with memory footprint but also means we have a accelerated structure for storing the global information regarding the volume.
Not only we can cast primary rays more efficiently but also we can cast secondary rays for things like shadows and reflections.

The advantage of having a proper accelerated global data structure is that it allowed us to do fancy effects such as proper reflections, map-less shadows, global space AO and other GI stuff




One edit arrives each frame.
Calculate an AABB for the edit and find all the blocks that overlap with the new edit, create new blocks if necessary.
Compute the distance field for each of the new/modified blocks and generate meshes using MC.


Also what's worth mentioning here is that although theoretically MC is one of those algorithms that are considered embarrassingly parallel, it is still a non trivial task to implement a well balanced GPU MC in practice.

First of all a vertex can be shared by up to 4 triangles, so it is important to generate indexed triangle list rather than just the vertex buffer

At first the meshing process was divided to 3 passes:

For each cell look up the triangle table to generate a vertex marker for vertex on edge 0, 3, 8, and triangle buffers
For each vertex buffer generate a vertex, and output its index into a temporary indices lookup volume
For each triangle buffer output the indices by lookup from the lookup volume

It's 3 dispatches for each block but it's very work efficient since we don't waste threads on empty cells

It can be merged into a single pass

There is a more advanced method for proper stream compaction called histogram pyramid, but here I just used prefix scans

For each cell check how many vertices and triangles will be generated
Do a prefix sum to determine where to put the vertices and indices in VB and IB
Output vertices and indices into compact VB and IB

The first attempt is to render the distance field by extracting a polygonal mesh out of it via Marching Cubes.



Marching Cubes is pretty much the de facto approach for extracting a explicit model from implicit field.



One of the most common ways of rendering a distance field is to extract a ploygonal model from it and render via rasterization.

I've played with Marching Cubes before so the first prototype is based on MC.

A few notes:

For each cell, determine the cube case and get how many triangle will be generated for this cube.
For edges 0,3,8, generate up to 3 vertices.
Generate indices for corners of result triangles.


The problem with MC is that it generates a huge number of triangles even for flat surfaces.
And in my case there was another problem.
The initial idea was by extracting meshes I can take advantage of the Unity rendering backend.
But while Unity support procedurally generated meshes to make the most out of it you need to copy the mesh data from GPU to CPU, which is very expensive
The built in rendering pipeline does not support IB/VB generated on GPU, so even the IB/VB is already on GPU and ready for rendering, I need to copy them from GPU to CPU, and Unity upload them to GPU via separate IB/VB, which is ridicules to say the least

Also MC is not perfect in a way that it generate a uniform mesh which means a huge number of triangles even for flat surfaces.
Besides there is the jagged edges resulted from a reletivly low resolution



### The Edit List

For each edit, calculate a AABB.
Use the AABB to get all the bricks that could potentially affected by the edit, create new bricks if necessary.
Calculate distance field for the affected bricks.
Extract meshes for the bricks.

So the logic for manage bricks and the edits are on CPU.

A problem is that a brick use a separate buffer/texture.
So there is a limit to how many bricks we can have.

Also a big edit could potentially affect a huge number of bricks.

I took a short cut and generate a preview geometry for a edit, and slowly fill in the brick. But it will only work for fills but not substracts.

### Filter Edits

One fundamental problem is that we need to cull edits somehow.

For each edit, find out which bricks are intersecting the surface and only process those bricks.
For each brick, find out which edits are intersecting with the brick and only process those edits.

It is really good for incremental editing but bad for things like undo/redo

Command buffer

One attempt to address this problem is to use a command buffer for edit evaluation and mesh extraction
Once a block is marked for modification it is not immediately evaluated/meshed, but to put a edit then a meshing command into a command queue.
And before modifying a block the current distance field is cached



The next approach looked at the problem from a different perspective.
Rather than look at each edit individually and determine its effect, we should consider how a list of all the edits affects the global volume

Suppose we have a overall volume of 1024^3, and a edit list consists of ~10k edits, that's 10 trillion evaluations and way too many
What I did is to start from a coarse grid of 4^3, filter all the edits that overlap each node, repeat this process and at the leaf nodes there are only a handful of edits to consider
Also since we have filtered out all the empty/solid leafs there are much less nodes to compute

A very simple attempt to render the result from the evaluator is since we have a list of the valid leafs, for each leaf render a cube, and the pixel shader would use spherical ray marching to get to the surface, so it's like ray marching into tiny 8x8x8 SDF volumes

### Sparse Voxel Octree

Since we are using a discrete grid to represent a continous surface sooner or later we will get into the problem of accuracy.

The SDF representation actually already provides an extra layer of accuracy since we can recover most of the information regarding the surface somewhat accurately.

But to get better accuracy, we need a higher resolution grid.

Normally we use grid of size 512^3.
If we store distances as halfs then that's 250 mb of data for the distance field.
But if we want to bump the res up to 1024^3 then it's 2 gb for the distance field alone.

One thing is that the distance field is mostly empty.

This naturally leads to octrees.

We actually use a Giga Voxel style sparse octree implementation.

That is we don't store distances at the leafs but rather small 8^3 bricks of distances. This allowed us to cull most of the empty spaces while allowing us to use hardware interpolation.

By using a SVO with 8^3 bricks, I use 256^3 nodes which resulted in voxel res of 2k^3.

Actually we don't use a octree but a 4-nary tree, each node has 64 children, which plays well with warp size of 32 on Nvidia cards and should have no problem with AMD as well.



### Ray Tracer



Sadly this is around the time I got to a point where I've burned through most of my savings and have to wrap it up and move on. My partner is still actively trying to secure some funding for production and turn this into a proper comercial project, but at the time I really don't have the means to keep it going on my own.

Overall the project took ~6 months and resulted in a dozen of prototypes/tech demos.

We will end with some shots of the lastest build running the stress test of a big ball of sticks
It's 240k edits of thin sticks which would be considered a very complex case as far as geometrical complexity goes
And it renders at >100 fps with secondary shadow rays, so I'd say it's not so bad.
