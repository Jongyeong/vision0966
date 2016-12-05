# vision0966

Jongyeong LEE 2014170966 EE, Korea University for ENGINEERING DESIGN Ⅰ -software course. <br>
It was completed at July, 2016.

  # Introduction <br>
  If we input 'word' or 'ID', this code will collect pictures from twitter and analyze which brands appear in them.<br>
  Actually, at first time, I want to use 'Instagram', however, I cannot get permission to use Instagram code.<br>
  So, pictures are based on twitter. It means lack of accuracy.<br>
  If possible, it is better to use pictures from Instgram.<br><br>
  
  # How to use <br>
  Word : Analyze photos from twits which contain specific "word".<br>
  ID   : Analyze photos twitted by that person(ID).<br>
  Results will be Pie Chart made by Pygal.<br>
  <br>
  # Flow <br>
  input -> request to find picture from Twitter -> bring pictures' url list -> send url to Google Cloud Vision <br>
  -> receive result -> show the result with a pi graph
  
  <br>
  Using Google Cloud Platform, App engine (Using PyCharm) and based on Flask<br>
  Because it uses server of Google, it is possible to access from other computers.<br>
  Also, it looks like doing well only in "Chrome" (only english)<br>
  In processing, there are 'A / B', A means # of success of analyzing requested pictures.<br>
  So, it does not count when request is fail.(not accepted)<br>
  It works well. But, if there are a lot of twitts, it might make errors because it takes more than 60 seconds.<br>
  In case of Google App Engine, it is possible to handle same request at the same time in different server. <br>
  It means that different servers save only their 'own' results. To deal with this problem, there might be two simple ways. <br> 
  One is using Data Base(DB), and the other is using memcahce provided by Google Cloud Platform.<br>
  I use that memcache to save the overall results instead of using DB.<br>
  
  
  # I Used - <br>
  Python27(Pycharm), Flask, Google Cloud vision, Google Cloud Platform, Twitter, jQuery <br>
  And several lib including Pygal <br> 
  
  <b> All html files have to be in 'templates' folder which locates same folder of main code. </b>
    
    
