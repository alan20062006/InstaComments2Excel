# Instagram Comments Scraper (fork)

Extract all comments from your desired Instagram post into an excel sheet

## Changes from original
- No longer a need to specify how often to load any given post. It will now instead load all comments in the post
- All Replies will also be loaded
- Records more data to the excel sheet such as
  - Number of likes
  - Number of replies
  - Comment type (reply or main comment)
  - Comment ID (evry main comment has a unique ID, but replies have the same as the main comment)
- The program runs headless now to reduce some minor load times
- Lastly, the code structure has been changed. Some printouts have changed as well.


## Installation
1. Clone:

   `git clone https://github.com/jayveedee/Instagram-Comments-Scraper.git`
   
    
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
    - `python scraper.py 'URL'`
   
    Change the 'URL' with your desired instagram post target. <br/>
    For example : `python scraper.py https://www.instagram.com/p/CBHH2KjI6BW/` 
 
7. Deactivate the virtual environment
    - `deactivate`

## License
This project is under the [MIT License](https://github.com/AgiMaulana/instagram-comments-scraper/blob/master/LICENSE.md)
