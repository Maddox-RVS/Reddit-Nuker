from rich.progress import Progress
from rich.prompt import IntPrompt
from rich.console import Console
from rich.columns import Columns
from rich.prompt import Confirm
from rich.align import Align
from rich.panel import Panel
import praw.models
import colorama
import prawcore
import time
import praw
import rich
import sys
import os

CONSOLE: rich.console.Console = Console()
colorama.reinit()

CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

def _printOAuthFailureMessage():
    CONSOLE.print('[white on red]ERROR[/] Failed to complete request, make sure the '
                      'account you logged in with is authentic.')

def login(handle: str, passcode: str) -> praw.Reddit:
    '''
    Log in to Reddit using PRAW with the provided credentials.

    Parameters
    ----------
    handle : str
        Reddit username.
    passcode : str
        Reddit password.

    Returns
    -------
    praw.Reddit
        Authenticated praw.Reddit instance.

    Examples
    --------
    >>> reddit: praw.models.Redditor = login('username', 'password')
    '''

    userAgent: str = f'script:reddit-nuker (by u/{handle})'

    reddit: praw.Reddit = praw.Reddit(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET,
        username=handle,
        password=passcode,
        user_agent=userAgent)
    
    return reddit
    
def getTotalComments(reddit: praw.Reddit) -> int:
    '''
    Get the total number of comments made by the authenticated user.

    Parameters
    ----------
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.

    Returns
    -------
    int
        Total number of comments.

    Examples
    --------
    >>> total: int = getTotalComments(reddit)
    '''

    user: praw.models.Redditor = reddit.user.me()
    return sum([1 for comment in user.comments.new(limit=None)])

def getTotalPosts(reddit: praw.Reddit) -> int:
    '''
    Get the total number of posts (submissions) made by the authenticated user.

    Parameters
    ----------
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.

    Returns
    -------
    int
        Total number of posts.

    Examples
    --------
    >>> total: int = getTotalPosts(reddit)
    '''

    user: praw.models.Redditor = reddit.user.me()
    return sum([1 for post in user.submissions.new(limit=None)])
    
def nukeComments(commentsToNuke: int, reddit: praw.Reddit, rateSeconds: int = 5) -> None:
    '''
    Delete a specified number of comments from the authenticated user's account.

    Parameters
    ----------
    commentsToNuke : int
        Number of comments to delete.
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.
    rateSeconds : int, optional
        Seconds to wait between deletions (default is 5).

    Returns
    -------
    None

    Examples
    --------
    >>> nukeComments(10, reddit) # default rate is 5 seconds
    >>> nukeComments(10, reddit, rateSeconds=2) # set the rate to 2 seconds
    '''

    user: praw.models.Redditor = reddit.user.me()
    totalComments: int = getTotalComments(reddit)

    if commentsToNuke > totalComments:
        raise ValueError('Comments to nuke cannot be greater '
                         'than the total number of comments the reddit account has.')
    
    with Progress() as progress:
        taskID: int = progress.add_task(f'[blue1]Deleting {commentsToNuke} comments...', total=commentsToNuke)

        iterator: int = 0
        for comment in user.comments.new(limit=None):
            comment.delete()
            iterator += 1

            progress.update(taskID, advance=1)
            
            if iterator == commentsToNuke: break

            time.sleep(rateSeconds)

def nukePosts(postsToNuke: int, reddit: praw.Reddit, rateSeconds: int = 5) -> None:
    '''
    Delete a specified number of posts from the authenticated user's account.

    Parameters
    ----------
    postsToNuke : int
        Number of posts to delete.
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.
    rateSeconds : int, optional
        Seconds to wait between deletions (default is 5).

    Returns
    -------
    None

    Examples
    --------
    >>> nukePosts(10, reddit) # default rate is 5 seconds
    >>> nukePosts(10, reddit, rateSeconds=2) # set the rate to 2 seconds
    '''

    user: praw.models.Redditor = reddit.user.me()
    totalPosts: int = getTotalPosts(reddit)

    if postsToNuke > totalPosts:
        raise ValueError('Posts to nuke cannot be greater '
                         'than the total number of posts the reddit account has.')
    
    with Progress() as progress:
        taskID: int = progress.add_task(f'[blue1]Deleting {postsToNuke} comments...', total=postsToNuke)
        
        iterator: int = 0
        for post in user.submissions.new(limit=None):
            post.delete()
            iterator += 1

            progress.update(taskID, advance=1)

            if iterator == postsToNuke: break

            time.sleep(rateSeconds)

def nukeAllComments(reddit: praw.Reddit, rateSeconds: int = 5) -> None:
    '''
    Delete all comments from the authenticated user's account.

    Parameters
    ----------
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.
    rateSeconds : int, optional
        Seconds to wait between deletions (default is 5).

    Returns
    -------
    None

    Examples
    --------
    >>> nukeAllComments(reddit) # default rate is 5 seconds
    >>> nukeAllComments(reddit, rateSeconds=2) # set the rate to 2 seconds
    '''

    totalComments: int = getTotalComments(reddit)
    nukeComments(totalComments, reddit, rateSeconds)

def nukeAllPosts(reddit: praw.Reddit, rateSeconds: int = 5) -> None:
    '''
    Delete all posts from the authenticated user's account.

    Parameters
    ----------
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.
    rateSeconds : int, optional
        Seconds to wait between deletions (default is 5).

    Returns
    -------
    None

    Examples
    --------
    >>> nukeAllPosts(reddit) # default rate is 5 seconds
    >>> nukeAllPosts(reddit, rateSeconds=2) # set the rate to 2 seconds
    '''

    totalPosts: int = getTotalPosts(reddit)
    nukePosts(totalPosts, reddit, rateSeconds)

def nukeAll(reddit: praw.Reddit, rateSeconds: int = 5):
    '''
    Delete all comments and posts from the authenticated user's account.

    Parameters
    ----------
    reddit : praw.Reddit
        Authenticated praw.Reddit instance.
    rateSeconds : int, optional
        Seconds to wait between deletions (default is 5).

    Returns
    -------
    None

    Examples
    --------
    >>> nukeAll(reddit) # default rate is 5 seconds
    >>> nukeAll(reddit, rateSeconds=2) # set the rate to 2 seconds
    '''

    nukeAllComments(reddit, rateSeconds)
    nukeAllPosts(reddit, rateSeconds)

def _actionsChooser(chooserTitle: str, options: list[str]) -> int:
    '''
    Display a numbered, centered list of options in a Rich panel and prompt the user to select one.

    Parameters
    ----------
    chooserTitle : str
        The title to display at the top of the options panel.
    options : list[str]
        A list of option strings for the user to choose from.

    Returns
    -------
    int
        The zero-based index of the selected option.

    Examples
    --------
    >>> idx = _actionsChooser("Choose Action", ["Option 1", "Option 2"])
    >>> print(idx) # 0 if the user selects the first option
    '''

    printOptions: list[str] = [f'[blue1]{[i + 1]} {option}[/]' for i, option in enumerate(options)]
    formattedOptionsString: str = '\n'.join(printOptions)
    optionsPanel: Panel = Panel.fit(Align.center(formattedOptionsString),
                                    title=chooserTitle,
                                    border_style='light_sky_blue1')
    
    CONSOLE.print(optionsPanel)
    
    while True:
        choiceStr: str = CONSOLE.input('[blue1] Please enter a number that corresponds to one of the above options[/]: ')

        try:
            choiceInt: int = int(choiceStr)
        
            if choiceInt < 1 or choiceInt > len(options):
                sys.stdout.write(f'\033[1A\033[2K\r')
                sys.stdout.flush()
                continue
        except ValueError:
            sys.stdout.write(f'\033[1A\033[2K\r')
            sys.stdout.flush()
            continue

        break

    sys.stdout.write(f'{'\033[1A\033[2K' * (len(options) + 3)}\r')
    sys.stdout.flush()

    return choiceInt - 1

if __name__ == '__main__':

    # Ask for login credentials
    CONSOLE.rule('[light_sky_blue1]Login[/]', style='light_sky_blue1')
    username: str = CONSOLE.input('[blue1]Enter your Reddit username[/]: ')
    passcode: str = CONSOLE.input('[blue1]Enter your Reddit passcode[/]: ')

    sys.stdout.write(f'{'\033[1A' * 3}\r')
    sys.stdout.flush()

    loginPanel: Panel = Panel((f'[blue1]Enter your Reddit username[/]: {username}\n'
                              f'[blue1]Enter your Reddit passcode[/]: {'●' * len(passcode)}'),
                              title='Login',
                              border_style='light_sky_blue1')
    CONSOLE.print(loginPanel)

    reddit: praw.Reddit = login(handle='Greedy_Rip_4694', passcode='Burner46583#%^&')

    # Attempt to display total comments and posts
    try:
        with CONSOLE.status('[blue1]Fetching Data[/]', spinner='dots'):
            totalComments: int = getTotalComments(reddit)
            totalPosts: int = getTotalPosts(reddit)
    except prawcore.exceptions.OAuthException as e:
        _printOAuthFailureMessage()
        CONSOLE.print(e)
        exit(1)

    userInfoPanel: Panel = Panel((f'[blue1]Total Comments → [/][gray42]{totalComments}[/]\n'
                                  f'[blue1]Total Posts → [/][gray42]{totalPosts}[/]'),
                                  title='User Info',
                                  border_style='light_sky_blue1')
    
    sys.stdout.write(f'{'\033[1A\033[2K' * 4}\r')
    sys.stdout.flush()

    CONSOLE.print(Columns([loginPanel, userInfoPanel]))

    # Ask for program action from user
    options: list[str] = ['# of Comments', 
                          'All Comments',
                          '# of Posts',
                          'All Posts',
                          'Everything']
    choiceIndex: int = _actionsChooser('Choose What To Nuke', options)

    # Perform action
    if choiceIndex == 0:
        amount: int = IntPrompt.ask('[blue1]Enter the number of comments you want deleted[/]')
        confirmed: bool = Confirm.ask((f'[blue1]Are you sure you want to delete {amount} comments? '
                                       'The comments will be impossible to restore after running '
                                       'the script, they will be gone forever.'))
        if confirmed: nukeComments(amount, reddit)
        else: CONSOLE.print('\n[bold white on red]PROCESS CANCELLED')
    elif choiceIndex == 1:
        confirmed: bool = Confirm.ask((f'[blue1]Are you sure you want to delete ALL {totalComments} comments? '
                                       'The comments will be impossible to restore after running '
                                       'the script, they will be gone forever.'))
        if confirmed: nukeAllComments(reddit)
        else: CONSOLE.print('\n[bold white on red]PROCESS CANCELLED')
    elif choiceIndex == 2:
        amount: int = IntPrompt.ask('[blue1]Enter the number of posts you want deleted[/]')
        confirmed: bool = Confirm.ask((f'[blue1]Are you sure you want to delete {amount} posts? '
                                       'The posts will be impossible to restore after running '
                                       'the script, they will be gone forever.'))
        if confirmed: nukeAllPosts(amount, reddit)
        else: CONSOLE.print('\n[bold white on red]PROCESS CANCELLED')
    elif choiceIndex == 3:
        confirmed: bool = Confirm.ask((f'[blue1]Are you sure you want to delete ALL {totalPosts} posts? '
                                       'The posts will be impossible to restore after running '
                                       'the script, they will be gone forever.'))
        if confirmed: nukeAllPosts(reddit)
        else: CONSOLE.print('\n[bold white on red]PROCESS CANCELLED')
    elif choiceIndex == 4:
        confirmed: bool = Confirm.ask((f'[blue1]Are you sure you want to delete ALL {totalComments} comments '
                                       f'and ALL {totalPosts} posts? The comments and posts will be impossible '
                                       'to restore after running the script, they will be gone forever.'))
        if confirmed: nukeAll(reddit)
        else: CONSOLE.print('\n[bold white on red]PROCESS CANCELLED')