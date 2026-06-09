# scrapeKeyTerms

Extracts key terms from Quantic course pages

**Why**  
*One cannot simply copy and paste the key terms from the Quantic course pages.*

I was inspecting element to copy them individually, and decided I didn't want to do that for 13 months.

**What**  
This script pulls key terms and definitions from the Quantic course pages so you don't have to.

**How**
1. Navigate to a Quantic course page with Key Terms
2. Save the page as an HTML file **in the same directory as your python script**.
3. Run the python script
4. When prompted, input the full file name
  
The script will create a .txt file of the same name as your HTML, with the key terms and definitions extracted cleanly.

**Packages needed**    
pathlib    
beautifulsoup4    
