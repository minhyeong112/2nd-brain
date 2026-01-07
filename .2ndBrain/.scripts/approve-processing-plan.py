#!/usr/bin/env python3
"""
HARD-CODED APPROVAL GATE: Processing Plan Review
This script must be run before AI executes any changes.
Forces human review of PROCESSING-PLAN.md before proceeding.

Usage: python3 .2ndBrain/.scripts/approve-processing-plan.py
"""

from pathlib import Path
import sys

def main():
    root_dir = Path(".")
    plan_file = root_dir / "PROCESSING-PLAN.md"
    
    if not plan_file.exists():
        print("❌ ERROR: PROCESSING-PLAN.md not found")
        print("AI must create PROCESSING-PLAN.md first using semantic search")
        exit(1)
    
    print(f"\n{'='*60}")
    print(f"⏸️  HARD STOP: Processing Plan Approval Required")
    print(f"{'='*60}")
    print(f"📝 Review PROCESSING-PLAN.md carefully")
    print(f"✓ Verify semantic search was used for each item")
    print(f"✓ Check recommendations are appropriate")
    print(f"✓ Ensure nothing important was missed")
    print(f"{'='*60}\n")
    
    # Display summary of plan
    try:
        with open(plan_file, 'r') as f:
            content = f.read()
            # Extract summary section if it exists
            if "## Summary of Actions" in content:
                summary_start = content.index("## Summary of Actions")
                summary_section = content[summary_start:summary_start+500]
                print("📊 Plan Summary:")
                print(summary_section.split('\n\n')[0])
                print()
    except:
        pass
    
    # HARD-CODED HUMAN-IN-THE-LOOP: Cannot proceed without approval
    while True:
        approval = input("Type 'approved' to execute plan (or 'reject' to cancel): ").strip().lower()
        if approval == 'approved':
            print("\n✅ Approval received. AI can now execute all changes from the plan")
            print("🤖 Tell AI: 'approved' to execute changes\n")
            exit(0)
        elif approval == 'reject':
            print("\n❌ Plan rejected. AI must revise PROCESSING-PLAN.md")
            print("📝 Provide feedback to AI about what needs to change\n")
            exit(1)
        else:
            print("❌ Invalid input. Please type 'approved' or 'reject'")

if __name__ == "__main__":
    main()
