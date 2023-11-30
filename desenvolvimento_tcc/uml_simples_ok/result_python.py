class Funcionario:
	def __init__(self):
		pass
class Programador(Funcionario):
	def __init__(self, projeto, linguagemProgramacao):
		super().__init__(projeto, linguagemProgramacao)
		self.projeto = ''
		self.linguagemProgramacao = ''

	def setprojeto(self, projeto): 
		self.projeto = ''

	def setlinguagemProgramacao(self, linguagemProgramacao): 
		self.linguagemProgramacao = ''

class Gerente_Projeto(Gerente):
	def __init__(self, projetos, orcamentosControlados, dataDesignacao):
		super().__init__(projetos, orcamentosControlados, dataDesignacao)
		self.projetos = ''

	def setprojetos(self, projetos): 
		self.projetos = ''

class Gerente_Departamento(Gerente):
	def __init__(self, departamento, orcamentosControlados, dataDesignacao):
		super().__init__(departamento, orcamentosControlados, dataDesignacao)
		self.departamento = ''

	def setdepartamento(self, departamento): 
		self.departamento = ''

class Gerente_Estrategico(Gerente):
	def __init__(self, responsabilidades, orcamentosControlados, dataDesignacao):
		super().__init__(responsabilidades, orcamentosControlados, dataDesignacao)
		self.responsabilidades = ''

	def setresponsabilidades(self, responsabilidades): 
		self.responsabilidades = ''

class Gerente(Funcionario):
	def __init__(self, orcamentosControlados, dataDesignacao):
		super().__init__(orcamentosControlados, dataDesignacao)
		self.orcamentosControlados = ''
		self.dataDesignacao = ''

	def setorcamentosControlados(self, orcamentosControlados): 
		self.orcamentosControlados = ''

	def setdataDesignacao(self, dataDesignacao): 
		self.dataDesignacao = ''
