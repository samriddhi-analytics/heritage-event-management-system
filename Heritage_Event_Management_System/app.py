import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import date

DB = Path(__file__).with_name("heritage_events.db")

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def setup():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS events(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, venue TEXT NOT NULL,
          event_date TEXT NOT NULL, event_type TEXT NOT NULL, capacity INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS visitors(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
          city TEXT);
        CREATE TABLE IF NOT EXISTS registrations(
          id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_id INTEGER NOT NULL, event_id INTEGER NOT NULL,
          registered_on TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Registered',
          UNIQUE(visitor_id,event_id),
          FOREIGN KEY(visitor_id) REFERENCES visitors(id), FOREIGN KEY(event_id) REFERENCES events(id));
        """)
        if c.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
            c.executemany("INSERT INTO events(name,venue,event_date,event_type,capacity) VALUES(?,?,?,?,?)", [
             ("Heritage Walk: Stories of Delhi","Purana Qila","2026-12-12","Heritage Walk",80),
             ("Design and the Built City","National Gallery of Modern Art","2026-12-18","Talk",120),
             ("Craft and Material Workshop","Crafts Museum","2027-01-09","Workshop",45),
             ("Public Art Documentation Session","Red Fort","2027-01-17","Workshop",60),
             ("Student Design Dialogue","Lalit Kala Akademi","2027-02-06","Student Programme",100)])
        if c.execute("SELECT COUNT(*) FROM visitors").fetchone()[0] == 0:
            c.executemany("INSERT INTO visitors(name,email,city) VALUES(?,?,?)", [
             ("Aarav Sharma","aarav.demo01@example.com","Delhi"),
             ("Meera Kapoor","meera.demo02@example.com","Noida"),
             ("Riya Verma","riya.demo03@example.com","Ghaziabad"),
             ("Kabir Singh","kabir.demo04@example.com","Lucknow")])

class App:
    def __init__(self, root):
        self.root=root; root.title("Heritage Event Management System"); root.geometry("1050x650")
        root.configure(bg="#f3f6fa")
        header=tk.Frame(root,bg="#1f4e78",padx=18,pady=14); header.pack(fill="x")
        tk.Label(header,text="Heritage Event Management System",font=("Segoe UI",18,"bold"),
                 bg="#1f4e78",fg="white").pack(anchor="w")
        tk.Label(header,text="Events • Visitors • Registrations • Reports",font=("Segoe UI",10),
                 bg="#1f4e78",fg="white").pack(anchor="w")
        self.tabs=ttk.Notebook(root); self.tabs.pack(fill="both",expand=True,padx=12,pady=12)
        self.make_events(); self.make_visitors(); self.make_regs(); self.make_reports(); self.refresh()

    def tree(self, parent, cols, heads, widths=None):
        f=ttk.Frame(parent); f.pack(fill="both",expand=True,pady=8)
        t=ttk.Treeview(f,columns=cols,show="headings")
        for i,col in enumerate(cols):
            t.heading(col,text=heads[i]); t.column(col,width=widths[i] if widths else 130,anchor="w")
        sy=ttk.Scrollbar(f,orient="vertical",command=t.yview); t.configure(yscrollcommand=sy.set)
        t.grid(row=0,column=0,sticky="nsew"); sy.grid(row=0,column=1,sticky="ns")
        f.rowconfigure(0,weight=1); f.columnconfigure(0,weight=1); return t

    def make_events(self):
        p=ttk.Frame(self.tabs,padding=12); self.tabs.add(p,text="Events")
        ttk.Label(p,text="Add event",font=("Segoe UI",12,"bold")).pack(anchor="w")
        form=ttk.Frame(p); form.pack(fill="x",pady=6)
        self.en=tk.StringVar(); self.ev=tk.StringVar(); self.ed=tk.StringVar(value=date.today().isoformat())
        self.et=tk.StringVar(value="Workshop"); self.ec=tk.StringVar(value="50")
        for i,(label,var,width) in enumerate([("Event name",self.en,25),("Venue",self.ev,20),
            ("Date YYYY-MM-DD",self.ed,15),("Type",self.et,16),("Capacity",self.ec,8)]):
            ttk.Label(form,text=label).grid(row=0,column=i,padx=3,sticky="w")
            ttk.Entry(form,textvariable=var,width=width).grid(row=1,column=i,padx=3)
        ttk.Button(form,text="Add event",command=self.add_event).grid(row=1,column=5,padx=5)
        self.etree=self.tree(p,("id","name","venue","date","type","capacity","registrations"),
          ("ID","Event","Venue","Date","Type","Capacity","Registrations"),(45,250,190,100,130,80,100))

    def make_visitors(self):
        p=ttk.Frame(self.tabs,padding=12); self.tabs.add(p,text="Visitors")
        form=ttk.Frame(p); form.pack(fill="x",pady=8)
        self.vn=tk.StringVar(); self.ve=tk.StringVar(); self.vc=tk.StringVar()
        for i,(label,var,width) in enumerate([("Full name",self.vn,22),("Email",self.ve,30),("City",self.vc,18)]):
            ttk.Label(form,text=label).grid(row=0,column=i,padx=4,sticky="w")
            ttk.Entry(form,textvariable=var,width=width).grid(row=1,column=i,padx=4)
        ttk.Button(form,text="Add visitor",command=self.add_visitor).grid(row=1,column=3,padx=8)
        self.vtree=self.tree(p,("id","name","email","city"),("ID","Name","Email","City"),(60,200,300,180))

    def make_regs(self):
        p=ttk.Frame(self.tabs,padding=12); self.tabs.add(p,text="Registrations")
        form=ttk.Frame(p); form.pack(fill="x",pady=8)
        self.rv=tk.StringVar(); self.re=tk.StringVar(); self.rs=tk.StringVar(value="Attended")
        ttk.Label(form,text="Visitor").grid(row=0,column=0,padx=4)
        self.vcombo=ttk.Combobox(form,textvariable=self.rv,state="readonly",width=38); self.vcombo.grid(row=0,column=1,padx=4)
        ttk.Label(form,text="Event").grid(row=0,column=2,padx=4)
        self.ecombo=ttk.Combobox(form,textvariable=self.re,state="readonly",width=45); self.ecombo.grid(row=0,column=3,padx=4)
        ttk.Button(form,text="Register",command=self.register).grid(row=0,column=4,padx=5)
        ttk.Label(form,text="Selected registration status:").grid(row=1,column=0,pady=8,sticky="e")
        ttk.Combobox(form,textvariable=self.rs,state="readonly",values=["Registered","Attended","Cancelled"],width=18).grid(row=1,column=1,sticky="w")
        ttk.Button(form,text="Update selected",command=self.update_status).grid(row=1,column=2,sticky="w")
        self.rtree=self.tree(p,("id","visitor","email","event","date","status"),
          ("Reg ID","Visitor","Email","Event","Event date","Status"),(65,160,230,280,100,100))

    def make_reports(self):
        p=ttk.Frame(self.tabs,padding=12); self.tabs.add(p,text="Reports")
        self.summary=ttk.Label(p,text="",font=("Segoe UI",13,"bold")); self.summary.pack(anchor="w",pady=8)
        self.ptree=self.tree(p,("event","venue","capacity","registrations","attended","rate"),
          ("Event","Venue","Capacity","Registrations","Attended","Attendance rate"),(280,180,90,110,90,120))

    def add_event(self):
        try:
            name,venue,dt,typ=self.en.get().strip(),self.ev.get().strip(),self.ed.get().strip(),self.et.get().strip()
            date.fromisoformat(dt); cap=int(self.ec.get())
            if not name or not venue or not typ or cap<1: raise ValueError
        except ValueError:
            messagebox.showerror("Check details","Enter event name, venue, valid date (YYYY-MM-DD), type and positive capacity."); return
        with db() as c: c.execute("INSERT INTO events(name,venue,event_date,event_type,capacity) VALUES(?,?,?,?,?)",(name,venue,dt,typ,cap))
        self.en.set(""); self.ev.set(""); self.refresh(); messagebox.showinfo("Saved","Event added.")

    def add_visitor(self):
        name,email,city=self.vn.get().strip(),self.ve.get().strip(),self.vc.get().strip()
        if not name or "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Check details","Enter a name and valid email."); return
        try:
            with db() as c: c.execute("INSERT INTO visitors(name,email,city) VALUES(?,?,?)",(name,email,city))
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate email","That email is already in the system."); return
        self.vn.set(""); self.ve.set(""); self.vc.set(""); self.refresh(); messagebox.showinfo("Saved","Visitor added.")

    def register(self):
        if not self.rv.get() or not self.re.get():
            messagebox.showerror("Choose records","Select a visitor and an event."); return
        vid=int(self.rv.get().split(" | ")[0]); eid=int(self.re.get().split(" | ")[0])
        try:
            with db() as c:
                cap=c.execute("SELECT capacity FROM events WHERE id=?",(eid,)).fetchone()["capacity"]
                n=c.execute("SELECT COUNT(*) FROM registrations WHERE event_id=? AND status!='Cancelled'",(eid,)).fetchone()[0]
                if n>=cap: messagebox.showerror("Event full","This event has reached capacity."); return
                c.execute("INSERT INTO registrations(visitor_id,event_id,registered_on,status) VALUES(?,?,?,?)",
                          (vid,eid,date.today().isoformat(),"Registered"))
        except sqlite3.IntegrityError:
            messagebox.showerror("Not saved","This visitor is already registered for this event."); return
        self.refresh(); messagebox.showinfo("Saved","Registration created.")

    def update_status(self):
        sel=self.rtree.selection()
        if not sel: messagebox.showwarning("Select row","Select a registration first."); return
        rid=self.rtree.item(sel[0],"values")[0]
        with db() as c: c.execute("UPDATE registrations SET status=? WHERE id=?",(self.rs.get(),rid))
        self.refresh(); messagebox.showinfo("Updated","Registration status updated.")

    def clear(self,t):
        for item in t.get_children(): t.delete(item)

    def refresh(self):
        with db() as c:
            self.clear(self.etree)
            for r in c.execute("""SELECT e.*,COUNT(CASE WHEN r.status!='Cancelled' THEN r.id END) regs
                FROM events e LEFT JOIN registrations r ON e.id=r.event_id GROUP BY e.id ORDER BY e.event_date"""):
                self.etree.insert("","end",values=(r["id"],r["name"],r["venue"],r["event_date"],r["event_type"],r["capacity"],r["regs"]))
            visitors=c.execute("SELECT * FROM visitors ORDER BY name").fetchall()
            self.clear(self.vtree)
            for r in visitors: self.vtree.insert("","end",values=(r["id"],r["name"],r["email"],r["city"] or ""))
            events=c.execute("SELECT * FROM events ORDER BY event_date").fetchall()
            self.vcombo["values"]=[f'{r["id"]} | {r["name"]} ({r["email"]})' for r in visitors]
            self.ecombo["values"]=[f'{r["id"]} | {r["name"]} — {r["event_date"]}' for r in events]
            self.clear(self.rtree)
            regs=c.execute("""SELECT r.id,v.name visitor,v.email,e.name event,e.event_date,r.status
                FROM registrations r JOIN visitors v ON v.id=r.visitor_id JOIN events e ON e.id=r.event_id
                ORDER BY r.id DESC""").fetchall()
            for r in regs: self.rtree.insert("","end",values=(r["id"],r["visitor"],r["email"],r["event"],r["event_date"],r["status"]))
            total=c.execute("SELECT COUNT(*) FROM registrations WHERE status!='Cancelled'").fetchone()[0]
            self.summary.config(text=f'Events: {len(events)}     Visitors: {len(visitors)}     Active registrations: {total}')
            self.clear(self.ptree)
            for r in c.execute("""SELECT e.name,e.venue,e.capacity,
                COUNT(CASE WHEN r.status!='Cancelled' THEN r.id END) regs,
                COUNT(CASE WHEN r.status='Attended' THEN r.id END) attended
                FROM events e LEFT JOIN registrations r ON e.id=r.event_id
                GROUP BY e.id ORDER BY regs DESC"""):
                rate=(100*r["attended"]/r["regs"]) if r["regs"] else 0
                self.ptree.insert("","end",values=(r["name"],r["venue"],r["capacity"],r["regs"],r["attended"],f"{rate:.1f}%"))

if __name__=="__main__":
    setup()
    root=tk.Tk()
    try: ttk.Style().theme_use("clam")
    except tk.TclError: pass
    App(root)
    root.mainloop()
