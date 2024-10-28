import numpy as np
import joblib
import os
from .utils import (
    allocate_resources,
    coin_flip,
    resource_bar,
    log_battle_data,
    calculate_strength,
    reinforce_units
)

# Dynamically resolve the paths to the model and scaler
model_path = os.path.join(os.path.dirname(__file__), 'models', 'optimized_battle_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), 'models', 'scaler.pkl')

# Load the pre-trained battle model and scaler with error handling
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("Model and scaler loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading model or scaler: {e}")
    raise
# Function to simulate a single battle day
def simulate_day(user_role, user_resources, model_resources, day):
    print(f"\n--- Day {day} ---")

    print("\nYour resources to deploy:")
    print(resource_bar("Units", user_resources['units'], 6000))
    print(resource_bar("Tanks", user_resources['tanks'], 100))
    print(resource_bar("Drones", user_resources['drones'], 60))
    print(resource_bar("Artillery", user_resources['artillery'], 80))
    print(resource_bar("Air Support", user_resources['air_support'], 100))

    # Collect user input for deployment
    try:
        user_deployed = {
            'units': min(int(input("How many units? ")), user_resources['units']),
            'tanks': min(int(input("How many tanks? ")), user_resources['tanks']),
            'drones': min(int(input("How many drones? ")), user_resources['drones']),
            'artillery': min(int(input("How many artillery? ")), user_resources['artillery']),
            'air_support': min(int(input("How many air support? ")), user_resources['air_support'])
        }
    except ValueError:
        print("Invalid input! Please enter numbers only.")
        return user_resources, model_resources

    # Update user resources
    for key in user_deployed:
        user_resources[key] -= user_deployed[key]

    # Prepare the input for the model (10 features: 5 user + 5 model resources)
    model_input = np.array([[user_resources['units'], user_resources['tanks'], 
                             user_resources['drones'], user_resources['artillery'], 
                             user_resources['air_support'],
                             model_resources['units'], model_resources['tanks'], 
                             model_resources['drones'], model_resources['artillery'], 
                             model_resources['air_support']]])

    # Scale the input using the trained scaler
    scaled_input = scaler.transform(model_input)
    model_decision = model.predict(scaled_input)[0]

    # Decide deployment ratio based on model's decision
    deploy_ratio = 0.7 if model_decision == 0 else 0.4
    model_deployed = {k: int(v * deploy_ratio) for k, v in model_resources.items()}

    # Update model resources
    for key in model_deployed:
        model_resources[key] -= model_deployed[key]

    print(f"\nYou deployed: {user_deployed}")
    print(f"Model deployed: {model_deployed}")

    # Calculate the strengths
    user_strength = calculate_strength(user_deployed)
    model_strength = calculate_strength(model_deployed)

    # Determine the outcome
    if user_strength > model_strength:
        outcome = 'User Wins Day'
        damage = int((user_strength - model_strength) * 0.1)
        model_resources['units'] -= max(0, damage)
    elif model_strength > user_strength:
        outcome = 'Model Wins Day'
        damage = int((model_strength - user_strength) * 0.1)
        user_resources['units'] -= max(0, damage)
    else:
        outcome = 'Stalemate'

    # Log the battle data
    log_battle_data(day, user_deployed, model_deployed, user_resources, model_resources, outcome)

   # Display remaining resources using the progress bar
    print("\nRemaining Resources after today's battle:")
    print(resource_bar("Your Units", user_resources['units'], 6000))
    print(resource_bar("Model's Units", model_resources['units'], 6000))

    return user_resources, model_resources

# Function to start the battle simulation
def start_battle_simulation():
    print("Welcome to the Battle Simulation!")

    user_role = coin_flip()
    model_role = 'defender' if user_role == 'attacker' else 'attacker'

    user_resources = allocate_resources(user_role)
    model_resources = allocate_resources(model_role)

    print(f"\nYou are the {user_role}. Your resources: {user_resources}")
    print(f"The model is the {model_role}. Model's resources: {model_resources}")

    day = 1
    while user_resources['units'] > 0 and model_resources['units'] > 0 and day <= 10:
        if day > 1:
            reinforce_units(user_resources)
            reinforce_units(model_resources)

        user_resources, model_resources = simulate_day(user_role, user_resources, model_resources, day)
        day += 1

    if user_resources['units'] <= 0:
        print("The model wins!")
    elif model_resources['units'] <= 0:
        print("You win!")
    else:
        print("The battle ends in a stalemate.")

# Entry point
if __name__ == "__main__":
    start_battle_simulation()
