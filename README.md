# vision0966

Korea univ. EE 2014170966   July/2016
for ENGINEERING DESIGN Ⅰ -software course. 

  # Introduction
  If we input 'word' or 'ID', this code will collect pictures from twitter and analyze which brands appear in them.
  Actually, at first time, I want to use 'Instagram', however, I cannot get permission to use Instagram code.
  So, pictures are based on twitter. It means lack of accuracy.
  If possible, I think it is more accurate to use pictures from Instgram.
  
  # How to use 
  Word : Analyze photos from twits which contain specific "word".
  ID   : Analyze photos twitted by that person(ID).
  Results will be Pie Chart made by Pygal.
  
  
  Using Google Cloud Platform, App engine (Using PyCharm) and based on Flask
  Because it uses server of Google, it is possible to access from other computers.
  Also, it looks like doing well only in "Chrome" (only english)
  In processing, there are 'A / B', A means # of success of analyzing requested pictures.
  So, it does not count when request is fail.(not accepted)
  It works well. But, if there are a lot of twits, it might result in errors because it takes more than 60 seconds.
  In case of Google App Engine, it is possible to handle same request at the same time in different server, I use memcache to save the     result instead of DB.
           
  Google cloud system offers memcache.
  
  
  # Used things.
  Python27(Pycharm), Flask, Google Cloud vision, Google Cloud Platform, Twitter, jQuery
    
    
