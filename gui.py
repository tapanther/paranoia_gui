#!/usr/bin/env python3

from cmd import Cmd
from pathlib import Path

class PPrompt(Cmd):
    prompt = 'prce> '

    doc_header = 'Commands:'
    undoc_header = ''

    def do_exit(self, inp):
        return True

    def help_exit(self):
        print('Exit application. Shorthand: x q Ctrl-D')

    # Shorthands
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        return super().default(inp)
        
    # Create "infinite" gui by reprompting with commands
    def preloop(self):
        self.do_help(None)
        
    def postcmd(self, stop, line):
        if not stop:
            self.do_help(None)
        return stop
 
    do_EOF = do_exit
    help_EOF = help_exit



class mainPrompt(PPrompt):
    prompt = 'prce> '
    
    def do_audio(self, inp):
        a_cmd = audioPrompt()
        a_cmd.cmdloop()

    def help_audio(self):
        print('Play an audio track. Shorthand: a')
        
    def default(self, inp):
        if inp == 'a':
            return self.do_audio(inp)

        return super().default(inp)

        

class audioPrompt(PPrompt):
    prompt = 'audio: '

    def __init__(self):
        self.audioPath = Path('./audio')
        self.tracks = {x.stem : x for x in self.audioPath.iterdir() if x.is_file()}
        self.track_list = list(self.tracks.keys())
        self.track_list.sort()
        super().__init__()

    def listTracks(self):
        print('\nTracks:')
        for idx, track in enumerate(self.track_list):
            print(f'  {idx+1:<2d} : {track}')

        print('')

    def play(self, track):
        print(f'\nThis is where {self.track_list[track]} would be played.')
        print(f'  File: {self.tracks[self.track_list[track]]}')

    def do_print(self, inp):
        """Print arguments"""
        print(inp)

    def default(self, inp):
        try:
            track = int(inp)
            if 1 <= track <= len(self.tracks.keys()):
                return self.play(track-1)
        except ValueError:
            pass

        return super().default(inp)
        
    def preloop(self):
        self.listTracks()

    def postcmd(self, stop, line):
        if not stop:
            self.listTracks()
        return stop

    
def main():
    """Run the Paranoia GUI"""

    mainPrompt().cmdloop()

        

if __name__ == '__main__':
    main()
