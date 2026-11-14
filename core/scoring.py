# Calculate affordability scores
def affordability_score(monthly_cost, monthly_budget):
    """
    Score affordability from 0 to 100.
    A property at or above the buyer's budget receives 0.
    Lower monthly costs receive higher scores.
    """
    if monthly_budget <= 0:
        raise ValueError("Monthly budget must be positive.")
    if monthly_cost < 0:
        raise ValueError("Monthly cost cannot be negative.")
    score = 100 * (1 - monthly_cost / monthly_budget)
    return max(0.0, min(100.0, score))

def space_score(square_feet, desired_square_feet):
    """
    Score how well a property meets the buyer's desired living space.
    Meeting or exceeding the target earns 100.
    """
    if desired_square_feet <= 0:
        raise ValueError("Desired square footage must be positive.")
    if square_feet < 0:
        raise ValueError("Square footage cannot be negative.")
    score = 100 * square_feet / desired_square_feet
    return min(100.0, score)

def weighted_score(scores, weights):
    """
    Calculated the weighted average of criterion scores.
    Scores and weights must have matching keys.
    """
    if scores.keys() != weights.keys():
        raise ValueError("Scores and weights must use the same criteria.")
    if any(score < 0 or score > 100 for score in scores.values()):
        raise ValueError("Scores must be between 0 and 100.")
    if any(weight < 0 for weight in weights.values()):
        raise ValueError("Weights cannot be negative.")
    total_weight = sum(weights.values())
    if total_weight == 0:
        raise ValueError("At least one weight must be positive.")
    total = sum(
        scores[criterion] * weights[criterion] 
        for criterion in scores
    )
    return total / total_weight

# Calculate living space scores


# Combine all criteria using buyer-selected weights