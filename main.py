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
commandSingleHandlerTemplate = loadTemplate('command-single-handler')
messageHandlerTemplate = loadTemplate('message-handler')
stepHandlerTemplate = loadTemplate('step-handler')
stepMediaTemplate = loadTemplate('step-media')
stepPhotoTemplate = loadTemplate('step-photo')
stepTextTemplate = loadTemplate('step-text')
stepNextTemplate = loadTemplate('step-next')
stepEndTemplate = loadTemplate('step-end')
handlerBindTemplate = loadTemplate('handler-bind')

RENDER_ERROR = 'number of args must be equal to the number of template place holders'

def render(template:str, args : list[str], place_holder : str = '%'):
    for arg in args:
        if(template.find(place_holder) > -1):
            template = template.replace(place_holder, arg, 1)
        else:
            raise Exception(RENDER_ERROR)
    if(template.find(place_holder) > 1):
        raise Exception(RENDER_ERROR)
    return template

def getMediaTypePropertyName(mtype:int,condition:bool = False) -> str:
    if(mtype == MESSAGE_TYPE_TEXT):
        return 'text'
    elif(mtype == MESSAGE_TYPE_DOC):
        return 'document'
    elif(mtype == MESSAGE_TYPE_AUDIO):
        return 'audio'
    elif(mtype == MESSAGE_TYPE_VIDEO):
        return 'video'
    elif(condition):
        return 'photo != None and len(message.photo) > 0 and message.photo[-1] != None'
    else:
        return 'message.photo[-1]'
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
    def generate(self,bot:Bot) -> str:
        self.bot = bot
        self.src = ''
        self.assignIds()
        self.generateImports()
        self.generateConstants()
        self.generateConfigs()
        self.generateCommandDefs()
        self.generateUtils()
        self.generateBasicHandlers()
        self.generateCommandHandlers()
        self.generateMessageHandler()
        self.generateMain()
        return self.src


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
            repr(self.bot.token),
            repr(self.bot.storage_root),
            repr(self.bot.resp_cancel),
            repr(self.bot.resp_help),
            repr(self.bot.resp_invalid),
            repr(self.bot.resp_start),
        ])
        self.write(code)

    def generateCommandDef(self,command:Command):
        code = render(commandTemplate,[
            str(command.index),
            repr(command.name),
            str(command.index),
            repr(command.success)
        ])
        self.write(code)

    def generateStepDef(self, command:Command, step:Step):
        code = render(stepTemplate,[
            str(command.index),
            str(step.index),
            str(step.id),
            str(command.index),
            str(step.index),
            repr(step.question),
        ])
        self.write(code)

    def generateCommandDefs(self):
        for command in self.bot.commands:
            self.generateCommandDef(command)
            for step in command.steps:
                self.generateStepDef(command, step)
            
    def generateUtils(self):
        self.write(utilTemplate)

    def generateCommandHandlers(self):
        for command in self.bot.commands:
            if(len(command.steps) == 0):
                code = render(commandSingleHandlerTemplate,[
                    str(command.index),
                    str(command.index),
                ])
                self.write(code)
            else:
                code = render(commandHandlerTemplate,[
                    str(command.index),
                    str(command.index), '1',
                    str(command.index), '1',
                ])
                self.write(code)

    def isLast(self,command: Command, step: Step) -> bool:
        return len(command.steps) > 0 and command.steps[-1] == step
    
    def getDataBlock(self,command: Command, step: Step):
        getDataBlock = ''
        if (step.mtype == MESSAGE_TYPE_TEXT):
            getDataBlock = stepTextTemplate
        elif (step.mtype == MESSAGE_TYPE_IMAGE):
            getDataBlock = stepPhotoTemplate
        else:
            getDataBlock = render(stepMediaTemplate,[
                getMediaTypePropertyName(step.mtype)
            ])
        return getDataBlock
    
    def getTransitionBlock(self,command: Command, step: Step):
        transitionBlock = ''
        if (self.isLast(command,step)):
            transitionBlock = render(stepEndTemplate,[
                str(command.index)
            ])
        else:
            transitionBlock = render(stepNextTemplate,[
                str(command.index),
                str(step.index + 1),
                str(command.index),
                str(step.index + 1),
            ])
        return transitionBlock

    def generateMessageHandler(self):
        body = ''
        for command in self.bot.commands:
            for step in command.steps:
                getDataBlock = self.getDataBlock(command,step)
                transitionBlock = self.getTransitionBlock(command,step)
                code = render(stepHandlerTemplate,[
                    str(command.index),
                    str(step.index),
                    getMediaTypePropertyName(step.mtype,True),
                    getDataBlock + transitionBlock
                ])
                body += code
        code = render(messageHandlerTemplate,[body])
        self.write(code)

    def generateBasicHandlers(self):
        self.write(basicHandlerTemplate)

    def generateMain(self):
        bindings = ''
        for command in self.bot.commands:
            index = str(command.index)
            bindings += render(handlerBindTemplate,[
                index,
                index,
                index,
                index,
            ])
        code = render(mainTemplate,[bindings],'$')
        self.write(code)

if __name__ == "__main__":
    bot = Bot('TOKEN::38u38i__','./storage','welcome','cancel','help','invalid',[
        Command('foo','foo suc',[
            Step('name the foo',MESSAGE_TYPE_TEXT),
            Step('send foo vid',MESSAGE_TYPE_VIDEO),
            Step('send foo aud',MESSAGE_TYPE_AUDIO),
        ]),
        Command('bar','bar suc',[
            Step('name the bar',MESSAGE_TYPE_TEXT),
            Step('send bar code',MESSAGE_TYPE_TEXT),
        ]),
    ])
    src = Generator().generate(bot)
    print(src)