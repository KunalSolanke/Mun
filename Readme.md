Workflow of then MUN project

Models Created

1.) User model which inherits from AbstractUSer model--->There is a role field which allows multiple types of users

2.) There is a country model which has name, id and flag

3.) Team model ==> leader has onetoone relation with User

4.) Deligate profile,Profile==> user ->OneToOne  


In Chits

There is a Chit model for storing the chits.

 Every chit has a status field
	0->Disapproved
	1->Checking
	2->Approved
	3->Ratified
chit field stores the content of message
chit_from,chit_to have Country as a foreign key
there is another field i.e reply_to_chit which has onetoone relation with itself


Now come to Working of the project

There will be 3 different kind of index pages depending upon the user.

First of all There will be a home page of the site which will have a login form.
That is described by the logon view.
When user clicks Log In. A post request is sent.
We will store the role of user in a variable 
Based on the role An index page will be shown to each user.


To each user chits will be displayed depending upon the status of the chits

Workflow of messaging:

When a user sends a message. We will send an ajax request to an end Point having current url. That will create a chit 
with status = 1. Since we will be fetching chits from database every minute. Chit will reach to moderator because status=1

Now moderator will click Approve or Disapprove.

If moderator approves the the we will update the chit status to 2.
since ajax is sending request to server to fetch the chits.
Now chit will be reached to judge and will be removed from admin.

Same process will be repeated for judge.


Now comes handling replies.


When a user will be replying we will update the chit by adding content to reply_to field.
now. We will first check if there already has been a reply to chit whose status is 3.

of that is the case furthur reply is note allowed.

else we will update the chits status.
