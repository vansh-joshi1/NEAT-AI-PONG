# Pong AI Game

Neural network-based AI that learns to play Pong using the NEAT algorithm. Features both training mode and player-vs-AI gameplay.

## Requirements
- Python3 3.7+
- pygame
- neat-python 
- numpy

```bash
pip3 install pygame 
pip3 install neat-python
pip3 install numpy
```

## Usage

### Train AI
```python
# In pong.py:
run_neat(config)  # Uncomment
# test_best_network(config)  # Comment out
```
```bash
python pong.py
```

### Play vs AI
```python
# In pong.py:
# run_neat(config)  # Comment out
test_best_network(config)  # Uncomment
```

## Controls
- W: Move left paddle up
- S: Move left paddle down
- AI controls right paddle

## Display
- Left score: Human player
- Right score: AI
- Red number (training mode): Total hits

## Game Mechanics
- Dynamic ball physics
- Angle-based paddle deflection
- Wall/paddle collision detection
- Progressive AI learning

## Architecture
- NEAT algorithm for AI training

## Troubleshooting
- Missing best.pickle: Retrain AI
- pygame not found: Check Python path
- Crashes on launch: Verify config.txt
  
