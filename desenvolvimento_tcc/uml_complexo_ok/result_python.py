class Designer(Employee):
	def __init__(self, dribbleLink, updateDribbleLink, name, id, phone):
		super().__init__(dribbleLink, updateDribbleLink, name, id, phone)
		self.dribbleLink = ''
		self.updateDribbleLink = ''

	def setdribbleLink(self, dribbleLink): 
		self.dribbleLink = ''

	def setupdateDribbleLink(self, updateDribbleLink): 
		self.updateDribbleLink = ''





class Project:
	def __init__(self, title, createdDate):
		self.title = ''
		self.createdDate = ''



	def settitle(self, title): 
		self.title = ''

	def setcreatedDate(self, createdDate): 
		self.createdDate = ''

class Developer(Employee):
	def __init__(self, githubLink, name, id, phone):
		super().__init__(githubLink, name, id, phone)
		self.githubLink = ''

	def setgithubLink(self, githubLink): 
		self.githubLink = ''

class Department:
	def __init__(self, name):
		self.name = ''

	def setname(self, name): 
		self.name = ''

class ProjectMilestone:
	def __init__(self, targetData, projectId):
		self.targetData = ''
		self.projectId = ''

	def settargetData(self, targetData): 
		self.targetData = ''

	def setprojectId(self, projectId): 
		self.projectId = ''

class Employee:
	def __init__(self, name, id, phone):
		self.name = ''
		self.id = ''
		self.phone = ''

	def setname(self, name): 
		self.name = ''

	def setid(self, id): 
		self.id = ''

	def setphone(self, phone): 
		self.phone = ''
