Saud Albuainain

IST-4320

CSUSB

December 9, 2024

Final Project - Build an App!

I wanted to create an app which can enable the user to consolidate their movie collection because the files can be spread out across different hard drives and directories on the computer. 
This app has really simple functionalities such as the ability to:
1.	Select a movie location (folder)
2.	Add additional location (folder)
3.	Finish and Save the Database to Excel file.
4.	Perform an OS search for files with file size greater than 700 MB.
5.	Show video files in a list with ability to play the movie. Adds ‘Play’ button.
6.	Load saved database to play movies from.
The code for the app is added in the Appendix.
The app should collect and save to database the following information:
1.	File name
2.	Path
3.	File Size (MB)
4.	Resolution
5.	Duration (minutes)
6.	Date added
Once the user specifies the directories where the movies are located using a location, plus additional locations, the app saves the information to the Excel database file. Showing the video files in the list produces a pop-up window from the database with the names of the files and information collected and a ‘Play’ button.

The GUI of the app looks like this:
  
To be able to run the app, the following modules are needed: tkinter, cv2, pandas.
I had to run a terminal commands to install these modueles, which are:
pip install pandas
pip install opencv-python openpyxl
Comments
I had to first identifies the modules to be used (os for OS commands), tkinter for GUI, cv2 for images, datetime for date and time, and pandas for data manipulation and analysis (reading and writing data for the spreadsheet and for data frame (2d table) .
For the classes, I set up the following: VideoFileScannerApp app gui, create_widgets for buttons and status label, add_directory, scan_videos (video data fetching and append), get_video_info (with parameters for width, height, resolution, frames, fps, duration – minutes and seconds), finish_and_save (appropriate message boxes included error messages, save path selection), search_large_videos (selecting a folder and specifying the file size over 700 Mb, plus the message box pop-up), show_video_list (to output the list of found videos or videos loaded from the database file), load_database, and play_video classes.  
I used a scrollable canvas and scrollbar using tk commands, populating the scrollable frame from the video list and a ‘Play’ button. The play functionality is realized via Windows startfile command or Linux/Mac subprocess.call command.
 Overall, this is an easy app with several functionalities which is a good practice for someone like me who is just learning Python, I am proud that I was able to produce such an app which is what I needed in real life – to consolidate my collection of movies in a database and also to play from the list within the app.
Of course, I will make efforts to improve the app such as making the executable (which I don’t have practice with and will need to use trial and error before I get it right). Also, I could try to make the integration of the app and executable with the default video program to play the files from within the app. Also, I would like to be able to edit the Excel database file and use the name of the movie (editable) instead of the file names.
