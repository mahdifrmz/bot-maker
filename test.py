from codegen import *

if __name__ == '__main__':
    print(Generator().generate(
        Bot('6107216509:AAGSIEC4W0ReW-pnThSqNwh823O5Hya5shk','storage','-start-','-cancel-','-help-','-invalid-',[
            Command('foo','Yey!',[
                Step('your name?', MESSAGE_TYPE_TEXT),
                Step('your age?', MESSAGE_TYPE_TEXT),
            ]),
            Command('bar','Bee!',[
                Step('description', MESSAGE_TYPE_TEXT),
                Step('video footage', MESSAGE_TYPE_VIDEO),
                Step('audio cover', MESSAGE_TYPE_AUDIO),
            ]),
        ]),
        discoverPlugins(Path('.'))
    ))