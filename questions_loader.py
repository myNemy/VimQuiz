#!/usr/bin/env python3
"""
Questions Loader - Sistema di caricamento dinamico delle domande Vim
Carica le domande dai file JSON organizzati per categoria
"""

import json
import os
import random
from typing import Dict, List, Any, Optional

class QuestionsLoader:
    def __init__(self, questions_dir: str = "questions", i18n_manager=None):
        """
        Inizializza il caricatore delle domande
        
        Args:
            questions_dir: Directory contenente i file delle domande
            i18n_manager: Gestore delle traduzioni (opzionale)
        """
        self.questions_dir = questions_dir
        self.i18n_manager = i18n_manager
        self.categories = {}
        self.all_questions = []
        self.load_all_questions()
    
    def load_all_questions(self):
        """Carica tutte le domande da tutti i file JSON"""
        if not os.path.exists(self.questions_dir):
            raise FileNotFoundError(f"Directory {self.questions_dir} non trovata")
        
        # Carica tutti i file JSON nella directory
        for filename in os.listdir(self.questions_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.questions_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        category_name = data.get('category', 'Unknown')
                        self.categories[category_name] = data
                        
                        # Aggiungi le domande alla lista generale
                        category_difficulty = data.get('difficulty', 'beginner')
                        for question in data.get('questions', []):
                            question['source_category'] = category_name
                            question['source_file'] = filename
                            question['difficulty'] = category_difficulty
                            self.all_questions.append(question)
                            
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Errore nel caricamento di {filename}: {e}")
                    continue
        
        print(f"Caricate {len(self.all_questions)} domande da {len(self.categories)} categorie")
    
    def get_questions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Ottieni tutte le domande di una categoria specifica
        
        Args:
            category: Nome della categoria
            
        Returns:
            Lista delle domande della categoria
        """
        if category not in self.categories:
            return []
        
        questions = self.categories[category].get('questions', [])
        return self.get_translated_questions(questions)
    
    def get_questions_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """
        Ottieni tutte le domande di una difficoltà specifica
        
        Args:
            difficulty: Livello di difficoltà (beginner, intermediate, advanced)
            
        Returns:
            Lista delle domande della difficoltà
        """
        questions = [q for q in self.all_questions if q.get('difficulty', 'beginner') == difficulty]
        return self.get_translated_questions(questions)
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """Ottieni tutte le domande"""
        return self.get_translated_questions(self.all_questions.copy())
    
    def get_translated_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ottieni le domande con le descrizioni tradotte"""
        if not self.i18n_manager:
            return questions
        
        # Mappa delle categorie per le chiavi di traduzione
        category_mapping = {
            "File Operations": "file_operations",
            "Basic Movement": "basic_movement",
            "Screen Movement": "screen_movement",
            "Insert Mode": "insert_mode",
            "Editing": "editing",
            "Visual Mode": "visual_mode",
            "Copy/Paste": "copy_paste",
            "Search and Replace": "search_replace",
            "Macros": "macros",
            "Marks and Jumps": "marks_jumps"
        }
        
        translated_questions = []
        for question in questions:
            translated_question = question.copy()
            category = question.get('source_category', 'File Operations')
            command = question.get('command', '')
            
            # Mappa la categoria per la traduzione
            translation_category = category_mapping.get(category, 'file_operations')
            
            # Ottieni la descrizione tradotta
            translated_description = self.i18n_manager.get_question_description(translation_category, command)
            # Se trovata una traduzione (non è uguale al comando originale)
            if translated_description and translated_description != command:
                translated_question['description'] = translated_description
            
            translated_questions.append(translated_question)
        
        return translated_questions
    
    def get_random_questions(self, count: int, category: Optional[str] = None, 
                           difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Ottieni un numero casuale di domande
        
        Args:
            count: Numero di domande da ottenere
            category: Categoria specifica (opzionale)
            difficulty: Difficoltà specifica (opzionale)
            
        Returns:
            Lista casuale di domande
        """
        questions = self.all_questions.copy()
        
        # Filtra per categoria se specificata
        if category:
            questions = [q for q in questions if q.get('source_category') == category]
        
        # Filtra per difficoltà se specificata
        if difficulty:
            questions = [q for q in questions if q.get('difficulty', 'beginner') == difficulty]
        
        # Mescola e prendi il numero richiesto
        random.shuffle(questions)
        selected_questions = questions[:count]
        return self.get_translated_questions(selected_questions)
    
    def get_categories(self) -> List[str]:
        """Ottieni la lista delle categorie disponibili"""
        return list(self.categories.keys())
    
    def get_difficulties(self) -> List[str]:
        """Ottieni la lista delle difficoltà disponibili"""
        difficulties = set()
        for question in self.all_questions:
            difficulties.add(question.get('difficulty', 'beginner'))
        return sorted(list(difficulties))
    
    def get_question_count_by_category(self) -> Dict[str, int]:
        """Ottieni il conteggio delle domande per categoria"""
        counts = {}
        for category, data in self.categories.items():
            counts[category] = len(data.get('questions', []))
        return counts
    
    def get_question_count_by_difficulty(self) -> Dict[str, int]:
        """Ottieni il conteggio delle domande per difficoltà"""
        counts = {}
        for question in self.all_questions:
            difficulty = question.get('difficulty', 'beginner')
            counts[difficulty] = counts.get(difficulty, 0) + 1
        return counts
    
    def search_questions(self, query: str) -> List[Dict[str, Any]]:
        """
        Cerca domande per comando o descrizione
        
        Args:
            query: Termine di ricerca
            
        Returns:
            Lista delle domande che corrispondono alla ricerca
        """
        query = query.lower()
        results = []
        
        for question in self.all_questions:
            command = question.get('command', '').lower()
            description = question.get('description', '').lower()
            
            if query in command or query in description:
                results.append(question)
        
        return results
    
    def get_question_by_command(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Ottieni una domanda specifica per comando
        
        Args:
            command: Comando Vim da cercare
            
        Returns:
            Dizionario della domanda o None se non trovata
        """
        for question in self.all_questions:
            if question.get('command') == command:
                return question
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Ottieni statistiche complete sulle domande"""
        return {
            'total_questions': len(self.all_questions),
            'total_categories': len(self.categories),
            'questions_by_category': self.get_question_count_by_category(),
            'questions_by_difficulty': self.get_question_count_by_difficulty(),
            'categories': self.get_categories(),
            'difficulties': self.get_difficulties()
        }

def main():
    """Funzione di test per il caricatore delle domande"""
    try:
        loader = QuestionsLoader()
        
        print("=== STATISTICHE DOMANDE ===")
        stats = loader.get_statistics()
        print(f"Totale domande: {stats['total_questions']}")
        print(f"Totale categorie: {stats['total_categories']}")
        print()
        
        print("Domande per categoria:")
        for category, count in stats['questions_by_category'].items():
            print(f"  {category}: {count}")
        print()
        
        print("Domande per difficoltà:")
        for difficulty, count in stats['questions_by_difficulty'].items():
            print(f"  {difficulty}: {count}")
        print()
        
        print("Categorie disponibili:")
        for category in stats['categories']:
            print(f"  - {category}")
        print()
        
        print("Difficoltà disponibili:")
        for difficulty in stats['difficulties']:
            print(f"  - {difficulty}")
        print()
        
        # Test ricerca
        print("=== TEST RICERCA ===")
        search_results = loader.search_questions("save")
        print(f"Risultati per 'save': {len(search_results)}")
        for result in search_results[:3]:  # Mostra solo i primi 3
            print(f"  {result['command']}: {result['description']}")
        print()
        
        # Test domande casuali
        print("=== TEST DOMANDE CASUALI ===")
        random_questions = loader.get_random_questions(5)
        print(f"5 domande casuali:")
        for q in random_questions:
            print(f"  {q['command']}: {q['description']}")
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == '__main__':
    main()
