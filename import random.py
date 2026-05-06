import random

# BASKETBALL END-GAME MONTE CARLO SIMULATION
# Scenario: Your team is down 3 points with 30 seconds left.

# Strategy A: Attempt a 3-pointer right away.
# ==============================================================
# Strategy B: Take an easy 2 and immediately foul to get the ball back.
 
# PARAMETERS
NUM_TRIALS          = 10_000   # Number of simulated games per strategy
 
MY_3PT_PERCENT      = 0.35     # Probability of making a 3-pointer
MY_2PT_PERCENT      = 0.55     # Probability of making a 2-pointer
OPP_FT_PERCENT      = 0.70     # Opponent's free-throw percentage
OFFREB_PERCENT      = 0.25     # Probability of grabbing an offensive rebound
OT_WIN_PERCENT      = 0.50     # Probability of winning in overtime
STARTING_TIME       = 30       # Time remaining in the game (seconds)
 
# Time costs (seconds) for each event
TIME_3PT_ATTEMPT    = 5        # Time used to run a 3-point play
TIME_2PT_ATTEMPT    = 4        # Time used to run a 2-point play
TIME_INBOUND        = 3        # Time for opponent to inbound + dribble before foul
TIME_FT_SEQUENCE    = 5        # Time for a free-throw sequence
TIME_REBOUND_PLAY   = 4        # Time after grabbing an offensive rebound

# Keep the "Big Picture" logic separate from the "Tiny Detail" logic.
def shoot_free_throw():
    """Simulate shooting a free throw and return True if made, False if missed."""
    return random.random() < OPP_FT_PERCENT
# this is our helper to simulate free throws, which we will use in both strategies
