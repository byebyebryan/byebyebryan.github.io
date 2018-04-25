---
layout: default
---

# Cubey
## A OpenGL Compute Shader Playground

This project dates all the way back to the days when I was still learning OpenGL.

I'll skip through the basics such as setting up the camera and rendering a triangle as there are some really good tutorials online.
All I can say about those is that to learn graphics programming, the best way really is to implement a simple rendering engine from scratch.
Not only you will gain insights to how the graphics pipeline works, it is also a really good practice for OO design patterns.

### GPU Particles

[![GPU Particles](http://img.youtube.com/vi/XKr-VAtpp-8/0.jpg)](http://www.youtube.com/watch?v=XKr-VAtpp-8)

A classic intro to compute shaders : how to render a million Particles.

I added some attractors that are randomly roaming around to get the particles to dance a bit.

A geometry shader is used to expand each particle to a camera facing quad.

### Real-time Fluid Simulation

[![GPU Particles](http://img.youtube.com/vi/_likq0EsXFI/0.jpg)](http://www.youtube.com/watch?v=_likq0EsXFI)

Eulerian fluid simulation using compute shaders.

Rendering is done via simple fixed-steps ray marching. The volumetric lighting effect is a result of a second opacity/shadow volume.

Tips:
- A higher order advection method (for example Mac-Cormack instead of Euler) improved quality of the simulation considerably.
- Vortices confinement helps hugely with bringing back the lost details resulted by numerical dissipation.
