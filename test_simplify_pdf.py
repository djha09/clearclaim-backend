from simplify_pdf import simplify_policy_pdf

pdf_path = "../data/1. Policy- NMP.pdf"  # replace with real one
results = simplify_policy_pdf(pdf_path)

print("\n📋 Final Output:\n")
for i, r in enumerate(results):
    print(f"{i+1}. 🔒 Original: {r['original']}")
    print(f"   💬 Simplified: {r['simplified']}\n")
