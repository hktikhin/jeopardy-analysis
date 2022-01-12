import pandas as pd
import numpy as np
import re

pd.set_option('display.max_columns', None)

# 1 -- look at the context of dataset and rename the column if needed
df = pd.read_csv("jeopardy.csv")

# there is space in the column name
newCol = []
for col in df.columns:
    # remove all space in columns
    newCol.append(col.replace(" ", ""))
df.columns = newCol
#print(df.head())
#print(df.info())

# 2 -- define a function to only return question having all the string in list
def filterDataByQuestion(df1, lst):
    """
    :param df1: jeopardy data frame(pass by reference)
    :param lst: list of string
    :return: filtered data frame
    """
    result = df1[df1.Question.apply(
        lambda question:\
        # check if question contain string 1,2,...
        # use a list to contain bool value, use all to check if all bool is true
        all([ re.search(r"\b{}\b".format(str.lower()), question.lower()) is not None
              for str in lst]))
    ]
    return result

#print((filterData(df, ["King", "England"])).Question)

# --3 modify the function so that it is more robust
# solving 'viking' vs 'king'
# print(re.search(r"\bking\b", "king is me"))

# --4 convert value col into float type
df.Value = df.Value.apply(lambda valStr:
                          # remove number format($/,)
                          np.float64(valStr[1:].replace(",",""))
                          # handle missing value
                          if valStr != "None"
                          else np.nan
                          )
print(df.info())
#  What is the average value of questions that contain the word "King"?
king_questions = filterDataByQuestion(df, ["King"])
#print(king_questions.Value.mean())

# --6 define a function that return unique answer and its count
def countAns(df1):
    """
    given data frame, find the count of different answer
    :return: data series
    """
    return df1.Answer.value_counts()

#print(len(king_questions))
#print(countAns(king_questions))

# --7 self exploring question
# How many questions from the 90s use the word "Computer" compared to question from the 2000s?
# print(df.AirDate)

# first transform the airDate column into date type
df.AirDate = pd.to_datetime(df.AirDate, format="%Y-%m-%d")

def filterDataByDate(df1, startDate, endDate):
    # check if current date is between start and end date
    boolDf = df1.AirDate.apply(lambda date:
                      (date>=startDate)&(date<endDate)
                      )
    return df1[boolDf]

computerQuestion = filterDataByQuestion(df, ["Computer"])
# 1990s
computerQuestionNinety = filterDataByDate(computerQuestion,
                                          pd.to_datetime("1990-01-01"),
                                          pd.to_datetime("2000-01-01")
                                          )
# 2000s
computerQuestionZero = filterDataByDate(computerQuestion,
                                          pd.to_datetime("2000-01-01"),
                                          pd.to_datetime("2010-01-01")
                                          )
#print(len(computerQuestion))
#print(len(computerQuestionNinety))
#print(len(computerQuestionZero))

# Is there a connection between the round and the category?
# Are you more likely to find certain categories, like "Literature"
# in Single Jeopardy or Double Jeopardy?

# first group the data by round and category
#print(df.Round.value_counts())
#print(df.Category.value_counts())

countByRoundCat = df.groupby(["Round", "Category"])\
    .Question.count().reset_index().sort_values("Question", ascending=False)

# filter out the group which have less than 150 question
countByRoundCat = countByRoundCat[countByRoundCat.Question>150]
#print(len(countByRoundCat))
# make it easy to visualize the relationship
countByRoundCatPivot = countByRoundCat.pivot(
    columns = "Category",
    index = "Round",
    values = "Question"
)
#print(countByRoundCatPivot)
# it seem more likely to find "Literature" question in 'Double Jeopardy!'


# Here I will create a system to generate random question to quiz the user
# And check if the answer is correct or not
def generateRandomQuestion(df1):
    """
    given dataframe, try to get a random question
    :return: a single question record
    """
    ranNum = np.random.randint(0, len(df1))
    return df1.iloc[ranNum]

def play(df1):
    """
    implement the logic of the game
    """
    randomQuestion = generateRandomQuestion(df1)
    print(randomQuestion)
    while(True):
        ans = input(f"""Please infer what is being said from the following description:
    {randomQuestion.Question}
""")
        if ans.lower() == randomQuestion.Answer.lower():
            print("You got it")
            exit()
        else:
            print("Try Again!!")

play(df)
















