# Marching Cubes - The First Prototype

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
