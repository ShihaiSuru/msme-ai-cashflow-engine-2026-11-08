# MSME AI Cash-Flow Engine

**Practical AI-assisted cash-flow forecasting and invoice-UPI reconciliation tool for Indian MSMEs.**

Created: 8 November 2026  
Focus: Working capital estimation, delayed payment detection, GST liquidity insights.

## The Problem

Indian MSMEs face chronic liquidity stress:
- Over ₹7–8 lakh crore locked in delayed receivables at any time.
- Payment cycles often stretch 60–120 days despite the 45-day MSMED Act mandate.
- GST is paid on invoice (accrual) while cash arrives later → forced short-term borrowing.
- UPI, NEFT, and invoice data live in separate systems, making reconciliation manual and error-prone.
- Limited real-time visibility into cash conversion cycle and working capital gap.

This leads to missed orders, supplier payment delays, higher cost of capital, and restricted growth.

## The Solution

A lightweight, transparent Python starter that:
1. Ingests sample invoices + UPI/bank payment records.
2. Reconciles payments against invoices.
3. Calculates aging buckets and delayed receivables.
4. Estimates GST cash outflow vs actual collections.
5. Produces a simple 30/60/90-day cash-flow forecast and working-capital requirement.

Designed as a demo / foundation that can later integrate Account Aggregator, GSTN e-invoices, TReDS, or bank APIs.

## Usage

```bash
# Clone and run (Python 3.10+)
python cashflow_forecaster.py
```

Expected output includes:
- Matched vs unmatched invoices
- Aging analysis (0-30, 31-60, 61-90, 90+ days)
- Estimated GST liquidity gap
- Projected cash position and working capital shortfall

## Sample Output (illustrative)

```
=== MSME Cash-Flow Snapshot ===
Total invoices: 5
Reconciled: 3
Outstanding receivables: ₹4,25,000
Overdue (>45 days): ₹1,80,000
Estimated GST paid on unrealised revenue: ₹32,400
30-day cash gap: ₹2,10,000
Working capital requirement: ₹2,85,000
```

## Next Steps / Extension Ideas

- Connect to real bank statement CSV / UPI transaction export
- Parse GST e-invoice JSON
- Add simple ML model for payment probability
- Export to Excel / Google Sheets for MSME owners
- Integrate with TReDS or early-payment platforms

## Disclaimer

This is a starter demo for educational and portfolio purposes. Not financial advice. Validate all calculations with your CA / accountant. Data used is synthetic.

---

Built to help Indian MSMEs see their cash clearly.
