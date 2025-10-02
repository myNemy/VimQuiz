#!/usr/bin/env python3
"""
VIM QUIZ - Quiz interattivo per imparare i comandi Vim
Versione con GUI Qt6 e sistema modulare delle domande
"""

import sys
import random
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QRadioButton, 
                             QButtonGroup, QProgressBar, QTextEdit, QGroupBox,
                             QMessageBox, QMenuBar, QStatusBar, QSplitter,
                             QComboBox, QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

# Importa il caricatore delle domande e il sistema i18n
from questions_loader import QuestionsLoader
from i18n_manager import I18nManager

class VimQuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Inizializza il sistema i18n
        try:
            self.i18n = I18nManager()
            # Forza l'inglese come lingua predefinita all'avvio
            self.i18n.set_language("en")
        except Exception as e:
            print(f"Error initializing i18n: {e}")
            # Fallback all'inglese
            self.i18n = I18nManager()
        
        # Imposta il titolo della finestra
        self.setWindowTitle(self.i18n.get_text("app.title"))
        self.setGeometry(100, 100, 1000, 700)
        
        # Inizializza il caricatore delle domande
        try:
            self.questions_loader = QuestionsLoader(i18n_manager=self.i18n)
            self.vim_commands = self._build_commands_dict()
        except Exception as e:
            QMessageBox.critical(self, self.i18n.get_text("errors.load_questions", error=str(e)), 
                               self.i18n.get_text("errors.load_questions", error=str(e)))
            sys.exit(1)
        
        # Variabili del quiz
        self.current_question = 0
        self.total_questions = 0
        self.score = 0
        self.wrong_answers = []
        self.questions = []
        self.current_options = []
        self.correct_answer = ""
        self.selected_category = self.i18n.get_text("quiz.all_categories")
        self.selected_difficulty = self.i18n.get_text("quiz.all_difficulties")
        self.question_limit = 20
        
        self.init_ui()
        self.setup_quiz()
    
    def _build_commands_dict(self):
        """Costruisce il dizionario dei comandi dal caricatore delle domande"""
        commands = {}
        for question in self.questions_loader.get_all_questions():
            commands[question['command']] = question['description']
        return commands
        
    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        
        # Barra del menu
        self.create_menu_bar()
        
        # Pannello superiore - Informazioni quiz
        self.info_group = QGroupBox(self.i18n.get_text("ui.info_group"))
        info_layout = QVBoxLayout(self.info_group)
        
        # Prima riga: informazioni base
        info_row1 = QHBoxLayout()
        self.question_label = QLabel(self.i18n.get_text("quiz.question_label", current=0, total=0))
        self.question_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.score_label = QLabel(self.i18n.get_text("quiz.score_label", score=0))
        self.score_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        
        info_row1.addWidget(self.question_label)
        info_row1.addWidget(self.score_label)
        info_row1.addWidget(self.progress_bar)
        
        # Seconda riga: controlli filtro
        filter_row = QHBoxLayout()
        
        # Selettore lingua
        self.language_label = QLabel(self.i18n.get_text("ui.language_label"))
        filter_row.addWidget(self.language_label)
        self.language_combo = QComboBox()
        for lang_code in self.i18n.get_supported_languages():
            lang_name = self.i18n.get_language_name(lang_code)
            self.language_combo.addItem(f"{lang_name} ({lang_code})", lang_code)
        # Seleziona l'inglese come predefinito
        self.language_combo.setCurrentText(f"{self.i18n.get_language_name('en')} (en)")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        filter_row.addWidget(self.language_combo)
        
        # Filtro categoria
        self.category_label = QLabel(self.i18n.get_text("quiz.category_label"))
        filter_row.addWidget(self.category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItem(self.i18n.get_text("quiz.all_categories"))
        for category in self.questions_loader.get_categories():
            self.category_combo.addItem(category)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        filter_row.addWidget(self.category_combo)
        
        # Filtro difficoltà
        self.difficulty_label = QLabel(self.i18n.get_text("quiz.difficulty_label"))
        filter_row.addWidget(self.difficulty_label)
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem(self.i18n.get_text("quiz.all_difficulties"))
        for difficulty in self.questions_loader.get_difficulties():
            translated_difficulty = self.i18n.get_text(f"questions.difficulties.{difficulty}")
            self.difficulty_combo.addItem(translated_difficulty, difficulty)
        self.difficulty_combo.currentTextChanged.connect(self.on_difficulty_changed)
        filter_row.addWidget(self.difficulty_combo)
        
        # Limite domande
        self.questions_label = QLabel(self.i18n.get_text("quiz.questions_label"))
        filter_row.addWidget(self.questions_label)
        self.question_limit_spin = QSpinBox()
        self.question_limit_spin.setMinimum(5)
        self.question_limit_spin.setMaximum(100)
        self.question_limit_spin.setValue(20)
        self.question_limit_spin.valueChanged.connect(self.on_limit_changed)
        filter_row.addWidget(self.question_limit_spin)
        
        # Pulsante aggiorna
        self.update_quiz_button = QPushButton(self.i18n.get_text("quiz.update_quiz_button"))
        self.update_quiz_button.clicked.connect(self.update_quiz_settings)
        filter_row.addWidget(self.update_quiz_button)
        
        filter_row.addStretch()
        
        info_layout.addLayout(info_row1)
        info_layout.addLayout(filter_row)
        
        # Pannello centrale - Domanda e opzioni
        self.question_group = QGroupBox(self.i18n.get_text("ui.question_group"))
        question_layout = QVBoxLayout(self.question_group)
        
        self.description_label = QLabel(self.i18n.get_text("ui.description_label"))
        self.description_label.setWordWrap(True)
        self.description_label.setFont(QFont("Arial", 11))
        self.description_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }")
        
        self.options_group = QButtonGroup()
        self.options_layout = QVBoxLayout()
        
        question_layout.addWidget(self.description_label)
        question_layout.addLayout(self.options_layout)
        
        # Pannello inferiore - Controlli
        self.controls_group = QGroupBox(self.i18n.get_text("ui.controls_group"))
        controls_layout = QHBoxLayout(self.controls_group)
        
        self.answer_button = QPushButton(self.i18n.get_text("quiz.answer_button"))
        self.answer_button.clicked.connect(self.check_answer)
        self.answer_button.setEnabled(False)
        
        self.next_button = QPushButton(self.i18n.get_text("quiz.next_button"))
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setEnabled(False)
        
        self.restart_button = QPushButton(self.i18n.get_text("quiz.restart_button"))
        self.restart_button.clicked.connect(self.restart_quiz)
        
        self.shuffle_button = QPushButton(self.i18n.get_text("quiz.shuffle_button"))
        self.shuffle_button.clicked.connect(self.shuffle_questions)
        
        controls_layout.addWidget(self.answer_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.restart_button)
        controls_layout.addWidget(self.shuffle_button)
        
        # Pannello laterale - Risultati
        self.results_group = QGroupBox(self.i18n.get_text("ui.results_group"))
        results_layout = QVBoxLayout(self.results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(200)
        self.results_text.setReadOnly(True)
        
        results_layout.addWidget(self.results_text)
        
        # Layout principale con splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.info_group)
        left_layout.addWidget(self.question_group)
        left_layout.addWidget(self.controls_group)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(self.results_group)
        splitter.setSizes([600, 200])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.i18n.get_text("ui.status_ready"))
        
    def create_menu_bar(self):
        """Crea la barra del menu"""
        menubar = self.menuBar()
        
        # Menu Quiz
        quiz_menu = menubar.addMenu(self.i18n.get_text("menu.quiz"))
        
        new_quiz_action = quiz_menu.addAction(self.i18n.get_text("menu.new_quiz"))
        new_quiz_action.triggered.connect(self.restart_quiz)
        
        shuffle_action = quiz_menu.addAction(self.i18n.get_text("menu.shuffle_questions"))
        shuffle_action.triggered.connect(self.shuffle_questions)
        
        update_action = quiz_menu.addAction(self.i18n.get_text("menu.update_settings"))
        update_action.triggered.connect(self.update_quiz_settings)
        
        quiz_menu.addSeparator()
        
        stats_action = quiz_menu.addAction(self.i18n.get_text("menu.statistics"))
        stats_action.triggered.connect(self.show_statistics)
        
        quiz_menu.addSeparator()
        
        exit_action = quiz_menu.addAction(self.i18n.get_text("menu.exit"))
        exit_action.triggered.connect(self.close)
        
        # Menu Aiuto
        help_menu = menubar.addMenu(self.i18n.get_text("menu.help"))
        
        about_action = help_menu.addAction(self.i18n.get_text("menu.about"))
        about_action.triggered.connect(self.show_about)
        
    def setup_quiz(self):
        """Configura il quiz iniziale"""
        self.load_questions()
        self.current_question = 0
        self.score = 0
        self.wrong_answers = []
        
        self.update_ui()
        self.load_question()
    
    def load_questions(self):
        """Carica le domande in base ai filtri selezionati"""
        category = self.selected_category if self.selected_category != self.i18n.get_text("quiz.all_categories") else None
        difficulty = self.selected_difficulty if self.selected_difficulty != self.i18n.get_text("quiz.all_difficulties") else None
        
        # Ottieni le domande filtrate
        if category and difficulty:
            # Filtra per entrambi
            category_questions = self.questions_loader.get_questions_by_category(category)
            self.questions = [q for q in category_questions if q.get('difficulty', 'beginner') == difficulty]
        elif category:
            self.questions = self.questions_loader.get_questions_by_category(category)
        elif difficulty:
            self.questions = self.questions_loader.get_questions_by_difficulty(difficulty)
        else:
            self.questions = self.questions_loader.get_all_questions()
        
        # Limita il numero di domande
        if len(self.questions) > self.question_limit:
            random.shuffle(self.questions)
            self.questions = self.questions[:self.question_limit]
        
        self.total_questions = len(self.questions)
        
        # Mescola le domande
        random.shuffle(self.questions)
    
    def on_language_changed(self, text):
        """Gestisce il cambio di lingua"""
        # Estrai il codice lingua dal testo selezionato
        lang_code = self.language_combo.currentData()
        if lang_code and self.i18n.set_language(lang_code):
            # Aggiorna le variabili selezionate con le nuove traduzioni
            if (self.selected_category == "Tutte" or 
                self.selected_category == "All" or 
                self.selected_category == "Todas" or 
                self.selected_category == "Toutes" or 
                self.selected_category == "Alle"):
                self.selected_category = self.i18n.get_text("quiz.all_categories")
            
            if (self.selected_difficulty == "Tutte" or 
                self.selected_difficulty == "All" or 
                self.selected_difficulty == "Todas" or 
                self.selected_difficulty == "Toutes" or 
                self.selected_difficulty == "Alle"):
                self.selected_difficulty = self.i18n.get_text("quiz.all_difficulties")
            
            # Ricarica le domande con le nuove traduzioni
            self.load_questions()
            
            # Aggiorna il dizionario dei comandi con le nuove traduzioni
            self.vim_commands = self._build_commands_dict()
            
            # Ricarica la domanda corrente se il quiz è in corso
            if self.questions:
                self.load_question()
            
            self.refresh_ui_texts()
            self.status_bar.showMessage(self.i18n.get_text("ui.status_language_changed", language=self.i18n.get_language_name(lang_code)))
    
    def on_category_changed(self, category):
        """Gestisce il cambio di categoria"""
        self.selected_category = category
        self.status_bar.showMessage(self.i18n.get_text("ui.status_category_selected", category=category))
    
    def on_difficulty_changed(self, difficulty):
        """Gestisce il cambio di difficoltà"""
        # Ottieni il valore originale della difficoltà (non tradotto)
        difficulty_data = self.difficulty_combo.currentData()
        if difficulty_data:
            self.selected_difficulty = difficulty_data
        else:
            self.selected_difficulty = difficulty
        self.status_bar.showMessage(self.i18n.get_text("ui.status_difficulty_selected", difficulty=difficulty))
    
    def on_limit_changed(self, limit):
        """Gestisce il cambio del limite domande"""
        self.question_limit = limit
        self.status_bar.showMessage(self.i18n.get_text("ui.status_limit_changed", limit=limit))
    
    def refresh_ui_texts(self):
        """Aggiorna tutti i testi dell'interfaccia con la lingua corrente"""
        # Aggiorna il titolo della finestra
        self.setWindowTitle(self.i18n.get_text("app.title"))
        
        # Aggiorna i gruppi
        self.info_group.setTitle(self.i18n.get_text("ui.info_group"))
        self.question_group.setTitle(self.i18n.get_text("ui.question_group"))
        self.controls_group.setTitle(self.i18n.get_text("ui.controls_group"))
        self.results_group.setTitle(self.i18n.get_text("ui.results_group"))
        
        # Aggiorna le etichette
        self.question_label.setText(self.i18n.get_text("quiz.question_label", 
                                                      current=self.current_question + 1, 
                                                      total=self.total_questions))
        self.score_label.setText(self.i18n.get_text("quiz.score_label", score=self.score))
        
        # Aggiorna i pulsanti
        self.answer_button.setText(self.i18n.get_text("quiz.answer_button"))
        self.next_button.setText(self.i18n.get_text("quiz.next_button"))
        self.restart_button.setText(self.i18n.get_text("quiz.restart_button"))
        self.shuffle_button.setText(self.i18n.get_text("quiz.shuffle_button"))
        self.update_quiz_button.setText(self.i18n.get_text("quiz.update_quiz_button"))
        
        # Aggiorna le etichette dei filtri
        self.language_label.setText(self.i18n.get_text("ui.language_label"))
        self.category_label.setText(self.i18n.get_text("quiz.category_label"))
        self.difficulty_label.setText(self.i18n.get_text("quiz.difficulty_label"))
        self.questions_label.setText(self.i18n.get_text("quiz.questions_label"))
        
        # Aggiorna i combo box
        self.category_combo.setItemText(0, self.i18n.get_text("quiz.all_categories"))
        self.difficulty_combo.setItemText(0, self.i18n.get_text("quiz.all_difficulties"))
        
        # Aggiorna le difficoltà tradotte
        for i, difficulty in enumerate(self.questions_loader.get_difficulties(), 1):
            translated_difficulty = self.i18n.get_text(f"questions.difficulties.{difficulty}")
            self.difficulty_combo.setItemText(i, translated_difficulty)
        
        # Aggiorna il selettore di lingua
        current_lang = self.i18n.get_current_language()
        self.language_combo.setCurrentText(f"{self.i18n.get_language_name(current_lang)} ({current_lang})")
        
        # Aggiorna il menu
        self.create_menu_bar()
        
        # Aggiorna la status bar
        self.status_bar.showMessage(self.i18n.get_text("ui.status_ready"))
    
    def update_quiz_settings(self):
        """Aggiorna le impostazioni del quiz"""
        self.setup_quiz()
        self.results_text.clear()
        self.status_bar.showMessage(self.i18n.get_text("ui.status_quiz_updated"))
        
    def shuffle_questions(self):
        """Mescola le domande"""
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.wrong_answers = []
        self.update_ui()
        self.load_question()
        self.status_bar.showMessage(self.i18n.get_text("ui.status_questions_shuffled"))
        
    def load_question(self):
        """Carica una nuova domanda"""
        if self.current_question >= self.total_questions:
            self.show_final_results()
            return
            
        # Pulisci le opzioni precedenti
        for i in reversed(range(self.options_layout.count())):
            self.options_layout.itemAt(i).widget().setParent(None)
        
        self.options_group = QButtonGroup()
        
        # Ottieni domanda corrente
        current_question_data = self.questions[self.current_question]
        self.correct_answer = current_question_data['command']
        description = current_question_data['description']
        category = current_question_data.get('source_category', 'Unknown')
        difficulty = current_question_data.get('difficulty', 'beginner')
        
        # Aggiorna descrizione con informazioni aggiuntive
        info_text = f"<b>Descrizione:</b><br>{description}"
        if category != 'Unknown':
            info_text += f"<br><b>Categoria:</b> {category}"
        if difficulty != 'beginner':
            info_text += f"<br><b>Difficoltà:</b> {difficulty}"
        
        self.description_label.setText(info_text)
        
        # Genera opzioni
        self.current_options = [self.correct_answer]
        
        # Aggiungi opzioni casuali da tutte le domande disponibili
        all_commands = list(self.vim_commands.keys())
        other_commands = [cmd for cmd in all_commands if cmd != self.correct_answer]
        random.shuffle(other_commands)
        
        for cmd in other_commands[:3]:  # Aggiungi 3 opzioni casuali
            self.current_options.append(cmd)
        
        # Mescola le opzioni
        random.shuffle(self.current_options)
        
        # Crea radio buttons
        for i, option in enumerate(self.current_options):
            radio = QRadioButton(f"{option}")
            radio.setFont(QFont("Courier", 10))
            self.options_group.addButton(radio, i)
            self.options_layout.addWidget(radio)
        
        # Abilita il pulsante rispondi
        self.answer_button.setEnabled(True)
        self.next_button.setEnabled(False)
        
        # Aggiorna UI
        self.update_ui()
        
    def check_answer(self):
        """Controlla la risposta selezionata"""
        selected_id = self.options_group.checkedId()
        
        if selected_id == -1:
            QMessageBox.warning(self, self.i18n.get_text("messages.select_answer"), 
                               self.i18n.get_text("messages.select_answer"))
            return
        
        selected_answer = self.current_options[selected_id]
        is_correct = selected_answer == self.correct_answer
        
        if is_correct:
            self.score += 1
            self.results_text.append(self.i18n.get_text("messages.correct_answer", 
                                                       command=self.correct_answer, 
                                                       description=self.vim_commands[self.correct_answer]))
        else:
            current_question_data = self.questions[self.current_question]
            self.wrong_answers.append({
                'question': self.current_question + 1,
                'correct': self.correct_answer,
                'selected': selected_answer,
                'description': self.vim_commands[self.correct_answer],
                'category': current_question_data.get('source_category', 'Unknown'),
                'difficulty': current_question_data.get('difficulty', 'beginner')
            })
            self.results_text.append(self.i18n.get_text("messages.wrong_answer", 
                                                       command=self.correct_answer, 
                                                       description=self.vim_commands[self.correct_answer]))
        
        # Disabilita il pulsante rispondi e abilita prossima domanda
        self.answer_button.setEnabled(False)
        self.next_button.setEnabled(True)
        
        # Aggiorna punteggio
        self.update_ui()
        
        # Evidenzia la risposta corretta
        for i, option in enumerate(self.current_options):
            radio = self.options_group.button(i)
            if option == self.correct_answer:
                radio.setStyleSheet("QRadioButton { color: green; font-weight: bold; }")
            elif option == selected_answer and not is_correct:
                radio.setStyleSheet("QRadioButton { color: red; font-weight: bold; }")
        
    def next_question(self):
        """Passa alla prossima domanda"""
        self.current_question += 1
        self.load_question()
        
    def restart_quiz(self):
        """Riavvia il quiz"""
        self.setup_quiz()
        self.results_text.clear()
        self.status_bar.showMessage(self.i18n.get_text("ui.status_quiz_restarted"))
        
    def update_ui(self):
        """Aggiorna l'interfaccia utente"""
        self.question_label.setText(self.i18n.get_text("quiz.question_label", 
                                                      current=self.current_question + 1, 
                                                      total=self.total_questions))
        self.score_label.setText(self.i18n.get_text("quiz.score_label", score=self.score))
        
        if self.total_questions > 0:
            progress = int((self.current_question / self.total_questions) * 100)
            self.progress_bar.setValue(progress)
        
    def show_final_results(self):
        """Mostra i risultati finali"""
        percentage = (self.score / self.total_questions) * 100
        
        if percentage == 100:
            message = self.i18n.get_text("messages.perfect_score")
        elif percentage >= 70:
            message = self.i18n.get_text("messages.excellent_work")
        elif percentage >= 50:
            message = self.i18n.get_text("messages.good_work")
        else:
            message = self.i18n.get_text("messages.review_commands")
        
        # Mostra risultati in una finestra
        results_dialog = QMessageBox(self)
        results_dialog.setWindowTitle(self.i18n.get_text("messages.quiz_completed"))
        results_dialog.setText(f"""
        <h2>{self.i18n.get_text('messages.quiz_completed')}</h2>
        <p><b>{self.i18n.get_text('messages.final_score')}</b> {self.score}/{self.total_questions}</p>
        <p><b>{self.i18n.get_text('messages.percentage')}</b> {percentage:.1f}%</p>
        <p><b>{self.i18n.get_text('messages.message')}</b> {message}</p>
        """)
        
        if self.wrong_answers:
            wrong_text = f"<h3>{self.i18n.get_text('messages.wrong_answers')}</h3><ul>"
            for wrong in self.wrong_answers:
                wrong_text += f"<li><b>{self.i18n.get_text('messages.question_number', number=wrong['question'])}</b> {wrong['description']}<br>"
                wrong_text += f"{self.i18n.get_text('messages.correct')} <span style='color: green'>{wrong['correct']}</span> | "
                wrong_text += f"{self.i18n.get_text('messages.selected')} <span style='color: red'>{wrong['selected']}</span><br>"
                if 'category' in wrong:
                    wrong_text += f"{self.i18n.get_text('messages.category')} {wrong['category']} | "
                if 'difficulty' in wrong:
                    wrong_text += f"{self.i18n.get_text('messages.difficulty')} {wrong['difficulty']}"
                wrong_text += "</li>"
            wrong_text += "</ul>"
            results_dialog.setDetailedText(wrong_text)
        
        results_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        results_dialog.exec()
        
        # Disabilita i pulsanti
        self.answer_button.setEnabled(False)
        self.next_button.setEnabled(False)
        
        self.status_bar.showMessage(self.i18n.get_text("ui.status_quiz_completed", 
                                                      score=self.score, total=self.total_questions))
    
    def show_statistics(self):
        """Mostra statistiche dettagliate sulle domande"""
        stats = self.questions_loader.get_statistics()
        
        stats_text = f"""
        <h2>{self.i18n.get_text('statistics.title')}</h2>
        <p><b>{self.i18n.get_text('statistics.total_questions')}</b> {stats['total_questions']}</p>
        <p><b>{self.i18n.get_text('statistics.total_categories')}</b> {stats['total_categories']}</p>
        
        <h3>{self.i18n.get_text('statistics.questions_by_category')}</h3>
        <ul>
        {''.join([f'<li><b>{cat}:</b> {self.i18n.get_text("statistics.questions_count", count=count)}</li>' for cat, count in stats['questions_by_category'].items()])}
        </ul>
        
        <h3>{self.i18n.get_text('statistics.questions_by_difficulty')}</h3>
        <ul>
        {''.join([f'<li><b>{diff}:</b> {self.i18n.get_text("statistics.questions_count", count=count)}</li>' for diff, count in stats['questions_by_difficulty'].items()])}
        </ul>
        
        <h3>{self.i18n.get_text('statistics.available_categories')}</h3>
        <ul>
        {''.join([f'<li>{cat}</li>' for cat in stats['categories']])}
        </ul>
        
        <h3>{self.i18n.get_text('statistics.available_difficulties')}</h3>
        <ul>
        {''.join([f'<li>{diff}</li>' for diff in stats['difficulties']])}
        </ul>
        """
        
        QMessageBox.about(self, self.i18n.get_text("statistics.title"), stats_text)
        
    def show_about(self):
        """Mostra informazioni sull'applicazione"""
        stats = self.questions_loader.get_statistics()
        QMessageBox.about(self, self.i18n.get_text("about.title"), f"""
        <h2>{self.i18n.get_text('app.title')}</h2>
        <p>{self.i18n.get_text('about.description')}</p>
        <p><b>{self.i18n.get_text('app.version')}</b> 4.0 (GUI Qt6 + Sistema Modulare + i18n)</p>
        <p><b>{self.i18n.get_text('statistics.total_questions')}</b> {stats['total_questions']} comandi Vim</p>
        <p><b>{self.i18n.get_text('statistics.total_categories')}</b> {stats['total_categories']}</p>
        <p><b>{self.i18n.get_text('about.features')}</b></p>
        <ul>
        <li>{self.i18n.get_text('about.feature_gui')}</li>
        <li>{self.i18n.get_text('about.feature_quiz')}</li>
        <li>{self.i18n.get_text('about.feature_filters')}</li>
        <li>{self.i18n.get_text('about.feature_score')}</li>
        <li>{self.i18n.get_text('about.feature_shuffle')}</li>
        <li>{self.i18n.get_text('about.feature_results')}</li>
        <li>{self.i18n.get_text('about.feature_modular')}</li>
        <li>{self.i18n.get_text('about.feature_control')}</li>
        </ul>
        <p><b>{self.i18n.get_text('about.developed_with')}</b> Python 3 + PyQt6</p>
        <p><b>{self.i18n.get_text('about.questions_by_category')}</b></p>
        <ul>
        {''.join([f'<li>{cat}: {count}</li>' for cat, count in stats['questions_by_category'].items()])}
        </ul>
        """)

def main():
    app = QApplication(sys.argv)
    
    # Imposta lo stile dell'applicazione
    app.setStyle('Fusion')
    
    # Crea e mostra la finestra principale
    window = VimQuizApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
