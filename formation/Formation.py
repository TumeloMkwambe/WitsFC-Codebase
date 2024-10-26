import numpy as np

def GenerateBasicFormation(ball_position, opposition_team):

    if ball_position[0] < -1:
        formation = [
        np.array([-13, 0]),    # Goalkeeper
        opposition_team[10],  # Left Defender
        opposition_team[9],   # Center Back Left
        opposition_team[8],    # Center Back Right
        opposition_team[7],   # Right Defender
        opposition_team[6],    # Left Midfielder
        np.array([5, -2]),    # Center Midfielder Left
        np.array([10, -1]),     # Center Midfielder Right
        np.array([8, 2.5]),     # Right Midfielder
        np.array([-0.5, 0]),    # Forward Left
        np.array([12, 2])      # Forward Right
        ]
        return formation
    else:
        formation = [
            np.array([-13, 0]),    # Goalkeeper
            np.array([-9, -3]),  # Left Defender
            np.array([-5, -1.5]),   # Center Back Left
            np.array([-9, 3]),    # Center Back Right
            np.array([-5, 1.5]),   # Right Defender
            np.array([3, 2]),    # Left Midfielder
            np.array([5, -2]),    # Center Midfielder Left
            np.array([10, -1]),     # Center Midfielder Right
            np.array([8, 2.5]),     # Right Midfielder
            np.array([-0.5, 0]),    # Forward Left
            np.array([12, 2])      # Forward Right
        ]
        return formation
