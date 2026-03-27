# kerain_runoff_model.py

def calculate_runoff(C, rainfall_intensity, area):
    """
    C: runoff coefficient (0 - 1)
    rainfall_intensity: mm/hour
    area: square kilometers
    """
    Q = C * rainfall_intensity * area
    return Q


def calculate_flood_risk(C, rainfall_intensity, area, drainage_capacity):
    runoff = calculate_runoff(C, rainfall_intensity, area)
    risk_ratio = runoff / drainage_capacity
    
    if risk_ratio > 1:
        flood_status = "FLOOD LIKELY"
    else:
        flood_status = "SAFE"
    
    return runoff, risk_ratio, flood_status


if __name__ == "__main__":
    # Example scenario
    C = 0.8  # urban concrete-heavy area
    rainfall_intensity = 50  # mm/hour
    area = 10  # km^2
    drainage_capacity = 300  # system capacity

    runoff, risk_ratio, status = calculate_flood_risk(
        C, rainfall_intensity, area, drainage_capacity
    )

    print("Runoff:", runoff)
    print("Risk Ratio:", risk_ratio)
    print("Status:", status)