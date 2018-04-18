---
layout: default
---

# Cubey
## A OpenGL Compute Shader Playground

This project dates all the way back to the days when I was still learning OpenGL.

I'll skip through the basics such as setting up the camera and rendering a cube as there are some really good tutorials online.
All I can say about those is that to learn graphics programming, the best way really is to implement a simple rendering engine from scratch.
Not only you will gain insights to how the graphics pipeline works, it is also a really good practice for OO design patterns.

GPU Particles

A classic intro to compute shaders : how to render a million Particles.
I used a fat flat buffer to store the position of all the particles and updated every frame using a compute shader.
I added some attractors that are randomly roaming around to get the particles to move.
A geometry shader is used to expand each particle to a camera facing quad.

Marching Cubes

Another good topic for GPGPU is procedural content generation.
To generate a voxel terrain, typically some noise function (Perlin noise or FBM noise) are used to generate a density field.
Then Marching Cubes can be used to polygonise the field and extract a mesh to be rendered onto screen.
It is fairly standard to implement MC so that the result mesh already lives in GPU memory.
The tricky part is to generate the indices buffer to eliminate the duplicated vertices.

Fluid Simulation

Usually in video games or real time applications smokes are done via particles.
Compute shaders allows us to do fluid simulations that provides impressive visuals.

Tips:
A higher order advocation method really helps with the visual quality.
Vortice confinement helps hugely with bringing back the lost details resulted by numerical dissipation.

Volumetric Lighting/Shadowing

Now you have simulated how the smoke moves, but you still need to render it.
One way of doing it is actually feed the density field through MC and render the result mesh using traditional rasterization.
A more popular method is to ray trace into the field directly.
By adding a extra step of calculating a shadow volume, you get nice shadows and those sexy light shafts.
