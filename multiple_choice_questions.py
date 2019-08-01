#!/usr/bin/env python3

import sys
import os
import random
import argparse
import markdown2          # Install using  "pip install markdown2"
import AdvancedHTMLParser # Install using  "pip install AdvancedHTMLParser"

#================================================================================================================================
# Question class
# Holds the questions and answers data and methods to format the output
#================================================================================================================================
class Question():
    def __init__(self, questionType, questionText):
        self.__questionType = questionType
        self.__questionText = questionText
        self.__answers = []

    # Return a string for the full question and answers
    def getFormattedQuestion(self):
        prefix = self.__getQuestionPrefix()

        if prefix == "TF":
            # Output true or false question
            return "\t".join([prefix, self.__getFormmattedLines(self.__questionText), self.__getTrueOrFalseText()])
        else:
            # Output multiple choice/answer question
            return "\t".join([prefix, self.__getFormmattedLines(self.__questionText), self.__getFormattedAnswers()])

    # Build string to be output to command line
    def outputToTerminal(self):
        prefix = self.__getQuestionPrefix()

        output = "QUESTION "

        if prefix == "TF":
            questionType = "(" + self.__getTrueOrFalseText() + ")"
        elif prefix == "MC":
            questionType = "(Multiple Choice)"
        elif prefix == "MA":
            questionType = "(Multiple Answers)"

        output = output + questionType + ': ' + self.__questionText

        for answer in self.__answers:
            output = output + "ANSWER (" + self.__getCorrectText(answer[1]) + "): " + answer[0]
        print(output)

    # Add a new answer
    def addAnswer(self, line, correct):
        self.__answers.append([line, correct])

    # Add a line of text to the correct location
    def addLine(self, line):
        if self.__hasAnswers() == True:
            # Will be a line for the last answer
            self.__addAnswerLine(line)
        else:
            # Will be a line for the question
            self.__addQuestionLine(line)

    # Add a line of text to the question text
    def __addQuestionLine(self, line):
        self.__questionText = self.__questionText + line

    # Add a line of text to the last answer
    def __addAnswerLine(self, line):
        self.__answers[-1][0] = self.__answers[-1][0] + line

    # Randomize the order of the answers
    def __getShuffledAnswers(self):
        shuffled = self.__answers.copy()
        random.shuffle(shuffled)
        return shuffled

    # Check if there are any answers
    def __hasAnswers(self):
        return len(self.__answers) > 0

    # Count the number of correct answers
    def __countCorrectAnswers(self):
        correctCount = 0
        for answer in self.__answers:
            if answer[1] == True:
                correctCount += 1
        return correctCount

    # Determine the code for the question type
    def __getQuestionPrefix(self):
        noCorrectAnswers = self.__countCorrectAnswers()
        if self.__questionType in ["QT", "QF"]:
            if self.__hasAnswers() == True:
                print("Error: True or False question does not require answers. Question: " + self.__questionText)
                exit()
            return "TF"
        elif self.__questionType == "Q":
            if self.__hasAnswers() == False:
                print("Error: Multiple choice question has no answers. Question: " + self.__questionText)
                exit()
            elif noCorrectAnswers == 0:
                print("Error: Question has no correct answers. Question: " + self.__questionText)
                exit()
            elif noCorrectAnswers > 1:
                return "MA"
            else:
                return "MC"
        else:
            print("Error: Invalid question type. Question: " + self.__questionText)
            exit()

    # Format the content of the question or answer block using markdown formatter (to convert markdown to HTML) and html parser (to add extras)
    # Uses markdown2 https://github.com/trentm/python-markdown2
    # Uses AdvancedHTMLParser https://pypi.org/project/AdvancedHTMLParser/
    def __getFormmattedLines(self, lines):
        HTML_LINEBREAK = "<br>"
        html = markdown2.markdown(lines, extras={"break-on-newline": True, "fenced-code-blocks": True, "code-friendly": True, "tables": True})

        # Add style to the code blocks so code is displayed fixed width
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(html)

        # Add stlye for <code> tags
        codeElements = parser.getElementsByTagName("code")
        for element in codeElements:
            element.setStyle("font-family", "Courier New")

        # Add stlye for <table>, <td> and <th> tags
        tableElements = parser.getElementsByTagName("table")
        thElements = parser.getElementsByTagName("th")
        tdElements = parser.getElementsByTagName("td")
        for element in (tableElements + tdElements + thElements):
            element.setStyle("border", "1px solid black")
            element.setStyle("border-collapse", "collapse")

        minhtml = parser.getMiniHTML()

        # Remove remaining excess linebreaks (from the code blocks) and any tabs so doesn't break output file rules
        return minhtml.replace("\n\r", HTML_LINEBREAK).replace("\n", HTML_LINEBREAK).replace("\r", HTML_LINEBREAK).replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

    # Return text indicating if correct or incorrect
    def __getCorrectText(self, isCorrect):
        return "correct" if (isCorrect == True) else "incorrect"

    # Return text indicating if correct or incorrect
    def __getTrueOrFalseText(self):
        return "true" if (self.__questionType == "QT") else "false"

    # Return a string containing the answers for the question. The answers should be shuffled at this point
    def __getFormattedAnswers(self):
        shuffled = self.__getShuffledAnswers()
        formattedAnswers = []
        for answer in shuffled:
            formattedAnswers.append("\t".join([self.__getFormmattedLines(answer[0]), self.__getCorrectText(answer[1])]))
        return "\t".join(formattedAnswers)
#================================================================================================================================

#================================================================================================================================
# Main Application class
#================================================================================================================================
class Application():

    def __init__(self):

        # Setup command line parameters
        # https://docs.python.org/3.7/library/argparse.html
        parser = argparse.ArgumentParser(description="Process file and output in valid format.")
        parser.add_argument("-i", "--input-file", dest="input", metavar="file",
                            type=argparse.FileType("r"),
                            default="multiple_choice.txt", help="Input file (default: multiple_choice.txt)")
        parser.add_argument("-o", "--output-file", dest="output", metavar="file",
                            type=argparse.FileType("w"),
                            default="multiple_choice_output.txt", help="Output file (default: multiple_choice_output.txt)")

        args = parser.parse_args()
        
        inputFileHandler = args.input
        outputFileHandler = args.output

        questionsList = [] # A list of Question objects
        question = None    # The current Question object being worked on

        # Loop through each line in the input file determining if the line
        # is a question or an answer
        with inputFileHandler as inputFile:
            for line in inputFile: # loop through each line
                line = line.replace('\ufeff', "")
                splitLine = line.split("|")
                lineType = splitLine[0]
                restOfLine = "|".join(splitLine[1:])

                if lineType in ["Q", "QT", "QF"]:
                    # If there is a previous question object add it to the list
                    if question != None:
                        questionsList.append(question)

                    # Define the new question with a new instance of the Question class
                    question = Question(lineType, restOfLine)
                elif lineType == "A-":
                    # it's an incorrect answer
                    question.addAnswer(restOfLine, False)
                elif lineType == "A+":
                    # it's a correct answer
                    question.addAnswer(restOfLine, True)
                else:
                    # Just a line of text that needs adding
                    question.addLine(line)

        # Add the final question object to the list
        questionsList.append(question)

        with outputFileHandler as outputFile:
            for question in questionsList:
                question.outputToTerminal()
                outputFile.write(question.getFormattedQuestion() + "\n")

        print('\nTotal questions formed: ' + str(len(questionsList)))
#================================================================================================================================

applicationInstance = Application()