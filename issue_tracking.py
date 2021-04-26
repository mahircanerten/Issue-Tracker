import re
import datetime

## Get the issue id from the user and search active issues first to find
## if there is no such issue then search for other lists to give an appropiate error message to the user
def closeissue(IssueId,ToDoList,DoingList,DoneList,CancelledList):
    for issue in DoingList:
        if(issue['ID']==IssueId):
            DoneList.append(issue)
            DoingList.remove(issue)
            issue['Status History']["closed"]=datetime.datetime.now()
            return
    for issue in DoneList:
        if issue['ID']==IssueId:
            print("This issue has already been done.")
    for issue in CancelledList:
        if issue['ID']==IssueId:
            print("This issue has been cancelled.")
    for issue in ToDoList:
        if issue['ID']==IssueId:
            print("This issue has not been activated yet.")

   
## Get the necessary information required to create issue (Id,Name,Description) 
## Then if format is valid then create the issue and return the issue to main
def createIssue(id, name, description):
    if (not re.match("^Issue-\d\d\d$", id)):
        raise Exception("ID is not in format Issue-XXX where X represents a digit.")
    if (len(id) == 0 or len(name) == 0 or len(description) == 0):
        raise Exception("One or more fields are empty, please fill all the details.")
    if (not re.match("^\w+$", name)):
        raise Exception("Name is not alphanumeric.")

    issue = {}
    issue['ID'] = id
    issue['Name'] = name
    issue['Description'] = description
    issue['Status History'] = {'To do': datetime.datetime.now()}
    return issue

## get a issue and print the details of it
def PrintIssueDetails(issue):
    print("--------------------")
    print("ID:", issue['ID'])
    print("Name:", issue['Name'])
    print("Description:", issue['Description'])
    if ('To do' in issue['Status History']):
        print("Date and time of Creation:", issue['Status History']['To do'].strftime("%Y-%m-%d %H:%M:%S"))
    if ('Doing' in issue['Status History']):
        print("Date and time of Activation:", issue['Status History']['Doing'].strftime("%Y-%m-%d %H:%M:%S"))
    if ('Done' in issue['Status History']):
        print("Date and time of Closure:", issue['Status History']['Done'].strftime("%Y-%m-%d %H:%M:%S"))
    if ('Cancelled' in issue['Status History']):
        print("Date and time of Closure:", str(issue['Status History']['Cancelled'][0].strftime("%Y-%m-%d %H:%M:%S")) + '(' + str(issue['Status History']['Cancelled'][1]) + ')')

## Get a list of issues and print them according to their creation time in ascending order
def ListIssues(list):
    print("")
    ordered_list = sorted(list, key = lambda x: x['Status History']['To do'])
    for issue in ordered_list:
        PrintIssueDetails(issue)
    print("")

## Get a keyword from user and search issues that contain that substring
def SearchKeyword(keyword, todoList, doingList, doneList, cancelledList):
    for issue in todoList:
        if (keyword in issue['ID'] or keyword in issue['Name'] or keyword in issue['Description']):
            PrintIssueDetails(issue)
            
    for issue in doingList:
        if (keyword in issue['ID'] or keyword in issue['Name'] or keyword in issue['Description']):
            PrintIssueDetails(issue)
            
    for issue in doneList:
        if (keyword in issue['ID'] or keyword in issue['Name'] or keyword in issue['Description']):
            PrintIssueDetails(issue)
            
    for issue in cancelledList:
        if (keyword in issue['ID'] or keyword in issue['Name'] or keyword in issue['Description']):
            PrintIssueDetails(issue)

## Activate an issue in todolist by getting id from user 
## If such issue does not exist in todolist then search other lists to give an appropiate error message
def activeissue(Id,todolist,doinglist,canceledlist,donelist):
    for issue in canceledlist:
        if issue['ID']==Id:
            print("This issue has already canceled")
            return
    for issue in donelist:
        if issue['ID']==Id:
            print("This issue has already done")
            return
    for issue in doinglist:
        if issue['ID']==Id:
            print("This issue is already active")
            return
    for issue in todolist:
        if issue['ID']==Id:
            issue['Status History']['Doing']=datetime.datetime.now()
            doinglist.append(issue)
            todolist.remove(issue)
            print("Updated")
            return
    print("Invalid ID")

## Cancel an issue in doinglist by getting id from user 
## If such issue does not exist in doinglist then search other lists to give an appropiate error message
def cancelissue(Id,todolist,doinglist,canceledlist,donelist,reason):
    for issue in todolist:
        if issue['ID']==Id:
            print("This issue is not active")
            return
    for issue in donelist:
        if issue['ID']==Id:
            print("This issue has already done")
            return
    for issue in canceledlist:
        if issue['ID']==Id:
            print("This issue has already cancelled")
            return
    for issue in doinglist:
        if issue['ID']==Id:
            issue['Status History']['Cancelled']=(datetime.datetime.now(),reason)
            canceledlist.append(issue)
            doinglist.remove(issue)
            print("Updated")
            return
    print("Invalid ID")

## An infinite loop for menu that constantly asks user for their selection
## Does operations selected by the input
ToDoList=[]
DoingList=[]
DoneList=[]
CancelledList=[]
while 1:    
    print("1. Create an issue")
    print("2. Activate an issue")
    print("3. Close an issue")
    print("4. Cancel an issue")
    print("5. List all issues")
    print("6. Search issues")
    val=input("Enter your selection: ")
    if val == '1':
        name=input("\nName: ")
        Id=input("Id: ")
        description=input("Description: ")
        
        ## Detect problems in createIssue function and display error message to user
        try:
            issue = createIssue(Id,name,description)
            ToDoList.append(issue)
        except Exception as exception:
            print("Error while creating a new issue:\n" + str(exception))
        finally:
            print("")

    elif val == '2':
        Id=input("Id: ")
        activeissue(Id,ToDoList,DoingList,CancelledList,DoneList)
    elif val == '3':
        Id=input("Id: ")
        closeissue(Id,ToDoList,DoingList,DoneList,CancelledList)
    elif val == '4':
        Id=input("Id: ")
        Reason=input("Enter your reason to cancel: ")
        cancelissue(Id,ToDoList,DoingList,CancelledList,DoneList,Reason)
    elif val == '5':
        print("")
        print(""" 5.(1) List issues with the "To Do" status """)
        print(""" 5.(2) List issues with the "Doing" status """)
        print(""" 5.(3) List issues with the "Done" status """)
        print(""" 5.(4) List issues with the "Cancelled" status """)
        secSelect=input("Enter a selection: ")
        if secSelect=='1':
            ListIssues(ToDoList)
        elif secSelect=='2':
            ListIssues(DoingList)
        elif secSelect=='3':
            ListIssues(DoneList)
        elif secSelect=='4':
            ListIssues(CancelledList)
        else:
            print("Invalid selection")
    elif val == '6':
        Keyword=input("Keyword: ")
        SearchKeyword(Keyword,ToDoList,DoingList,DoneList,CancelledList)
    else:
        print("Invalid selection")
