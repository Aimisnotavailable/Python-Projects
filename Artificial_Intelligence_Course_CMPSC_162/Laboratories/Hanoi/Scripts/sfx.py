class SoundMixer:

    def __init__(self, assets):
        self.assets = assets
        self.playing = []

    def play(self, s_type, variant=0, loop=-1, vol=1.0):
        self.assets[s_type][variant].play(loop)
        self.assets[s_type][variant].set_volume(vol)
        self.playing.append([s_type, variant])

    def check(self):
        if self.playing:
            if self.assets[self.playing[0][0]][self.playing[0][1]]:
                temp = self.playing[0]
                self.playing.pop()
                return temp
        return []
    
    def stop(self, s_type='', variant=0, stop_all=False):
        if stop_all:
            if s_type != '':
                sfx = self.assets[s_type]
                for i in range(len(sfx)):
                    sfx[i].stop()
            else:
                for sound_type in self.assets:
                    sfx = self.assets[sound_type]
                    for i in range(len(sfx)):
                        sfx[i].stop()
        else:
            self.assets[s_type][variant].stop()