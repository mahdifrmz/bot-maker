MESSAGE_TYPE_TEXT = 1
MESSAGE_TYPE_IMAGE = 2
MESSAGE_TYPE_AUDIO = 3
MESSAGE_TYPE_VIDEO = 4
MESSAGE_TYPE_DOC = 5


def loadTemplate(name:str) -> str:
    file = open('./templates/'+name+'.txt',)
    content = file.read()
    return content

importTemplate = loadTemplate('import')
utilTemplate = loadTemplate('util')
configTemplate = loadTemplate('config')
constantsTemplate = loadTemplate('constants')
mainTemplate = loadTemplate('main')
stepTemplate = loadTemplate('step')
commandTemplate = loadTemplate('command')
basicHandlerTemplate = loadTemplate('basic-handler')
commandHandlerTemplate = loadTemplate('command-handler')
messageHandlerTemplate = loadTemplate('message-handler')
stepHandlerTemplate = loadTemplate('step-handler')
stepHandlerMediaTemplate = loadTemplate('step-handler-media')
handlerBindTemplate = loadTemplate('handler-bind')

RENDER_ERROR = 'number of args must be equal to the number of template place holders'

def render(template:str, args : list[str]):
    for arg in args:
        arg.replace('\n','\\n')
        if(arg.find('%') > -1):
            template = template.replace('%', arg, 1)
        else:
            raise Exception(RENDER_ERROR)
    if(template.find('%') > 1):
        raise Exception(RENDER_ERROR)
    return template

class Step:

    def __init__(self, question:str, mtype:int):
        self.mtype = mtype
        self.question = question
        self.id = 0
        self.index = 0

class Command:
    def __init__(self, name:str, success:str, steps:list[Step] = []):
        self.name = name
        self.steps = steps
        self.success = success
        self.index = 0

    def addStep(self,step:Step):
        self.steps.append(step)        

class Bot:
    def __init__(self, token:str, storage_root:str, resp_start:str, resp_cancel:str, resp_help:str, resp_invalid:str, commands:list[Command] = []):
        self.token = token
        self.storage_root = storage_root
        self.commands = commands
        self.resp_start = resp_start
        self.resp_cancel = resp_cancel
        self.resp_help = resp_help
        self.resp_invalid = resp_invalid
    
    def addCommand(self,command:Command):
        self.commands.append(command)

class Generator:
    def generate(self,bot:Bot):
        self.bot = bot
        self.src = ''
        self.assignIds()
        self.generateImports()

    def write(self,code:str):
        self.src += (code + '\n')

    def assignIds(self):
        gid = 1
        commandIdx = 1
        for cmd in self.bot.commands:
            cmd.index = commandIdx
            commandIdx += 1
            stepIdx = 1
            for step in cmd.steps:
                step.index = stepIdx
                stepIdx += 1
                step.id = gid
                gid += 1 
    
    def generateImports(self):
        self.write(importTemplate)

    def generateConstants(self):
        self.write(constantsTemplate)

    def generateConfigs(self):
        code = render(configTemplate,[
            self.bot.token,
            self.bot.storage_root,
            self.bot.resp_cancel,
            self.bot.resp_help,
            self.bot.resp_invalid,
            self.bot.resp_start,
        ])
        self.write(code)

    def generateCommandDef(self,command:Command):
        code = render(commandTemplate,[
            str(command.index),
            command.name,
            str(command.index),
            command.success
        ])
        self.write(code)

    def generateStepDef(self, command:Command, step:Step):
        code = render(commandTemplate,[
            str(command.index),
            str(step.index),
            str(step.id),
            str(command.index),
            str(step.index),
            step.question,
        ])
        self.write(code)

    def generateCommandDefs(self):
        for command in self.bot.commands:
            self.generateCommandDef(command)
            for step in command.steps:
                self.generateStepDef(command, step)
            
    def generateUtils(self):
        self.write(utilTemplate)


if __name__ == "main":
    bot = Bot('TOKEN::38u38i__','./storage','welcome','cancel','help','invalid')
    Generator().generate(bot)