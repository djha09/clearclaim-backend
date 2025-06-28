from simplify import simplifyit
clause = """
Coverage is excluded for pre-existing conditions unless the waiting period of 48 months has been completed from the policy inception date.
"""

result = simplifyit(clause)
print("\n📄 Simplified Explanation:\n")
print(result)