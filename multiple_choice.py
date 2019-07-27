#!/usr/bin/env python3

import sys
import os
import random
import argparse


class Application():

    
    def __init__(self):

        #=====================================================================================
        # Setup command line parameters
        # https://docs.python.org/3.7/library/argparse.html
        #=====================================================================================
        parser = argparse.ArgumentParser(description='Process file and output in valid format.')
        parser.add_argument('-m', '--max-answers', dest='maxAnswers', metavar='int', type=int, default=10,
                            help='maximum number of answers allowed (default: 10)')
        parser.add_argument('-i', '--input-file', dest='input', metavar='file', type=argparse.FileType('r'),
                            default='multiple_choice.txt', help='Input file (default: multiple_choice.txt)')
        parser.add_argument('-o', '--output-file', dest='output', metavar='file', type=argparse.FileType('w'),
                            default='multiple_choice_output.txt', help='Output file (default: multiple_choice_output.txt)')

        args = parser.parse_args()
        
        maxAnswers = args.maxAnswers
        ifh = args.input
        ofh = args.output


        #=====================================================================================
        # Detect orphan format characters and close program with an error message if found
        #=====================================================================================
        for line in ifh: # loop through each line
            if line.count('#') % 2 != 0: # if odd number of hashes exit with error
                print('Orphan \'#\' at line:\n' + line + '\n')
                exit()
        #=====================================================================================                

        ifh.seek(0)  # Rewind the file back to the start.

        # Read entire contents of file into "contents" variable
        contents = ifh.read()

        # Remove triple line characters (2 blank line separate questions)
        # TODO: Is this necessary?
        contents = contents.replace('\n\n\n', '')

        # Replace 4 spaces (code indentation in input file) with HTML spaces
        # TODO: Possibly not necessary. A more standard approach on all HTML might be better at
        # end of process? e.g. question 13
        contents = contents.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')

        
        #=====================================================================================
        # Convert all occurences of 'code' in between # symbols to use the Courier New font
        # This is done by replacing the first # with the opening span HTML tag
        # and the second # with the closing span HTML tag
        #=====================================================================================
        newContents = ''
        openFormat = True
        for c in contents: # loop through every character
            if (c == '#'): # find the hashes
                if openFormat: 
                    newContents = newContents + '<span style=\"font-family: \'Courier New\';\">'
                    openFormat = False
                else:
                    newContents = newContents + '</span>'
                    openFormat = True
            else:
                newContents = newContents + c

        contents = newContents
        #=====================================================================================

        # Split questions into an array (each element of array will contain the text for the question and the answers)
        questions = contents.split('Q-') # TODO: Possibly ensure first character of line? First line would need handling however

        # Remove first element as it will not be a question
        questions.pop(0) 

        print('Number of questions found: ' + str(len(questions)))

        count = 0
        # Loop through each question and process accordingly
        for q in questions:
            
            # Split each answer into an array element
            qa = q.split('\nA-')
            
            # Get text of question without the final new line character
            question = qa[0][0:-1]
            
            question = question.strip().replace('\n\r', '<br>').replace('\n', '<br>').replace('\r', '<br>')

            question = '<p style="font-size: medium;">' + question + '</p>'

            # Get the answers
            answers = qa[1:maxAnswers + 1]
            newAnswers = []  # List of 2-element lists, each element containing the answer and whether it is correct on not.

            # Start printing of quesiton to command line
            print('\nQUESTION: |' + question + '|')

            if len(answers) == 0:
                print('Error, question has no answers')
                exit() 

            # Loop through the answers
            for ai in range(len(answers)):

                # The first answer given is always the correct one
                correct = 'correct' if (ai == 0) else 'incorrect'


                # Format the answer
                newAnswer = '<span style="font-size: medium;">' + \
                    answers[ai].strip().replace('\n\r', '<br>').replace('\n', '<br>').replace('\r', '<br>') + \
                    '</span>'
                newAnswers.append(newAnswer + '\t' + correct)

                # Print the pre-shuffled answers
                print('ANSWER:   |' + newAnswer + '|')

            # Shuffle the answers into a random order
            random.shuffle(newAnswers)
            
            # Output question and answers to the file
            ofh.write('MC\t' + question + '\t' + '\t'.join(newAnswers) + '\n')

            count = count + 1

        print('\nTotal questions formed: ' + str(count))

        ifh.close()
        ofh.close()



applicationInstance = Application()