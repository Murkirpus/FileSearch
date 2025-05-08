import sys
import os
import re
import glob # Не используется напрямую, но может быть полезен для альтернативных реализаций
import datetime
import chardet
import subprocess # <<< ДОБАВЛЕНО
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
                            QFileDialog, QGroupBox, QMessageBox, QTabWidget, QSplitter,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QFont, QIcon, QTextCursor # QFont и QIcon не используются в текущей версии
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QTranslator, QLocale # QTranslator не используется

class LocalizedStrings:
    """Класс для локализации строк интерфейса."""

    def __init__(self):
        # Определение языка системы
        locale = QLocale.system().name()

        if locale.startswith("ru"):
            self.current_language = "ru"
        elif locale.startswith("uk"):
            self.current_language = "uk"
        else:
            self.current_language = "en"

        # Словари для локализации
        self.strings = {
            "en": {
                "ProgramTitle": "Text Search in Files Program",
                "ResultsFileName": "search_results",
                "ParamsError": "Error in parameters",
                "UseHelpParam": "Use /? parameter for help",
                "EnterFolderPath": "Enter the folder path for search",
                "FolderNotExist": "Folder does not exist!",
                "EnterFilePatterns": "Enter file patterns separated by semicolons (for example *.cs;*.txt)",
                "UsingDefaultPattern": "Default pattern will be used", # Не используется
                "EnterSearchText": "Enter text to search",
                "EmptySearchQuery": "Search query is empty!",
                "SearchInSubfolders": "Search in subfolders?", # Не используется напрямую в GUI как текст
                "CaseSensitive": "Case sensitive?", # Не используется напрямую в GUI как текст
                "EnterExcludeFolders": "Enter folders to exclude separated by semicolons (leave empty if not required)", # Не используется
                "ExcludedFolders": "Excluded folders",
                "SaveToDesktop": "Save results to desktop?", # Не используется
                "EnterResultFileName": "Enter file name for saving results", # Не используется
                "DefaultIs": "default is", # Не используется
                "ResultsSavedToDesktop": "Results will be saved to desktop in file",
                "ResultsSavedToFile": "Results will be saved to file",
                "SearchInProgress": "Searching",
                "SearchCompleted": "Search completed",
                "MatchesFound": "Matches found",
                "ResultsSavedToPath": "Results saved to file",
                "PressEnter": "Press Enter to exit", # Для консольной версии
                "SearchResults": "Search Results",
                "SearchFolder": "Search folder",
                "SearchQuery": "Search query",
                "RecursiveSearch": "Search in subfolders",
                "CaseSensitiveSearch": "Case sensitive search",
                "FilePatterns": "File patterns",
                "Yes": "Yes",
                "No": "No",
                "FilesFound": "Files found", # Используется в SearchWorker
                "UniqueFiles": "Total unique files", # Используется в SearchWorker
                "Results": "Results", # Используется в SearchWorker
                "FilesProcessed": "Files processed", # Используется в SearchWorker
                "ErrorReadingFile": "Error reading file", # Используется в SearchWorker
                "SearchError": "Search error", # Используется в SearchWorker
                "RepeatSearchCommand": "To repeat the search with the same parameters, use the command", # Для консольной версии
                "SearchDate": "Search date and time", # Используется в SearchWorker
                "FolderPath": "Folder Path",
                "Browse": "Browse...",
                "FilePattern": "File Pattern (*.txt;*.py;*.cs)",
                "SearchText": "Search Text",
                "SearchOptions": "Search Options", # Не используется, заменено на SearchParams
                "SubFolders": "Search in subfolders",
                "CaseSens": "Case sensitive",
                "SaveToDesktopOpt": "Save results to desktop",
                "ExcludeFolders": "Exclude folders (separated by semicolons)",
                "StartSearch": "Start Search",
                "SearchInfo": "Search Information",
                "ResultsTable": "Results Table", # Не используется как заголовок группы
                "FoundMatches": "Found Matches", # Используется как часть другой строки
                "SaveResults": "Save Results",
                "ResultsTab": "Results",
                "LogTab": "Log",
                "ClearResults": "Clear Results",
                "FileName": "File Name",
                "Line": "Line",
                "Content": "Content",
                "Status": "Status",
                "Ready": "Ready",
                "About": "About",
                "AboutText": "Text Search in Files Program\nVersion 1.0\n\nDeveloped with Python and PyQt6\n\nThis is a port of the original C# application.",
                "SearchingPattern": "Searching pattern", # Используется в SearchWorker
                "Of": "of", # Используется в SearchWorker
                # Строки для новой функциональности
                "ErrorOpenFileTitle": "Error Opening File",
                "ErrorOpenFileMsg": "Could not open file",
                "FileNotFoundTitle": "File Not Found",
                "FileNotFoundMsg": "The file path is invalid or the file does not exist",
                "AttemptingToOpenFile": "Attempting to open file"
            },
            "ru": {
                "ProgramTitle": "Программа поиска текста в файлах",
                "ResultsFileName": "результаты_поиска",
                "ParamsError": "Ошибка в параметрах",
                "UseHelpParam": "Используйте параметр /? для получения справки",
                "EnterFolderPath": "Введите путь к папке для поиска",
                "FolderNotExist": "Папка не существует!",
                "EnterFilePatterns": "Введите шаблоны файлов через точку с запятой (например *.cs;*.txt)",
                "UsingDefaultPattern": "Будет использован шаблон по умолчанию",
                "EnterSearchText": "Введите текст для поиска",
                "EmptySearchQuery": "Поисковый запрос пуст!",
                "SearchInSubfolders": "Искать в подпапках?",
                "CaseSensitive": "Учитывать регистр?",
                "EnterExcludeFolders": "Введите папки для исключения через точку с запятой (оставьте пустым, если не требуется)",
                "ExcludedFolders": "Исключенные папки",
                "SaveToDesktop": "Сохранить результаты на рабочий стол?",
                "EnterResultFileName": "Введите имя файла для сохранения результатов",
                "DefaultIs": "по умолчанию",
                "ResultsSavedToDesktop": "Результаты будут сохранены на рабочий стол в файл",
                "ResultsSavedToFile": "Результаты будут сохранены в файл",
                "SearchInProgress": "Идет поиск",
                "SearchCompleted": "Поиск завершен",
                "MatchesFound": "Найдено совпадений",
                "ResultsSavedToPath": "Результаты сохранены в файл",
                "PressEnter": "Нажмите Enter для выхода",
                "SearchResults": "Результаты поиска",
                "SearchFolder": "Папка поиска",
                "SearchQuery": "Поисковый запрос",
                "RecursiveSearch": "Поиск в подпапках",
                "CaseSensitiveSearch": "Учет регистра",
                "FilePatterns": "Шаблоны файлов",
                "Yes": "Да",
                "No": "Нет",
                "FilesFound": "Найдено файлов",
                "UniqueFiles": "Всего уникальных файлов",
                "Results": "Результаты",
                "FilesProcessed": "Обработано файлов",
                "ErrorReadingFile": "Ошибка при чтении файла",
                "SearchError": "Ошибка при поиске",
                "RepeatSearchCommand": "Для повторения поиска с теми же параметрами используйте команду",
                "SearchDate": "Дата и время поиска",
                "FolderPath": "Путь к папке",
                "Browse": "Обзор...",
                "FilePattern": "Шаблон файлов (*.txt;*.py;*.cs)",
                "SearchText": "Текст для поиска",
                "SearchOptions": "Параметры поиска",
                "SubFolders": "Искать в подпапках",
                "CaseSens": "Учитывать регистр",
                "SaveToDesktopOpt": "Сохранить результаты на рабочий стол",
                "ExcludeFolders": "Исключить папки (через точку с запятой)",
                "StartSearch": "Начать поиск",
                "SearchInfo": "Информация о поиске",
                "ResultsTable": "Таблица результатов",
                "FoundMatches": "Найденные совпадения",
                "SaveResults": "Сохранить результаты",
                "ResultsTab": "Результаты",
                "LogTab": "Журнал",
                "ClearResults": "Очистить результаты",
                "FileName": "Имя файла",
                "Line": "Строка",
                "Content": "Содержимое",
                "Status": "Статус",
                "Ready": "Готово",
                "About": "О программе",
                "AboutText": "Программа поиска текста в файлах\nВерсия 1.0\n\nРазработано на Python и PyQt6\n\nЭто порт оригинального приложения на C#.",
                "SearchingPattern": "Поиск по шаблону",
                "Of": "из",
                # Строки для новой функциональности
                "ErrorOpenFileTitle": "Ошибка открытия файла",
                "ErrorOpenFileMsg": "Не удалось открыть файл",
                "FileNotFoundTitle": "Файл не найден",
                "FileNotFoundMsg": "Путь к файлу недействителен или файл не существует",
                "AttemptingToOpenFile": "Попытка открыть файл"
            },
            "uk": {
                "ProgramTitle": "Програма пошуку тексту у файлах",
                "ResultsFileName": "результати_пошуку",
                "ParamsError": "Помилка в параметрах",
                "UseHelpParam": "Використовуйте параметр /? для отримання довідки",
                "EnterFolderPath": "Введіть шлях до папки для пошуку",
                "FolderNotExist": "Папка не існує!",
                "EnterFilePatterns": "Введіть шаблони файлів через крапку з комою (наприклад *.cs;*.txt)",
                "UsingDefaultPattern": "Буде використаний шаблон за замовчуванням",
                "EnterSearchText": "Введіть текст для пошуку",
                "EmptySearchQuery": "Пошуковий запит порожній!",
                "SearchInSubfolders": "Шукати в підпапках?",
                "CaseSensitive": "Враховувати регістр?",
                "EnterExcludeFolders": "Введіть папки для виключення через крапку з комою (залиште порожнім, якщо не потрібно)",
                "ExcludedFolders": "Виключені папки",
                "SaveToDesktop": "Зберегти результати на робочий стіл?",
                "EnterResultFileName": "Введіть ім'я файлу для збереження результатів",
                "DefaultIs": "за замовчуванням",
                "ResultsSavedToDesktop": "Результати будуть збережені на робочий стіл у файл",
                "ResultsSavedToFile": "Результати будуть збережені у файл",
                "SearchInProgress": "Йде пошук",
                "SearchCompleted": "Пошук завершено",
                "MatchesFound": "Знайдено збігів",
                "ResultsSavedToPath": "Результати збережені у файл",
                "PressEnter": "Натисніть Enter для виходу",
                "SearchResults": "Результати пошуку",
                "SearchFolder": "Папка пошуку",
                "SearchQuery": "Пошуковий запит",
                "RecursiveSearch": "Пошук у підпапках",
                "CaseSensitiveSearch": "Врахування регістру",
                "FilePatterns": "Шаблони файлів",
                "Yes": "Так",
                "No": "Ні",
                "FilesFound": "Знайдено файлів",
                "UniqueFiles": "Всього унікальних файлів",
                "Results": "Результати",
                "FilesProcessed": "Оброблено файлів",
                "ErrorReadingFile": "Помилка при читанні файлу",
                "SearchError": "Помилка при пошуку",
                "RepeatSearchCommand": "Для повторення пошуку з тими ж параметрами використовуйте команду",
                "SearchDate": "Дата і час пошуку",
                "FolderPath": "Шлях до папки",
                "Browse": "Огляд...",
                "FilePattern": "Шаблон файлів (*.txt;*.py;*.cs)",
                "SearchText": "Текст для пошуку",
                "SearchOptions": "Параметри пошуку",
                "SubFolders": "Шукати в підпапках",
                "CaseSens": "Враховувати регістр",
                "SaveToDesktopOpt": "Зберегти результати на робочий стіл",
                "ExcludeFolders": "Виключити папки (через крапку з комою)",
                "StartSearch": "Почати пошук",
                "SearchInfo": "Інформація про пошук",
                "ResultsTable": "Таблиця результатів",
                "FoundMatches": "Знайдені збіги",
                "SaveResults": "Зберегти результати",
                "ResultsTab": "Результати",
                "LogTab": "Журнал",
                "ClearResults": "Очистити результати",
                "FileName": "Ім'я файлу",
                "Line": "Рядок",
                "Content": "Вміст",
                "Status": "Статус",
                "Ready": "Готово",
                "About": "Про програму",
                "AboutText": "Програма пошуку тексту у файлах\nВерсія 1.0\n\nРозроблено на Python і PyQt6\n\nЦе порт оригінального додатку на C#.",
                "SearchingPattern": "Пошук за шаблоном",
                "Of": "з",
                # Строки для новой функциональности
                "ErrorOpenFileTitle": "Помилка відкриття файлу",
                "ErrorOpenFileMsg": "Не вдалося відкрити файл",
                "FileNotFoundTitle": "Файл не знайдено",
                "FileNotFoundMsg": "Шлях до файлу недійсний або файл не існує",
                "AttemptingToOpenFile": "Спроба відкрити файл"
            }
        }

    def get_string(self, key):
        """Получить локализованную строку по ключу."""
        try:
            return self.strings[self.current_language][key]
        except KeyError:
            # Если строка не найдена, возвращаем ключ или строку из английской локализации как fallback
            return self.strings["en"].get(key, key)


class SearchWorker(QThread):
    """Класс для выполнения поиска в отдельном потоке."""

    # Сигналы для обновления интерфейса
    update_log = pyqtSignal(str)
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int, int) # Не используется в GUI явно, но может быть полезен
    add_result = pyqtSignal(str, int, str)
    search_completed = pyqtSignal(int, str)

    def __init__(self, folder_path, file_patterns, search_text, recursive,
                 case_sensitive, exclude_folders, save_to_desktop, strings):
        super().__init__()
        self.folder_path = folder_path
        self.file_patterns = file_patterns
        self.search_text = search_text
        self.recursive = recursive
        self.case_sensitive = case_sensitive
        self.exclude_folders = exclude_folders
        self.save_to_desktop = save_to_desktop
        self.strings = strings
        self.result_file_path = ""
        self.running = True

    def run(self):
        """Выполняет поиск в файлах."""
        total_matches = 0
        processed_files = 0
        # Определение пути для сохранения результатов
        date_time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result_file_name = f"{self.strings.get_string('ResultsFileName')}_{date_time_str}.txt"

        try:
            # Пробуем несколько вариантов размещения файла
            if self.save_to_desktop:
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                if not os.path.exists(desktop_path):
                    desktop_path_ru = os.path.join(os.path.expanduser("~"), "Рабочий стол")
                    desktop_path_uk = os.path.join(os.path.expanduser("~"), "Робочий стіл")
                    if os.path.exists(desktop_path_ru):
                        desktop_path = desktop_path_ru
                    elif os.path.exists(desktop_path_uk):
                        desktop_path = desktop_path_uk
                    else: # Если не удалось найти рабочий стол, используем текущую директорию
                        desktop_path = os.getcwd()
                        self.update_log.emit(f"Не удалось найти рабочий стол, сохраняем в текущую директорию: {desktop_path}")

                result_file_path = os.path.join(desktop_path, result_file_name)
                try:
                    with open(result_file_path, 'w', encoding='utf-8') as test_file:
                        pass
                    self.update_log.emit(f"{self.strings.get_string('ResultsSavedToDesktop')}: {result_file_name} ({result_file_path})")
                except (IOError, PermissionError) as ex_perm:
                    self.update_log.emit(f"Ошибка прав доступа при сохранении на рабочий стол: {str(ex_perm)}. Пробуем текущую директорию.")
                    result_file_path = os.path.join(os.getcwd(), result_file_name) #Fallback to current dir
                    try:
                         with open(result_file_path, 'w', encoding='utf-8') as test_file:
                            pass
                         self.update_log.emit(f"{self.strings.get_string('ResultsSavedToFile')}: {result_file_path}")
                    except (IOError, PermissionError) as ex_cwd:
                        import tempfile
                        result_file_path = os.path.join(tempfile.gettempdir(), result_file_name)
                        self.update_log.emit(f"Ошибка прав доступа и в текущей директории: {str(ex_cwd)}. Используем временную директорию: {result_file_path}")


            else:
                try:
                    temp_path = os.path.join(os.getcwd(), result_file_name)
                    with open(temp_path, 'w', encoding='utf-8') as test_file:
                        pass
                    result_file_path = temp_path
                except (IOError, PermissionError):
                    import tempfile
                    result_file_path = os.path.join(tempfile.gettempdir(), result_file_name)
                    self.update_log.emit(f"Не удалось сохранить в текущую директорию, используем временную: {result_file_path}")
                self.update_log.emit(f"{self.strings.get_string('ResultsSavedToFile')}: {result_file_path}")

            self.result_file_path = os.path.abspath(result_file_path)

        except Exception as ex:
            import tempfile
            result_file_path = os.path.join(tempfile.gettempdir(), result_file_name)
            self.result_file_path = result_file_path
            self.update_log.emit(f"Ошибка при определении места для сохранения: {str(ex)}")
            self.update_log.emit(f"Используем временную директорию: {result_file_path}")

        try:
            with open(self.result_file_path, 'w', encoding='utf-8') as writer:
                writer.write(f"{self.strings.get_string('SearchResults')}\n")
                writer.write("=======================================\n")
                writer.write(f"{self.strings.get_string('SearchFolder')}: {self.folder_path}\n")
                writer.write(f"{self.strings.get_string('SearchQuery')}: \"{self.search_text}\"\n")
                writer.write(f"{self.strings.get_string('RecursiveSearch')}: {self.strings.get_string('Yes') if self.recursive else self.strings.get_string('No')}\n")
                writer.write(f"{self.strings.get_string('CaseSensitiveSearch')}: {self.strings.get_string('Yes') if self.case_sensitive else self.strings.get_string('No')}\n")
                writer.write(f"{self.strings.get_string('FilePatterns')}: {self.file_patterns}\n")

                if self.exclude_folders:
                    writer.write(f"{self.strings.get_string('ExcludedFolders')}: {self.exclude_folders}\n")

                writer.write("\n")
                writer.write("=======================================\n\n")
        except Exception as ex:
            self.update_log.emit(f"Ошибка при записи заголовка в файл результатов: {str(ex)}")
            self.running = False # Stop search if header cannot be written
            self.search_completed.emit(0, "")
            return


        all_files = []
        file_patterns_list = self.file_patterns.split(';')
        exclude_folders_list = [f.strip().lower() for f in self.exclude_folders.split(';') if f.strip()]

        for pattern in file_patterns_list:
            pattern = pattern.strip()
            if not pattern:
                continue

            msg_pattern = f"{self.strings.get_string('SearchingPattern')}: {pattern}"
            self.update_log.emit(msg_pattern)
            self.update_status.emit(msg_pattern)

            files_for_pattern = self._get_files_with_exclusions(
                self.folder_path, pattern, exclude_folders_list, self.recursive
            )

            msg_found = f"{self.strings.get_string('FilesFound')} ({pattern}): {len(files_for_pattern)}"
            self.update_log.emit(msg_found)

            all_files.extend(files_for_pattern)

        all_files = sorted(list(set(all_files))) # Sort for consistent processing order

        msg_unique = f"{self.strings.get_string('UniqueFiles')}: {len(all_files)}"
        self.update_log.emit(msg_unique)
        self.update_log.emit("")
        self.update_log.emit(f"{self.strings.get_string('Results')}:")
        self.update_log.emit("---------------------------------------")

        try:
            with open(self.result_file_path, 'a', encoding='utf-8') as writer:
                writer.write(f"{self.strings.get_string('UniqueFiles')}: {len(all_files)}\n\n")
                writer.write(f"{self.strings.get_string('Results')}:\n")
                writer.write("---------------------------------------\n")
        except Exception as ex:
             self.update_log.emit(f"Ошибка при записи в файл результатов (перед циклом файлов): {str(ex)}")


        for i, file_path in enumerate(all_files):
            if not self.running:
                break

            processed_files += 1
            if processed_files % 10 == 0 or processed_files == len(all_files): # Update more frequently
                msg_proc = f"{self.strings.get_string('ProcessedFiles')}: {processed_files} {self.strings.get_string('Of')} {len(all_files)}"
                self.update_log.emit(msg_proc)
                self.update_status.emit(msg_proc)
                self.update_progress.emit(processed_files, len(all_files))

            try:
                # Определение кодировки файла
                with open(file_path, 'rb') as fb:
                    raw_data = fb.read(2048) # Read more bytes for better detection
                detection = chardet.detect(raw_data)
                encoding = detection['encoding'] if detection['encoding'] else 'utf-8' # Fallback to utf-8
                confidence = detection['confidence']

                # self.update_log.emit(f"Detected encoding for {os.path.basename(file_path)}: {encoding} (Confidence: {confidence:.2f})")

                lines = []
                encodings_to_try = [encoding, 'utf-8', 'cp1251', 'windows-1251', 'latin-1']
                if encoding and encoding.lower() not in [e.lower() for e in encodings_to_try]:
                    encodings_to_try.insert(0, encoding)
                
                encodings_to_try = list(dict.fromkeys(e.lower() for e in encodings_to_try if e)) # Unique, preserve order, filter None

                file_decoded = False
                for enc in encodings_to_try:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            lines = f.readlines()
                        file_decoded = True
                        # self.update_log.emit(f"Successfully read {os.path.basename(file_path)} with {enc}")
                        break
                    except (UnicodeDecodeError, LookupError): # LookupError for unknown encodings
                        # self.update_log.emit(f"Failed to read {os.path.basename(file_path)} with {enc}")
                        continue
                
                if not file_decoded:
                    raise UnicodeDecodeError(f"Не удалось декодировать файл {file_path}, испробованы кодировки: {encodings_to_try}")


                for line_num, line_text in enumerate(lines, 1):
                    if not self.running: # Check running flag inside inner loop too
                        break
                    
                    match_found = False
                    if self.case_sensitive:
                        if self.search_text in line_text:
                            match_found = True
                    else:
                        if self.search_text.lower() in line_text.lower():
                            match_found = True

                    if match_found:
                        line_content = line_text.strip()
                        result_line_log = f"{file_path}({line_num}): {line_content}"

                        self.update_log.emit(result_line_log)
                        self.add_result.emit(file_path, line_num, line_content)

                        try:
                            with open(self.result_file_path, 'a', encoding='utf-8') as writer:
                                writer.write(result_line_log + "\n")
                        except Exception as ex_write:
                            self.update_log.emit(f"Ошибка при записи результата в файл: {str(ex_write)}")

                        total_matches += 1
            except Exception as ex_file:
                error_message = f"{self.strings.get_string('ErrorReadingFile')} {file_path}: {str(ex_file)}"
                self.update_log.emit(error_message)
                try:
                    with open(self.result_file_path, 'a', encoding='utf-8') as writer:
                        writer.write(error_message + "\n")
                except Exception as ex_write_err:
                    self.update_log.emit(f"Ошибка при записи ошибки чтения файла в файл результатов: {str(ex_write_err)}")


        summary = f"\n{self.strings.get_string('SearchCompleted')}. {self.strings.get_string('MatchesFound')}: {total_matches}"
        details = f"{self.strings.get_string('FilesProcessed')}: {processed_files}\n{self.strings.get_string('SearchDate')}: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        self.update_log.emit(summary)
        self.update_log.emit(details)

        try:
            with open(self.result_file_path, 'a', encoding='utf-8') as writer:
                writer.write("\n=======================================\n")
                writer.write(summary + "\n")
                writer.write(details + "\n")
        except Exception as ex_final:
            self.update_log.emit(f"Ошибка при записи итогов в файл результатов: {str(ex_final)}")

        self.search_completed.emit(total_matches, self.result_file_path if self.running else "")


    def stop(self):
        """Останавливает поиск."""
        self.running = False
        self.update_log.emit(self.strings.get_string("SearchStopped", "Search stopped by user."))


    def _get_files_with_exclusions(self, root_path, search_pattern, exclude_folders_lower, recursive):
        """Возвращает список файлов с исключением определенных папок."""
        result = []
        try:
            if not os.path.exists(root_path) or not os.path.isdir(root_path):
                return result

            # Функция для проверки, исключена ли папка
            def is_excluded(current_path_abs):
                current_path_lower = current_path_abs.lower()
                # Проверяем по полному пути и по имени папки
                path_parts = current_path_lower.split(os.sep)
                for excluded_folder_name in exclude_folders_lower:
                    # Если excluded_folder_name это полный путь
                    if os.path.abspath(excluded_folder_name) == current_path_lower:
                        return True
                    # Если excluded_folder_name это просто имя папки
                    if excluded_folder_name in path_parts:
                        return True
                return False

            for root, dirs, files in os.walk(root_path, topdown=True):
                # Удаляем исключенные папки из списка для обхода
                # Важно: dirs[:] изменяет список на месте
                original_dirs = list(dirs) # Копируем для итерации, так как dirs будет изменяться
                dirs[:] = [d for d in original_dirs if not is_excluded(os.path.abspath(os.path.join(root, d)))]

                for file_name in files:
                    if self._match_pattern(file_name, search_pattern):
                        result.append(os.path.join(root, file_name))

                if not recursive:
                    break
        except Exception as ex:
            self.update_log.emit(f"{self.strings.get_string('SearchError')} при обходе {root_path}: {str(ex)}")
        return result

    def _match_pattern(self, filename, pattern):
        """Проверяет соответствие имени файла шаблону (glob-like)."""
        # Простое сопоставление, можно улучшить с помощью fnmatch
        # Конвертирует шаблон glob в регулярное выражение
        # Экранируем специальные символы regex, кроме * и ?
        regex_pattern = pattern.replace('.', r'\.').replace('*', '.*').replace('?', '.')
        return re.fullmatch(f"^{regex_pattern}$", filename, re.IGNORECASE) is not None


class FileSearchApp(QMainWindow):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()

        self.strings = LocalizedStrings()
        self.settings = QSettings("MyFileSearch", "FileSearchApp") # Изменено имя компании для избежания конфликтов

        self.init_ui()
        self.load_settings()

        self.search_worker = None
        self.search_running = False
        self.result_file_path_from_worker = "" # Хранение пути к файлу результатов


    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle(self.strings.get_string("ProgramTitle"))
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        search_params_group = QGroupBox(self.strings.get_string("SearchParams")) # Используем добавленную строку
        search_params_layout = QVBoxLayout()

        folder_layout = QHBoxLayout()
        folder_label = QLabel(self.strings.get_string("FolderPath"))
        self.folder_edit = QLineEdit()
        browse_button = QPushButton(self.strings.get_string("Browse"))
        browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_edit, 1)
        folder_layout.addWidget(browse_button)
        search_params_layout.addLayout(folder_layout)

        pattern_layout = QHBoxLayout()
        pattern_label = QLabel(self.strings.get_string("FilePattern"))
        self.pattern_edit = QLineEdit()
        self.pattern_edit.setText("*.txt;*.py;*.cs;*.json;*.xml;*.html;*.css;*.js;*.log") # Расширенные шаблоны по умолчанию
        pattern_layout.addWidget(pattern_label)
        pattern_layout.addWidget(self.pattern_edit, 1)
        search_params_layout.addLayout(pattern_layout)

        search_text_layout = QHBoxLayout()
        search_text_label = QLabel(self.strings.get_string("SearchText"))
        self.search_text_edit = QLineEdit()
        search_text_layout.addWidget(search_text_label)
        search_text_layout.addWidget(self.search_text_edit, 1)
        search_params_layout.addLayout(search_text_layout)

        options_layout = QHBoxLayout()
        left_options = QVBoxLayout()
        self.recursive_check = QCheckBox(self.strings.get_string("SubFolders"))
        self.recursive_check.setChecked(True)
        self.case_sensitive_check = QCheckBox(self.strings.get_string("CaseSens"))
        self.save_desktop_check = QCheckBox(self.strings.get_string("SaveToDesktopOpt"))
        left_options.addWidget(self.recursive_check)
        left_options.addWidget(self.case_sensitive_check)
        left_options.addWidget(self.save_desktop_check)

        right_options = QVBoxLayout()
        exclude_label = QLabel(self.strings.get_string("ExcludeFolders"))
        self.exclude_edit = QLineEdit()
        self.exclude_edit.setPlaceholderText(".git;.svn;__pycache__;node_modules;build;dist") # Подсказка
        right_options.addWidget(exclude_label)
        right_options.addWidget(self.exclude_edit)
        right_options.addStretch()

        options_layout.addLayout(left_options)
        options_layout.addLayout(right_options)
        search_params_layout.addLayout(options_layout)

        buttons_layout = QHBoxLayout()
        self.search_button = QPushButton(self.strings.get_string("StartSearch"))
        self.search_button.clicked.connect(self.start_search)
        self.clear_button = QPushButton(self.strings.get_string("ClearResults"))
        self.clear_button.clicked.connect(self.clear_results_gui) # Переименован для ясности
        self.about_button = QPushButton(self.strings.get_string("About"))
        self.about_button.clicked.connect(self.show_about)

        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.about_button)
        search_params_layout.addLayout(buttons_layout)

        search_params_group.setLayout(search_params_layout)
        main_layout.addWidget(search_params_group)

        splitter = QSplitter(Qt.Orientation.Vertical)

        self.tab_widget = QTabWidget()

        self.results_table = QTableWidget(0, 3)
        self.results_table.setHorizontalHeaderLabels([
            self.strings.get_string("FileName"),
            self.strings.get_string("Line"),
            self.strings.get_string("Content")
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Запрет редактирования
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Выделение строк
        # >>> СОЕДИНЕНИЕ ДЛЯ ОТКРЫТИЯ ФАЙЛА <<<
        self.results_table.cellDoubleClicked.connect(self.open_file_from_table)


        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.tab_widget.addTab(self.results_table, self.strings.get_string("ResultsTab"))
        self.tab_widget.addTab(self.log_text, self.strings.get_string("LogTab"))

        info_group = QGroupBox(self.strings.get_string("SearchInfo"))
        info_layout = QVBoxLayout()

        info_text_layout = QHBoxLayout()
        self.total_matches_label = QLabel(f"{self.strings.get_string('MatchesFound')}: 0")
        self.status_label = QLabel(f"{self.strings.get_string('Status')}: {self.strings.get_string('Ready')}")
        info_text_layout.addWidget(self.total_matches_label)
        info_text_layout.addStretch()
        info_text_layout.addWidget(self.status_label)
        info_layout.addLayout(info_text_layout)

        save_results_layout = QHBoxLayout()
        self.save_results_button = QPushButton(self.strings.get_string("SaveResults"))
        self.save_results_button.clicked.connect(self.save_results_manually) # Переименован
        self.save_results_button.setEnabled(False)
        save_results_layout.addStretch()
        save_results_layout.addWidget(self.save_results_button)
        info_layout.addLayout(save_results_layout)

        info_group.setLayout(info_layout)

        splitter.addWidget(self.tab_widget)
        splitter.addWidget(info_group)
        splitter.setSizes([500, 120]) # Немного больше места для info_group
        main_layout.addWidget(splitter, 1)

        self.statusBar().showMessage(self.strings.get_string("Ready"))


    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.strings.get_string("EnterFolderPath"),
            self.folder_edit.text() or os.path.expanduser("~") # Начинаем с домашней папки если поле пустое
        )
        if folder:
            self.folder_edit.setText(folder)

    def start_search(self):
        if self.search_running: # Если поиск запущен, кнопка работает как "Стоп"
            self.stop_search()
            return

        folder_path = self.folder_edit.text().strip()
        if not folder_path:
            QMessageBox.warning(self, self.strings.get_string("ParamsError"), self.strings.get_string("EnterFolderPath"))
            return
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            QMessageBox.warning(self, self.strings.get_string("ParamsError"), self.strings.get_string("FolderNotExist"))
            return

        file_patterns = self.pattern_edit.text().strip()
        if not file_patterns: # Если пусто, используем значение по умолчанию (хотя оно уже установлено)
            file_patterns = "*.txt;*.py;*.cs;*.json;*.xml;*.html;*.css;*.js;*.log"
            self.pattern_edit.setText(file_patterns)

        search_text = self.search_text_edit.text() # Не .strip() чтобы искать пробелы по краям если надо
        if not search_text: # Пустой текст можно искать, это найдет все строки во всех файлах (если так задумано)
             reply = QMessageBox.question(self,
                                         self.strings.get_string("EmptySearchQueryTitle", "Empty Search Query"),
                                         self.strings.get_string("EmptySearchQueryMsg", "The search query is empty. Do you want to proceed and find all lines in matching files? This might take a long time and produce a very large result set."),
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
             if reply == QMessageBox.StandardButton.No:
                 return
        
        # Добавляем строки для пустого запроса в LocalizedStrings если нужно будет
        # "EmptySearchQueryTitle": "Empty Search Query",
        # "EmptySearchQueryMsg": "The search query is empty. Do you want to proceed...",


        self.save_settings()
        self.clear_results_gui() # Очищаем перед новым поиском
        self.tab_widget.setCurrentWidget(self.log_text) # Переключаемся на лог при старте

        self.search_button.setText(self.strings.get_string("StopSearch"))
        self.search_running = True
        self.save_results_button.setEnabled(False)
        self.result_file_path_from_worker = "" # Сбрасываем путь

        recursive = self.recursive_check.isChecked()
        case_sensitive = self.case_sensitive_check.isChecked()
        save_to_desktop = self.save_desktop_check.isChecked()
        exclude_folders = self.exclude_edit.text().strip()

        self.search_worker = SearchWorker(
            folder_path, file_patterns, search_text, recursive,
            case_sensitive, exclude_folders, save_to_desktop, self.strings
        )

        self.search_worker.update_log.connect(self.update_log)
        self.search_worker.update_status.connect(self.update_status)
        self.search_worker.update_progress.connect(self.update_progress_bar) # Подключаем к прогресс-бару
        self.search_worker.add_result.connect(self.add_result_to_table)
        self.search_worker.search_completed.connect(self.search_finished)
        
        self.search_worker.finished.connect(self.on_worker_finished) # Обработка фактического завершения потока

        self.search_worker.start()
        self.update_log(f"{self.strings.get_string('SearchInProgress')}...")
        self.update_status(f"{self.strings.get_string('SearchInProgress')}...")


    def stop_search(self):
        if self.search_worker and self.search_running:
            self.search_worker.stop()
            # Не меняем текст кнопки и search_running здесь, это произойдет в search_finished или on_worker_finished

    def on_worker_finished(self):
        """Срабатывает когда поток SearchWorker действительно завершил работу."""
        self.search_running = False
        self.search_button.setText(self.strings.get_string("StartSearch"))
        if not self.result_file_path_from_worker: # Если поиск был прерван до генерации файла
             self.update_status(self.strings.get_string("SearchStopped", "Search stopped"))
        # Если worker был остановлен принудительно, search_completed может не вызваться или вызваться с пустым путем
        # self.search_worker = None # Можно обнулить здесь


    def update_log(self, message):
        self.log_text.append(message)
        # self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum()) # Автопрокрутка
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)


    def update_status(self, message):
        self.statusBar().showMessage(message)
        self.status_label.setText(f"{self.strings.get_string('Status')}: {message}")

    def update_progress_bar(self, current, total):
        # Здесь можно было бы обновлять QProgressBar, если бы он был добавлен в GUI
        pass

    def add_result_to_table(self, file_path, line_num, content):
        row_count = self.results_table.rowCount()
        self.results_table.insertRow(row_count)

        file_name = os.path.basename(file_path)
        file_item = QTableWidgetItem(file_name)
        file_item.setToolTip(file_path) # Полный путь для открытия и подсказки

        # Выделяем найденный текст в строке (простой вариант)
        # content_item = QTableWidgetItem(content) # Заменено на QTextEdit для Rich Text
        
        self.results_table.setItem(row_count, 0, file_item)
        self.results_table.setItem(row_count, 1, QTableWidgetItem(str(line_num)))
        self.results_table.setItem(row_count, 2, QTableWidgetItem(content)) # Для простоты оставим QTableWidgetItem

        self.total_matches_label.setText(f"{self.strings.get_string('MatchesFound')}: {row_count + 1}")
        if row_count == 0: # Переключиться на вкладку результатов при первом совпадении
            self.tab_widget.setCurrentWidget(self.results_table)


    def search_finished(self, total_matches, result_file_path):
        """Обрабатывает сигнал search_completed от worker'а."""
        # Этот метод вызывается из потока worker'а, когда он считает поиск завершенным
        # (успешно или с ошибкой, или остановлен).
        # Фактическое завершение потока обрабатывается в on_worker_finished.

        self.result_file_path_from_worker = result_file_path # Сохраняем путь

        if total_matches > 0 and result_file_path: # Если есть результаты и путь к файлу
            self.save_results_button.setEnabled(True)
            # Переключаемся на вкладку результатов, если там еще не находимся
            if self.results_table.rowCount() > 0 and self.tab_widget.currentWidget() != self.results_table:
                 self.tab_widget.setCurrentWidget(self.results_table)

        completion_msg = f"{self.strings.get_string('SearchCompleted')}. {self.strings.get_string('MatchesFound')}: {total_matches}"
        if not self.search_worker.running and not result_file_path : # Если был остановлен и нет файла результатов
            completion_msg = self.strings.get_string("SearchStopped", "Search stopped by user")
        
        self.update_status(completion_msg)
        
        # search_running и текст кнопки лучше менять в on_worker_finished,
        # так как search_completed может прийти до фактического останова потока.


    def clear_results_gui(self):
        self.results_table.setRowCount(0)
        self.log_text.clear() # Очищаем и лог
        self.total_matches_label.setText(f"{self.strings.get_string('MatchesFound')}: 0")
        self.status_label.setText(f"{self.strings.get_string('Status')}: {self.strings.get_string('Ready')}")
        self.save_results_button.setEnabled(False)
        self.result_file_path_from_worker = ""


    def save_results_manually(self):
        if self.result_file_path_from_worker and os.path.exists(self.result_file_path_from_worker):
            default_filename = os.path.basename(self.result_file_path_from_worker)
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                self.strings.get_string("SaveResults"),
                os.path.join(os.path.expanduser("~"), default_filename), # Предлагаем сохранить в домашнюю папку
                self.strings.get_string("TextFilesFilter", "Text Files (*.txt);;All Files (*)")
            )
            # "TextFilesFilter": "Text Files (*.txt);;All Files (*)" - добавить в локализацию

            if save_path:
                try:
                    # Копируем файл
                    import shutil
                    shutil.copy2(self.result_file_path_from_worker, save_path)
                    QMessageBox.information(
                        self,
                        self.strings.get_string("SaveResults"),
                        f"{self.strings.get_string('ResultsSavedToPath')}: {save_path}"
                    )
                except Exception as ex:
                    QMessageBox.warning(
                        self,
                        self.strings.get_string("SaveResults"), # Можно заменить на "ErrorSavingResultsTitle"
                        f"{self.strings.get_string('ErrorSavingResults')}: {str(ex)}"
                    )
        else:
            QMessageBox.information(
                self,
                self.strings.get_string("SaveResults"),
                self.strings.get_string("NoResultsToSave", "No results file available to save.")
            )
            # "NoResultsToSave": "No results file available to save." - добавить в локализацию


    # >>> НОВЫЙ МЕТОД ДЛЯ ОТКРЫТИЯ ФАЙЛА <<<
    def open_file_from_table(self, row, column):
        """Открывает файл, указанный в ячейке таблицы результатов (по двойному клику)."""
        if column == 0: # Если клик на столбце "Имя файла"
            item = self.results_table.item(row, column)
            if item:
                file_path_from_tooltip = item.toolTip() # Полный путь хранится в подсказке
                if file_path_from_tooltip and os.path.exists(file_path_from_tooltip):
                    try:
                        normalized_path = os.path.normpath(file_path_from_tooltip)
                        self.update_log(f"{self.strings.get_string('AttemptingToOpenFile')}: {normalized_path}")
                        if sys.platform == "win32":
                            os.startfile(normalized_path)
                        elif sys.platform == "darwin":  # macOS
                            subprocess.call(["open", normalized_path])
                        else:  # Linux и другие UNIX-подобные
                            subprocess.call(["xdg-open", normalized_path])
                    except Exception as e:
                        error_msg = f"{self.strings.get_string('ErrorOpenFileMsg')}: {normalized_path}\n{str(e)}"
                        self.update_log(error_msg)
                        QMessageBox.warning(
                            self,
                            self.strings.get_string("ErrorOpenFileTitle"),
                            error_msg
                        )
                else:
                    error_msg = f"{self.strings.get_string('FileNotFoundMsg')}: {file_path_from_tooltip}"
                    self.update_log(error_msg)
                    QMessageBox.warning(
                        self,
                        self.strings.get_string("FileNotFoundTitle"),
                        error_msg
                    )

    def show_about(self):
        QMessageBox.about(
            self,
            self.strings.get_string("About"),
            self.strings.get_string("AboutText")
        )

    def save_settings(self):
        self.settings.setValue("folder_path", self.folder_edit.text())
        self.settings.setValue("file_patterns", self.pattern_edit.text())
        self.settings.setValue("search_text_history", self.search_text_edit.text()) # Сохраняем последний поисковый запрос
        self.settings.setValue("recursive", self.recursive_check.isChecked())
        self.settings.setValue("case_sensitive", self.case_sensitive_check.isChecked())
        self.settings.setValue("save_to_desktop", self.save_desktop_check.isChecked())
        self.settings.setValue("exclude_folders", self.exclude_edit.text())
        self.settings.setValue("geometry", self.saveGeometry()) # Сохраняем размер и положение окна


    def load_settings(self):
        self.folder_edit.setText(self.settings.value("folder_path", os.path.expanduser("~")))
        self.pattern_edit.setText(self.settings.value("file_patterns", "*.txt;*.py;*.cs;*.json;*.xml;*.html;*.css;*.js;*.log"))
        self.search_text_edit.setText(self.settings.value("search_text_history", ""))
        self.recursive_check.setChecked(self.settings.value("recursive", True, type=bool))
        self.case_sensitive_check.setChecked(self.settings.value("case_sensitive", False, type=bool))
        self.save_desktop_check.setChecked(self.settings.value("save_to_desktop", False, type=bool))
        self.exclude_edit.setText(self.settings.value("exclude_folders", ".git;.svn;__pycache__;node_modules;build;dist"))
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)


    def closeEvent(self, event):
        if self.search_running and self.search_worker:
            self.search_worker.stop() # Попытка остановить поток
            # Дать потоку немного времени на завершение?
            # self.search_worker.wait(1000) # Ожидать до 1 сек. (может заморозить GUI)

        self.save_settings()
        event.accept()


# Дополнительные строки для локализации, которые могли быть пропущены или используются в GUI
def add_missing_strings(strings_obj: LocalizedStrings):
    """Добавляет недостающие строки локализации."""
    missing = {
        "en": {
            "SearchParams": "Search Parameters",
            "StopSearch": "Stop Search",
            "SearchStopped": "Search stopped",
            "ErrorSavingResults": "Error saving results",
            "TextFilesFilter": "Text Files (*.txt);;All Files (*)",
            "NoResultsToSave": "No results file available to save.",
            "EmptySearchQueryTitle": "Empty Search Query",
            "EmptySearchQueryMsg": "The search query is empty. Do you want to proceed and find all lines in matching files?\nThis might take a long time and produce a very large result set.",

        },
        "ru": {
            "SearchParams": "Параметры поиска",
            "StopSearch": "Остановить поиск",
            "SearchStopped": "Поиск остановлен",
            "ErrorSavingResults": "Ошибка при сохранении результатов",
            "TextFilesFilter": "Текстовые файлы (*.txt);;Все файлы (*)",
            "NoResultsToSave": "Файл результатов для сохранения недоступен.",
            "EmptySearchQueryTitle": "Пустой поисковый запрос",
            "EmptySearchQueryMsg": "Поисковый запрос пуст. Вы хотите продолжить и найти все строки в соответствующих файлах?\nЭто может занять много времени и привести к очень большому набору результатов.",
        },
        "uk": {
            "SearchParams": "Параметри пошуку",
            "StopSearch": "Зупинити пошук",
            "SearchStopped": "Пошук зупинено",
            "ErrorSavingResults": "Помилка при збереженні результатів",
            "TextFilesFilter": "Текстові файли (*.txt);;Всі файли (*)",
            "NoResultsToSave": "Файл результатів для збереження недоступний.",
            "EmptySearchQueryTitle": "Порожній пошуковий запит",
            "EmptySearchQueryMsg": "Пошуковий запит порожній. Ви хочете продовжити та знайти всі рядки у відповідних файлах?\nЦе може зайняти багато часу та призвести до дуже великого набору результатів.",
        }
    }

    for lang, values in missing.items():
        if lang not in strings_obj.strings: # Если языка нет, добавляем его
            strings_obj.strings[lang] = {}
        for key, value in values.items():
            if key not in strings_obj.strings[lang]: # Добавляем только если ключ отсутствует
                strings_obj.strings[lang][key] = value

def main():
    """Главная функция программы."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    strings_instance = LocalizedStrings()
    add_missing_strings(strings_instance) # Убедимся, что все строки есть

    # Проверка прав на запись (опционально, т.к. worker уже пытается это делать)
    # test_file_path = os.path.join(os.getcwd(), "test_write_permission.tmp")
    # can_write_current_dir = True
    # try:
    #     with open(test_file_path, 'w') as f:
    #         f.write("test")
    #     os.remove(test_file_path)
    # except (IOError, PermissionError):
    #     can_write_current_dir = False
    #     # print("Предупреждение: нет прав на запись в текущую директорию.")
    #     # print("Результаты поиска могут быть сохранены во временную директорию, если другие опции не выбраны.")


    window = FileSearchApp() # strings_instance передается неявно через конструктор FileSearchApp
    window.show()

    # if not can_write_current_dir:
    #     QMessageBox.warning(
    #         window,
    #         strings_instance.get_string("WritePermissionWarningTitle", "Write Permission Warning"),
    #         strings_instance.get_string("WritePermissionWarningMsg",
    #             "The program may not have write permissions in the current directory.\n"
    #             "Search results might be saved to a temporary directory if other options are not selected or fail.\n"
    #             "Consider running as administrator or using the 'Save to Desktop' option if you encounter issues.")
    #     )
    #     # "WritePermissionWarningTitle": "Write Permission Warning",
    #     # "WritePermissionWarningMsg": "The program may not have write permissions..."

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
