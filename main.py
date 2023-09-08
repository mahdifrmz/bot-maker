MESSAGE_TYPE_TEXT = 1
MESSAGE_TYPE_IMAGE = 2
MESSAGE_TYPE_AUDIO = 3
MESSAGE_TYPE_VIDEO = 4
MESSAGE_TYPE_FILE = 5

class Step:
    def __init__(self, question:str, failure:str, mtype:int):
        self.mtype = mtype
        self.question = question
        self.failure = failure
        self.id = 0

class Command:
    def __init__(self, name:str, success:str, steps:list[Step] = []):
        self.name = name
        self.steps = steps
        self.success = success

    def addStep(self,step:Step):
        self.steps.append(step)        

class Bot:
    def __init__(self, token:str, commands:list[Command] = []):
        self.token = token
        self.commands = commands
    
    def addCommand(self,command:Command):
        self.commands.append(command)

class Generator:
    def generate(self,bot:Bot):
        self.bot = bot
        self.src = ''
        self.assignIds()
        self.generateInitials()
        self.generateCommands()
        self.generateInputs()
    def write(self,code:str):
        self.src += code
    def assignIds(self):
        gid = 1
        for cmd in self.bot.commands:
            for step in cmd.steps:
                step.id = gid
                gid += 1 
    
    def generateInitials(self):
        pass
    def generateCommands(self):
        for cmd in self.bot.commands:
            self.generateCommand(cmd)
    def generateCommand(self,cmd:Command):
        pass
    def generateInputs(self):
        pass

if __name__ == "main":
    bot = Bot('TOKEN::38u38i__')
    Generator().generate(bot)