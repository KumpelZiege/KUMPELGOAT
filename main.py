"""
KUMPELGOAT - Material You + Glassmorphism Edition 🐐
A stunning personal assistant with Android 12+ design language
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.utils import platform
from kivy.core.text import LabelBase
import datetime
import json
import os
import sqlite3
import threading
import time

# Material You Color Palette
MATERIAL_PRIMARY = (0.25, 0.45, 0.95, 1)      # #3A5FEF - Vibrant Blue
MATERIAL_PRIMARY_DARK = (0.15, 0.25, 0.55, 1) # #263F8C - Dark Blue
MATERIAL_SECONDARY = (0.95, 0.45, 0.45, 1)    # #F27373 - Soft Red
MATERIAL_TERTIARY = (0.45, 0.85, 0.65, 1)     # #73D9A6 - Mint Green
MATERIAL_BACKGROUND = (0.03, 0.03, 0.05, 1)   # #08080D - Almost Black
MATERIAL_SURFACE = (0.08, 0.08, 0.12, 1)      # #14141F - Dark Surface
MATERIAL_ERROR = (0.95, 0.35, 0.35, 1)        # #F25959 - Error Red

# Glassmorphism Effects
GLASS_BG = (1, 1, 1, 0.08)                    # Frosted glass background
GLASS_BG_HOVER = (1, 1, 1, 0.12)               # Frosted glass hover
GLASS_BORDER = (1, 1, 1, 0.15)                 # Glass border
GLASS_HIGHLIGHT = (1, 1, 1, 0.03)              # Subtle highlight

# Priority Colors
PRIORITY_HIGH = (0.95, 0.35, 0.35, 1)          # 🔴 Red
PRIORITY_MEDIUM = (0.95, 0.75, 0.35, 1)        # 🟡 Yellow
PRIORITY_LOW = (0.45, 0.85, 0.65, 1)            # 🔵 Mint

# Database
DB_PATH = 'kumpel.db'

class MaterialButton(Button):
    """Material You button with glass morphism effects"""
    def __init__(self, text="", primary=False, secondary=False, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.primary = primary
        self.secondary = secondary
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = sp(16)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(56)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.primary:
                Color(*MATERIAL_PRIMARY)
            elif self.secondary:
                Color(*MATERIAL_SECONDARY)
            else:
                Color(*GLASS_BG)
            
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(28)])
            
            if not self.primary and not self.secondary:
                Color(*GLASS_BORDER)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(28)], width=dp(1))

class MaterialInput(TextInput):
    """Material You text input with glass effect"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.foreground_color = (1, 1, 1, 1)
        self.padding = [dp(20), dp(18)]
        self.font_size = sp(16)
        self.cursor_color = MATERIAL_PRIMARY
        self.cursor_width = dp(3)
        self.size_hint_y = None
        self.height = dp(60)
        self.hint_text_color = (0.6, 0.6, 0.6, 1)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*GLASS_BG)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(30)])
            Color(*MATERIAL_PRIMARY, 0.5 if self.focus else 0.2)
            RoundedRectangle(pos=(self.x, self.y), size=(self.width, dp(2)), radius=[dp(1)])

class TaskCard(RelativeLayout):
    """Beautiful task card with material you design"""
    def __init__(self, task_id, description, due_time, priority, **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id
        self.size_hint_y = None
        self.height = dp(100)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
        # Priority color
        if priority == 1:
            self.priority_color = PRIORITY_HIGH
            priority_text = "🔴 HIGH"
        elif priority == 2:
            self.priority_color = PRIORITY_MEDIUM
            priority_text = "🟡 MEDIUM"
        else:
            self.priority_color = PRIORITY_LOW
            priority_text = "🔵 LOW"
        
        # Left accent bar
        with self.canvas.before:
            Color(*self.priority_color)
            self.accent = RoundedRectangle(pos=(self.x, self.y), size=(dp(8), self.height), radius=[dp(4)])
        
        # Task description
        desc_label = Label(
            text=description,
            color=(1, 1, 1, 1),
            size_hint=(0.6, 0.3),
            pos_hint={'x': 0.15, 'top': 0.75},
            font_size=sp(16),
            bold=True,
            halign='left'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        self.add_widget(desc_label)
        
        # Due time
        try:
            due_obj = datetime.datetime.fromisoformat(due_time)
            time_str = due_obj.strftime("%I:%M %p")
        except:
            time_str = "Now"
        
        time_label = Label(
            text=f"⏰ {time_str}",
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.6, 'top': 0.75},
            font_size=sp(14)
        )
        self.add_widget(time_label)
        
        # Priority badge
        priority_label = Label(
            text=priority_text,
            color=self.priority_color,
            size_hint=(0.3, 0.25),
            pos_hint={'x': 0.15, 'y': 0.1},
            font_size=sp(12),
            bold=True
        )
        self.add_widget(priority_label)
        
        # Done button
        done_btn = MaterialButton(
            text="✓ DONE",
            size_hint=(0.2, 0.4),
            pos_hint={'x': 0.75, 'y': 0.3}
        )
        done_btn.bind(on_release=lambda x: self.mark_done())
        self.add_widget(done_btn)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*GLASS_BG)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
            Color(*GLASS_BORDER)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)], width=dp(1))
            Color(*self.priority_color)
            self.accent = RoundedRectangle(pos=(self.x, self.y), size=(dp(8), self.height), radius=[dp(4)])
    
    def mark_done(self):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("UPDATE tasks SET completed=1 WHERE id=?", (self.task_id,))
            conn.commit()
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *x: self.parent.remove_widget(self))
        anim.start(self)

class KumpelGoatApp(App):
    def build(self):
        Window.clearcolor = MATERIAL_BACKGROUND
        Window.size = (400, 780)
        
        main = FloatLayout()
        
        # Background gradient effect
        with main.canvas.before:
            Color(*MATERIAL_BACKGROUND)
            Rectangle(pos=(0, 0), size=Window.size)
            
            # Subtle accent circles
            Color(*MATERIAL_PRIMARY, 0.05)
            Ellipse(pos=(-100, 500), size=(300, 300))
            Color(*MATERIAL_SECONDARY, 0.05)
            Ellipse(pos=(250, 600), size=(250, 250))
            Color(*MATERIAL_TERTIARY, 0.05)
            Ellipse(pos=(150, 100), size=(200, 200))
        
        # Header
        header = RelativeLayout(size_hint=(1, 0.12), pos_hint={'top': 1})
        with header.canvas.before:
            Color(*GLASS_BG)
            RoundedRectangle(pos=header.pos, size=header.size, radius=[(0, 0, dp(30), dp(30))])
        
        title = Label(
            text="🐐 KUMPELGOAT",
            color=MATERIAL_PRIMARY,
            size_hint=(1, 1),
            font_size=sp(32),
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        header.add_widget(title)
        main.add_widget(header)
        
        # Main content card
        content = FloatLayout(size_hint=(0.95, 0.8), pos_hint={'center_x': 0.5, 'y': 0.1})
        
        with content.canvas.before:
            Color(*GLASS_BG)
            RoundedRectangle(pos=content.pos, size=content.size, radius=[dp(30)])
            Color(*GLASS_BORDER)
            RoundedRectangle(pos=content.pos, size=content.size, radius=[dp(30)], width=dp(1))
        
        # Input section
        input_box = BoxLayout(orientation='vertical', size_hint=(0.9, 0.25), 
                              pos_hint={'center_x': 0.5, 'top': 0.95}, spacing=dp(10))
        
        self.task_input = MaterialInput(hint_text="What needs to be done?")
        input_box.add_widget(self.task_input)
        
        # Priority selector
        priority_box = BoxLayout(size_hint=(1, 0.4), spacing=dp(8))
        
        self.high_btn = Button(
            text="🔴 HIGH",
            background_color=PRIORITY_HIGH,
            size_hint=(0.33, 1),
            color=(1,1,1,1),
            bold=True
        )
        self.high_btn.bind(on_release=lambda x: self.set_priority(1))
        
        self.medium_btn = Button(
            text="🟡 MEDIUM",
            background_color=PRIORITY_MEDIUM,
            size_hint=(0.33, 1),
            color=(1,1,1,1),
            bold=True
        )
        self.medium_btn.bind(on_release=lambda x: self.set_priority(2))
        
        self.low_btn = Button(
            text="🔵 LOW",
            background_color=PRIORITY_LOW,
            size_hint=(0.33, 1),
            color=(1,1,1,1),
            bold=True
        )
        self.low_btn.bind(on_release=lambda x: self.set_priority(3))
        
        priority_box.add_widget(self.high_btn)
        priority_box.add_widget(self.medium_btn)
        priority_box.add_widget(self.low_btn)
        input_box.add_widget(priority_box)
        
        # Add button
        add_btn = MaterialButton(text="➕ ADD TASK", primary=True)
        add_btn.bind(on_release=self.add_task)
        input_box.add_widget(add_btn)
        
        content.add_widget(input_box)
        
        # Tasks header
        tasks_header = Label(
            text="📋 YOUR TASKS",
            color=(1,1,1,0.9),
            size_hint=(0.9, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.65},
            font_size=sp(18),
            bold=True
        )
        content.add_widget(tasks_header)
        
        # Task list
        self.task_scroll = ScrollView(
            size_hint=(0.9, 0.45),
            pos_hint={'center_x': 0.5, 'top': 0.6},
            bar_width=dp(4),
            bar_color=MATERIAL_PRIMARY
        )
        
        self.task_list = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8),
            padding=[dp(5)]
        )
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.task_scroll.add_widget(self.task_list)
        content.add_widget(self.task_scroll)
        
        main.add_widget(content)
        
        # Stats bar
        stats = RelativeLayout(size_hint=(0.95, 0.05), pos_hint={'center_x': 0.5, 'y': 0.02})
        with stats.canvas.before:
            Color(*GLASS_BG)
            RoundedRectangle(pos=stats.pos, size=stats.size, radius=[dp(15)])
        
        self.stats_label = Label(
            text="✨ 0 tasks • ready to help",
            color=(1,1,1,0.7),
            size_hint=(1,1),
            font_size=sp(14)
        )
        stats.add_widget(self.stats_label)
        main.add_widget(stats)
        
        # Initialize
        self.priority = 2
        self.medium_btn.background_color = PRIORITY_MEDIUM
        self.init_db()
        Clock.schedule_once(lambda dt: self.load_tasks(), 0.1)
        
        return main
    
    def init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS tasks
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          description TEXT,
                          due_time TEXT,
                          priority INTEGER,
                          completed INTEGER,
                          created_at TEXT)''')
            conn.commit()
    
    def set_priority(self, p):
        self.priority = p
        self.high_btn.background_color = PRIORITY_HIGH if p == 1 else (0.3,0.3,0.3,0.3)
        self.medium_btn.background_color = PRIORITY_MEDIUM if p == 2 else (0.3,0.3,0.3,0.3)
        self.low_btn.background_color = PRIORITY_LOW if p == 3 else (0.3,0.3,0.3,0.3)
    
    def add_task(self, instance):
        desc = self.task_input.text.strip()
        if not desc:
            return
        
        due_time = datetime.datetime.now().isoformat()
        
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO tasks 
                         (description, due_time, priority, completed, created_at)
                         VALUES (?,?,?,?,?)''',
                      (desc, due_time, self.priority, 0, datetime.datetime.now().isoformat()))
            conn.commit()
        
        self.task_input.text = ''
        self.load_tasks()
        
        # Animation
        anim = Animation(opacity=0.5, duration=0.1) + Animation(opacity=1, duration=0.3)
        anim.start(self.task_list)
    
    def load_tasks(self):
        self.task_list.clear_widgets()
        
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''SELECT id, description, due_time, priority 
                         FROM tasks 
                         WHERE completed=0 
                         ORDER BY priority ASC, due_time ASC''')
            tasks = c.fetchall()
        
        for task in tasks:
            card = TaskCard(*task)
            self.task_list.add_widget(card)
        
        count = len(tasks)
        self.stats_label.text = f"✨ {count} task{' • ready to help' if count==0 else ' pending'}"

if __name__ == '__main__':
    KumpelGoatApp().run()
