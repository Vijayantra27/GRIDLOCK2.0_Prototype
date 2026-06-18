# backend/app/utils/scoring_utils.py


def calculate_risk_score(
        frequency_score,
        peak_hour_score,
        recurrence_score,
        growth_score
):

    risk = (
        0.40 * frequency_score
        +
        0.25 * peak_hour_score
        +
        0.20 * recurrence_score
        +
        0.15 * growth_score
    )

    return round(risk, 2)