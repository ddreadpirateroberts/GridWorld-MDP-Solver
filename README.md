# GridWorld-MDP-Solver
A visual implementation of Markov Decision Process (MDP) algorithms using Pygame, featuring interactive gridworld environments with Value Iteration and Policy Iteration solvers.

## Features

### Core Functionality
- **Interactive GridWorld Environment**: Customizable grid-based world with walls, pits, diamonds, and walkable tiles
- **MDP Algorithms**: Complete implementations of Value Iteration and Policy Iteration
- **Visual Learning**: Real-time visualization of algorithm convergence and policy learning
- **Stochastic Actions**: Configurable noise model for realistic action uncertainty

### Visualization Modes
- **Utility + Direction Display**: Shows state values and optimal policy directions
- **Q-Value Display**: Visualizes action-value functions with color-coded triangular segments
- **Real-time Updates**: Watch algorithms converge step-by-step

### Environment Features
- **Random World Generation**: Procedurally generated gridworlds with customizable goal and wall ratios
- **Connectivity Validation**: Ensures all terminal states remain reachable
- **Configurable Parameters**: Adjustable discount factor, noise level, and living rewards

## Getting Started

### Prerequisites
```bash
pip install pygame
```

### Quick Start
```bash
# Run basic gridworld
python gridworld.py

# Run MDP solver interface
python optimal_policy.py

# Run performance tests
python test.py
```

### Controls
- **V + 1**: Run Value Iteration (Utility/Direction view)
- **V + 2**: Run Value Iteration (Q-Value view)
- **P + 1**: Run Policy Iteration (Utility/Direction view)
- **P + 2**: Run Policy Iteration (Q-Value view)
- **W**: Wipe current values and reset
- **N**: Generate new random gridworld
- **ESC**: Exit application

## Technical Details

- **Environment**: Discrete state-action space with customizable transitions
- **Rewards**: Terminal states (diamonds: +1, pits: -1) plus optional living rewards
- **Convergence**: Configurable threshold-based stopping criteria
- **Performance**: Optimized for large gridworlds

## Code Structure

- `gridworld.py`: Core environment and visualization
- `optimal_policy.py`: MDP solver implementations
- `settings.py`: Configuration constants
- `test.py`: Performance benchmarking and robot simulation
