"""
AI NUMBER GUESSER - Complete Version
Created by: Fatima Zahra Oubella
Email: fatimazahra.oubella@etu.uae.ac.ma
Location: Tangier, Morocco
"""

import tkinter as tk
from tkinter import messagebox, ttk
import math
import json
import os
from datetime import datetime

class NumberGuessingGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🤖 AI Number Guesser - Fatima Zahra Oubella")
        self.window.geometry("700x800")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Personal information
        self.author = "Fatima Zahra Oubella"
        self.email = "fatimazahra.oubella@etu.uae.ac.ma"
        self.location = "Tangier, Morocco"
        self.university = "Abdelmalek Essaâdi University"
        
        # Game variables
        self.reset_game()
        self.load_stats()
        
        # Setup UI
        self.setup_ui()
        
        # Center window
        self.center_window()
        
    def reset_game(self):
        """Reset game variables"""
        self.lower = 0
        self.upper = None
        self.guesses = 0
        self.state = 'idle'
        self.max_range = None
        
    def load_stats(self):
        """Load statistics from file"""
        self.stats_file = 'game_stats.json'
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = self.init_stats()
        else:
            self.stats = self.init_stats()
    
    def init_stats(self):
        return {
            'games': 0,
            'total_guesses': 0,
            'best': float('inf'),
            'last_game': None
        }
    
    def save_stats(self):
        """Save statistics to file"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=4)
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Create user interface"""
        
        # ===== HEADER WITH PERSONAL INFO =====
        header = tk.Frame(self.window, bg='#3498db', height=140)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🤖 AI NUMBER GUESSER",
            font=('Arial', 24, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(expand=True)
        
        tk.Label(
            header,
            text="Think of a positive number, I'll guess it!",
            font=('Arial', 11),
            bg='#3498db',
            fg='white'
        ).pack()
        
        # Personal info frame
        info_perso = tk.Frame(header, bg='#2980b9', height=60)
        info_perso.pack(fill='x', pady=(5, 0))
        info_perso.pack_propagate(False)
        
        tk.Label(
            info_perso,
            text=f"👩‍💻 {self.author}",
            font=('Arial', 10, 'bold'),
            bg='#2980b9',
            fg='white'
        ).pack()
        
        tk.Label(
            info_perso,
            text=f"📧 {self.email}",
            font=('Arial', 9),
            bg='#2980b9',
            fg='white'
        ).pack()
        
        tk.Label(
            info_perso,
            text=f"📍 {self.location} | 🏫 {self.university}",
            font=('Arial', 9, 'italic'),
            bg='#2980b9',
            fg='#ecf0f1'
        ).pack()
        
        # ===== STATISTICS =====
        stats_frame = tk.Frame(self.window, bg='#34495e', pady=10)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self.stats_label = tk.Label(
            stats_frame,
            text=self.get_stats_text(),
            font=('Arial', 11),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.stats_label.pack()
        
        # ===== QUESTION AREA =====
        question_frame = tk.Frame(self.window, bg='#34495e', height=120)
        question_frame.pack(fill='x', padx=20, pady=10)
        question_frame.pack_propagate(False)
        
        self.question_label = tk.Label(
            question_frame,
            text="✨ Click 'New Game' to start!",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='white',
            wraplength=500
        )
        self.question_label.pack(expand=True)
        
        # ===== PROGRESS BAR =====
        self.progress = ttk.Progressbar(
            self.window,
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # ===== YES/NO BUTTONS =====
        btn_frame = tk.Frame(self.window, bg='#2c3e50')
        btn_frame.pack(pady=20)
        
        self.yes_btn = tk.Button(
            btn_frame,
            text="✓ YES",
            command=lambda: self.handle_response(True),
            bg='#2ecc71',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=12,
            height=2,
            state='disabled'
        )
        self.yes_btn.pack(side='left', padx=10)
        
        self.no_btn = tk.Button(
            btn_frame,
            text="✗ NO",
            command=lambda: self.handle_response(False),
            bg='#e74c3c',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=12,
            height=2,
            state='disabled'
        )
        self.no_btn.pack(side='left', padx=10)
        
        # ===== CONTROL BUTTONS =====
        control_frame = tk.Frame(self.window, bg='#2c3e50')
        control_frame.pack(pady=10)
        
        self.new_game_btn = tk.Button(
            control_frame,
            text="🎮 NEW GAME",
            command=self.start_game,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=12,
            height=2
        )
        self.new_game_btn.pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="📊 STATISTICS",
            command=self.show_stats,
            bg='#f39c12',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=12,
            height=2
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="🔄 RESET",
            command=self.reset_stats,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=12,
            height=2
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="📧 CONTACT",
            command=self.show_contact,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 11, 'bold'),
            width=12,
            height=2
        ).pack(side='left', padx=5)
        
        # ===== INFORMATION =====
        info_frame = tk.Frame(self.window, bg='#34495e')
        info_frame.pack(fill='x', padx=20, pady=20)
        
        info_text = f"""
        ⚡ HOW IT WORKS?
        
        1. First, I find an upper bound
        2. Then, I divide the range in half each time
        3. I find your number in record time!
        
        Complexity: O(log n) questions
        
        ─────────────────────────────────
        Developed by: {self.author}
        {self.university}
        {self.location}
        ─────────────────────────────────
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            bg='#34495e',
            fg='#bdc3c7',
            justify='left'
        ).pack(pady=10)
    
    def get_stats_text(self):
        """Get statistics text"""
        avg = self.stats['total_guesses'] / self.stats['games'] if self.stats['games'] > 0 else 0
        best = self.stats['best'] if self.stats['best'] != float('inf') else '-'
        return f"📈 Games: {self.stats['games']} | Average: {avg:.1f} | Best: {best}"
    
    def show_contact(self):
        """Show contact information"""
        contact_text = f"""
        📬 CONTACT INFORMATION
        ════════════════════════════
        
        👤 Name: {self.author}
        📧 Email: {self.email}
        📍 Location: {self.location}
        🏫 University: {self.university}
        
        🤝 Feel free to contact me!
        """
        messagebox.showinfo("Contact", contact_text)
    
    def start_game(self):
        """Start a new game"""
        self.reset_game()
        self.state = 'finding'
        self.lower = 0
        self.upper = 1
        self.guesses = 0
        
        # Enable buttons
        self.yes_btn.config(state='normal')
        self.no_btn.config(state='normal')
        self.new_game_btn.config(state='disabled')
        
        # Update display
        self.progress['value'] = 20
        self.update_question()
    
    def update_question(self):
        """Update displayed question"""
        if self.state == 'finding':
            self.question_label.config(
                text=f"❓ Is your number between 0 and {self.upper}?"
            )
        elif self.state == 'guessing':
            mid = (self.lower + self.upper) // 2
            self.question_label.config(
                text=f"❓ Is your number between {self.lower} and {mid}?"
            )
    
    def handle_response(self, response):
        """Handle user's response"""
        self.guesses += 1
        
        if self.state == 'finding':
            if response:  # YES
                self.state = 'guessing'
                self.max_range = self.upper
                self.progress['value'] = 40
            else:  # NO
                self.lower = self.upper + 1
                self.upper *= 2
                self.progress['value'] = min(40, 20 + self.guesses * 5)
            
            self.update_question()
            
        elif self.state == 'guessing':
            if self.lower == self.upper:
                self.make_guess()
                return
            
            mid = (self.lower + self.upper) // 2
            
            if response:  # YES
                self.upper = mid
            else:  # NO
                self.lower = mid + 1
            
            # Update progress
            if self.max_range:
                progress = 40 + (60 * (1 - (self.upper - self.lower) / self.max_range))
                self.progress['value'] = min(95, progress)
            
            self.update_question()
    
    def make_guess(self):
        """Make final guess"""
        self.progress['value'] = 100
        guess = self.lower
        
        # Update statistics
        self.stats['games'] += 1
        self.stats['total_guesses'] += self.guesses
        if self.guesses < self.stats['best']:
            self.stats['best'] = self.guesses
        self.stats['last_game'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.save_stats()
        
        # Calculate efficiency
        theoretical = math.ceil(math.log2(guess + 1)) + 1
        efficiency = (theoretical / self.guesses) * 100
        
        # Show result with personal information
        result = f"""🎉 VICTORY! I FOUND IT! 🎉

╔════════════════════════════╗
║      GAME RESULTS          ║
╠════════════════════════════╣
║                             ║
║   🔢 Your number: {guess:<8}      ║
║   ❓ Questions: {self.guesses:<8}      ║
║   📊 Theoretical: {theoretical:<8}      ║
║   ⚡ Efficiency: {efficiency:.1f}%      ║
║                             ║
╚════════════════════════════╝

Developed by: {self.author}
📧 {self.email}
📍 {self.location}"""

        messagebox.showinfo("🎉 Victory! 🎉", result)
        
        # Reset
        self.yes_btn.config(state='disabled')
        self.no_btn.config(state='disabled')
        self.new_game_btn.config(state='normal')
        self.question_label.config(text="✨ Ready for a new game?")
        self.stats_label.config(text=self.get_stats_text())
    
    def show_stats(self):
        """Show detailed statistics"""
        if self.stats['games'] == 0:
            messagebox.showinfo("Statistics", "No games played yet!")
            return
        
        avg = self.stats['total_guesses'] / self.stats['games']
        stats_text = f"""
╔════════════════════════════╗
║    DETAILED STATISTICS     ║
╠════════════════════════════╣
║                             ║
║   🎮 Games: {self.stats['games']:<8}      ║
║   🎯 Total questions: {self.stats['total_guesses']:<4}      ║
║   📉 Average: {avg:.2f}{' ' * (8 - len(f'{avg:.2f}'))}      ║
║   🏆 Best: {self.stats['best'] if self.stats['best'] != float('inf') else '-':<8}      ║
║   📅 Last game: {self.stats['last_game'] or 'Never'}  ║
║                             ║
╠════════════════════════════╣
║   👩‍💻 {self.author}              ║
║   📍 {self.location}           ║
╚════════════════════════════╝
        """
        messagebox.showinfo("Statistics", stats_text)
    
    def reset_stats(self):
        """Reset statistics"""
        if messagebox.askyesno("Confirmation", "Do you really want to reset all statistics?"):
            self.stats = self.init_stats()
            self.save_stats()
            self.stats_label.config(text=self.get_stats_text())
            messagebox.showinfo("Success", "Statistics have been reset!")
    
    def run(self):
        """Run the application"""
        self.window.mainloop()

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()