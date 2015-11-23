import praw, OAuth2Util, time, re


##### Fork by /u/_korbendallas_
##### Made with python 2.7.6 so it may need some tweaks to run on 3.x
##### Very little of this has been tested!!!!!!!
##### Use on test sub only

def Main():

    subname = 'photoshopbattles'
    user_agent = 'Plagiarism control by /u/Captain_McFiesty ver 0.4.1'
    wikiPage = 'plagnames'
    interval = 30

    r = praw.Reddit(user_agent)
    o = OAuth2Util.OAuth2Util(r)


    ##### Main loop
    while True:

        try:
            
            o.refresh()

            commentsWithLinks = getCommentsWithLinks(subname, r)

            if commentsWithLinks:
                plagiarisedLinks = removePlagiarisedLinks(commentsWithLinks)
                if plagiarisedLinks:
                    updateWiki(subname, wikiPage, plagiarisedLinks, r)

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
            comments = submission.comments
            if comments:
                for comment in comments:
                    linksCollector = re.compile('href="(.*?)"')
                    links = linksCollector.findall(comment.body_html)
                    if links:
                        for link in links:
                            commentsWithLinks.append([link, comment])

    except (Exception) as e:
        
        print e.message


    return commentsWithLinks


##### Finds and removes plagiarised links and returns a list of the evil-doers comments
def removePlagiarisedLinks(commentsWithLinks):

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
                                    if commentA[1].created > commentB[1].created:
                                        plagiarisedLinks.append(commentA[1])
                                        commentA[1].remove(spam=False)
                                    else:
                                        plagiarisedLinks.append(commentB[1])
                                        commentB[1].remove(spam=False)
                                        
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



Main()