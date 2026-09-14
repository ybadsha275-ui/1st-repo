import customtkinter as ctk
from tkinter import messagebox


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_TITLE = "Student Study Planner"
APP_WIDTH = 1400
APP_HEIGHT = 850


# ============================================================
# THEME
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# MAIN APPLICATION
# ============================================================

class StudyPlannerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(1100, 700)

        # Main window background
        self.configure(fg_color="#0f172a")

        # Configure layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Current page
        self.current_page = None

        # Build interface
        self.create_sidebar()
        self.create_main_area()

        # Start on dashboard
        self.show_dashboard()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color="#111827"
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # ----------------------------------------------------
        # Logo
        # ----------------------------------------------------

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(25, 10)
        )

        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="🎓",
            font=("Arial", 32)
        )

        logo_icon.pack(
            anchor="w"
        )

        logo_title = ctk.CTkLabel(
            logo_frame,
            text="Study Planner",
            font=("Arial", 20, "bold"),
            text_color="#f8fafc"
        )

        logo_title.pack(
            anchor="w",
            pady=(4, 0)
        )

        logo_subtitle = ctk.CTkLabel(
            logo_frame,
            text="Stay focused. Keep learning.",
            font=("Arial", 11),
            text_color="#94a3b8"
        )

        logo_subtitle.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # Separator
        # ----------------------------------------------------

        separator = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#263244"
        )

        separator.pack(
            fill="x",
            padx=18,
            pady=18
        )

        # ----------------------------------------------------
        # Navigation Buttons
        # ----------------------------------------------------

        self.nav_buttons = {}

        navigation = [
            ("🏠", "Dashboard", self.show_dashboard),
            ("📝", "Tasks", self.show_tasks),
            ("📅", "Calendar", self.show_calendar),
            ("🍅", "Focus", self.show_focus),
            ("📊", "Analytics", self.show_analytics),
            ("🏆", "Achievements", self.show_achievements),
            ("⚙️", "Settings", self.show_settings),
        ]

        for icon, name, command in navigation:

            button = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {name}",
                height=45,
                corner_radius=10,
                anchor="w",
                fg_color="transparent",
                hover_color="#1e293b",
                text_color="#cbd5e1",
                font=("Arial", 13, "bold"),
                command=command
            )

            button.pack(
                fill="x",
                padx=15,
                pady=4
            )

            self.nav_buttons[name] = button

        # ----------------------------------------------------
        # Bottom section
        # ----------------------------------------------------

        self.sidebar_bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        self.sidebar_bottom.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        version_label = ctk.CTkLabel(
            self.sidebar_bottom,
            text="Student Study Planner\nVersion 2.0",
            font=("Arial", 10),
            text_color="#64748b",
            justify="left"
        )

        version_label.pack(
            anchor="w"
        )

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#0f172a"
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_area.grid_rowconfigure(
            1,
            weight=1
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # Top Bar
        # ----------------------------------------------------

        self.top_bar = ctk.CTkFrame(
            self.main_area,
            height=70,
            corner_radius=0,
            fg_color="#0f172a"
        )

        self.top_bar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 0)
        )

        self.top_bar.grid_columnconfigure(
            0,
            weight=1
        )

        self.page_title = ctk.CTkLabel(
            self.top_bar,
            text="Dashboard",
            font=("Arial", 28, "bold"),
            text_color="#f8fafc"
        )

        self.page_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.page_subtitle = ctk.CTkLabel(
            self.top_bar,
            text="Your study progress at a glance",
            font=("Arial", 12),
            text_color="#94a3b8"
        )

        self.page_subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(2, 0)
        )

        # ----------------------------------------------------
        # Content Area
        # ----------------------------------------------------

        self.content_frame = ctk.CTkScrollableFrame(
            self.main_area,
            corner_radius=16,
            fg_color="#111827",
            scrollbar_button_color="#334155",
            scrollbar_button_hover_color="#475569"
        )

        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=20
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1
        )

    # ========================================================
    # PAGE HELPERS
    # ========================================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def set_active_nav(self, active_name):

        for name, button in self.nav_buttons.items():

            if name == active_name:

                button.configure(
                    fg_color="#2563eb",
                    text_color="#ffffff"
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color="#cbd5e1"
                )

    def set_page_header(self, title, subtitle):

        self.page_title.configure(
            text=title
        )

        self.page_subtitle.configure(
            text=subtitle
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.current_page = "Dashboard"

        self.set_active_nav("Dashboard")

        self.set_page_header(
            "Dashboard",
            "Your study progress at a glance"
        )

        self.clear_content()

        # ----------------------------------------------------
        # Welcome
        # ----------------------------------------------------

        welcome = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#172554"
        )

        welcome.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        welcome.grid_columnconfigure(
            0,
            weight=1
        )

        welcome_title = ctk.CTkLabel(
            welcome,
            text="Welcome back, Student 👋",
            font=("Arial", 25, "bold"),
            text_color="#f8fafc"
        )

        welcome_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(22, 4)
        )

        welcome_text = ctk.CTkLabel(
            welcome,
            text="Stay consistent today and keep building your academic progress.",
            font=("Arial", 13),
            text_color="#bfdbfe"
        )

        welcome_text.grid(
            row=1,
            column=0,
            sticky="w",
            padx=25,
            pady=(0, 22)
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        stats_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
            pady=(20, 5)
        )

        for column in range(4):
            stats_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.create_stat_card(
            stats_frame,
            0,
            "📚",
            "0",
            "Total Tasks"
        )

        self.create_stat_card(
            stats_frame,
            1,
            "✅",
            "0",
            "Completed"
        )

        self.create_stat_card(
            stats_frame,
            2,
            "⏳",
            "0",
            "Pending"
        )

        self.create_stat_card(
            stats_frame,
            3,
            "🔥",
            "0",
            "Study Streak"
        )

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        progress_card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        progress_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        progress_title = ctk.CTkLabel(
            progress_card,
            text="📊 Overall Study Progress",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        )

        progress_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        progress_info = ctk.CTkLabel(
            progress_card,
            text="0% completed",
            font=("Arial", 13),
            text_color="#94a3b8"
        )

        progress_info.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        progress_bar = ctk.CTkProgressBar(
            progress_card,
            height=15,
            corner_radius=8,
            progress_color="#3b82f6"
        )

        progress_bar.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        progress_bar.set(0)

        # ----------------------------------------------------
        # Quick Actions
        # ----------------------------------------------------

        quick_card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        quick_card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=5,
            pady=10
        )

        quick_title = ctk.CTkLabel(
            quick_card,
            text="⚡ Quick Actions",
            font=("Arial", 18, "bold"),
            text_color="#f8fafc"
        )

        quick_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        quick_buttons = ctk.CTkFrame(
            quick_card,
            fg_color="transparent"
        )

        quick_buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        add_task_button = ctk.CTkButton(
            quick_buttons,
            text="➕ Add Task",
            height=42,
            corner_radius=10,
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.add_task_placeholder
        )

        add_task_button.pack(
            side="left",
            padx=(0, 10)
        )

        focus_button = ctk.CTkButton(
            quick_buttons,
            text="🍅 Start Focus",
            height=42,
            corner_radius=10,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.show_focus
        )

        focus_button.pack(
            side="left",
            padx=10
        )

        tasks_button = ctk.CTkButton(
            quick_buttons,
            text="📝 View Tasks",
            height=42,
            corner_radius=10,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.show_tasks
        )

        tasks_button.pack(
            side="left",
            padx=10
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        column,
        icon,
        number,
        label
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=18,
            fg_color="#1e293b"
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 28)
        )

        icon_label.pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )

        number_label = ctk.CTkLabel(
            card,
            text=number,
            font=("Arial", 28, "bold"),
            text_color="#f8fafc"
        )

        number_label.pack(
            anchor="w",
            padx=18
        )

        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=("Arial", 12),
            text_color="#94a3b8"
        )

        label_widget.pack(
            anchor="w",
            padx=18,
            pady=(0, 18)
        )

    # ========================================================
    # TASKS
    # ========================================================

    def show_tasks(self):

        self.current_page = "Tasks"

        self.set_active_nav("Tasks")

        self.set_page_header(
            "Tasks",
            "Manage your study tasks"
        )

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="📝 All Study Tasks",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 15)
        )

        empty_card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        empty_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        message = ctk.CTkLabel(
            empty_card,
            text="Your task manager will appear here.\n\nWe will connect your existing tasks.json data next.",
            font=("Arial", 14),
            text_color="#94a3b8",
            justify="center"
        )

        message.pack(
            padx=30,
            pady=60
        )

    # ========================================================
    # CALENDAR
    # ========================================================

    def show_calendar(self):

        self.current_page = "Calendar"

        self.set_active_nav("Calendar")

        self.set_page_header(
            "Calendar",
            "Plan and track your study schedule"
        )

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="📅 Study Calendar",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        card.pack(
            fill="both",
            expand=True,
            padx=5
        )

        message = ctk.CTkLabel(
            card,
            text="Calendar module coming next.",
            font=("Arial", 16),
            text_color="#94a3b8"
        )

        message.pack(
            pady=80
        )

    # ========================================================
    # FOCUS
    # ========================================================

    def show_focus(self):

        self.current_page = "Focus"

        self.set_active_nav("Focus")

        self.set_page_header(
            "Focus",
            "Use focused study sessions to stay productive"
        )

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="🍅 Pomodoro Focus",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=20,
            fg_color="#1e293b"
        )

        card.pack(
            fill="x",
            padx=5
        )

        timer = ctk.CTkLabel(
            card,
            text="25:00",
            font=("Arial", 64, "bold"),
            text_color="#f8fafc"
        )

        timer.pack(
            pady=(35, 10)
        )

        status = ctk.CTkLabel(
            card,
            text="Ready to focus",
            font=("Arial", 14),
            text_color="#94a3b8"
        )

        status.pack(
            pady=(0, 20)
        )

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=(0, 35)
        )

        start_button = ctk.CTkButton(
            button_frame,
            text="▶️ Start",
            width=110,
            height=40,
            fg_color="#16a34a",
            hover_color="#15803d"
        )

        start_button.pack(
            side="left",
            padx=5
        )

        pause_button = ctk.CTkButton(
            button_frame,
            text="⏸️ Pause",
            width=110,
            height=40,
            fg_color="#ca8a04",
            hover_color="#a16207"
        )

        pause_button.pack(
            side="left",
            padx=5
        )

        reset_button = ctk.CTkButton(
            button_frame,
            text="🔄 Reset",
            width=110,
            height=40,
            fg_color="#475569",
            hover_color="#334155"
        )

        reset_button.pack(
            side="left",
            padx=5
        )

    # ========================================================
    # ANALYTICS
    # ========================================================

    def show_analytics(self):

        self.current_page = "Analytics"

        self.set_active_nav("Analytics")

        self.set_page_header(
            "Analytics",
            "Understand your study performance"
        )

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="📊 Advanced Analytics",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        card.pack(
            fill="x",
            padx=5
        )

        message = ctk.CTkLabel(
            card,
            text="Your Matplotlib analytics dashboard will be connected here next.",
            font=("Arial", 15),
            text_color="#94a3b8"
        )

        message.pack(
            pady=70
        )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    def show_achievements(self):

        self.current_page = "Achievements"

        self.set_active_nav("Achievements")

        self.set_page_header(
            "Achievements",
            "Track milestones and rewards"
        )

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="🏆 Achievements",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        card.pack(
            fill="x",
            padx=5
        )

        message = ctk.CTkLabel(
            card,
            text="XP, levels and achievements will be added here.",
            font=("Arial", 15),
            text_color="#94a3b8"
        )

        message.pack(
            pady=70
        )

    # ========================================================
    # SETTINGS
    # ========================================================

    def show_settings(self):

        self.current_page = "Settings"

        self.set_active_nav("Settings")

        self.set_page_header(
            "Settings",
            "Customize your study planner"
        )

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="⚙️ Settings",
            font=("Arial", 24, "bold"),
            text_color="#f8fafc"
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=18,
            fg_color="#1e293b"
        )

        card.pack(
            fill="x",
            padx=5
        )

        appearance_label = ctk.CTkLabel(
            card,
            text="Appearance Mode",
            font=("Arial", 15, "bold"),
            text_color="#f8fafc"
        )

        appearance_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 8)
        )

        appearance_menu = ctk.CTkOptionMenu(
            card,
            values=["Dark", "Light", "System"],
            command=self.change_appearance
        )

        appearance_menu.set("Dark")

        appearance_menu.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # ========================================================
    # PLACEHOLDER ACTION
    # ========================================================

    def add_task_placeholder(self):

        messagebox.showinfo(
            "Add Study Task",
            "The full task manager will be connected next."
        )

    # ========================================================
    # THEME
    # ========================================================

    def change_appearance(self, mode):

        ctk.set_appearance_mode(
            mode.lower()
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = StudyPlannerApp()

    app.mainloop()