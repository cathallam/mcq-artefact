#!/usr/bin/env python3

import datetime
import sys
import os
import tkinter as tk 
import random

class Application () :
	 def __init__(self):
	 	self.infilename = 'phi_resit' # TODO: Pass the input filename as a COMMAND LINE PARAMETER
	 	self.outfilename = self.infilename + '_td.txt'
	 	self.infilename = self.infilename + '.txt'

	 	ifh = open (self.infilename, 'r')
	 	ofh = open (self.outfilename, 'w')

	 	#Detect orphan format characters
	 	for line in ifh: # loop through and READ every line of input file
	 		if line.count('#') % 2 !=0: # count number of occurences of # in the line
	 			print('Orphan \'#\' at line:\n' + line + 'n')
	 			exit()

	 			# Seek sets the file's current position at the offset. 
	 			ifh.seek(0)
	 			contents = ifh.read()
	 			contents = contents.replace('\n\n\n', '')
	 			content = content.replace('    ', '&nbsp;&nbsp;&nbsp;')

	 			newContents = ''
	 			openFormat = True
	 			for c in contents:
	 				if (c == '#') :
	 					if openFormat:
	 						newContents = newContents + '<span style=\"font-family: \'Helvetica\';\">'
	 						openFormat = False
	 					else:
						newContents = newContents + '</span>'
						openFormat = True
					else:
						newContents = newContents + c;

					contents = newContents

					questions = contents.split('Q-')
					questions.pop(0)
					print('Number of questions found: ' + str(len(questions)))

					#Split the string, using a dash, followed by a space, as a separator
					#The pop() method removes the element at the specified position - removes the first number 0

					count = 0
					for q in questions:
						qa = q.split('\nA-')

						question = qa[0] [0:-1]
						questionLines = question.split('\n')
						question = ''
						for ql in questionLines:
							question = question + '<p><span style="font-size:medium;">' + ql + '</span></p>'

							answers = qa[1:5]
							newAnswers = []
							#List of 2-element lists, each element containing the answer and whether it's correct or incorrect.

							for ai in range(len(answers)):
								if ai == 0:
									newAnswers.append(['<span style ="font-size: medium;">' + answers[ai].strip() + '</span>', 'correct'])
								else:
									newAnswers.append(['<span style="font-size: medium;">' + answers[ai].strip() + '</span>', 'incorrect'])
										answers = newAnswers

									#Print before shuffling
									print('QUESTION:\n|' + question + '|')
									for a in answers:
										print('ANSWER: |' + a[0] + a[0] + '|')

										random.shuffle(answers)

										ofh.write('MC\t' + question + '\t' 
											+ answers[0][0] + '\t' 
											+ answers[0][1] + '\t' 
											+ answers[1][0] + '\t' 
											+ answers[1][1] + '\t' 
											+ answers[2][0] + '\t' 
											+ answers[2][1] + '\t' 
											+ answers[3][0] + '\t' 
											+ answers[3][1] + '\n')

										count = count + 1

									print('\nTotal questions formed: ' + str(count))

									ifh.close()
									ofh.close()

								applicationInstance = Application()



