

from read_pdf import read_pdf_file, read_clauses
# from simplify_pdf import simplifyit

pdf_path = "../data/1. Policy- NMP.pdf"

# Step 1: Get full text
text = read_pdf_file(pdf_path)

# Step 2: Extract clause-like lines
clauses = read_clauses(text)

print(f"\n✅ Found {len(clauses)} clause-like sentences:\n")
for i, clause in enumerate(clauses[:10]):
    print(f"{i+1}. {clause}")
