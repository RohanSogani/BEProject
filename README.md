Change following path directory variables before running the project:
	- 'BASE_DJANGO_DIR' in appWindow/runAndrowarn.py
	- Path in appWindow/manifest.py
	- Path in showReport() in appWindow/views.py

Dependencies: 
	- Django
	- Pymongo
	- MongoDB
	- Androwarn
	- crispy-forms(Django)
	- Apktools
	- Android Permission Mapper
	
Current status:

	- Upload APk -> Run Androwarn -> Produce report

To-do:
	Decorate report. Currently plain text HTML

How to work with branches in Git:
1. Create new branch using 'git checkout -b <name-of-branch>'
2. Make changes
3. Add to staging area 'git add -A .'
4. Commit changes 'git commit -m <commit-msg>'
5. Update master with origin master[The one on Bitbucket] 'git pull origin master'
5. Merge master with new branch 'git checkout master, git merge <name-of-branch>'