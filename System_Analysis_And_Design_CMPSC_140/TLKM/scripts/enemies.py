from scripts.entities import NonobjEntities


class Enemy(NonobjEntities):

    def __init__(self, game, e_type='enemy', pos=..., size=...):
        self.running = 0
        super().__init__(game, 'enemy', pos, size)
        self.set_action('idle')