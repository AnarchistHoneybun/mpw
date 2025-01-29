---
title: Warehouse Sokoban
subtitle: Advent of Code '24, Day 15
author: Nirv
author-url: "https://github.com/AnarchistHoneybun"
date: 2024-12-15
lang: en
toc-title: Contents
version: v0.1.0
---

## Introduction

This post explores [Day 15](https://adventofcode.com/2024/day/15) of Advent of Code 2024. The problem presents an interesting scenario involving a robot navigating a warehouse while pushing boxes around, with an unusual twist in how the boxes behave in Part 2.

![](../../assets/warehouse_part1_ascii.gif)


## Problem Statement

We're tasked with helping some lanternfish manage their warehouse automation. Their robot has gone rogue and is moving boxes around, but its movements follow a predictable pattern. The challenge involves:

1. Predicting robot movement and box positions in a warehouse
2. Calculating a "GPS" score based on final box positions
3. Handling special double-width boxes in Part 2

Here's a small example of the input:
```
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
```

[Part 1 movement visualization should go here - warehouse_part1_ascii.gif]

## Solution Approach

### Part 1: Single-Width Box Movement

The core challenge is modeling how boxes move when pushed by the robot. This involves:
1. Checking if a move is valid
2. Finding all boxes that would be affected by a push
3. Moving boxes in the correct order

Here's the algorithm for attempting a move:

```
╭───────────────────────────────────────────────────────────╮
│function TryMove(direction):                               │
│    new_pos = robot_pos + direction                        │
│                                                           │
│    if new_pos contains wall:                              │
│        return false                                       │
│                                                           │
│    if new_pos is empty:                                   │
│        move robot                                         │
│        return true                                        │
│                                                           │
│    // Moving into a box - need to check all affected      │
│    boxes = BFS from robot position to find connected boxes│
│                                                           │
│    if any box would hit wall:                             │
│        return false                                       │
│                                                           │
│    // Move boxes in direction-appropriate order           │
│    sort boxes based on movement direction                 │
│    for each box in sorted order:                          │
│        if next position is free:                          │
│            move box                                       │
│                                                           │
│    move robot                                             │
│    return true                                            │
╰───────────────────────────────────────────────────────────╯
```

<details>
<summary>Example: Box Movement Chain Reaction</summary>

Initial state:
```
########
#..O.O.#  Robot (@) attempts to move right
##@.O..#  This will cause a chain reaction
#...O..#  of box movements
########
```

1. Robot moves right, pushing first box
```
########
#..O.O.#
##.@O..#  First box is pushed
#...O..#
########
```

2. Second box is pushed
```
########
#..O.O.#
##..@O.#  Second box moves
#...O..#
########
```

3. Final state after complete movement
```
########
#..O.O.#
##...@O#  Movement complete
#...O..#
########
```
</details>

### Part 2: Double-Width Box Logistics

Part 2 introduces an interesting twist: all boxes are now double-width, represented as `[]` instead of `O`. This changes how boxes move and interact:

[Part 2 movement visualization should go here - warehouse_part2_ascii.gif]

The core algorithm remains similar, but with modified box detection:

```
╭──────────────────────────────────────────────────────────╮
│function FindConnectedBoxes(position):                    │
│    boxes = empty set                                     │
│    queue = [position]                                    │
│                                                          │
│    while queue not empty:                                │
│        pos = queue.pop()                                 │
│        if pos in boxes:                                  │
│            continue                                      │
│                                                          │
│        boxes.add(pos)                                    │
│        curr_char = grid[pos]                             │
│                                                          │
│        if curr_char is '[':                              │
│            // Add matching ']' to right                  │
│            queue.add(pos + (0,1))                        │
│        if curr_char is ']':                              │
│            // Add matching '[' to left                   │
│            queue.add(pos + (0,-1))                       │
│                                                          │
│    return boxes                                          │
╰──────────────────────────────────────────────────────────╯
```

<details>
<summary>Example: Double-Width Box Movement</summary>

Initial state with double-width boxes:
```
##############
##......##..##
##..[]....[]##  Robot attempts to move right
##@.[]....[]##  Note how boxes take two spaces
##..........##
##############
```

After movement:
```
##############
##......##..##
##..[]....[]##  Both boxes shift together
##..@[]...[]##  maintaining their double-width
##..........##
##############
```
</details>

## Key Insights

1. **Box Chain Reactions**: The trickiest part is handling cases where moving one box causes others to move. Sorting boxes based on movement direction ensures we don't get stuck in impossible situations.

2. **Double-Width Box Handling**: Part 2's double-width boxes require careful tracking of box pairs. We need to ensure both parts of a box move together and maintain proper spacing.

3. **GPS Coordinate System**: The GPS scoring system creates an interesting optimization challenge, as moving boxes vertically has a much larger impact on the score than moving them horizontally.

## Implementation Details

Some interesting implementation challenges:

1. **Direction-Based Sorting**: When moving boxes, we need to sort them based on the movement direction to avoid blocking situations:
```python
# For rightward movement:
points.sort_by_key(|&(r, c)| (r, c))  # Sort by column ascending

# For leftward movement:
points.sort_by_key(|&(r, c)| (r, -c)) # Sort by column descending
```

2. **Box Detection**: Using breadth-first search (BFS) to find connected boxes ensures we don't miss any boxes that might be affected by a move.

## Conclusion

This puzzle combines spatial reasoning with careful state management. The Part 2 twist with double-width boxes adds an interesting layer of complexity that requires rethinking how we track and move objects in our grid.

The visualization of the robot's movement really helps understand how the boxes interact and move, especially in Part 2 where the double-width boxes create new movement patterns.