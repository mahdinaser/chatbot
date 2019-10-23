import config
import praw
import json
import argparse
import datetime
import schedule
import time
import pandas as pd
LIMIT = 100000

maximumSubmissionCount = 1000000

defaultTopic = 'opiates'

reddit = praw.Reddit(client_id = 'yorZFzg2emERXQ',
                    client_secret = 'oktOJHC_TmLCTC0uyfwxAsP5dk0',
                    username = 'mahdinaser1984',
                    password = 'mahdi900',
                    user_agent = 'opiodcrawler')

def get_parser():
    parser = argparse.ArgumentParser(description="Reddit Downloader")
    parser.add_argument("-s",
                        "--subreddit",
                        dest="subreddit",
                        help="Subreddit to PRAW",
                        default=('%s' % defaultTopic))

    parser.add_argument("-l",
                        "--limit",
                        dest="limit",
                        help="Pull N number of submissions",
                        default=None)

    return parser

collection=[]
def generateQA(post,childern):
    if (len(childern)==0):
        return
    for child in childern:
        if hasattr(post, 'body'):
            collection.append([post.body,child.body])
        else:
            collection.append([post.title, child.body])
        generateQA(child,child._replies)

def prawSubreddit(subName, lm):
    print("Collecting from /r/{}...".format(subName))
    submissionCount = 0
    commentCount = 0
    fileCount = 0
    redditData = {}

    subreddit = reddit.subreddit(subName)
    submissions = subreddit.new(limit=LIMIT)
    redditData[str(subreddit)] = [{}]


    # Iterate through each submissions and following comments
    for submission in submissions:
        title = submission.title
        if '?' not in title:
            continue
        submissionCount += 1
        comments = submission.comments
        comments.replace_more(limit=None)
        comments_list = comments.list()
        if (len(comments_list)==0):
            continue

        redditData[str(subreddit)][0][submission.fullname] = [{}]

        redditData[str(subreddit)][0][submission.fullname][0]['0_title'] = title
        redditData[str(subreddit)][0][submission.fullname][0]['comments'] = [{}]

        generateQA(submission,submission.comments)



        # for comment in comments_list:
        #     commentCount += 1
        #
        #     # original line
        #     # redditData[str(subreddit)][0][submission.fullname][0]['comments'][0][commentCount] = comment.body
        #
        # updateTerminal(submissionCount, commentCount, )
        # if (len(comments_list) != 0):
        #     print('print out data to file')
        #     if(submissionCount % maximumSubmissionCount == 0):
        #         writeOutput("{}_{}.txt".format(subName,fileCount),redditData)
        #         fileCount += 1
        #         redditData = {}
        #         subreddit = reddit.subreddit(subName)
        #         redditData[str(subreddit)] = [{}]

    print("Finished Collecting.")
    timestr = time.strftime("%Y%m%d-%H%M%S")

    df = pd.DataFrame(collection, columns=['question', 'answer'])
    print(len(df))
    df.to_csv("data/"+"{}.txt".format(subName+timestr))
    #writeOutput("{}_{}.txt".format(subName+timestr,fileCount),redditData)

def userExistInComments(commentList, user):
    if user in commentList:
        return True
    return False

def writeOutput(fileName, data):
    outputFile = open('data/'+fileName, "w")
    outputFile.write(json.dumps(data, sort_keys=True))

# After X amount of seconds, update progress to terminal
def updateTerminal( subCount, comCount):
    #if ((subCount % 350) == 0):
    print("Downloaded: {} Submissions".format(subCount))
    print("Downloaded: {} Comments".format(comCount))

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    limit = args.limit
    if (limit != None):
        limit = int(limit)


    #prawSubreddit(args.subreddit, limit)

    def job():
        prawSubreddit(args.subreddit, limit)

    schedule.every().day.at("02:18").do(  job  )

    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
