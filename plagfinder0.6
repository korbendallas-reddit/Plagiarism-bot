import praw
import OAuth2Util
import time
import requests
import re

plag_names = []
INTERVAL = 30 #minutes
running = True
subname = 'photoshopbattles'
backupsubname = 'plagiarismcontrol'
user_pat = re.compile('/u/[A-Za-z0-9]+')
SLEEPS = 24*60/INTERVAL #Number of times to sleep before checking SB
slps = SLEEPS
user_agent = "Plagiarism control by /u/Captain_McFiesty ver 0.6"

r = praw.Reddit(user_agent)
o = OAuth2Util.OAuth2Util(r)

subreddit = r.get_subreddit(subname)
# submission = r.get_submission(submission_id='3fpml4') # test thread


def check_comments(top):
    for comment in top:
        if(comment.author != None):
            for comment2 in top:
                if(comment2.author != None):
                    #print(comment2.author)
                    if (comment2.body == comment.body and
                            comment.author.name != comment2.author.name and
                            comment2.id != comment.id):
                        if (comment2.created > comment.created and
                               comment2.author.name not in plag_names):
                            print('Plagiarism, id = %r, user = %r'
                                      % (comment2.id, comment2.author.name))
                            plag_names.append(comment2.author.name)
                            #comment2.report('Bot report: Plagiarism suspected')
                            subreddit.add_ban(comment2.author.name)
                            comment2.remove(spam=False)
    return

def filter_comments(flat_comments):
    top_level = []
    for comment in flat_comments:
        #print(vars(comment))
        if (comment.is_root and comment.banned_by == None):
            top_level.append(comment)
    #print_list(top_level)
    return top_level

def print_list(top):
    print('\nTop Level List')
    for c in top:
        print(c.id)
        print(c.author)
    print('\n')
    return

def add_to_both_wiki():
    add_to_wiki(subname);
    add_to_wiki(backupsubname);
    plag_names.clear()
    return

def add_to_wiki(sn):
    wiki = r.get_wiki_page(sn,'plagnames')
    if (wiki.content_md == ''):
        text = 'Plagiarism users  \r\n'
    else:
        text = wiki.content_md
    if(plag_names != []):
        for user in plag_names:
            text += '/u/'+user+'  \r\n'
        wiki.edit(text, 'Added plagiarism users')
    return

def do_code():
    for submission in subreddit.get_hot(limit=5):
        if submission.num_comments > 100:
            print('Submission id: %r' % submission.id)
            submission.replace_more_comments(limit=None, threshold=0)
            flat_comments = praw.helpers.flatten_tree(submission.comments)
            top_level = filter_comments(flat_comments)
            check_comments(top_level)
            # print_list(top_level)
    add_to_both_wiki()
    return

def accept_invite():
    for message in r.get_unread():
    #for message in r.get_messages():
            if(message.body.startswith('**gadzooks!')):
                sub = r.get_info(thing_id=message.subreddit.fullname)
                if(message.subreddit.display_name == subname):
                    try:
                        sub.accept_moderator_invite()
                    except(praw.errors.InvalidInvite):
                        pass
                    message.mark_as_read()
    return

def sleep_check():
    global slps
    #print(SLEEPS)
    #print(slps)
    
    if(slps >= SLEEPS):
        print("Checking for Shadowbans")
        #print("inside")
        clear_shadowbanned()
        slps = 0
    else:
        #print("outside")
        slps += 1
    return

def clear_shadowbanned():
    #print("here")
    wiki = r.get_wiki_page(backupsubname,'plagnames')
    text = wiki.content_md
    users = re.findall(user_pat, text)
    new_text = ''
    for user in users:
        #print(user[3:])
        if(check_user(user[3:])):
            #print("found")
            new_text += user+'  \r\n'
            text = text.replace(user+'  \r\n', '')
    if(new_text != ''):
        #print("here 3")
        add_shadowbanned(new_text)
        #print(text)
        wiki.edit(text, 'Removed shadowbanned users')
    return

def check_user(user_name):
    try:
        user = r.get_redditor(user_name)
        karma = user.comment_karma # Throws an error if shadowbanned
        return False
    except:
        return True
    
def add_shadowbanned(new_text):
    wiki = r.get_wiki_page(backupsubname,'bannedplagnames')
    text = wiki.content_md
    text += new_text
    wiki.edit(text, 'Added shadowbanned users')
    return

#accept_invite()
#do_code()
#sleep_check()

while running:
    print("Local time: ", time.asctime(time.localtime(time.time())))
    try:
        o.refresh()
        #accept_invite()
        do_code()
        sleep_check()
    except KeyboardInterrupt:
        running = False
    except (praw.errors.APIException):
        print("[ERROR]: APIException")
    except (praw.errors.HTTPException):
        print("[ERROR]: HTTPException")
        time.sleep(INTERVAL/2*60)
        continue
    except (praw.errors.PRAWException):
        print("[ERROR]: PRAWException")
        time.sleep(INTERVAL/2*60)
        continue
    except (requests.exceptions.ConnectionError):
        print("Internet down")
        time.sleep(INTERVAL/2*60)
        continue
    except (Exception):
        print("[ERROR]: Other error")
        break
    #print('done')
    #running = False
    time.sleep(INTERVAL*60)
