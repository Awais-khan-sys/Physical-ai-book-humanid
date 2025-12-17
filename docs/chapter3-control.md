# Chapter 3: Control & Actuation

## 3.1 Control Hierarchy

Humanoid robot control is organized in hierarchical layers:

1. **High-Level Planning**: Task planning, behavior selection (1-10 Hz)
2. **Mid-Level Control**: Motion planning, trajectory generation (10-100 Hz)
3. **Low-Level Control**: Joint-level motor control (100-1000 Hz)

Each layer operates at different timescales and abstraction levels.

## 3.2 Kinematics

### Forward Kinematics

Computing end-effector position from joint angles:

**Mathematical Foundation**:
- Coordinate frames for each link
- Denavit-Hartenberg (DH) parameters
- Homogeneous transformation matrices

**Example**: For a 3-link planar arm:
```
x = l1·cos(θ1) + l2·cos(θ1+θ2) + l3·cos(θ1+θ2+θ3)
y = l1·sin(θ1) + l2·sin(θ1+θ2) + l3·sin(θ1+θ2+θ3)
```

**Applications**:
- Determining where the hand is in 3D space
- Collision checking
- Visualization and simulation

### Inverse Kinematics (IK)

Computing joint angles to reach a desired end-effector pose:

**Challenges**:
- **Multiple Solutions**: Multiple joint configurations may achieve the same pose
- **No Solution**: Target may be out of reach
- **Singularities**: Loss of degrees of freedom at certain configurations

**Solution Methods**:

**Analytical IK**:
- Closed-form solutions
- Fast computation
- Only available for specific kinematic structures (e.g., 6-DoF arms with spherical wrist)

**Numerical IK**:
- Iterative optimization (Jacobian-based methods)
- Handles arbitrary kinematic chains
- Slower, may get stuck in local minima

**Modern Approach - Learning-Based IK**:
- Train neural networks on IK solution datasets
- Fast inference, handles constraints
- Examples: IKFlow, TransIK

## 3.3 Dynamics

Understanding forces and torques in robot motion:

### Equations of Motion

**Lagrangian Mechanics**:
- Derive dynamics from kinetic and potential energy
- Standard form: M(q)q̈ + C(q,q̇)q̇ + G(q) = τ
  - M(q): Inertia matrix
  - C(q,q̇): Coriolis and centrifugal terms
  - G(q): Gravity terms
  - τ: Joint torques

**Recursive Newton-Euler**:
- Efficient algorithm for computing dynamics
- Used in real-time control

### Forward vs. Inverse Dynamics

**Forward Dynamics**: Given torques → compute accelerations
- Used in simulation

**Inverse Dynamics**: Given desired accelerations → compute required torques
- Used in control (computing feed-forward terms)

## 3.4 Locomotion Control

### Bipedal Walking Fundamentals

**Gait Cycle**:
1. **Double Support**: Both feet on ground
2. **Single Support**: One foot on ground, one swinging
3. **Flight Phase** (running): Both feet off ground

**Stability Criteria**:

**Zero Moment Point (ZMP)**:
- Point where net moment from ground reaction forces is zero
- For stable walking: ZMP must be inside support polygon
- Classical approach used in ASIMO, HRP series

**Center of Mass (CoM) Control**:
- Maintaining CoM over support polygon
- Linear Inverted Pendulum Model (LIPM)
- Model Predictive Control (MPC) for CoM trajectory

### Modern Walking Controllers

**Whole-Body Control (WBC)**:
- Simultaneously control all joints for balance, locomotion, and manipulation
- Formulated as optimization problem (Quadratic Program)
- Constraints: Joint limits, torque limits, friction cone, ZMP

**Learning-Based Locomotion**:
- Reinforcement learning in simulation, then deploy to hardware
- Examples: ANYmal (ETH Zurich), Cassie (Agility Robotics)
- Learns robust gaits that handle disturbances and terrain

**Trajectory Optimization**:
- Optimize full-body trajectories offline
- Use as reference for online controller
- Methods: Direct collocation, Differential Dynamic Programming (DDP)

### Terrain Adaptation

**Perception-Locomotion Integration**:
- Classify terrain from vision/depth
- Adjust gait parameters (step height, speed, foot placement)
- Predictive vs. reactive adaptation

**Stair Climbing**:
- Detect stair geometry
- Plan footholds
- Adjust torso height and pitch

## 3.5 Manipulation Control

### Grasping Strategies

**Force Closure**:
- Grasp that can resist arbitrary external forces
- Requires proper contact points and forces

**Grasp Planning**:
1. Detect object and estimate pose
2. Generate candidate grasps (e.g., using GraspNet)
3. Evaluate feasibility (collision-free, force closure)
4. Execute best grasp

**Learning-Based Grasping**:
- Train on large datasets (millions of grasps)
- Generalize to novel objects
- Examples: Dex-Net, Contact-GraspNet

### Compliant Manipulation

**Impedance Control**:
- Robot behaves like a spring-damper system
- Allows safe physical interaction
- Adjustable stiffness and damping

**Hybrid Force/Position Control**:
- Control force in some directions, position in others
- Example: Pushing a button (force along normal, position in tangent plane)

**Contact-Rich Tasks**:
- Assembly (peg-in-hole)
- Wiping surfaces
- Turning knobs, opening doors

## 3.6 Actuation Technologies

### Electric Motors

**Brushed DC Motors**:
- Simple, low-cost
- Maintenance required (brush wear)

**Brushless DC (BLDC) Motors**:
- High efficiency, long life
- Requires electronic commutation
- Most common in modern humanoids

**Servo Motors**:
- Built-in position control
- Easy to use, common in hobbyist robots

### Actuator Design Tradeoffs

**Direct Drive**:
- Motor directly connected to joint (no gearbox)
- Advantages: Backdrivable, no backlash, high-fidelity torque control
- Disadvantages: Low torque, requires large motors
- Example: MIT Mini Cheetah

**Geared Actuation**:
- Motor + gearbox for torque amplification
- Advantages: High torque, compact
- Disadvantages: Friction, backlash, reduced backdrivability
- Example: Boston Dynamics Atlas (hydraulic + planetary gears)

**Series Elastic Actuators (SEA)**:
- Spring in series with motor
- Advantages: Force sensing, shock absorption, safety
- Disadvantages: Lower bandwidth, added complexity

### Hydraulic vs. Electric

**Hydraulic**:
- Extremely high power density
- Continuous operation at high loads
- Requires pumps, fluid, maintenance
- Example: Boston Dynamics Atlas

**Electric**:
- Cleaner, quieter, easier to control
- Lower power density than hydraulic
- Advancing rapidly (better motors, batteries)
- Example: Tesla Optimus, Figure 01

## 3.7 Balance & Recovery

### Disturbance Rejection

Robots must handle:
- External pushes
- Uneven or slippery terrain
- Unexpected contact

**Techniques**:
- **Reactive Stepping**: Take a step to regain balance
- **Ankle/Hip Strategy**: Use ankle or hip torques to maintain balance
- **Momentum Control**: Adjust whole-body momentum

### Fall Detection & Recovery

**Fall Detection**:
- Monitor IMU (rapid acceleration/rotation)
- Predict loss of balance before falling

**Fall Mitigation**:
- Controlled fall (protect critical components)
- Posture adjustment to minimize damage

**Getting Up**:
- Pre-planned sequences (push-up, rolling)
- Learning-based approaches for diverse scenarios

## 3.8 Real-Time Control Systems

### Control Loop Requirements

**Latency**:
- Low-level control: <1ms
- Perception-to-action: <100ms
- Human reaction time: ~250ms (robots should be faster!)

**Determinism**:
- Real-Time Operating Systems (RTOS)
- Predictable execution time
- Priority-based scheduling

### Safety & Fault Tolerance

**Software Safety**:
- Watchdog timers
- Joint limit checks
- Emergency stop triggers

**Hardware Safety**:
- Torque limiters
- Mechanical hard stops
- Fuses and current limiters

**Graceful Degradation**:
- Continue operation with sensor/actuator failures
- Example: Walking with one broken ankle motor

## 3.9 Simulation for Control Development

### Why Simulate?

- Safe testing of controllers
- Rapid iteration (no hardware damage)
- Generate training data for learning
- Test edge cases (falls, collisions)

### Simulation Platforms

**Physics Engines**:
- **MuJoCo**: Fast, accurate contact dynamics
- **PyBullet**: Open-source, Python-friendly
- **Isaac Sim** (NVIDIA): GPU-accelerated, photorealistic rendering

**Robot Simulators**:
- **Gazebo**: ROS-integrated, widely used
- **Webots**: Commercial, user-friendly
- **CoppeliaSim**: Flexible scripting

### Sim-to-Real Transfer

**Domain Randomization**:
- Randomize physics parameters (friction, mass, damping)
- Randomize visual appearance
- Controller learns robust policies

**System Identification**:
- Measure real robot parameters
- Update simulation to match

## Summary

Control and actuation are where intelligence meets the physical world. Humanoid robots require hierarchical control systems spanning high-level planning to millisecond-level motor commands. Classical approaches (kinematics, dynamics, ZMP) provide foundations, while modern learning-based methods enable robust locomotion and manipulation in unstructured environments. The choice of actuation technology (electric vs. hydraulic, direct-drive vs. geared) fundamentally impacts robot capabilities and design. Simulation is essential for safe, rapid development and testing.

## Further Reading

- "Modern Robotics: Mechanics, Planning, and Control" by Kevin Lynch and Frank Park
- "Robotics: Modelling, Planning and Control" by Bruno Siciliano et al.
- Papers: Whole-body control (Sentis), Learning locomotion (Hwangbo), Atlas robot (Boston Dynamics)

---

**Next Chapter**: [Chapter 4: AI & Learning →](chapter4-ai-learning.md)
