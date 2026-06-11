"""
SportMonks Denmark Superliga discovery script.

Scope:
- Data Acquisition / discovery only.
- No importer.
- No database writes.
- No schema changes.
- No dataset/features/modeling/backtesting.

Goal:
Collect raw SportMonks API responses for Denmark Superliga (country 320, league 271)
to evaluate whether the API provides useful live/H8-style data such as events,
period scores, trends, pressure index, xG, statistics, and match center payload