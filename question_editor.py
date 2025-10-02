#!/usr/bin/env python3
"""
VIM QUIZ - Question Editor
Editor per la modifica delle domande con supporto i18n completo
"""

import sys
import json
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QTextEdit, QComboBox, QPushButton, QTableWidget, 
                             QTableWidgetItem, QTabWidget, QGroupBox, QSplitter,
                             QMessageBox, QFileDialog, QHeaderView, QCheckBox,
                             QSpinBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

from i18n_manager import I18nManager
from questions_loader import QuestionsLoader


class QuestionEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.i18n = I18nManager()
        self.questions_loader = QuestionsLoader(i18n_manager=self.i18n)
        self.current_question = None
        self.current_category = None
        self.questions_data = {}
        self.modified = False
        
        self.init_ui()
        self.load_questions_data()
        self.refresh_ui_texts()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Auto-save ogni 30 secondi
        
    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        self.setWindowTitle("VIM QUIZ - Question Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter per dividere la finestra
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Pannello sinistro - Lista domande
        self.create_questions_panel(splitter)
        
        # Pannello destro - Editor domanda
        self.create_editor_panel(splitter)
        
        # Imposta proporzioni
        splitter.setSizes([400, 1000])
        
        # Barra di stato
        self.statusBar().showMessage(self.i18n.get_text("editor.messages.ready"))
        
        # Menu
        self.create_menu_bar()
        
    def create_questions_panel(self, parent):
        """Crea il pannello con la lista delle domande"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Titolo
        title = QLabel(self.i18n.get_text("editor.questions_panel.title"))
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Filtri
        filters_group = QGroupBox(self.i18n.get_text("editor.questions_panel.filters"))
        filters_layout = QVBoxLayout(filters_group)
        
        # Filtro per categoria
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("All")
        self.category_filter.currentTextChanged.connect(self.filter_questions)
        category_layout.addWidget(self.category_filter)
        filters_layout.addLayout(category_layout)
        
        # Filtro per difficoltà
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_filter = QComboBox()
        self.difficulty_filter.addItem("All")
        self.difficulty_filter.currentTextChanged.connect(self.filter_questions)
        difficulty_layout.addWidget(self.difficulty_filter)
        filters_layout.addLayout(difficulty_layout)
        
        # Filtro per lingua
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel("Language:"))
        self.language_filter = QComboBox()
        self.language_filter.addItem("All")
        for lang in self.i18n.get_supported_languages():
            self.language_filter.addItem(lang.upper())
        self.language_filter.currentTextChanged.connect(self.filter_questions)
        language_layout.addWidget(self.language_filter)
        filters_layout.addLayout(language_layout)
        
        layout.addWidget(filters_group)
        
        # Tabella domande
        self.questions_table = QTableWidget()
        self.questions_table.setColumnCount(4)
        self.questions_table.setHorizontalHeaderLabels(["Command", "Category", "Difficulty", "Language"])
        self.questions_table.horizontalHeader().setStretchLastSection(True)
        self.questions_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.questions_table.itemSelectionChanged.connect(self.on_question_selected)
        layout.addWidget(self.questions_table)
        
        # Pulsanti azione
        buttons_layout = QHBoxLayout()
        
        self.new_question_btn = QPushButton("New Question")
        self.new_question_btn.clicked.connect(self.new_question)
        buttons_layout.addWidget(self.new_question_btn)
        
        self.delete_question_btn = QPushButton("Delete Question")
        self.delete_question_btn.clicked.connect(self.delete_question)
        self.delete_question_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_question_btn)
        
        layout.addLayout(buttons_layout)
        
        parent.addWidget(panel)
        
    def create_editor_panel(self, parent):
        """Crea il pannello editor per la domanda selezionata"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Titolo
        title = QLabel("Question Editor")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Tab widget per diverse sezioni
        self.editor_tabs = QTabWidget()
        layout.addWidget(self.editor_tabs)
        
        # Tab Informazioni base
        self.create_basic_info_tab()
        
        # Tab Traduzioni
        self.create_translations_tab()
        
        # Tab Opzioni di risposta
        self.create_options_tab()
        
        # Pulsanti di salvataggio
        save_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Question")
        self.save_btn.clicked.connect(self.save_question)
        self.save_btn.setEnabled(False)
        save_layout.addWidget(self.save_btn)
        
        self.save_all_btn = QPushButton("Save All Changes")
        self.save_all_btn.clicked.connect(self.save_all_changes)
        save_layout.addWidget(self.save_all_btn)
        
        self.revert_btn = QPushButton("Revert Changes")
        self.revert_btn.clicked.connect(self.revert_changes)
        self.revert_btn.setEnabled(False)
        save_layout.addWidget(self.revert_btn)
        
        layout.addLayout(save_layout)
        
        parent.addWidget(panel)
        
    def create_basic_info_tab(self):
        """Crea il tab per le informazioni base della domanda"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Comando Vim
        command_layout = QHBoxLayout()
        command_layout.addWidget(QLabel("Vim Command:"))
        self.command_edit = QLineEdit()
        self.command_edit.textChanged.connect(self.mark_modified)
        command_layout.addWidget(self.command_edit)
        layout.addLayout(command_layout)
        
        # Categoria
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.currentTextChanged.connect(self.mark_modified)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        # Difficoltà
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["beginner", "intermediate", "advanced"])
        self.difficulty_combo.currentTextChanged.connect(self.mark_modified)
        difficulty_layout.addWidget(self.difficulty_combo)
        layout.addLayout(difficulty_layout)
        
        # Descrizione (inglese)
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("Description (English):"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.textChanged.connect(self.mark_modified)
        desc_layout.addWidget(self.description_edit)
        layout.addLayout(desc_layout)
        
        # Spiegazione
        explanation_layout = QVBoxLayout()
        explanation_layout.addWidget(QLabel("Explanation:"))
        self.explanation_edit = QTextEdit()
        self.explanation_edit.setMaximumHeight(100)
        self.explanation_edit.textChanged.connect(self.mark_modified)
        explanation_layout.addWidget(self.explanation_edit)
        layout.addLayout(explanation_layout)
        
        self.editor_tabs.addTab(tab, "Basic Info")
        
    def create_translations_tab(self):
        """Crea il tab per le traduzioni"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Scroll area per le traduzioni
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.translation_edits = {}
        
        for lang in self.i18n.get_supported_languages():
            lang_group = QGroupBox(f"Translation - {lang.upper()}")
            lang_layout = QVBoxLayout(lang_group)
            
            # Descrizione tradotta
            desc_label = QLabel("Description:")
            lang_layout.addWidget(desc_label)
            
            desc_edit = QTextEdit()
            desc_edit.setMaximumHeight(80)
            desc_edit.textChanged.connect(self.mark_modified)
            lang_layout.addWidget(desc_edit)
            
            self.translation_edits[f"{lang}_description"] = desc_edit
            
            scroll_layout.addWidget(lang_group)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        self.editor_tabs.addTab(tab, "Translations")
        
    def create_options_tab(self):
        """Crea il tab per le opzioni di risposta"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Opzioni di risposta
        options_group = QGroupBox("Answer Options")
        options_layout = QVBoxLayout(options_group)
        
        self.options_table = QTableWidget()
        self.options_table.setColumnCount(3)
        self.options_table.setHorizontalHeaderLabels(["Option", "Correct", "Explanation"])
        self.options_table.horizontalHeader().setStretchLastSection(True)
        self.options_table.setMaximumHeight(200)
        options_layout.addWidget(self.options_table)
        
        # Pulsanti per gestire le opzioni
        options_buttons = QHBoxLayout()
        
        add_option_btn = QPushButton("Add Option")
        add_option_btn.clicked.connect(self.add_option)
        options_buttons.addWidget(add_option_btn)
        
        remove_option_btn = QPushButton("Remove Option")
        remove_option_btn.clicked.connect(self.remove_option)
        options_buttons.addWidget(remove_option_btn)
        
        options_layout.addLayout(options_buttons)
        layout.addWidget(options_group)
        
        self.editor_tabs.addTab(tab, "Answer Options")
        
    def create_menu_bar(self):
        """Crea la barra del menu"""
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Question")
        new_action.triggered.connect(self.new_question)
        
        file_menu.addSeparator()
        
        save_action = file_menu.addAction("Save All")
        save_action.triggered.connect(self.save_all_changes)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Menu Language
        lang_menu = menubar.addMenu("Language")
        
        for lang in self.i18n.get_supported_languages():
            lang_action = lang_menu.addAction(lang.upper())
            lang_action.triggered.connect(lambda checked, l=lang: self.change_language(l))
        
        # Menu Help
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
    def load_questions_data(self):
        """Carica tutti i dati delle domande"""
        self.questions_data = {}
        
        # Carica tutte le categorie
        for category_file in Path("questions").glob("*.json"):
            with open(category_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                category_name = category_file.stem
                self.questions_data[category_name] = data
                
                # Aggiungi categoria al combo
                if category_name not in [self.category_filter.itemText(i) for i in range(self.category_filter.count())]:
                    self.category_filter.addItem(category_name)
                    self.category_combo.addItem(category_name)
        
        # Aggiungi difficoltà al filtro
        for difficulty in ["beginner", "intermediate", "advanced"]:
            if difficulty not in [self.difficulty_filter.itemText(i) for i in range(self.difficulty_filter.count())]:
                self.difficulty_filter.addItem(difficulty)
        
        self.populate_questions_table()
        
    def populate_questions_table(self):
        """Popola la tabella delle domande"""
        questions = []
        
        for category_name, category_data in self.questions_data.items():
            for question in category_data.get('questions', []):
                questions.append({
                    'command': question.get('command', ''),
                    'category': category_name,
                    'difficulty': category_data.get('difficulty', 'beginner'),
                    'question_data': question,
                    'category_data': category_data
                })
        
        self.questions_table.setRowCount(len(questions))
        
        for row, question in enumerate(questions):
            self.questions_table.setItem(row, 0, QTableWidgetItem(question['command']))
            self.questions_table.setItem(row, 1, QTableWidgetItem(question['category']))
            self.questions_table.setItem(row, 2, QTableWidgetItem(question['difficulty']))
            self.questions_table.setItem(row, 3, QTableWidgetItem("EN"))
            
        self.questions_table.resizeColumnsToContents()
        
    def filter_questions(self):
        """Filtra le domande in base ai criteri selezionati"""
        # Implementazione del filtro
        pass
        
    def on_question_selected(self):
        """Gestisce la selezione di una domanda"""
        current_row = self.questions_table.currentRow()
        if current_row >= 0:
            command = self.questions_table.item(current_row, 0).text()
            category = self.questions_table.item(current_row, 1).text()
            
            # Trova la domanda nei dati
            for cat_name, cat_data in self.questions_data.items():
                if cat_name == category:
                    for question in cat_data.get('questions', []):
                        if question.get('command') == command:
                            self.load_question_into_editor(question, cat_name, cat_data)
                            break
                    break
                    
            self.delete_question_btn.setEnabled(True)
        else:
            self.clear_editor()
            self.delete_question_btn.setEnabled(False)
            
    def load_question_into_editor(self, question, category, category_data):
        """Carica una domanda nell'editor"""
        self.current_question = question
        self.current_category = category
        
        # Informazioni base
        self.command_edit.setText(question.get('command', ''))
        self.category_combo.setCurrentText(category)
        self.difficulty_combo.setCurrentText(category_data.get('difficulty', 'beginner'))
        self.description_edit.setPlainText(question.get('description', ''))
        self.explanation_edit.setPlainText(question.get('explanation', ''))
        
        # Traduzioni
        for lang in self.i18n.get_supported_languages():
            if lang != 'en':  # Inglese è già nel campo description
                desc_key = f"{lang}_description"
                if desc_key in self.translation_edits:
                    translated_desc = self.i18n.get_question_description(question.get('command', ''), lang)
                    if translated_desc != question.get('command', ''):
                        self.translation_edits[desc_key].setPlainText(translated_desc)
                    else:
                        self.translation_edits[desc_key].setPlainText('')
        
        # Opzioni di risposta
        self.load_options_into_table(question.get('options', []))
        
        self.save_btn.setEnabled(True)
        self.revert_btn.setEnabled(True)
        
    def load_options_into_table(self, options):
        """Carica le opzioni nella tabella"""
        self.options_table.setRowCount(len(options))
        
        for row, option in enumerate(options):
            # Testo dell'opzione
            self.options_table.setItem(row, 0, QTableWidgetItem(option.get('text', '')))
            
            # Checkbox per corretta
            correct_checkbox = QCheckBox()
            correct_checkbox.setChecked(option.get('correct', False))
            correct_checkbox.stateChanged.connect(self.mark_modified)
            self.options_table.setCellWidget(row, 1, correct_checkbox)
            
            # Spiegazione
            self.options_table.setItem(row, 2, QTableWidgetItem(option.get('explanation', '')))
            
    def clear_editor(self):
        """Pulisce l'editor"""
        self.current_question = None
        self.current_category = None
        
        self.command_edit.clear()
        self.description_edit.clear()
        self.explanation_edit.clear()
        
        for edit in self.translation_edits.values():
            edit.clear()
            
        self.options_table.setRowCount(0)
        
        self.save_btn.setEnabled(False)
        self.revert_btn.setEnabled(False)
        
    def mark_modified(self):
        """Marca le modifiche come non salvate"""
        self.modified = True
        self.statusBar().showMessage("Modified - Save changes")
        
    def new_question(self):
        """Crea una nuova domanda"""
        self.clear_editor()
        self.current_question = {
            'command': '',
            'description': '',
            'explanation': '',
            'options': []
        }
        self.current_category = self.category_combo.currentText()
        self.save_btn.setEnabled(True)
        self.revert_btn.setEnabled(True)
        
    def delete_question(self):
        """Elimina la domanda selezionata"""
        if not self.current_question or not self.current_category:
            return
            
        reply = QMessageBox.question(self, "Delete Question", 
                                   "Are you sure you want to delete this question?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Rimuovi la domanda dai dati
            category_data = self.questions_data[self.current_category]
            if self.current_question in category_data.get('questions', []):
                category_data['questions'].remove(self.current_question)
                self.modified = True
                self.populate_questions_table()
                self.clear_editor()
                
    def add_option(self):
        """Aggiunge una nuova opzione di risposta"""
        row_count = self.options_table.rowCount()
        self.options_table.insertRow(row_count)
        
        # Checkbox per corretta
        correct_checkbox = QCheckBox()
        correct_checkbox.stateChanged.connect(self.mark_modified)
        self.options_table.setCellWidget(row_count, 1, correct_checkbox)
        
        self.mark_modified()
        
    def remove_option(self):
        """Rimuove l'opzione selezionata"""
        current_row = self.options_table.currentRow()
        if current_row >= 0:
            self.options_table.removeRow(current_row)
            self.mark_modified()
            
    def save_question(self):
        """Salva la domanda corrente"""
        if not self.current_question:
            return
            
        # Aggiorna i dati della domanda
        self.current_question['command'] = self.command_edit.text()
        self.current_question['description'] = self.description_edit.toPlainText()
        self.current_question['explanation'] = self.explanation_edit.toPlainText()
        
        # Aggiorna le opzioni
        options = []
        for row in range(self.options_table.rowCount()):
            option_text = self.options_table.item(row, 0).text() if self.options_table.item(row, 0) else ""
            correct = self.options_table.cellWidget(row, 1).isChecked()
            explanation = self.options_table.item(row, 2).text() if self.options_table.item(row, 2) else ""
            
            options.append({
                'text': option_text,
                'correct': correct,
                'explanation': explanation
            })
        self.current_question['options'] = options
        
        # Se è una nuova domanda, aggiungila alla categoria
        if self.current_question not in self.questions_data[self.current_category]['questions']:
            self.questions_data[self.current_category]['questions'].append(self.current_question)
            
        # Aggiorna la difficoltà della categoria se necessario
        new_difficulty = self.difficulty_combo.currentText()
        if self.questions_data[self.current_category]['difficulty'] != new_difficulty:
            self.questions_data[self.current_category]['difficulty'] = new_difficulty
            
        self.populate_questions_table()
        self.modified = False
        self.statusBar().showMessage("Question saved")
        
    def save_all_changes(self):
        """Salva tutte le modifiche nei file"""
        try:
            # Salva i file delle domande
            for category_name, category_data in self.questions_data.items():
                file_path = Path("questions") / f"{category_name}.json"
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(category_data, f, indent=2, ensure_ascii=False)
            
            # Salva le traduzioni
            self.save_translations()
            
            self.modified = False
            self.statusBar().showMessage("All changes saved")
            QMessageBox.information(self, "Success", "All changes have been saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {str(e)}")
            
    def save_translations(self):
        """Salva le traduzioni nei file appropriati"""
        for lang in self.i18n.get_supported_languages():
            if lang == 'en':
                continue
                
            translations = {}
            
            # Raccoglie tutte le traduzioni delle descrizioni
            for category_name, category_data in self.questions_data.items():
                for question in category_data.get('questions', []):
                    command = question.get('command', '')
                    if command:
                        # Cerca la traduzione nell'editor
                        desc_key = f"{lang}_description"
                        if desc_key in self.translation_edits:
                            translated_desc = self.translation_edits[desc_key].toPlainText()
                            if translated_desc.strip():
                                translations[command] = translated_desc
                                
            # Salva nel file delle traduzioni
            if translations:
                trans_file = Path("locales") / lang / "question_descriptions.json"
                trans_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(trans_file, 'w', encoding='utf-8') as f:
                    json.dump(translations, f, indent=2, ensure_ascii=False)
                    
    def revert_changes(self):
        """Ripristina le modifiche non salvate"""
        if self.current_question and self.current_category:
            self.load_question_into_editor(self.current_question, self.current_category, 
                                         self.questions_data[self.current_category])
        self.modified = False
        self.statusBar().showMessage("Changes reverted")
        
    def change_language(self, language):
        """Cambia la lingua dell'interfaccia"""
        self.i18n.set_language(language)
        self.refresh_ui_texts()
        
    def refresh_ui_texts(self):
        """Aggiorna tutti i testi dell'interfaccia"""
        # Aggiorna il titolo della finestra
        self.setWindowTitle(self.i18n.get_text("editor.title"))
        
        # Aggiorna i testi del pannello domande
        self.questions_table.setHorizontalHeaderLabels([
            self.i18n.get_text("editor.questions_panel.table_headers.command"),
            self.i18n.get_text("editor.questions_panel.table_headers.category"),
            self.i18n.get_text("editor.questions_panel.table_headers.difficulty"),
            self.i18n.get_text("editor.questions_panel.table_headers.language")
        ])
        
        # Aggiorna i pulsanti
        self.new_question_btn.setText(self.i18n.get_text("editor.questions_panel.new_question"))
        self.delete_question_btn.setText(self.i18n.get_text("editor.questions_panel.delete_question"))
        
        # Aggiorna i tab
        self.editor_tabs.setTabText(0, self.i18n.get_text("editor.editor_panel.basic_info"))
        self.editor_tabs.setTabText(1, self.i18n.get_text("editor.editor_panel.translations"))
        self.editor_tabs.setTabText(2, self.i18n.get_text("editor.editor_panel.answer_options"))
        
        # Aggiorna i pulsanti dell'editor
        self.save_btn.setText(self.i18n.get_text("editor.buttons.save_question"))
        self.save_all_btn.setText(self.i18n.get_text("editor.buttons.save_all"))
        self.revert_btn.setText(self.i18n.get_text("editor.buttons.revert"))
        
        # Aggiorna la barra di stato
        if not self.modified:
            self.statusBar().showMessage(self.i18n.get_text("editor.messages.ready"))
        
    def auto_save(self):
        """Salvataggio automatico"""
        if self.modified:
            self.save_all_changes()
            
    def show_about(self):
        """Mostra la finestra About"""
        QMessageBox.about(self, "About VIM QUIZ Editor", 
                         "VIM QUIZ Question Editor\n\n"
                         "A powerful tool for managing Vim quiz questions\n"
                         "with full i18n support.\n\n"
                         "Version 1.0")
        
    def closeEvent(self, event):
        """Gestisce la chiusura dell'applicazione"""
        if self.modified:
            reply = QMessageBox.question(self, "Unsaved Changes", 
                                       "You have unsaved changes. Do you want to save them?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No | 
                                       QMessageBox.StandardButton.Cancel)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_all_changes()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    
    # Imposta lo stile dell'applicazione
    app.setStyle('Fusion')
    
    # Crea e mostra la finestra principale
    window = QuestionEditor()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
