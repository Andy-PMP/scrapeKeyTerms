# Quantic Course Scraper

Extract **Key Terms** and **Assigned Readings** from Quantic course HTML files.

**Note:** The Python script is cross-platform (Windows, Mac, Linux). The `.bat` file is **Windows-specific only**.

## 📋 What It Does

This tool automatically extracts two things from your saved Quantic course pages:

1. **Key Terms** — All course terms with their definitions
2. **Assigned Readings** — All assigned readings organized by lesson with clickable links

Output is saved to a clean, readable `.txt` file organized by section.

---

## 🖥️ Setup (Works on Windows, Mac, Linux)

### Prerequisites

You need Python installed on your machine. If you don't have it:

1. **Download Python 3.8+** from [python.org](https://www.python.org/downloads/)
2. **During installation**: ✅ Check the box that says **"Add Python to PATH"** (Windows) or install to PATH (Mac/Linux)
3. **Click Install Now**

### Verify Python Installation

Open your terminal/command prompt and type:
```
python --version
```

You should see a version number like `Python 3.11.0`.

### Install Required Package

Open your terminal/command prompt and run:
```
pip install beautifulsoup4
```

This installs the HTML parser the script needs. You only need to do this once. ✅ This step is the **same on all platforms**.

---

## 🚀 How to Use

### Step 1: Save Course HTML from Quantic
1. Go to your Quantic course page in your browser
2. **Right-click** anywhere on the page
3. Select **"Save as..."**
4. Choose a folder where you want to organize your course materials
5. Save as **Webpage, Complete (*.htm, *.html)** (not "Webpage, HTML Only" or "Webpage, Single File")
   - For example: `YourCourseName.html`
   - ⚠️ **Important**: This should save the .html/.html file AND the _files folder that accompanies it
  
### Step 2: Run the Scraper
⚠️ **Important**: For all Options below, the `run_scraper_windows.bat`, `scrapeKeyTerms.py`, and `YourCourseName.html` files MUST be in the **same folder**

**Option A: Using the .bat file (Windows only) - Drag & Drop - Easiest for Windows users**
1. In Windows File Explorer, drag `YourCourseName.html` file onto `run_scraper_windows.bat` and drop it 
2. A Command Prompt window opens with a response explaining how many Key Terms and how many Assigned Readings were extracted - see Output Format section below. If the Command Prompt window disappears without pausing, an error occurred - see the Troubleshooting section below. 
3. In Windows File Explorer, you should now see `YourCourseName.txt` alongside the original `YourCourseName.html`

**Option B: Using the .bat file (Windows only) via Command Prompt**
1. **Double-click** `run_scraper_windows.bat`
2. A Command Prompt window opens
3. Type the filename: `YourCourseName.html` and press Enter

**Option C: Using Command Prompt / Terminal (Works on Windows, Mac, Linux)**
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to your folder:
   ```
   cd "path/to/your/course/folder"
   ```
   (Replace with your actual folder path)
3. Run:
   ```
   python scrapeKeyTerms.py YourCourseName.html
   ```

### Step 3: Get Your Output

The script creates a new file in the same folder:
- `YourCourseName.txt` ← Your extracted content!

---

## 📄 Output Format

The `.txt` file is organized in two sections:

```
KEY TERMS
==================================================

Term One
Definition of term one goes here, with clear explanation.

Term Two
Another term definition that explains the concept simply.

[more terms...]


ASSIGNED READINGS
==================================================

CHAPTER 1 | LESSON 1: FIRST LESSON TITLE
----------------------------------------
Reading Title Here | https://example-resource.org/article
Another Reading Title | https://another-resource.com/paper

CHAPTER 1 | LESSON 2: SECOND LESSON TITLE
----------------------------------------
Additional Reading Title | https://learning-resource.org/guide

[more readings...]
```

All URLs are clickable in most text editors. Open the file and Ctrl+Click to follow links!

---

## 🛡️ Security Features

The script includes built-in safety checks:

- ✅ Only processes `.html` files (blocks `.exe`, `.txt`, etc.)
- ✅ Works only in the script's folder (prevents accidental processing of random files)
- ✅ Rejects files larger than 50 MB
- ✅ Validates file encoding (UTF-8)

---

## ⚠️ Troubleshooting

### Windows-Specific Issues

**".bat file closes immediately"**
- An error occurred
- **Solution**: The `.bat` file should already have `pause` at the end to keep it open. If it closes too fast, add this line to the end of `run_scraper_windows.bat`:
  ```
  pause
  ```

**"Python is not recognized" (Command Prompt)**
- Python isn't in your PATH
- **Solution**: Uninstall Python, reinstall, and **check "Add Python to PATH"** during setup

### General Issues (All Platforms)

**"ModuleNotFoundError: No module named 'bs4'"**
- BeautifulSoup4 isn't installed
- **Solution**: Run `pip install beautifulsoup4` in Command Prompt / Terminal

**"File not found"**
- The `.html` file isn't in the same folder as the script
- **Solution**: Move your `.html` file to the same folder as the Python script

**"No valid terms were extracted"**
- The HTML file is corrupted or from the wrong page
- **Solution**: 
  - Save the page again from Quantic
  - Make sure you saved it as "HTML file", not "Web page, complete"

---

## 📂 File Organization (Recommended)

Keep everything organized:

```
YourFolder/
├── scrapeKeyTerms.py
├── run_scraper_windows.bat          (Windows only)
├── CourseName1.html
├── CourseName1.txt          (output)
├── CourseName2.html
└── CourseName2.txt          (output)
```

**Windows users:** All files in one folder = easy to run the `.bat` file!
**Mac/Linux users:** All files in one folder = easy to run from Terminal

---

## 💡 Tips

- **Batch processing**: Save multiple HTML files in the folder, then run the script multiple times (once per file)
- **Back up your files**: Keep a copy of original `.html` files in case you need to re-extract
- **Share the output**: The `.txt` file is plain text—share it via email, Notion, or anywhere

---

## 🔧 Advanced: Manual Command Line (All Platforms)

If you prefer Command Prompt / Terminal instead of the `.bat` file:

**Windows (Command Prompt):**
```batch
cd path\to\your\folder
python scrapeKeyTerms.py YourCourseName.html
```

**Mac/Linux (Terminal):**
```bash
cd path/to/your/folder
python3 scrapeKeyTerms.py YourCourseName.html
```

---

## ❓ Questions?

- **Issue not listed?** Check the error message carefully—it usually tells you what went wrong
- **File path issues?** Make sure your HTML file is in the same folder as the Python script
- **Still stuck?** Take a screenshot of the error and share it

---

## 📝 What Gets Extracted

✅ All key term definitions
✅ All assigned readings with URLs
✅ Lesson organization (Chapter/Lesson headers)
✅ Clickable links

❌ Videos or media
❌ Course text/lesson content (only key terms)
❌ Discussion forums or chat

---

**Version**: 2.0 (with Assigned Readings support)
**Last Updated**: June 2026
