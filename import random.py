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
    """Simulate shooting a free throw and return True if made, False if missed.""" #Docstring to explain the function's purpose
    return random.random() < OPP_FT_PERCENT
# This is our helper to simulate free throws, which we will use in both strategies

# STRATEGY A: Take a 3-pointer

def simulate_three_point_strategy():
    """
    Simulate one game trial using the 3-point strategy.
    Returns a tuple: (won: bool, points_scored: int)
    """
    score_diff = -3     # We start down 3
    time_left  = STARTING_TIME
    points_scored = 0   # Track our points
 
    # --- Step 1: Attempt 
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


# STRATEGY B: Take a 2 and foul (the "hack-a-opponent" strategy)

def simulate_two_point_strategy():
    """
    Simulate one game trial using the 2-point + foul strategy.
    Returns a tuple: (won: bool, points_scored: int)
    """
    score_diff = -3    # We start down 3
    time_left  = STARTING_TIME
    points_scored = 0  # Track our points
 
    # -------------------------------------------------------------------------
    # PHASE 1: Attempt the quick 2-pointer
    
    time_left -= TIME_2PT_ATTEMPT
    if random.random() < MY_2PT_PERCENT:
        score_diff += 2   # Now down 1
        points_scored += 2
 
    # If we're still down and out of time, no point continuing
    if time_left <= 0:
        return (score_diff >= 0, points_scored)
 
    # -------------------------------------------------------------------------
    # PHASE 2: Foul the opponent immediately after scoring/missing
    
    while time_left > 0 and score_diff < 0:
        # The opponent gets free throws. We keep fouling until time runs out
        # or we tie/lead.
 
        # Opponent gets the ball, we foul quickly
        time_left -= TIME_INBOUND
        if time_left <= 0:
            break
 
        # Opponent shoots 2 free throws
        time_left -= TIME_FT_SEQUENCE
        ft1 = shoot_free_throw()
        ft2 = shoot_free_throw()
 
        if ft1:
            score_diff -= 1
        if ft2:
            score_diff -= 1
 
        # Did they miss one? Chance for an offensive rebound (rare — it's a FT)
        # In real basketball, only the 2nd FT can be rebounded
        if not ft2:
            if random.random() < OFFREB_PERCENT and time_left > TIME_REBOUND_PLAY:
                # We grab the rebound and attempt a shot
                time_left -= TIME_REBOUND_PLAY
                if random.random() < MY_2PT_PERCENT:
                    score_diff += 2
                    points_scored += 2
                elif random.random() < MY_3PT_PERCENT * 0.5:  # Desperation 3
                    score_diff += 3
                    points_scored += 3
 
        # Do we now have the ball back to attempt another foul cycle?
        # In real strategy, we'd immediately foul again after inbound.
        # The loop continues as long as time allows.
        if time_left <= 0:
            break
 
        # If we're tied or ahead, we're done — hold the ball or game is over
        if score_diff >= 0:
            break
 
    # -------------------------------------------------------------------------
    # PHASE 3: If time ran out or we have a final possession
    # If we are tied, go to overtime (OT)
    
    if score_diff == 0:
        won = random.random() < OT_WIN_PERCENT
        return (won, points_scored)
    elif score_diff > 0:
        return (True, points_scored)   # We're winning!
    else:
        # Down at end — one last desperation 3 if we have any time
        if time_left > 2:
            if random.random() < MY_3PT_PERCENT * 0.6:  # Rushed, lower %
                score_diff += 3
                points_scored += 3
                if score_diff == 0:
                    won = random.random() < OT_WIN_PERCENT
                    return (won, points_scored)
                elif score_diff > 0:
                    return (True, points_scored)
        return (False, points_scored)
    
# =============================================================================
# RUN THE SIMULATION
def run_simulation(num_trials):
    """
    Runs both strategies over many trials.
    Returns a dictionary of results.
    """
    results = {
        "three_pt": {"wins": 0, "losses": 0, "total_points": 0},
        "two_pt":   {"wins": 0, "losses": 0, "total_points": 0},
    }
 
    for _ in range(num_trials):
        # Run both strategies independently each trial
        won_3pt, points_3pt = simulate_three_point_strategy()
        if won_3pt:
            results["three_pt"]["wins"] += 1
        else:
            results["three_pt"]["losses"] += 1
        results["three_pt"]["total_points"] += points_3pt
 
        won_2pt, points_2pt = simulate_two_point_strategy()
        if won_2pt:
            results["two_pt"]["wins"] += 1
        else:
            results["two_pt"]["losses"] += 1
        results["two_pt"]["total_points"] += points_2pt
 
    return results
# =============================================================================
# OUTPUT RESULTS
def display_results(results, num_trials):
    three_wins = results["three_pt"]["wins"]
    two_wins   = results["two_pt"]["wins"]
 
    three_pct  = (three_wins / num_trials) * 100
    two_pct    = (two_wins   / num_trials) * 100
 
    three_avg_pts = results["three_pt"]["total_points"] / num_trials
    two_avg_pts   = results["two_pt"]["total_points"] / num_trials
 
    print("=" * 55)
    print("   BASKETBALL END-GAME SIMULATION RESULTS")
    print("=" * 55)
    print(f"  Trials run         : {num_trials:,}")
    print(f"  Time remaining     : {STARTING_TIME} seconds")
    print(f"  Your 3PT%          : {MY_3PT_PERCENT*100:.0f}%")
    print(f"  Your 2PT%          : {MY_2PT_PERCENT*100:.0f}%")
    print(f"  Opponent FT%       : {OPP_FT_PERCENT*100:.0f}%")
    print(f"  Offensive Reb%     : {OFFREB_PERCENT*100:.0f}%")
    print(f"  OT Win%            : {OT_WIN_PERCENT*100:.0f}%")
    print("-" * 55)
    print(f"  STRATEGY A (Take the 3):")
    print(f"    Wins             : {three_wins:,}  ({three_pct:.1f}%)")
    print(f"    Avg points scored: {three_avg_pts:.2f}")
    print()
    print(f"  STRATEGY B (2 + Foul):")
    print(f"    Wins             : {two_wins:,}  ({two_pct:.1f}%)")
    print(f"    Avg points scored: {two_avg_pts:.2f}")
    print("-" * 55)
 
    if three_pct > two_pct:
        better = "STRATEGY A — Take the 3-pointer!"
    elif two_pct > three_pct:
        better = "STRATEGY B — Take the 2 and foul!"
    else:
        better = "Both strategies are statistically equal."
 
    print(f"  Recommendation     : {better}")
    print("=" * 55)
 
 # added if this needs to be imported as a module without running the simulation immediately
if __name__ == "__main__":
    print(f"\nRunning {NUM_TRIALS:,} trials for each strategy...\n")
    results = run_simulation(NUM_TRIALS)
    display_results(results, NUM_TRIALS)
 
