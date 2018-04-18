---
layout: default
---

# Gomoku
## A practical problem for tree search

Tree search algorithms are one of the most popular among coding interview questions.
You often hear people say : but it's boring and I will never use it in real life.
Here is a perfect example of how tree search works in a practical setting.

Gomoku is essentially a super supped up version of Tic Tac Toe.
Played on a Go board, first player to have a line of five stones wins.

To implement a Gomoku AI, the starting point is the mini-max search algorithm.
Basically you treat the current state of the game as the root of tree, and each possible successive move as a child node, and keep expanding.
You evaluate each node (current situation) based on the best outcome for you.
Two player take turns to make moves so that the next level is always the result of the component's move, and you assume his decision is to choose the best outcome for him thus worst outcome for you.
So you pick from all the children nodes which represent the worst cases, and you pick the best one.

We do a depth first search of tree, since the score of a node depends on its children.
How alpha-beta pruning works is that once we evaluated a child there is no point keep of expending the siblings that are guaranteed to result in a lower score.

The biggest problem here is the size of the search space (depth and width of the tree).
First of all we have to limit the max depth of the search, we can't keep looking ahead forever. Usually looking forward 10 plys would already result in a strong AI player since a human player usually only consider 4-5 plys ahead.
But it means most of the time when we reaches the max depth, we don't reach a terminal state, so we need a heuristics to estimate the goodness of the situation
Next is the number of children at each node. A standard Gomoku game plays on a 15x15 board, that's ~1.5k children at each node. If we have a max depth of 10, that's 1.5k^9 nodes to consider and that's just impossible.
A typical strategy is scan the board and rank children based on heuristics, and only expanding the top ones. That cuts down the number of nodes to 1 billion, which is still a lot, but manageable. What's more, by choosing the top children, we have a higher chance that most of the nodes will be trimmed by alpha-beta.

I've spent some time to build the game in Unity. It was a lot of fun to do the pixel art style assets.
The AI could be done in C# scripts but for a task that is as heavy as this it's really more appropriate to use native C++, so I implemented the AI as a native dll.
The AI logic can take a bit of mental gymnastics to process but mostly straight forward.
What's interesting is to provide some visualizations of how the search works, here I simply plot the scores for the level 1 nodes.
