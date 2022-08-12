# Python reddit challenge
# Completed by David Hamilton

# this program was developed to answer 2 questions regarding the things on reddit dataset.
# these questions are:
# - What are the top five most mentioned product categories across all of Reddit?
# - What are the top three product categories that appear across the greatest number of subreddits?
# please change the file path to the location of your reddits folder (the folder containing folders 1-Z
# additionally please make sure the required imported libraries are available

# library imports
import pandas as pd
import glob
import os


# reads in csv file contents and puts them into 1 single pandas dataframe
def readDataset():
    path = r'C:\Users\David\Desktop\kaggle-project\top-things\reddits'  # path to reddits folder which contains csv files.

    # creates a list consisting of the path to every CSV file in the reddits folder, specified by */*.csv wildcard mark.
    files = glob.glob(os.path.join(path, "*/*.csv"))
    redditList = []  # defines a list for csv content to be appended too when read in using pandas

    # loops through each item in the files list, then uses pandas to read the content of the files in
    for fileName in files:
        dataframe = pd.read_csv(fileName, index_col=None)
        redditList.append(dataframe)  # appends everything read in by pandas to a list

    frame = pd.concat(redditList, axis=0, ignore_index=True)  # converts the redditList into a single pandas dataframe
    frame = frame.fillna(0)  # removes nan values, replacing them with 0

    return frame  # the prepared dataframe is returned


# code for answering question 1
def question1(frame):
    categoryList = {}  # dictionary to count how many times a specific category appears

    # loops through the dataframe provided, adds new categories as a new value in the dictionary.
    # any repeating categories get added to the value assigned to that category in the dictionary.
    # additional subreddit mentions are added to the value to count the total mentions
    for i in range(len(frame)):
        if frame['category'][i] not in categoryList:
            categoryList[frame['category'][i]] = frame['subreddit_mentions'][i]  # adds new categories to the dictionary
        else:
            categoryList[frame['category'][i]] += frame['subreddit_mentions'][i]  # adds subreddit mentions to category value

    sortedList = sorted(categoryList.items(), key=lambda x: x[1])  # sorts the dictionary into a list, highest value at the end

    top5 = list(reversed(sortedList[-5:]))  # reverses the list, as well as extracting the top 5 results

    return top5  # returns the top 5 list (answer to question 1)


# code for answering question 2
def question2(frame):
    nameSet = set()  # set to remove duplicate products based on names
    categoryList = {}  # dictionary to count total mentions of a category

    # loops through dataframe provided, first checks to see if the name value is present in the nameSet to exclude duplicates
    # any new categories get added as a new value in the dictionary, repeating values have their total mentions added to the total
    # adds the name of each iteration to the set to exclude duplicates
    for i in range(len(frame)):
        if frame['name'][i] not in nameSet:  # checks to see if iterations name is in nameSet
            if frame['category'][i] not in categoryList:
                categoryList[frame['category'][i]] = frame['total_mentions'][i]  # adds new categories to the dictionary
            else:
                categoryList[frame['category'][i]] += frame['total_mentions'][i]  # adds total mentions to category value
        nameSet.add(frame['name'][i])  # adds current iterations name to nameSet

    sortedList = sorted(categoryList.items(), key=lambda x: x[1])  # sorts the dictionary into a list, the highest value at end

    top3 = list(reversed(sortedList[-3:]))  # reverses the list from before so that the highest number is at the top
    return top3  # returns the top 3 list (answer to question 2)


# used to print results to console
def question1Answer(top5):
    print('The top 5 most mentioned product categories across reddit are: ')
    for items in top5:  # loops through top 5 list in order to display each result
        print(str(items[0]) + ': ' + str(items[1]) + ' mentions.')



def question2Answer(top3):
    print('===============================================================')  # used to separate each answer
    print('The top 3 product categories that appear across the greatest number of subreddits are: ')
    for items in top3:  # loops through top 3 list in order to display each result
        print(str(items[0]) + ': ' + str(int(items[1])) + ' appearances.')



def main():
    dataset = readDataset()

    question1Answer(question1(dataset))
    question2Answer(question2(dataset))


if __name__ == '__main__':
    main()
