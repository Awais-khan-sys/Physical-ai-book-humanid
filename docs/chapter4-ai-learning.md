# Chapter 4: AI & Learning for Physical Intelligence

## 4.1 Machine Learning Paradigms for Robotics

### Supervised Learning

**Definition**: Learn from labeled examples (input-output pairs)

**Robotics Applications**:
- Object detection: Images → bounding boxes + labels
- Inverse kinematics: Target pose → joint angles
- Grasping: Object image → grasp pose

**Limitations**:
- Requires large labeled datasets
- Expensive to collect for robotics (real-world demonstrations)
- Struggles with distribution shift

### Imitation Learning (Behavioral Cloning)

**Definition**: Learn by mimicking expert demonstrations

**Process**:
1. Collect demonstrations (human teleoperation or kinesthetic teaching)
2. Train policy: observations → actions
3. Deploy policy on robot

**Challenges**:
- **Compounding errors**: Small mistakes accumulate
- **Distribution shift**: Training data doesn't cover all situations
- **Covariate shift**: Robot ends up in states not seen during training

**Advanced Techniques**:
- **DAgger** (Dataset Aggregation): Iteratively collect data from policy, get expert corrections
- **HG-DAgger**: Human-guided DAgger with safety guarantees

### Reinforcement Learning (RL)

**Definition**: Learn by trial-and-error interaction with environment

**Framework**:
- **Agent**: The robot
- **Environment**: Physical world or simulation
- **State** (s): Observations
- **Action** (a): Robot commands
- **Reward** (r): Scalar feedback signal
- **Goal**: Maximize cumulative reward

**RL Algorithms**:

**Policy Gradient Methods**:
- Directly optimize policy parameters
- Examples: PPO (Proximal Policy Optimization), TRPO
- Pro: Stable, works with continuous actions
- Con: Sample inefficient

**Value-Based Methods**:
- Learn value function Q(s,a)
- Examples: DQN, SAC (Soft Actor-Critic)
- Pro: More sample efficient
- Con: Harder for continuous action spaces

**Model-Based RL**:
- Learn model of environment dynamics
- Plan using the model
- Pro: Sample efficient, interpretable
- Con: Model errors can degrade performance

## 4.2 Deep Reinforcement Learning for Robotics

### Sim-to-Real RL

**Why Simulation?**
- Safe: No hardware damage
- Fast: Parallelize thousands of environments
- Cheap: No physical robot required

**The Sim-to-Real Gap**:
- Physics simulation is imperfect
- Visual appearance differs
- Sensor noise patterns differ

**Bridging the Gap**:

**Domain Randomization**:
- Randomize physics parameters (mass, friction, damping)
- Randomize visual appearance (lighting, textures)
- Policy learns to be robust to variations

**Adversarial Training**:
- Train policy to handle worst-case perturbations
- More robust than random perturbations alone

**Privileged Learning**:
- Train with extra information in sim (ground-truth state)
- Deploy with only real sensors
- Examples: Learning with oracle perception, then using vision

### Case Study: Learning Quadruped Locomotion

**Approach** (ANYmal, ETH Zurich):
1. Train policy in simulation (Isaac Gym, parallelized)
2. Inputs: Proprioception (joint angles, velocities), IMU
3. Outputs: Joint torques
4. Reward: Forward velocity, low energy, smooth gait
5. Domain randomization: Mass, friction, latency, noise
6. Deploy to real robot → robust locomotion on diverse terrain

**Results**:
- Walking on grass, gravel, stairs, slopes
- Recovers from pushes and slips
- Zero-shot transfer (no real-world training)

## 4.3 Foundation Models for Robotics

### What are Foundation Models?

Large models pre-trained on massive datasets, then adapted to specific tasks:

**Key Properties**:
- **Generalization**: Handle diverse scenarios
- **Few-shot learning**: Adapt with minimal task-specific data
- **Multimodal**: Process vision, language, action, proprioception

### Vision-Language-Action Models

**RT-1 (Robotics Transformer)**:
- Architecture: Vision Transformer + Transformer policy
- Training: 130k robot manipulation demonstrations
- Capabilities: 700+ tasks (pick, place, open, close, etc.)

**RT-2 (RT + VLM)**:
- Combines RT-1 with vision-language pre-training (PaLI-X)
- Leverages web-scale image-text data
- Emergent capabilities: Reasoning, novel object manipulation

**How It Works**:
1. Input: Camera image + language instruction ("pick up the blue cup")
2. Vision encoder: Extract visual features
3. Language encoder: Embed instruction
4. Transformer policy: Output robot action (joint positions or velocities)
5. Execute action, observe next state, repeat

### π0 (Physical Intelligence Foundation Model)

**Vision**: A generalist policy for physical AI

**Architecture**:
- Multimodal input: Vision, language, proprioception
- Output: Low-level control (joint positions/torques)
- Pre-trained on diverse robot data (multiple platforms, tasks)

**Key Innovation**:
- Flow matching for action prediction
- Handles high-dimensional, multi-modal action spaces
- Generalizes across robot morphologies

**Demonstrated Capabilities**:
- Folding clothes
- Assembling boxes
- Table bussing
- Zero-shot generalization to new objects and scenarios

### GPT-4o / Gemini for Robotics

**Multimodal Large Language Models (MLLMs)**:
- Understand images, text, video
- Reasoning about physical tasks
- Code generation for robot control

**Use Cases**:

**Task Planning**:
- Input: "Make me a sandwich"
- Output: Step-by-step plan ("1. Get bread, 2. Open jar, 3. Spread peanut butter...")

**Visual Reasoning**:
- Input: Image of cluttered table + "Which object should I pick first?"
- Output: Reasoning about object dependencies

**Code-as-Policy**:
- Generate Python code to control robot
- Example: SayCan (Google), Code-as-Policies (MIT)

## 4.4 Learning Dexterous Manipulation

### Challenges

- High-dimensional action space (20+ DoF for hands)
- Contact-rich dynamics
- Precise control required

### Approaches

**Model-Free RL**:
- Learn end-to-end from reward signal
- Example: OpenAI's Dactyl (solving Rubik's cube with robot hand)
- Trained entirely in simulation with domain randomization

**Model-Based RL**:
- Learn dynamics model, plan with it
- More sample efficient
- Example: Visual Foresight (Sergey Levine)

**Imitation Learning**:
- Learn from human demonstrations
- Example: DexMV (learning from multi-view video of human hands)

### Hardware Considerations

**Dexterous Hands**:
- **Shadow Hand**: 20 DoF, anthropomorphic
- **Allegro Hand**: 16 DoF, affordable research platform
- **Leap Hand**: 16 DoF, low-cost (~$2000)

**Tactile Sensing**:
- Essential for fine manipulation
- DIGIT sensors on fingertips
- Learn tactile-based policies

## 4.5 Multi-Task & Lifelong Learning

### The Generalist Robot Challenge

Single-task policies don't scale:
- Need separate policy for each task
- Cannot leverage shared knowledge
- Expensive to train

**Goal**: One policy for many tasks

### Multi-Task Learning

**Shared Representation**:
- Single neural network, task-conditioned
- Input: Observation + task specification (language, task ID)
- Output: Actions for that task

**Benefits**:
- Positive transfer (learning one task helps others)
- Data efficiency (share data across tasks)

**Challenges**:
- Negative transfer (tasks interfere)
- Balancing task diversity vs. specialization

### Continual Learning

**Problem**: Catastrophic forgetting
- Training on new tasks degrades performance on old tasks

**Solutions**:

**Rehearsal**:
- Store examples from old tasks, replay during training
- Example: Experience replay buffers

**Regularization**:
- Penalize changes to parameters important for old tasks
- Example: Elastic Weight Consolidation (EWC)

**Modular Architectures**:
- Separate modules for different tasks
- Learn which modules to activate

## 4.6 Sim-to-Real Transfer in Detail

### Visual Sim-to-Real

**Appearance Gap**:
- Simulated images look different from real
- Solutions:
  - **Photorealistic rendering**: NVIDIA Isaac Sim, Blender
  - **Domain randomization**: Vary lighting, textures, colors
  - **CycleGAN**: Translate sim images to look real

**Depth Sim-to-Real**:
- Depth sensors have specific noise patterns
- Simulate realistic depth noise

### Dynamics Sim-to-Real

**Parameter Identification**:
- Measure real robot parameters (mass, friction, motor constants)
- Update simulation to match

**Learned Residuals**:
- Learn correction on top of simulator
- Hybrid model: Physics simulator + learned residual

**Adaptive Policies**:
- Policy that can adapt online to real dynamics
- Example: Meta-learning (learning to learn)

## 4.7 Safety in Learning-Based Control

### Challenges

- RL explores randomly during training (unsafe!)
- Learned policies can be unpredictable
- No formal guarantees

### Safe RL Approaches

**Constrained RL**:
- Optimize reward subject to safety constraints
- Example: Constrained Policy Optimization (CPO)

**Shielding**:
- Safety monitor overrides unsafe actions
- Backup controller takes over if needed

**Verification**:
- Formally verify neural network policies
- Check if policy satisfies safety properties

### Sim-Safe, Real-Safe

**Strategy**:
- Ensure policy is safe in simulation (including worst-case scenarios)
- Domain randomization includes safety-critical variations
- If safe in diverse sims → likely safe in reality

## 4.8 Data for Robot Learning

### Data Sources

**Real Robot Data**:
- Gold standard, but expensive
- Examples: RT-X dataset (1M+ trajectories, 22 robot types)

**Simulation**:
- Cheap, scalable
- Used for pre-training

**Human Video**:
- Abundant (YouTube, Ego4D)
- Learn visual representations, task structure
- Example: R3M (learning representations from video)

**Teleoperation**:
- Human controls robot to collect demos
- High-quality, goal-directed data
- Example: ALOHA system for mobile manipulation

### Data Efficiency

**Why It Matters**:
- Real robot data is expensive (wear, time, safety)
- Goal: Learn from as few samples as possible

**Techniques**:
- **Pre-training**: Transfer from large datasets
- **Data augmentation**: Perturb images, add noise
- **Model-based RL**: Learn model, generate synthetic data

## Summary

AI and learning are revolutionizing physical intelligence. Reinforcement learning enables robots to discover complex behaviors through trial-and-error in simulation, then transfer to the real world via domain randomization. Foundation models pre-trained on massive datasets unlock generalization to novel tasks and objects with minimal fine-tuning. The frontier is moving toward generalist robots: single policies capable of hundreds or thousands of tasks, continuously learning from experience. Key challenges remain: safety, sample efficiency, and bridging the sim-to-real gap. The integration of vision-language models with robotic control is enabling intuitive, natural-language interfaces for physical AI.

## Further Reading

- "Reinforcement Learning: An Introduction" by Sutton and Barto
- "Deep Reinforcement Learning" by Pieter Abbeel and Sergey Levine (course: CS 285)
- Papers: RT-2 (Google), π0 (Physical Intelligence), Dactyl (OpenAI), Isaac Gym (NVIDIA)
- Code: Stable-Baselines3, RLlib, OpenAI Gym

---

**Next Chapter**: [Chapter 5: Applications & Future →](chapter5-applications.md)
