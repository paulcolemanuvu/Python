# Python

# Search Engine / Web Scraper

The Haystack.py contains a constructor that receives a URL and optional search depth (default 3 levels). The constructor then 'crawls' starting from the given web page, finding and following all embedded webpage links until it reaches the maximum searchdepth and computes the following data items:
    1. An indexthat maps every word encountered on each crawled page to a list of URLs of all the pages that contain that word. Only keeps  words consisting of runs of alphabetic characters and apostrophes. Converts all words to lower case. Only considers text that is found outside of HTML tags.
    
    2. A graph that maps every URL encountered to a list of the web pages it links to directly.
   
The lookup method takes a word as a search key and outputs the webpages that contain that word in rank order, highest to lowest, and displays results via pprint module to the console.  
