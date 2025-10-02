#!/usr/bin/env python3
"""
I18n Manager - Sistema di internazionalizzazione per VIM QUIZ
Gestisce le traduzioni per multiple lingue
"""

import json
import os
import locale
from typing import Dict, Any, Optional

class I18nManager:
    def __init__(self, locales_dir: str = "locales", default_language: str = "en"):
        """
        Inizializza il gestore delle traduzioni
        
        Args:
            locales_dir: Directory contenente i file di traduzione
            default_language: Lingua predefinita
        """
        self.locales_dir = locales_dir
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}
        self.supported_languages = []
        
        # Rileva la lingua di sistema
        self.system_language = self._detect_system_language()
        
        # Carica le lingue supportate
        self._load_supported_languages()
        
        # Carica le traduzioni
        self.load_translations(self.current_language)
    
    def _detect_system_language(self) -> str:
        """Rileva la lingua di sistema"""
        try:
            # Prova a ottenere la lingua di sistema
            system_locale = locale.getlocale()[0]
            if system_locale:
                # Estrai il codice lingua (es. 'it_IT' -> 'it')
                lang_code = system_locale.split('_')[0].lower()
                return lang_code
        except:
            pass
        
        # Fallback alla lingua predefinita
        return self.default_language
    
    def _load_supported_languages(self):
        """Carica le lingue supportate dalla directory"""
        if not os.path.exists(self.locales_dir):
            return
        
        for item in os.listdir(self.locales_dir):
            if os.path.isdir(os.path.join(self.locales_dir, item)):
                self.supported_languages.append(item)
        
        self.supported_languages.sort()
    
    def load_translations(self, language: str) -> bool:
        """
        Carica le traduzioni per una lingua specifica
        
        Args:
            language: Codice lingua (es. 'en', 'it', 'es')
            
        Returns:
            True se il caricamento è riuscito, False altrimenti
        """
        if language not in self.supported_languages:
            print(f"Lingua '{language}' non supportata. Usando '{self.default_language}'")
            language = self.default_language
        
        try:
            # Carica il file di traduzione principale
            main_file = os.path.join(self.locales_dir, language, "main.json")
            if os.path.exists(main_file):
                with open(main_file, 'r', encoding='utf-8') as f:
                    self.translations[language] = json.load(f)
            else:
                print(f"File di traduzione non trovato: {main_file}")
                return False
            
            # Carica le traduzioni delle domande
            questions_file = os.path.join(self.locales_dir, language, "questions.json")
            if os.path.exists(questions_file):
                with open(questions_file, 'r', encoding='utf-8') as f:
                    questions_translations = json.load(f)
                    if language not in self.translations:
                        self.translations[language] = {}
                    self.translations[language]['questions'] = questions_translations
            
            # Carica le traduzioni delle descrizioni delle domande
            descriptions_file = os.path.join(self.locales_dir, language, "question_descriptions.json")
            if os.path.exists(descriptions_file):
                with open(descriptions_file, 'r', encoding='utf-8') as f:
                    descriptions_translations = json.load(f)
                    if language not in self.translations:
                        self.translations[language] = {}
                    self.translations[language]['question_descriptions'] = descriptions_translations
            
            self.current_language = language
            print(f"Traduzioni caricate per la lingua: {language}")
            return True
            
        except Exception as e:
            print(f"Errore nel caricamento delle traduzioni per '{language}': {e}")
            return False
    
    def get_text(self, key: str, **kwargs) -> str:
        """
        Ottieni il testo tradotto per una chiave
        
        Args:
            key: Chiave del testo (es. 'app.title')
            **kwargs: Parametri per la formattazione del testo
            
        Returns:
            Testo tradotto o la chiave stessa se non trovata
        """
        if self.current_language not in self.translations:
            return key
        
        # Naviga nella struttura delle traduzioni
        keys = key.split('.')
        value = self.translations[self.current_language]
        
        try:
            for k in keys:
                value = value[k]
            
            # Se il valore è una stringa, formattala con i parametri
            if isinstance(value, str):
                return value.format(**kwargs) if kwargs else value
            else:
                return str(value)
                
        except (KeyError, TypeError):
            # Se non trovato, prova con la lingua predefinita
            if self.current_language != self.default_language:
                return self.get_text_fallback(key, **kwargs)
            return key
    
    def get_text_fallback(self, key: str, **kwargs) -> str:
        """Ottieni il testo dalla lingua predefinita come fallback"""
        if self.default_language not in self.translations:
            return key
        
        keys = key.split('.')
        value = self.translations[self.default_language]
        
        try:
            for k in keys:
                value = value[k]
            
            if isinstance(value, str):
                return value.format(**kwargs) if kwargs else value
            else:
                return str(value)
                
        except (KeyError, TypeError):
            return key
    
    def get_question_text(self, question_key: str, **kwargs) -> str:
        """Ottieni il testo tradotto per una domanda specifica"""
        return self.get_text(f"questions.{question_key}", **kwargs)
    
    def get_question_description(self, category: str, command: str) -> str:
        """Ottieni la descrizione tradotta per un comando specifico"""
        try:
            if (self.current_language in self.translations and 
                'question_descriptions' in self.translations[self.current_language] and
                category in self.translations[self.current_language]['question_descriptions'] and
                command in self.translations[self.current_language]['question_descriptions'][category]):
                return self.translations[self.current_language]['question_descriptions'][category][command]
        except (KeyError, TypeError):
            pass
        
        # Fallback alla lingua predefinita
        try:
            if ('question_descriptions' in self.translations[self.default_language] and
                category in self.translations[self.default_language]['question_descriptions'] and
                command in self.translations[self.default_language]['question_descriptions'][category]):
                return self.translations[self.default_language]['question_descriptions'][category][command]
        except (KeyError, TypeError):
            pass
        
        # Se non trovato, restituisci la chiave originale
        return command
    
    def get_supported_languages(self) -> list:
        """Ottieni la lista delle lingue supportate"""
        return self.supported_languages.copy()
    
    def get_current_language(self) -> str:
        """Ottieni la lingua corrente"""
        return self.current_language
    
    def set_language(self, language: str) -> bool:
        """
        Imposta la lingua corrente
        
        Args:
            language: Codice lingua
            
        Returns:
            True se l'impostazione è riuscita
        """
        if language in self.supported_languages:
            return self.load_translations(language)
        return False
    
    def get_language_name(self, language_code: str) -> str:
        """Ottieni il nome della lingua in quella lingua"""
        language_names = {
            'en': 'English',
            'it': 'Italiano',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch'
        }
        return language_names.get(language_code, language_code)
    
    def get_language_info(self) -> Dict[str, Any]:
        """Ottieni informazioni complete sulle lingue"""
        return {
            'current': self.current_language,
            'default': self.default_language,
            'system': self.system_language,
            'supported': self.supported_languages,
            'language_names': {code: self.get_language_name(code) for code in self.supported_languages}
        }

def main():
    """Funzione di test per il gestore i18n"""
    try:
        i18n = I18nManager()
        
        print("=== INFORMAZIONI I18N ===")
        info = i18n.get_language_info()
        print(f"Lingua corrente: {info['current']}")
        print(f"Lingua predefinita: {info['default']}")
        print(f"Lingua di sistema: {info['system']}")
        print(f"Lingue supportate: {info['supported']}")
        print()
        
        print("Nomi delle lingue:")
        for code, name in info['language_names'].items():
            print(f"  {code}: {name}")
        print()
        
        # Test traduzioni
        print("=== TEST TRADUZIONI ===")
        test_keys = [
            'app.title',
            'quiz.question_label',
            'quiz.score_label',
            'quiz.answer_button',
            'quiz.next_button'
        ]
        
        for key in test_keys:
            text = i18n.get_text(key)
            print(f"{key}: {text}")
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == '__main__':
    main()
