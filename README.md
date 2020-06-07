# Instagram Comments Scraper


## Installation
1. Clone:
    `git clone git@github.com:AgiMaulana/Instagram-Comments-Scraper.git`<br/>
    or `git clone https://github.com/AgiMaulana/Instagram-Comments-Scraper.git` <br/>
    or download the [zip](https://github.com/AgiMaulana/Instagram-Comments-Scraper/archive/master.zip)
2. Create Virtual Environment (Recommended)<br/> 
    - `pip install virtualenv`
    - `virtualenv .venv`  

3. Install dependencies
    - `pip install -r requirements.txt`

4. Install Chrome Web Driver

    `wget https://chromedriver.storage.googleapis.com/x.xx/chromedriver_linux64.zip` <br>
    See the latest Chrome web driver on https://sites.google.com/a/chromium.org/chromedriver/downloads <br /> <br />
    
    Extract and move the binary to bin: `unzip chromedriver_linux64.zip -d .venv/bin/`
    
    Make it executable `chmod +x .venv/bin/chromedriver`


## Run
`python scraper.py post-url total-load-more-click`

Change the URL with your post target <br />
Example : <br />
`python scraper.py https://www.instagram.com/p/BqUfulwH6O4/ 5`

## License
This project is under the [MIT License](https://github.com/AgiMaulana/instagram-comments-scraper/blob/master/LICENSE.md)
