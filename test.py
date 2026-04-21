# test.py
from graph import run_agents

topic = input("Enter a research topic: ")
result = run_agents(topic)

print("\n" + "=" * 60)
print("FINAL REPORT")
print("=" * 60)
print(result.get("report", "No report generated"))

print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)
for i, point in enumerate(result.get("key_points", []), 1):
    print(f"  {i}. {point}")

print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)
for source in result.get("sources", []):
    print(f"  - {source}")

print("\n" + "=" * 60)
print("WORKFLOW STATS")
print("=" * 60)
print(f"  Revisions: {result.get('revision_count', 0)}")
print(f"  Approved: {result.get('is_approved', False)}")