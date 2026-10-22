HERITAGE EVENT MANAGEMENT SYSTEM — RUNNABLE WINDOWS PROJECT
============================================================

This version runs as a desktop application using Python + Tkinter + SQLite.
No MySQL setup and no pip install are required.

RUN IT:
1. Download and extract this ZIP to a folder on your Windows laptop.
2. Open the extracted folder in File Explorer.
3. Click the address bar, type cmd, and press Enter.
4. Type: py --version
5. Then type: py app.py

If `py` is not recognized, try `python --version` and then `python app.py`.
If Python is not installed, install it from https://www.python.org/downloads/
and tick "Add python.exe to PATH" during installation.

APP TABS:
- Events: view and add events
- Visitors: add visitor records
- Registrations: register a visitor for an event; update attendance status
- Reports: review registration counts and attendance rates

The app creates `heritage_events.db` automatically in this folder. Your changes
are saved when you close and reopen the app.

Files:
- app.py: runnable desktop application
- heritage_event_management.sql: MySQL schema/reference queries
- Project_Report.pdf: project report
- README.txt: these instructions

All sample names and records are fictional demo data. This is an independent
portfolio project, not an official IAADB or Ministry of Culture system.

To reset all local demo data: close the app and delete `heritage_events.db`.
The database will be recreated the next time the app starts.
