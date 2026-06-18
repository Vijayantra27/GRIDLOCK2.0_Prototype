def calculate_risk_score(
    frequency,
    peak_hour_density,
    recurrence,
    growth_trend
):

    score = (
        0.40 * frequency +
        0.25 * peak_hour_density +
        0.20 * recurrence +
        0.15 * growth_trend
    )

    return round(score, 2)