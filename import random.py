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

# STRATEGY A: Take a 3-pointer

def simulate_three_point_strategy():
    """
    Simulate one game trial using the 3-point strategy.
    Returns a tuple: (won: bool, points_scored: int)
    """
    score_diff = -3     # We start down 3
    time_left  = STARTING_TIME
    points_scored = 0   # Track our points
 
    # --- Step 1: Attempt a 3-pointer ---
    time_left -= TIME_3PT_ATTEMPT
    if random.random() < MY_3PT_PERCENT:
        score_diff += 3     # Tie game!
        points_scored += 3
        # Game goes to overtime
        won = random.random() < OT_WIN_PERCENT
        return (won, points_scored)
    else:
        # Missed the 3. Do we get an offensive rebound?
        if random.random() < OFFREB_PERCENT and time_left > TIME_2PT_ATTEMPT:
            # Got the rebound — try a quick 2-pointer
            time_left -= TIME_2PT_ATTEMPT
            if random.random() < MY_2PT_PERCENT:
                score_diff += 2   # Still down 1, game continues but time likely out
                points_scored += 2
            # Either way, almost certainly time has run out. We lose unless we tied.
        # If we missed everything, we lose
        won = score_diff >= 0  # Only wins if somehow tied (extremely rare path)
        return (won, points_scored)
 
