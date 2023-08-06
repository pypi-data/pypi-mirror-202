import tkinter as tk
import pandas as pd
from tkinter.filedialog import askopenfile, askopenfiles, asksaveasfile
from tkinter import ttk
from src import Final_Quiz, Final_Survey
#pip install ...
#from D2L import d2l

root = tk.Tk()
root.title('D2L API Test')
#root.iconbitmap('c:Users/cutepuppy.ico')  Here is a placeholder for an icon for our app

tabControl = ttk.Notebook(root)
tabControl.pack(pady=15)

quiz_tab = ttk.Frame(tabControl, width=500, height=500)
survey_tab = ttk.Frame(tabControl, width=500, height=500)

quiz_tab.pack(fill="both",expand=1)
survey_tab.pack(fill="both",expand=1)

tabControl.add(quiz_tab, text="Quiz Tab")
tabControl.add(survey_tab, text="Survey Tab")

def openfiles():
  browse_text.set("Loading...")
  files = askopenfiles(parent=root, mode='r', title="Choose files.", filetypes=(("CSV", "*.csv"),))
  if files is not None:
    #print(Final_Quiz.completeQuiz(files[0].name, files[1].name))
    quiz_res = Final_Quiz.completeQuiz(files[0].name, files[1].name)
    final_quiz = asksaveasfile(defaultextension='csv',filetypes=[("csv file",".csv"),("Excel file",".xlsx")])
    quiz_res.to_csv(final_quiz)
    final_quiz.close()
    print('File was sucessfully downloaded.')
  else:
    print('File was not selected or download was not successful.')
  return()

def openfile():
  browse_text.set("Loading...")
  file = askopenfile(parent=root, mode='r', title="Choose a file.", filetypes=(("CSV", "*.csv"),))
  if file is not None:
    #print(Final_Survey.completeSurvey(file.name))
    survey_res = Final_Survey.completeSurvey(file.name)
    final_survey = asksaveasfile(defaultextension='csv',filetypes=[("csv file",".csv"),("Excel file",".xlsx")])
    survey_res.to_csv(final_survey)
    final_survey.close()
    print('File was successfully downloaded.')
  else:
    print('File was not selected or download was not successful.') 
  return()

browse_text1 = tk.StringVar()  # Dealing with quiz data
browse_text1.set("Select quiz data files (QuestionDetail.csv and AttemptDetail.csv)")
browse_text2 = tk.StringVar()  # Dealing with survey data
browse_text2.set("Select survey data file")
browse_button1 = tk.Button(quiz_tab,textvariable=browse_text1,
 command=lambda:openfiles(),fg='#20bebe')
browse_button2 = tk.Button(survey_tab,textvariable=browse_text2, command=lambda:openfile())

download_text = tk.StringVar()
download_text.set("Download reformatted csv file")

button_quit1 = tk.Button(quiz_tab,text='Exit Program',command=root.quit, fg='#369110')
button_quit2 = tk.Button(survey_tab,text='Exit Program',command=root.quit, fg='#369110')

browse_button1.pack()
browse_button2.pack()
button_quit1.pack()
button_quit2.pack()
root.mainloop()

