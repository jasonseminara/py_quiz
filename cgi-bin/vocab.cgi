#!/usr/bin/python

# AUTHOR Jason Seminara
# 2015-11-22

import cgi, pdb,random,cgitb,sys

cgitb.enable()

f = open('/data/vocab.dat')

insertBreaks = lambda a,b: a+'<br>'+b
def showHeader(title): 
  return """
    <html>
      <head>
      <!-- Latest compiled and minified CSS -->
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">

      <body>
      <h2>{0}</h2>
    """.format(title)

def showFooter():
  return """
      </body>
    </html>
  """

def showOption(qName,qValue,qText):
  return """
  <div class="radio">
    <label>
        <input type="radio" name="q{0}" value="{1}">
        {2}
    </label>
  </div>
    """.format(qName,qValue,qText) 

def showInput(typ,clss,value,name):
  return """<input type="{0}" class="{1}" value="{2}" name={3}>""".format(typ,clss,value,name)
  


def gradeQuiz(frm):
  results={0:[],1:[]}
  print showHeader("Vocabulary Quiz Results")
 
  for qID in xrange(0,10):
    correct = frm.getvalue('a'+str(qID))==frm.getvalue('q'+str(qID))
    results[ int(correct) ].append(frm.getvalue('w'+str(qID)))
  
  print '<h4>You got '+str(len(results[1]))+' of '+ str(len(results[0])+len(results[1])) +' answers correct.</h4>'

  print '''
<div class="container row">
<table class="table" style="width:auto;">
  <tr>
    <th>Correct</th><th>Incorrect</th>
  </tr>
  <tr>
    <td class="success">{0}</td><td class="danger">{1}</td> 
  </tr>
</table>
</div>
'''.format( reduce(insertBreaks, results[1]),reduce(insertBreaks, results[0]) )
  print showFooter()


print "Content-Type: text/html\n\n"

form = cgi.FieldStorage()


# if the form was submitted, we should show them the results and die
if 'submitted' in form:
  gradeQuiz(form)
  sys.exit(0) 


# We haven't been here before


words = {}
questions =[]


# read the file, line-by-line
for word in f.readlines():

  # don't split lines that are empty
  if len(word)>1:
    #pdb.set_trace()
    # split the lines into three parts
    this_word,ty,definition = word.split("|")
    
    # init the words obj if we've never seen this word type before
    if ty not in words: 
      words[ty]=[]
   
    # add them to the words array, without the word-type
    words[ty].append((this_word,definition))
    #print('<li>'+this_word+'</li>')



# shuffle up the words
for kind in words:
  random.shuffle(words[kind])

# 40 random entries: 16 nouns (n), 
questions.extend(words['n.'][0:16])

# 12 verbs (v)
questions.extend(words['v.'][0:12])

# 12 adjectives (adj). 
questions.extend(words['adj.'][0:12])

#These words will be used to generate 4 noun questions, 3 verb questions and 3 adjective questions.



print showHeader("Vocabulary Quiz")
print """
    <form action="vocab.cgi" method="POST">
      <ol>
"""




# init the question ID
questionID = 0

# Walk over the questions by 4, choose a 
for answer in xrange(0,len(questions),4):
  answerID = random.randrange(0,4)
  currentWord = questions[answer+answerID][0]
  print "<li><strong>"+currentWord+"</strong>:<br>"
  print showInput('hidden','',str(answerID),'a'+str(questionID))
  print showInput('hidden','',currentWord  ,'w'+str(questionID))

  for offset in range(0,4):
    qID = answer+offset
    print showOption(str(questionID), str(offset), questions[qID][1]) 

  questionID+=1
  print '<br></li>'


print """
      </ol>
      <input name="submitted" type="submit" value="Grade" class="btn btn-primary btn-lg" >
"""

print showFooter()
