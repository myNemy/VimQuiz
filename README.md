# VIM QUIZ - Interactive Quiz to Learn Vim Commands

> **⚠️ VibeCode Experiment** - This is an experimental project created with VibeCode AI assistance. It demonstrates advanced GUI development, i18n implementation, and modular architecture using Python and PyQt6.

A modern GUI application to learn Vim commands through an interactive quiz with modular question system.

## 🚀 Features

### Vim Quiz
- **Modern graphical interface** with Qt6
- **271+ Vim commands** organized in 10 categories
- **Modular system** for questions (separate JSON files)
- **Internationalization (i18n)** with support for 5 languages
- **Advanced filters** by category and difficulty
- **Interactive quiz** with multiple choice options
- **Real-time score tracking**
- **Question shuffling** capability
- **Question count control** (5-100)
- **Detailed results** with errors and explanations
- **Complete statistics** on questions
- **Intuitive and user-friendly** interface

### Question Editor
- **Complete graphical editor** for question management
- **Integrated i18n support** for all translations
- **Tabbed interface** to organize functionality
- **Complete CRUD operations** for questions
- **Advanced filters** by category, difficulty, and language
- **Auto-save** every 30 seconds
- **Real-time translation management**
- **Integrated data validation**
- **Automatic backup** of changes

## 📋 Requirements

- Python 3.6 or higher
- PyQt6
- Linux/Windows/macOS operating system

## 🛠️ Installation

### Vim Quiz
```bash
# Automatic script (recommended)
./vimquiz.sh

# Direct launch
python3 vimquiz.py
```

### Question Editor
```bash
# Automatic script (recommended)
./editor.sh

# Direct launch
python3 question_editor.py
```

### Manual Installation
```bash
# Install PyQt6
pip3 install PyQt6

# Launch applications
python3 vimquiz.py          # Main quiz
python3 question_editor.py  # Question editor
```

## 🎮 Usage

### Application Launch
```bash
# Method 1: Automatic script (recommended)
./vimquiz.sh

# Method 2: Direct launch
python3 vimquiz.py
```

**Main interface**:
- **Top panel**: Quiz information and progress
- **Center panel**: Question and answer options
- **Bottom panel**: Quiz controls
- **Side panel**: Real-time results

**Available controls**:
- **Answer**: Confirm selected answer
- **Next Question**: Move to next question
- **Restart Quiz**: Restart the quiz
- **Shuffle Questions**: Shuffle question order

## 📊 Included Vim Commands

The quiz includes **271+ Vim commands** organized in **10 categories**:

### Available Categories:
- **File Operations** (15 questions): `:w`, `:wq`, `:x`, `:q`, `:q!`, `:qa`, `ZZ`, `ZQ`, `:e`, `:r`, etc.
- **Basic Movement** (28 questions): `h`, `j`, `k`, `l`, `w`, `W`, `e`, `E`, `b`, `B`, `0`, `^`, `$`, `G`, etc.
- **Screen Movement** (14 questions): `Ctrl+u`, `Ctrl+b`, `Ctrl+d`, `Ctrl+f`, `zz`, `zt`, `zb`, etc.
- **Insert Mode** (14 questions): `i`, `I`, `a`, `A`, `o`, `O`, `ea`, `Esc`, `R`, `gI`, etc.
- **Editing** (42 questions): `r`, `J`, `cc`, `cw`, `c$`, `s`, `S`, `xp`, `u`, `Ctrl+r`, `.`, `ciw`, `diw`, etc.
- **Copy/Paste** (43 questions): `yy`, `2yy`, `yw`, `y$`, `p`, `P`, `dd`, `2dd`, `dw`, `D`, `d$`, `x`, etc.
- **Search and Replace** (31 questions): `*`, `/pattern`, `?pattern`, `n`, `N`, `:%s/old/new/g`, etc.
- **Visual Mode** (24 questions): `v`, `V`, `Ctrl+v`, `aw`, `as`, `ap`, `iw`, `is`, `ip`, etc.
- **Marks and Jumps** (25 questions): `ma`, `'a`, `''`, `Ctrl+o`, `Ctrl+i`, etc.
- **Macros** (35 questions): `qa`, `q`, `@a`, `@@`, `:reg`, `"ayy`, `"ap`, etc.

## 🎯 How It Works

1. **Question selection**: Application randomly selects a Vim command
2. **Option generation**: Creates 4 answer options (1 correct + 3 distractors)
3. **User answer**: User selects the answer they think is correct
4. **Evaluation**: Application evaluates the answer and updates the score
5. **Feedback**: Shows if the answer is correct or wrong with explanations
6. **Final results**: At the end shows complete statistics and errors

## 🔧 Customization

### Adding new commands
The modular system allows easy addition of new commands:

1. **Add to existing category**: Modify the JSON file in the `questions/` folder
2. **Create new category**: Create a new JSON file following the structure:

```json
{
  "category": "New Category",
  "description": "Category description",
  "difficulty": "beginner|intermediate|advanced",
  "questions": [
    {
      "command": "new_command",
      "description": "command description",
      "category": "subcategory"
    }
  ]
}
```

### Question file structure
Each JSON file in the `questions/` folder contains:
- `category`: Category name
- `description`: Category description
- `difficulty`: General difficulty level
- `questions`: Array of questions with:
  - `command`: Vim command
  - `description`: Command description
  - `category`: Subcategory (optional)

### Adding new languages
The i18n system easily supports adding new languages:

1. **Create new directory** in the `locales/` folder (e.g., `locales/pt/` for Portuguese)
2. **Copy translation files** from an existing language
3. **Translate contents** in `main.json` and `questions.json` files
4. **Restart application** - the new language will automatically appear in the selector

### Translation file structure
Each language has two JSON files:
- `main.json`: Main interface translations
- `questions.json`: Category and difficulty translations

### Modifying the interface
The interface is completely customizable by modifying the `init_ui()` and `create_menu_bar()` methods.

## 📁 File Structure

```
VIMQ/
├── vimquiz.py              # Python GUI application (PyQt6)
├── question_editor.py       # Question editor application
├── questions_loader.py      # Question loading system
├── i18n_manager.py         # Internationalization system
├── vimquiz.sh              # Automatic launch script
├── editor.sh               # Editor launch script
├── requirements.txt        # Python dependencies
├── README.md              # Main documentation
├── example_usage.md       # Usage guide
├── questions/             # Modular questions directory
│   ├── file_operations.json
│   ├── basic_movement.json
│   ├── screen_movement.json
│   ├── insert_mode.json
│   ├── editing.json
│   ├── copy_paste.json
│   ├── search_replace.json
│   ├── visual_mode.json
│   ├── marks_jumps.json
│   └── macros.json
└── locales/               # Translations directory
    ├── en/                # English (base language)
    │   ├── main.json
    │   ├── questions.json
    │   └── question_descriptions.json
    ├── it/                # Italian
    │   ├── main.json
    │   ├── questions.json
    │   └── question_descriptions.json
    ├── es/                # Spanish
    │   ├── main.json
    │   ├── questions.json
    │   └── question_descriptions.json
    ├── fr/                # French
    │   ├── main.json
    │   ├── questions.json
    │   └── question_descriptions.json
    └── de/                # German
        ├── main.json
        ├── questions.json
        └── question_descriptions.json
```

## 🐛 Troubleshooting

### PyQt6 won't install
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-pyqt6

# On Arch Linux
sudo pacman -S python-pyqt6

# Manual installation
pip3 install --user PyQt6
```

### Application won't start
```bash
# Check Python
python3 --version

# Check PyQt6
python3 -c "import PyQt6; print('PyQt6 installed correctly')"

# Launch with debug
python3 -v vimquiz.py
```

## 📝 Changelog

### Version 4.2 (Question Editor)
- ✅ Complete question editor GUI with PyQt6
- ✅ Full i18n integration for all interface elements
- ✅ CRUD operations for questions (Create, Read, Update, Delete)
- ✅ Real-time translation management
- ✅ Advanced filtering by category, difficulty, and language
- ✅ Auto-save functionality every 30 seconds
- ✅ Tabbed interface for organized editing
- ✅ Answer options management with checkboxes
- ✅ Integrated with existing i18n system

### Version 4.1 (Internationalization)
- ✅ Complete internationalization (i18n) system
- ✅ Support for 5 languages: English, Italian, Spanish, French, German
- ✅ Automatic system language detection
- ✅ Language selector in interface
- ✅ Complete translations for interface and questions
- ✅ Fallback system for missing translations
- ✅ Automatic tests for i18n system

### Version 4.0 (Modular System)
- ✅ Modular system for questions (separate JSON files)
- ✅ 271+ Vim commands organized in 10 categories
- ✅ Advanced filters by category and difficulty
- ✅ Question count control (5-100)
- ✅ Complete statistics on questions
- ✅ Dynamic loading system
- ✅ Improved interface with additional controls

### Version 3.0 (Qt6 GUI)
- ✅ Modern graphical interface with Qt6
- ✅ Interactive quiz with multiple choice
- ✅ Real-time score tracking
- ✅ Detailed results with errors
- ✅ Question shuffling capability
- ✅ Intuitive menus and controls

### Version 2.x (Terminal)
- Command line quiz
- Debug system
- Quiet and verbose modes

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is released under MIT license. See the LICENSE file for details.

## 🙏 Acknowledgments

- **Vim Community** for command documentation
- **Qt/PyQt** for the GUI framework
- **Python** for development simplicity
- **Cursor** for easy implementation
- **VibeCode** for AI assistance in development
---

**Happy Vim command learning!** 🎉