#!/usr/bin/env python3
"""
MSME AI Cash-Flow Engine — Starter Script
========================================
Simple, transparent tool for Indian MSMEs to:
- Reconcile sample invoices with UPI/bank payments
- Calculate receivables aging and delayed payments
- Estimate GST liquidity impact
- Project short-term cash flow and working capital need

Uses only the Python standard library.
Data is synthetic for demonstration.
"""

from datetime import datetime, timedelta
from collections import defaultdict
import json

# ---------------------------------------------------------------------------
# Sample data (replace with real CSV / API data later)
# ---------------------------------------------------------------------------
INVOICES = [
    {"id": "INV-001", "date": "2026-09-15", "amount": 150000, "gst": 27000, "customer": "Buyer A", "due_days": 45},
    {"id": "INV-002", "date": "2026-10-01", "amount": 80000,  "gst": 14400, "customer": "Buyer B", "due_days": 30},
    {"id": "INV-003", "date": "2026-10-10", "amount": 220000, "gst": 39600, "customer": "Buyer C", "due_days": 45},
    {"id": "INV-004", "date": "2026-10-20", "amount": 95000,  "gst": 17100, "customer": "Buyer A", "due_days": 60},
    {"id": "INV-005", "date": "2026-11-01", "amount": 60000,  "gst": 10800, "customer": "Buyer D", "due_days": 30},
]

PAYMENTS = [
    {"id": "UPI-101", "date": "2026-10-25", "amount": 150000, "ref": "INV-001", "mode": "UPI"},
    {"id": "NEFT-202", "date": "2026-10-28", "amount": 80000,  "ref": "INV-002", "mode": "NEFT"},
    {"id": "UPI-303", "date": "2026-11-05", "amount": 100000, "ref": "INV-003", "mode": "UPI"},  # partial
]

TODAY = datetime(2026, 11, 8)

def parse_date(d: str) -> datetime:
    return datetime.strptime(d, "%Y-%m-%d")

def days_between(d1: datetime, d2: datetime) -> int:
    return (d2 - d1).days

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def reconcile(invoices, payments):
    """Match payments to invoices (exact or partial)."""
    paid = defaultdict(float)
    for p in payments:
        paid[p["ref"]] += p["amount"]

    results = []
    for inv in invoices:
        received = paid.get(inv["id"], 0.0)
        outstanding = max(0, inv["amount"] - received)
        inv_date = parse_date(inv["date"])
        age = days_between(inv_date, TODAY)
        overdue = age > inv["due_days"]
        results.append({
            **inv,
            "received": received,
            "outstanding": outstanding,
            "age_days": age,
            "overdue": overdue and outstanding > 0,
            "gst_on_outstanding": round(inv["gst"] * (outstanding / inv["amount"]), 2) if inv["amount"] else 0
        })
    return results

def aging_summary(reconciled):
    buckets = {"0-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
    for r in reconciled:
        if r["outstanding"] <= 0:
            continue
        age = r["age_days"]
        if age <= 30:
            buckets["0-30"] += r["outstanding"]
        elif age <= 60:
            buckets["31-60"] += r["outstanding"]
        elif age <= 90:
            buckets["61-90"] += r["outstanding"]
        else:
            buckets["90+"] += r["outstanding"]
    return buckets

def forecast(reconciled, horizon_days=90):
    """Very simple forecast: assume remaining amounts arrive on due date or delayed by 30 days if overdue."""
    cash_in = defaultdict(float)
    for r in reconciled:
        if r["outstanding"] <= 0:
            continue
        inv_date = parse_date(r["date"])
        expected = inv_date + timedelta(days=r["due_days"])
        if r["overdue"]:
            expected += timedelta(days=30)  # simple delay assumption
        if expected <= TODAY + timedelta(days=horizon_days):
            cash_in[expected.date()] += r["outstanding"]
    return dict(sorted(cash_in.items()))

def main():
    print("=== MSME AI Cash-Flow Engine ===")
    print(f"As of: {TODAY.strftime('%d %b %Y')}\n")

    reconciled = reconcile(INVOICES, PAYMENTS)

    total_inv = sum(i["amount"] for i in INVOICES)
    total_out = sum(r["outstanding"] for r in reconciled)
    total_gst_gap = sum(r["gst_on_outstanding"] for r in reconciled)
    overdue_amt = sum(r["outstanding"] for r in reconciled if r["overdue"])

    print(f"Total invoiced          : ₹{total_inv:,.0f}")
    print(f"Outstanding receivables : ₹{total_out:,.0f}")
    print(f"Overdue (> due days)    : ₹{overdue_amt:,.0f}")
    print(f"GST on unrealised sales : ₹{total_gst_gap:,.0f}\n")

    print("Aging of outstanding:")
    for bucket, amt in aging_summary(reconciled).items():
        print(f"  {bucket:>6} days : ₹{amt:,.0f}")

    print("\nSimple 90-day expected inflows (by date):")
    inflows = forecast(reconciled)
    for date, amt in list(inflows.items())[:8]:
        print(f"  {date} : ₹{amt:,.0f}")

    # Rough working capital need: 1.5x current outstanding + GST gap
    wc_need = total_out * 1.5 + total_gst_gap
    print(f"\nEstimated working capital requirement: ₹{wc_need:,.0f}")
    print("(Illustrative — adjust with actual operating cycle and safety margin)")

    print("\n--- Detailed reconciliation ---")
    for r in reconciled:
        status = "PAID" if r["outstanding"] == 0 else ("OVERDUE" if r["overdue"] else "OPEN")
        print(f"{r['id']} | {status:7} | Outstanding ₹{r['outstanding']:>10,.0f} | Age {r['age_days']}d")

if __name__ == "__main__":
    main()
