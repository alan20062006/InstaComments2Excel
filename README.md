# Instagram Comments Scraper (fork)

Extract all comments from your desired Instagram post into an excel sheet and group them by providing an "groupings.xlsx" file that defines which words or sentences should be categorized 

## Changes from original
- No longer a need to specify how often to load any given post. It will now instead load all comments in the post
- All Replies will also be loaded
- Records more data to the excel sheet such as
  - Number of likes
  - Number of replies
  - Comment type (reply or main comment)
  - Comment ID (every main comment has a unique ID, but replies have the same as the main comment)
- The program runs headless now to reduce some minor load times
- It is now possible to group comments into categories using the `grouper.py` program
  - `grouper.py` requires an extra file called `groupings.xlsx` which defines the categories to group the comments by. 
  This file is very flexible and all that's needed is names for the categories as the first row and words/sentences for that category in the subsequent rows
- Lastly, the code/package structure has been changed. Some printouts have changed as well.

## Known issues
- When trying to scrape an Instagram post that is a video, main comments do not load
  - (possible fix) Change name of the button class to match the one on the video post. (this will however reverse the problem and make it so that picture posts   will not load anymore)


## Installation
1. Clone:

   `git clone https://github.com/jayveedee/InstaComments2Excel.git`
   
    
2. Create Virtual Environment (Recommended)<br/> 
    - `pip install virtualenv`
    - `virtualenv .venv`  
    
3. Activate the virtual environment
    - `source .venv/bin/activate`

4. Install dependencies
    - `pip install -r requirements.txt`

5. Install Firefox Web Driver (geckodriver)
    - Find the latest Firefox web driver on https://github.com/mozilla/geckodriver/releases <br />
    - Extract and move the binary to bin: `.venv/bin/`
    - Make it executable `chmod +x .venv/bin/geckodriver`

6. Run 
    
    - Instagram scraper
      - `python src/scraper.py 'URL'`
   
      Change the 'URL' with your desired instagram post target. <br/>
      For example : `python scraper.py https://www.instagram.com/p/CBHH2KjI6BW/` 
    
    - Comment categorizer
      - `python src/grouper.py`
      
      To add your own categories all you have to do is create an excel sheet called `groupings.xlsx` 
      where every row is a category with the defining words or sentences in each subsequent cell. 
      Save this file to the directory `src/data/groupings.xlsx`. 
      The first row **must** be the name of said category, the rest of words per column can be whatever 
      you want
      
7. Deactivate the virtual environment
    - `deactivate`

## License
This project is under the [MIT License](https://github.com/AgiMaulana/instagram-comments-scraper/blob/master/LICENSE.md)
