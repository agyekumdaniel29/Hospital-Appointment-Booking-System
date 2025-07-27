import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.theme = "light"
        self.current_page = "Dashboard"
        self._set_theme_colors()
        self.title("Daniel's Hospital Appointment Booking System")
        self.geometry("1000x650")
        self.configure(bg=self.BG)
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.trash = {
            "patients": [],
            "doctors": [],
            "appointments": []
        }
        self.load_data()  # <-- Add this line
        self._setup_styles()
        self._build_layout()

    def _set_theme_colors(self):
        if self.theme == "light":
            self.PRIMARY = "#1565c0"
            self.ACCENT = "#43a047"
            self.BG = "#f4faff"
            self.SIDEBAR_BG = "#e3eafc"
            self.CARD_BG = "#ffffff"
            self.FG = "#222"
        else:
            self.PRIMARY = "#90caf9"
            self.ACCENT = "#66bb6a"
            self.BG = "#23272e"
            self.SIDEBAR_BG = "#2c313a"
            self.CARD_BG = "#323842"
            self.FG = "#f4faff"

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Sidebar.TFrame', background=self.SIDEBAR_BG)
        style.configure('Sidebar.TButton', background=self.SIDEBAR_BG, foreground=self.PRIMARY, font=('Arial', 12, 'bold'), borderwidth=0)
        style.map('Sidebar.TButton', background=[('active', self.PRIMARY)], foreground=[('active', 'white')])
        style.configure('Header.TLabel', font=('Arial', 20, 'bold'), foreground=self.PRIMARY, background=self.BG)
        style.configure('Card.TFrame', background=self.CARD_BG, relief='raised', borderwidth=1)
        style.configure('CardHeader.TLabel', font=('Arial', 14, 'bold'), foreground=self.PRIMARY, background=self.CARD_BG)
        style.configure('TLabel', background=self.CARD_BG, font=('Arial', 11), foreground=self.FG)
        style.configure('TButton', font=('Arial', 11), padding=6)
        style.configure('Accent.TButton', background=self.ACCENT, foreground='white', font=('Arial', 11, 'bold'))
        style.map('Accent.TButton', background=[('active', self.PRIMARY)])

    def _build_layout(self):
        # Sidebar
        sidebar = ttk.Frame(self, style='Sidebar.TFrame', width=200)
        sidebar.pack(side='left', fill='y')
        logo = ttk.Label(sidebar, text="🏥", font=('Arial', 32), background=self.SIDEBAR_BG)
        logo.pack(pady=(30, 10))
        ttk.Label(sidebar, text="Daniel's Hospital", font=('Arial', 14, 'bold'), background=self.SIDEBAR_BG, foreground=self.PRIMARY).pack(pady=(0, 30))
        self.menu_buttons = []
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Patients", self.show_patients),
            ("Doctors", self.show_doctors),
            ("Appointments", self.show_appointments),
            ("Schedules", self.show_schedules),
            ("Settings", self.show_settings),  # Added Settings
            ("Trash", self.show_trash),
        ]
        for text, cmd in menu_items:
            btn = ttk.Button(sidebar, text=text, style='Sidebar.TButton', command=cmd)
            btn.pack(fill='x', padx=20, pady=8)
            self.menu_buttons.append(btn)

        # Main content area
        self.content = ttk.Frame(self, style='Card.TFrame')
        self.content.pack(side='left', fill='both', expand=True, padx=30, pady=30)
        # self.show_dashboard()

        page_map = {
            "Dashboard": self.show_dashboard,
            "Patients": self.show_patients,
            "Doctors": self.show_doctors,
            "Appointments": self.show_appointments,
            "Schedules": self.show_schedules,
            "Settings": self.show_settings,
            "Trash": self.show_trash,
        }
        page_map.get(self.current_page, self.show_dashboard)()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.current_page = "Dashboard"
        self.clear_content()
        ttk.Label(self.content, text="Welcome to Daniel's Hospital", style='Header.TLabel').pack(pady=(10, 5))
        ttk.Label(self.content, text="Select a section from the sidebar to manage patients, doctors, appointments, or schedules.", background=self.CARD_BG).pack(pady=10)

    def show_patients(self):
        self.current_page = "Patients"
        self.clear_content()
        self.edit_patient_idx = None  # Track editing index
        ttk.Label(self.content, text="Patient Registration", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5), padx=20)
        form = ttk.Frame(self.content, style='Card.TFrame')
        form.pack(anchor='w', padx=20, pady=10)
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky='e', pady=5)
        name_entry = ttk.Entry(form, width=30)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Label(form, text="Age:").grid(row=1, column=0, sticky='e', pady=5)
        age_entry = ttk.Entry(form, width=30)
        age_entry.grid(row=1, column=1, pady=5, padx=5)

        def register():
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            if not name or not age.isdigit():
                messagebox.showerror("Error", "Enter valid name and age.")
                return
            if self.edit_patient_idx is not None:
                # Update existing
                self.patients[self.edit_patient_idx] = {'name': name, 'age': int(age)}
                self.edit_patient_idx = None
            else:
                # Add new
                self.patients.append({'name': name, 'age': int(age)})
            self.save_data()
            update_list()
            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)

        ttk.Button(form, text="Register", style='Accent.TButton', command=register).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Label(self.content, text="Registered Patients:", font=('Arial', 11, 'bold')).pack(anchor='w', padx=20, pady=(10, 0))
        patient_list = tk.Listbox(self.content, width=50, font=('Arial', 10))
        patient_list.pack(anchor='w', padx=20, pady=5)

        def update_list():
            patient_list.delete(0, tk.END)
            for p in self.patients:
                patient_list.insert(tk.END, f"{p['name']} (Age: {p['age']})")
        update_list()

        btn_frame = ttk.Frame(self.content)
        btn_frame.pack(anchor='w', padx=20, pady=5)
        def delete_patient():
            idx = patient_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select a patient to delete.")
                return
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?")
            if not confirm:
                return
            self.trash["patients"].append(self.patients[idx[0]])
            del self.patients[idx[0]]
            self.save_data()
            update_list()
        def edit_patient():
            idx = patient_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select a patient to edit.")
                return
            patient = self.patients[idx[0]]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, patient['name'])
            age_entry.delete(0, tk.END)
            age_entry.insert(0, str(patient['age']))
            self.edit_patient_idx = idx[0]  # Set editing index

        ttk.Button(btn_frame, text="Edit", command=edit_patient).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=delete_patient).pack(side='left', padx=5)

    def show_doctors(self):
        self.current_page = "Doctors"
        self.clear_content()
        self.edit_doctor_idx = None  # Track editing index
        ttk.Label(self.content, text="Doctor Management", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5), padx=20)
        form = ttk.Frame(self.content, style='Card.TFrame')
        form.pack(anchor='w', padx=20, pady=10)
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky='e', pady=5)
        name_entry = ttk.Entry(form, width=30)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Label(form, text="Specialty:").grid(row=1, column=0, sticky='e', pady=5)
        spec_entry = ttk.Entry(form, width=30)
        spec_entry.grid(row=1, column=1, pady=5, padx=5)
        ttk.Label(form, text="Slots (comma separated):").grid(row=2, column=0, sticky='e', pady=5)
        slot_entry = ttk.Entry(form, width=30)
        slot_entry.grid(row=2, column=1, pady=5, padx=5)

        def add_doctor():
            name = name_entry.get().strip()
            spec = spec_entry.get().strip()
            slots = [s.strip() for s in slot_entry.get().split(",") if s.strip()]
            if not name or not spec or not slots:
                messagebox.showerror("Error", "Fill all fields and at least one slot.")
                return
            if self.edit_doctor_idx is not None:
                self.doctors[self.edit_doctor_idx] = {'name': name, 'spec': spec, 'slots': slots}
                self.edit_doctor_idx = None
            else:
                self.doctors.append({'name': name, 'spec': spec, 'slots': slots})
            self.save_data()
            update_list()
            name_entry.delete(0, tk.END)
            spec_entry.delete(0, tk.END)
            slot_entry.delete(0, tk.END)

        ttk.Button(form, text="Add Doctor", style='Accent.TButton', command=add_doctor).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Label(self.content, text="Doctors & Slots:", font=('Arial', 11, 'bold')).pack(anchor='w', padx=20, pady=(10, 0))
        doc_list = tk.Listbox(self.content, width=70, font=('Arial', 10))
        doc_list.pack(anchor='w', padx=20, pady=5)

        def update_list():
            doc_list.delete(0, tk.END)
            for d in self.doctors:
                doc_list.insert(tk.END, f"{d['name']} ({d['spec']}) - Slots: {', '.join(d['slots'])}")
        update_list()

        btn_frame = ttk.Frame(self.content)
        btn_frame.pack(anchor='w', padx=20, pady=5)
        def delete_doctor():
            idx = doc_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select a doctor to delete.")
                return
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?")
            if not confirm:
                return
            self.trash["doctors"].append(self.doctors[idx[0]])  # Move to trash
            del self.doctors[idx[0]]
            self.save_data()
            update_list()
        def edit_doctor():
            idx = doc_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select a doctor to edit.")
                return
            doctor = self.doctors[idx[0]]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, doctor['name'])
            spec_entry.delete(0, tk.END)
            spec_entry.insert(0, doctor['spec'])
            slot_entry.delete(0, tk.END)
            slot_entry.insert(0, ", ".join(doctor['slots']))
            self.edit_doctor_idx = idx[0]  # Set editing index

        ttk.Button(btn_frame, text="Edit", command=edit_doctor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=delete_doctor).pack(side='left', padx=5)

    def show_appointments(self):
        self.current_page = "Appointments"
        self.clear_content()
        self.edit_appointment_idx = None  # Track editing index
        ttk.Label(self.content, text="Book/Cancel Appointment", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5), padx=20)
        form = ttk.Frame(self.content, style='Card.TFrame')
        form.pack(anchor='w', padx=20, pady=10)
        ttk.Label(form, text="Patient:").grid(row=0, column=0, sticky='e', pady=5)
        patient_combo = ttk.Combobox(form, state="readonly", width=28, values=[f"{p['name']} (Age: {p['age']})" for p in self.patients])
        patient_combo.grid(row=0, column=1, pady=5, padx=5)
        ttk.Label(form, text="Doctor:").grid(row=1, column=0, sticky='e', pady=5)
        doctor_combo = ttk.Combobox(form, state="readonly", width=28, values=[f"{d['name']} ({d['spec']})" for d in self.doctors])
        doctor_combo.grid(row=1, column=1, pady=5, padx=5)
        ttk.Label(form, text="Slot:").grid(row=2, column=0, sticky='e', pady=5)
        slot_combo = ttk.Combobox(form, state="readonly", width=28)
        slot_combo.grid(row=2, column=1, pady=5, padx=5)
        def update_slots(event=None):
            idx = doctor_combo.current()
            if idx >= 0:
                slots = self.doctors[idx]['slots']
                booked = [a['slot'] for a in self.appointments if a['doctor'] == self.doctors[idx]]
                available = [s for s in slots if s not in booked]
                slot_combo['values'] = available
            else:
                slot_combo['values'] = []
        doctor_combo.bind("<<ComboboxSelected>>", update_slots)
        def book():
            p_idx = patient_combo.current()
            d_idx = doctor_combo.current()
            slot = slot_combo.get()
            if p_idx < 0 or d_idx < 0 or not slot:
                messagebox.showerror("Error", "Select patient, doctor, and slot.")
                return
            patient = self.patients[p_idx]
            doctor = self.doctors[d_idx]
            for a in self.appointments:
                if a['doctor'] == doctor and a['slot'] == slot:
                    messagebox.showerror("Error", "Slot already booked.")
                    return
            if self.edit_appointment_idx is not None:
                self.appointments[self.edit_appointment_idx] = {'patient': patient, 'doctor': doctor, 'slot': slot}
                self.edit_appointment_idx = None
            else:
                self.appointments.append({'patient': patient, 'doctor': doctor, 'slot': slot})
            self.save_data()
            update_list()
            update_slots()
        ttk.Button(form, text="Book Appointment", style='Accent.TButton', command=book).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Label(self.content, text="Appointments:", font=('Arial', 11, 'bold')).pack(anchor='w', padx=20, pady=(10, 0))
        appt_list = tk.Listbox(self.content, width=80, font=('Arial', 10))
        appt_list.pack(anchor='w', padx=20, pady=5)
        def update_list():
            appt_list.delete(0, tk.END)
            for a in self.appointments:
                appt_list.insert(tk.END, f"{a['patient']['name']} with Dr. {a['doctor']['name']} at {a['slot']}")
        def cancel():
            idx = appt_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select an appointment to cancel.")
                return
            self.appointments.pop(idx[0])
            self.save_data()
            update_list()
            update_slots()
        ttk.Button(self.content, text="Cancel Appointment", command=cancel).pack(anchor='w', padx=20, pady=5)
        update_list()
        btn_frame = ttk.Frame(self.content)
        btn_frame.pack(anchor='w', padx=20, pady=5)
        def delete_appointment():
            idx = appt_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select an appointment to delete.")
                return
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?")
            if not confirm:
                return
            self.trash["appointments"].append(self.appointments[idx[0]])  # Move to trash
            self.appointments.pop(idx[0])
            self.save_data()
            update_list()
            update_slots()
        def edit_appointment():
            idx = appt_list.curselection()
            if not idx:
                messagebox.showerror("Error", "Select an appointment to edit.")
                return
            appt = self.appointments[idx[0]]
            patient_combo.set(f"{appt['patient']['name']} (Age: {appt['patient']['age']})")
            doctor_combo.set(f"{appt['doctor']['name']} ({appt['doctor']['spec']})")
            slot_combo.set(appt['slot'])
            self.edit_appointment_idx = idx[0]  # Set editing index
        ttk.Button(btn_frame, text="Edit", command=edit_appointment).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=delete_appointment).pack(side='left', padx=5)

    def show_schedules(self):
        self.current_page = "Schedules"
        self.clear_content()
        ttk.Label(self.content, text="Upcoming Appointments", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5), padx=20)
        sched_list = tk.Listbox(self.content, width=90, font=('Arial', 10))
        sched_list.pack(anchor='w', padx=20, pady=10)
        for a in self.appointments:
            sched_list.insert(tk.END, f"{a['patient']['name']} with Dr. {a['doctor']['name']} ({a['doctor']['spec']}) at {a['slot']}")
        def export():
            try:
                with open("appointments_schedule.txt", "w") as f:
                    for a in self.appointments:
                        f.write(
                            f"Dear {a['patient']['name']},\n"
                            f"You have an appointment with Dr. {a['doctor']['name']} ({a['doctor']['spec']}) at {a['slot']}.\n"
                            "Please arrive 10 minutes early and bring any necessary documents.\n"
                            "Thank you for choosing Daniel's Hospital.\n"
                            "---------------------------------------------\n\n"
                        )
                messagebox.showinfo("Exported", "Schedule exported to appointments_schedule.txt")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
        ttk.Button(self.content, text="Export Schedule", style='Accent.TButton', command=export).pack(anchor='w', padx=20, pady=10)

    def show_settings(self):
        self.current_page = "Settings"
        self.clear_content()
        ttk.Label(self.content, text="Settings", style='Header.TLabel').pack(pady=(10, 5))
        ttk.Label(self.content, text="Theme:", style='CardHeader.TLabel').pack(anchor='w', padx=20, pady=(20, 5))
        theme_frame = ttk.Frame(self.content, style='Card.TFrame')
        theme_frame.pack(anchor='w', padx=20, pady=5)
        theme_var = tk.StringVar(value=self.theme)
        def set_theme():
            self.theme = theme_var.get()
            self._set_theme_colors()
            self._setup_styles()
            self.configure(bg=self.BG)
            # Destroy all widgets before rebuilding layout
            for widget in self.winfo_children():
                widget.destroy()
            self._build_layout()
        ttk.Radiobutton(theme_frame, text="Light", variable=theme_var, value="light", command=set_theme).pack(side='left', padx=10)
        ttk.Radiobutton(theme_frame, text="Dark", variable=theme_var, value="dark", command=set_theme).pack(side='left', padx=10)

    def save_data(self):
        data = {
            "patients": self.patients,
            "doctors": self.doctors,
            "appointments": self.appointments,
            "trash": self.trash
        }
        with open("hospital_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("hospital_data.json"):
            with open("hospital_data.json", "r") as f:
                data = json.load(f)
                self.patients = data.get("patients", [])
                self.doctors = data.get("doctors", [])
                self.appointments = data.get("appointments", [])
                self.trash = data.get("trash", {"patients": [], "doctors": [], "appointments": []})

    def show_trash(self):
        self.current_page = "Trash"
        self.clear_content()
        main_frame = ttk.Frame(self.content, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)

        ttk.Label(main_frame, text="🗑️ Trash Bin", style='Header.TLabel', font=('Arial', 22, 'bold')).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # --- Patients Trash ---
        patient_section = ttk.LabelFrame(main_frame, text="Deleted Patients")
        patient_section.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        patient_trash = tk.Listbox(patient_section, width=35, font=('Arial', 10))
        patient_trash.pack(padx=10, pady=10)
        for p in self.trash["patients"]:
            patient_trash.insert(tk.END, f"{p['name']} (Age: {p['age']})")
        btns = ttk.Frame(patient_section)
        btns.pack(pady=(0, 10))
        def recover_patient():
            idx = patient_trash.curselection()
            if not idx:
                messagebox.showerror("Error", "Select a patient to recover.")
                return
            confirm = messagebox.askyesno("Recover Patient", "Restore this patient to the main list?")
            if not confirm:
                return
            self.patients.append(self.trash["patients"].pop(idx[0]))
            self.save_data()
            self.show_trash()
        def empty_patients():
            if not self.trash["patients"]:
                messagebox.showinfo("Empty", "No deleted patients to remove.")
                return
            confirm = messagebox.askyesno("Empty Patient Trash", "This will permanently delete all deleted patients. Continue?")
            if not confirm:
                return
            self.trash["patients"].clear()
            self.save_data()
            self.show_trash()
        ttk.Button(btns, text="Recover", command=recover_patient).pack(side='left', padx=1)
        ttk.Button(btns, text="Empty", command=empty_patients).pack(side='left', padx=1)

        # --- Doctors Trash ---
        doctor_section = ttk.LabelFrame(main_frame, text="Deleted Doctors")
        doctor_section.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        doctor_trash = tk.Listbox(doctor_section, width=45, font=('Arial', 10))
        doctor_trash.pack(padx=10, pady=10)
        for d in self.trash["doctors"]:
            doctor_trash.insert(tk.END, f"{d['name']} ({d['spec']}) - Slots: {', '.join(d['slots'])}")
        btns = ttk.Frame(doctor_section)
        btns.pack(pady=(0, 10))
        def recover_doctor():
            idx = doctor_trash.curselection()
            if not idx:
                messagebox.showerror("Error", "Select a doctor to recover.")
                return
            confirm = messagebox.askyesno("Recover Doctor", "Restore this doctor to the main list?")
            if not confirm:
                return
            self.doctors.append(self.trash["doctors"].pop(idx[0]))
            self.save_data()
            self.show_trash()
        def empty_doctors():
            if not self.trash["doctors"]:
                messagebox.showinfo("Empty", "No deleted doctors to remove.")
                return
            confirm = messagebox.askyesno("Empty Doctor Trash", "This will permanently delete all deleted doctors. Continue?")
            if not confirm:
                return
            self.trash["doctors"].clear()
            self.save_data()
            self.show_trash()
        ttk.Button(btns, text="Recover", command=recover_doctor).pack(side='left', padx=1)
        ttk.Button(btns, text="Empty", command=empty_doctors).pack(side='left', padx=1)

        # --- Appointments Trash ---
        appt_section = ttk.LabelFrame(main_frame, text="Deleted Appointments")
        appt_section.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        appt_trash = tk.Listbox(appt_section, width=55, font=('Arial', 10))
        appt_trash.pack(padx=10, pady=10)
        for a in self.trash["appointments"]:
            appt_trash.insert(tk.END, f"{a['patient']['name']} with Dr. {a['doctor']['name']} at {a['slot']}")
        btns = ttk.Frame(appt_section)
        btns.pack(pady=(0, 10))
        def recover_appt():
            idx = appt_trash.curselection()
            if not idx:
                messagebox.showerror("Error", "Select an appointment to recover.")
                return
            confirm = messagebox.askyesno("Recover Appointment", "Restore this appointment to the main list?")
            if not confirm:
                return
            self.appointments.append(self.trash["appointments"].pop(idx[0]))
            self.save_data()
            self.show_trash()
        def empty_appts():
            if not self.trash["appointments"]:
                messagebox.showinfo("Empty", "No deleted appointments to remove.")
                return
            confirm = messagebox.askyesno("Empty Appointment Trash", "This will permanently delete all deleted appointments. Continue?")
            if not confirm:
                return
            self.trash["appointments"].clear()
            self.save_data()
            self.show_trash()
        ttk.Button(btns, text="Recover", command=recover_appt).pack(side='left', padx=1)
        ttk.Button(btns, text="Empty", command=empty_appts).pack(side='left', padx=1)

        # Make columns expand equally
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()