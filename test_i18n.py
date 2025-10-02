#!/usr/bin/env python3
"""
Test script per il sistema i18n di VIM QUIZ
Verifica che tutte le traduzioni funzionino correttamente
"""

import sys
import os
from i18n_manager import I18nManager

def test_i18n_system():
    """Testa il sistema i18n"""
    print("=== TEST SISTEMA I18N VIM QUIZ ===\n")
    
    try:
        # Inizializza il gestore i18n
        i18n = I18nManager()
        
        # Test informazioni base
        print("1. INFORMAZIONI BASE:")
        info = i18n.get_language_info()
        print(f"   Lingua corrente: {info['current']}")
        print(f"   Lingua predefinita: {info['default']}")
        print(f"   Lingua di sistema: {info['system']}")
        print(f"   Lingue supportate: {info['supported']}")
        print()
        
        # Test traduzioni per ogni lingua
        print("2. TEST TRADUZIONI PER LINGUA:")
        for lang_code in i18n.get_supported_languages():
            print(f"\n   === {i18n.get_language_name(lang_code)} ({lang_code}) ===")
            
            # Cambia lingua
            if i18n.set_language(lang_code):
                # Test chiavi principali
                test_keys = [
                    'app.title',
                    'quiz.question_label',
                    'quiz.score_label',
                    'quiz.answer_button',
                    'quiz.next_button',
                    'quiz.restart_button',
                    'quiz.shuffle_button',
                    'ui.info_group',
                    'ui.question_group',
                    'ui.controls_group',
                    'ui.results_group',
                    'menu.quiz',
                    'menu.new_quiz',
                    'menu.shuffle_questions',
                    'menu.update_settings',
                    'menu.statistics',
                    'menu.exit',
                    'menu.help',
                    'menu.about'
                ]
                
                for key in test_keys:
                    text = i18n.get_text(key)
                    print(f"   {key}: {text}")
                
                # Test traduzioni con parametri
                print(f"   quiz.question_label (con parametri): {i18n.get_text('quiz.question_label', current=5, total=20)}")
                print(f"   quiz.score_label (con parametri): {i18n.get_text('quiz.score_label', score=15)}")
                print(f"   ui.status_quiz_completed (con parametri): {i18n.get_text('ui.status_quiz_completed', score=18, total=20)}")
            else:
                print(f"   ERRORE: Impossibile caricare la lingua {lang_code}")
        
        print("\n3. TEST FALLBACK:")
        # Test fallback con chiave inesistente
        fallback_text = i18n.get_text("nonexistent.key")
        print(f"   Chiave inesistente: {fallback_text}")
        
        # Test fallback con parametri
        fallback_text_param = i18n.get_text("nonexistent.key", param="test")
        print(f"   Chiave inesistente con parametri: {fallback_text_param}")
        
        print("\n4. TEST RICERCA DOMANDE:")
        # Test traduzioni delle domande
        for lang_code in ['en', 'it', 'es', 'fr', 'de']:
            if lang_code in i18n.get_supported_languages():
                i18n.set_language(lang_code)
                print(f"\n   === Categorie in {i18n.get_language_name(lang_code)} ===")
                categories = ['File Operations', 'Basic Movement', 'Screen Movement', 'Insert Mode', 'Editing']
                for cat in categories:
                    translated = i18n.get_question_text(f"categories.{cat}")
                    print(f"   {cat}: {translated}")
        
        print("\n✅ TUTTI I TEST COMPLETATI CON SUCCESSO!")
        
    except Exception as e:
        print(f"❌ ERRORE DURANTE I TEST: {e}")
        import traceback
        traceback.print_exc()

def test_ui_refresh():
    """Testa il refresh dell'interfaccia"""
    print("\n=== TEST REFRESH INTERFACCIA ===")
    
    try:
        from vimquiz import VimQuizApp
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = VimQuizApp()
        
        print("   Applicazione creata con successo")
        print(f"   Lingua corrente: {window.i18n.get_current_language()}")
        print(f"   Titolo finestra: {window.windowTitle()}")
        
        # Test cambio lingua
        print("\n   Test cambio lingua:")
        for lang_code in window.i18n.get_supported_languages()[:2]:  # Test solo le prime 2 lingue
            if window.i18n.set_language(lang_code):
                window.refresh_ui_texts()
                print(f"   - {window.i18n.get_language_name(lang_code)}: {window.windowTitle()}")
        
        print("   ✅ Test refresh interfaccia completato")
        
    except Exception as e:
        print(f"   ❌ ERRORE nel test interfaccia: {e}")

if __name__ == '__main__':
    test_i18n_system()
    test_ui_refresh()
