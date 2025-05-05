import numpy as np
import random

rows, cols = 5, 5
actions = ['north', 'south', 'east', 'west']
action_map = {'north': (-1, 0), 'south': (1, 0), 'east': (0, 1), 'west': (0, -1)}
gamma = 0.9
alpha = 0.2
epsilon = 0.1
episodes = 5000
steps = 5000

special_states = {'A': (0, 1), 'B': (0, 3)}
next_to_states = {"A'": (4, 1), "B'": (2, 3)}
special_rewards = {'A': 10, 'B': 5}

Q = np.zeros((rows, cols, len(actions)))

def step(state, action):
    if state == special_states['A']:
        return next_to_states["A'"], special_rewards['A']
    elif state == special_states['B']:
        return next_to_states["B'"], special_rewards['B']

    dr, dc = action_map[action]
    nr, nc = state[0] + dr, state[1] + dc

    if 0 <= nr < rows and 0 <= nc < cols:
        return (nr, nc), 0
    else:
        return state, -1  

def choose_action(state):
    if random.random() < epsilon:
        return random.randint(0, len(actions) - 1)
    else:
        r, c = state
        return np.argmax(Q[r, c])

print("Initializing Gridworld...")
print(f"Grid size: {rows}x{cols}")
print(f"Special_states = {special_states}")
print(f"Next_to_states = {next_to_states}")
print(f"Special_rewards = {special_rewards}")
print("Starting Q-learning with parameters:")
print(f"  γ = {gamma}")
print(f"  ε = {epsilon}")
print(f"  α = {alpha}")
print(f"  Episodes = {episodes}")
print(f"  Steps = {steps}\n")

for _ in range(episodes):
    state = (random.randint(0, rows - 1), random.randint(0, cols - 1))
    for _ in range(steps):
        a_idx = choose_action(state)
        action = actions[a_idx]
        next_state, reward = step(state, action)
        r, c = state
        nr, nc = next_state
        best_next = np.max(Q[nr, nc])
        Q[r, c, a_idx] += alpha * (reward + gamma * best_next - Q[r, c, a_idx])
        state = next_state

print("Evaluating optimal value function and policy...")

V = np.max(Q, axis=2)
policy_idx = np.argmax(Q, axis=2)

arrow_map = {0: '↑', 1: '↓', 2: '→', 3: '←'}

print("Optimal Value Function:")
for row in V:
    print("  ".join(f"{val:.2f}" for val in row))
print()

print("Optimal Policy:".ljust(30) + "Optimal Policy (arrows):")
for r in range(rows):
    word_policy = "  ".join(f"{actions[policy_idx[r, c]]:<6}" for c in range(cols))
    arrow_policy = "  ".join(f"{arrow_map[policy_idx[r, c]]:<3}" for c in range(cols))
    print(f"{word_policy}       {arrow_policy}")
