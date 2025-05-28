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

## Algorithm Implementations

### Value Iteration
Iteratively updates state utilities using the Bellman equation until convergence:
```
V*(s) = max_a Σ P(s'|s,a)[R(s,a,s') + γV*(s')]
```

### Policy Iteration
Alternates between policy evaluation and policy improvement:
1. **Policy Evaluation**: Compute utilities for current policy
2. **Policy Improvement**: Update policy based on computed utilities

### Stochastic Model
Actions succeed with probability (1-noise), with equal probability of deviating left or right, modeling realistic uncertainty in action execution.

## Applications

- **Reinforcement Learning Education**: Visual demonstration of fundamental MDP concepts
- **Algorithm Comparison**: Side-by-side performance analysis of VI vs PI
- **Research Prototyping**: Extensible framework for testing new MDP variants
- **Interactive Learning**: Hands-on exploration of how parameters affect optimal policies

## Technical Details

- **Environment**: Discrete state-action space with customizable transitions
- **Rewards**: Terminal states (diamonds: +1, pits: -1) plus optional living rewards
- **Convergence**: Configurable threshold-based stopping criteria
- **Performance**: Optimized for large gridworlds (tested up to 70x70)

## Code Structure

- `gridworld.py`: Core environment and visualization
- `optimal_policy.py`: MDP solver implementations
- `settings.py`: Configuration constants
- `test.py`: Performance benchmarking and robot simulation

Perfect for students learning reinforcement learning, researchers prototyping MDP algorithms, or anyone interested in visualizing how intelligent agents learn optimal behavior in uncertain environments.
