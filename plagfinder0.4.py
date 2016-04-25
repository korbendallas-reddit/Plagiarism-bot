import praw, OAuth2Util, time, re


def Main():

    subname = 'korbendallas'
    backupSubname = 'korbendallas'
    username = '_korbendallas_'
    user_agent = '_korbendallas_ by /u/_korbendallas_ ver 0.1'
    wikiPage = 'plagnames'
    interval = 30

    r = praw.Reddit(user_agent)
    o = OAuth2Util.praw.AuthenticatedReddit.login(r, disable_warning=True)
    #acceptInvite(subname, r)


    ##### Main loop
    while True:

        try:
            
            o.refresh()

            commentsWithLinks = getCommentsWithLinks(subname, r)

            if commentsWithLinks:
                plagiarisedLinks = findPlagiarisedLinks(commentsWithLinks, username, r)
                if plagiarisedLinks:
                    updateWiki(subname, wikiPage, plagiarisedLinks, r)
                    updateWiki(backupSubname, wikiPage, plagiarisedLinks, r)

        except (KeyboardInterrupt) as e:
            
            print e.message
            break

        except (praw.errors.APIException) as e:
            
            print e.message
            time.sleep(interval)

        except (praw.errors.HTTPException) as e:
            
            print e.message
            time.sleep(interval/2*60)

        except (praw.errors.PRAWException) as e:
            
            print e.message
            time.sleep(interval/2*60)

        except (Exception) as e:
            
            print e.message
            break

        time.sleep(interval*60)
        
                
    return


##### Return a list of comments with links as a matrix
##### Matrix format: [link, comment]
def getCommentsWithLinks(subname, r):

    commentsWithLinks = []

    try:
        
        sub = r.get_subreddit(subname)
        submissions = sub.get_hot(limit=5)
    
        for submission in submissions:
            submission.replace_more_comments(limit=None, threshold=0)
            comments = praw.helpers.flatten_tree(submission.comments)
            if comments:
                for comment in comments:
                    if comment.is_root and comment.banned_by == None:
                        linksCollector = re.compile('href="(.*?)"')
                        links = linksCollector.findall(comment.body_html)
                        if links:
                            for link in links:
                                commentsWithLinks.append([link, comment])

    except (Exception) as e:
        
        print e.message


    return commentsWithLinks


##### Finds and removes plagiarised links and returns a list of the evil-doers comments
def findPlagiarisedLinks(commentsWithLinks, subname, r):

    plagiarisedLinks = []
    
    try:
        
        commentsWithLinksB = commentsWithLinks

        for commentA in commentsWithLinks:
            if commentA[1].author:
                for commentB in commentsWithLinksB:
                    if commentB[1].author:
                        if commentA[0] == commentB[0]:
                            if commentA[1].author.name != commentB[1].author.name:
                                if commentA[1] not in plagiarisedLinks and commentB[1] not in plagiarisedLinks:

                                    # Matching links found
                                    try:

                                        # Remove 100% matches and add to list
                                        if commentA[1].body == commentB[1].body:
                                            if commentA[1].created > commentB[1].created:
                                                plagiarisedLinks.append(commentA[1])
                                                commentA[1].remove(spam=False)
                                            else:
                                                plagiarisedLinks.append(commentB[1])
                                                commentB[1].remove(spam=False)
                                                
                                        # Report suspected matches, but don't add to list
                                        else:
                                            messageBody = 'Suspected Plagiarised Comment: \n\n'
                                            if commentA[1].created > commentB[1].created:
                                                messageBody += commentA[1].permalink
                                                messageBody += '\n\n Original Comment: \n\n'
                                                messageBody += commentB[1].permalink
                                            else:
                                                messageBody += '\n' + commentB[1].permalink + '\n'
                                                messageBody += '\n Original Comment: \n'
                                                messageBody += '\n' + commentA[1].permalink
                                            r.send_message('/r/' + subname, 'Suspected Plagiarism', messageBody)
                                                
                                    except (Exception) as e:
        
                                        print e.message
                                        
                                        
    except (Exception) as e:
        
        print e.message

    
    return plagiarisedLinks


##### Adds evil-doers to the wall of shame
def updateWiki(subname, wikiPage, plagiarisedLinks, r):

    try:
        
        wiki = r.get_wiki_page(subname, wikiPage)
        wikiContents = wiki.content_md

        newWikiContents = ''

        if len(wikiContents) < 1:
            newWikiContents = 'Plagiarism users  \n'
        else:
            newWikiContents = wikiContents

        if plagiarisedLinks:
            for plagiarisedLink in plagiarisedLinks:
                user = '/u/' + plagiarisedLink.author.name + ' \n'
                if user not in newWikiContents:
                    newWikiContents += user

            wiki.edit(newWikiContents, 'Added plagiarism users')
            
    except (Exception) as e:
        
        print e.message

    
    return


def acceptInvite(subname, r):

    try:
        
        for message in r.get_unread():
    
            if message.body.startswith('**gadzooks!'):
                sub = r.get_info(thing_id=message.subreddit.fullname)
                if message.subreddit.display_name == subname:
                    
                    try:
                        
                        sub.accept_moderator_invite()
                        
                    except (praw.errors.InvalidInvite) as e:
    
                        print e.message
                        pass
                
                    message.mark_as_read()

    except (Exception) as e:
        
        print e.message

                
    return



Main()
