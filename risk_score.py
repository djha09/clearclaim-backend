def calculate_risk_score(data):
    age = data.get("age", 0)
    has_preexisting = data.get("preexisting", False)
    amount_claimed = data.get("amount", 0)
    hospitalization_type = data.get("hospitalization", "standard")  # 'standard', 'domiciliary', 'daycare'

    score = 100

    if age > 60:
        score -= 20
    if has_preexisting:
        score -= 25
    if amount_claimed > 500000:
        score -= 15
    if hospitalization_type == "domiciliary":
        score -= 10
    elif hospitalization_type == "daycare":
        score -= 5

    return max(0, min(score, 100))
