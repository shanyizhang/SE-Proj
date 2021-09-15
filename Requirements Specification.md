# Requirements Specification

Sep.15th, 2021 | CSCI-GA-2440-001 Software Engineering



### 1. Project Team

Ken S. Zhang | sz1851@nyu.edu

Qingyang Li | ql2048@nyu.edu



### 2. Introduction

The goal of this course project is to build a Python-based **Tetris** game. This game provides features that follow the widely-accepted rules. This document describes the requirements of this program. 



### 3. Use Cases

**UC1** Game Setup

**UC2** View Leader Board

UC3 Move Downward

UC4 Shift Horizontally

UC5 Rotate

UC6 View Next Tetromino







### UC1 Game Setup

**1.1 Preconditions:**
None.

**1.2 Main Flow:**

Right after the The user set the level of difficulty 

**1.3 Sub Flows:**

None.

**1.4 Alternative Flows：**

None.

### UC4 Shift Horizontally

**4.1 Preconditions:**

The current tetromino is still moving downward.

**4.2 Main Flow:**

The player may move the current tetromino left or right by one grid \[S1\] \[E1\]. After that, the horizontal location of the current tetromino is altered, and the tetromino continues to move downward (**UC3**).

**4.3 Sub Flows:**

\[S1\] The player clicks the "move left" or "move right" button. If the movement is valid, the tetromino will move to the corresponding location accordingly.

**4.4 Alternative Flows:**

\[E1\] When the current tetromino has reached the leftmost/rightmost column, "move left/right" will not succeed, and nothing will happen.

### UC5 Rotate

**5.1 Preconditions:**

The current tetromino is still moving downward.

**5.2 Main Flow:**

The player may rotate the current tetromino clockwise or counter-clockwise by 90 degrees \[S1\] \[E1\]. If the rotation is valid, the spatial position of the current tetromino is altered, and the tetromino continues to move downward (**UC3**).

**5.3 Sub Flows:**

\[S1\] The player clicks the "clockwise" or "counter-clockwise" button. The tetromino will then alter its spatial position.

**5.4 Alternative Flows:**

\[E1\] If, after the tetromino has been rotated to the new position, the tetromino is "out of boundary", or conflicted with the stacked tetrominoes, the movement will become invalid. In this case, the rotation operation will not succeed, and nothing will happen.

### UC6 View Next Tetromino

**6.1 Preconditions:**

The current tetromino is moving downward.

**6.2 Main Flow:**

While the current tetromino is moving downward (**UC3**), the appearance of the next tetromino generated \[S1\] will be displayed somewhere outside the playing field.

**6.3 Sub Flows:**

\[S1\] If this is not done, the system will generate the next tetromino randomly.

**6.4 Alternative Flows:**

None.