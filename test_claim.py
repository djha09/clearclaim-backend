from claim import explain_claim_denial

result = explain_claim_denial(
    treatment="Gallbladder removal surgery",
    reason="Pre-existing condition not disclosed",
    policy_type="Star Mediclaim Plus"
)

print("\n🧠 ClearClaim Output:\n")
print(result)
