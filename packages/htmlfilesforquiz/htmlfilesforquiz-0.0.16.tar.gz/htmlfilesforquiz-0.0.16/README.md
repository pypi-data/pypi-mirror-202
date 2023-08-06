# htmlfilesforquiz

## What is it?

htmlfilesforquiz is a package that generates question papers as HTML files to be distributed over the network and grades the answers in text files submitted by students.

## Help
<ul>
<li><a href="https://github.com/generateNscore/htmlfilesforquiz/wiki">Documentation</a></li>
</ul>

## Features
<ul>
<li>Generates as many personalized question sheets in HTML files as one wants with a few strings of text.</li>
<li>The amount of random personalization is under total control of users.</li>
<li>Each HTML file with a name corresponding to the identification number.</li>
<li>Multi-choice as well as short, default, questions can be made.</li>
<li>A figure, although a pre-made image can be used, can be varied as well as questions.</li>
<li>Mathematical equations can be included in questions with Latex.</li>
<li>User defined functions can be used.</li>
<li>With the question sheets in HTML files, students require only a web browser to answer and send text files including the answers over the network.</li>
<li>Scoring all different answers in text files submitted can be done in a second.</li>
</ul>

## Where to get it
<ul>
<li>The source code is currently hosted on GitHub at: <a href="https://github.com/generateNscore/htmlfilesforquiz">https://github.com/generateNscore/htmlfilesforquiz</a></li>
<br>

<pre lang=sh>pip install htmlfilesforquiz</pre>

</ul>


## Dependencies
<ul><li>None</li></ul>


## Changes

<li>Version 0.0.16</li>

<ul><li>In addition to typical short-answer questions that can be answered on the screen, a new kind questions for which students are required to "play" with mouse to complete a required task to answer is added.</li>
<li>Example: <a href="https://generateNscore.github.io/htmlfilesforquiz/Examples/Ex004/Ex004.py">Ex004.py</a></li>
</ul></ul>
<br>

<li>Version 0.0.11</li>

<ul><li>A way to stay in short-answer question is added as:</li>
  
  ```python
  
answer = [{'choices':None, 'ans': ans}]
  
  ```

  <ul><li>This answering form is different from the one of</li>
  
  ```python
  
  answer = [{'choices':None, 'ans':vA+vB, 'fn': 'variation0_int'}]
  
  ```
  <ul><li> This is about <a href="https://github.com/generateNscore/htmlfilesforquiz/wiki#2-specifying-method-of-converting-a-short-answer-to-a-set-of-choices">Specifying method of convering short-answer to a set of choices.</a></li></ul></ul>





## Example shots
<li>A short-answer question</li>
<img src="https://generateNscore.github.io/htmlfilesforquiz/img/example1-3.png">
<li>A multiple-choice question</li>
<img src="https://generateNscore.github.io/htmlfilesforquiz/img/example1-6.png">
<li>A multiple-choice question with a figure</li>
<img src="https://generateNscore.github.io/htmlfilesforquiz/img/example1-2.png">
<li>A question with multiple-choice figures</li>
<img src="https://generateNscore.github.io/htmlfilesforquiz/img/example1-1.png">
<li>A question with equation and with multiple-choices</li>
<img src="https://generateNscore.github.io/htmlfilesforquiz/img/example1-4.png">
<li>A question with equation and with multiple-choice figures</li>
<img src="https://generateNscore.github.io/htmlfilesforquiz/img/example1-5.png">
