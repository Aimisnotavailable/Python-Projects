import pygame

# Current Agent's reflexes
mood_list = ['Happy', 'Frown', 'Sad', 'Angry', 'Neutral']

action_dict = {
            'Happy' : 'Smile',
            'Frown' : 'Frown',
            'Sad'   : 'Cry',
            'Angry' : 'Shout',
            'Neutral' : 'Roll eyes',
}

class Avatar:
    
    def __init__(self, game, size=(50, 50)) -> None:
        self.game = game
        self.size = list(size)
        self.mood_list = mood_list
        self.actions = action_dict
        self.current_mood = 'Neutral'
        self.animation = self.game.assets['avatar' + '/' + self.current_mood]
        self.mood = 0
        self.mood_interval = 100

    # Function to manage hitboxes
    # Makes sure that the avatar stays on the middle of the display    
    def rect(self) -> pygame.Rect:
        img_rect = self.animation.img().get_rect(center=(self.game.display.get_width() // 2, self.game.display.get_height() // 2))
        return pygame.Rect(img_rect[0], img_rect[1], self.size[0], self.size[1])
    
    # Sets the mood by comparing previous mood
    # Should only be updated if there is a change in mood else the avatar animation will be stuck at frame 0
    def set_mood(self, mood) -> None:

        if self.current_mood != mood:
            self.current_mood = mood
            self.animation = self.game.assets['avatar' + '/' + self.current_mood].copy()

    # Updates the mood depending on user's action
    # If the user touches the avatar the mood decreases capping at (-1 * mood_interval) or 1 index below interval
    # Else the avatar mood increases capping at (1 + total number of moods) * mood_interval
    # P.S. len() function already account for the + 1    

    def update(self, update_mood=True) -> None:

        if update_mood:
            self.mood = min((len(self.mood_list)) * self.mood_interval, self.mood + 1)
        else:
            self.mood = max(-self.mood_interval, self.mood - 1)

        mood = self.mood_list[max(0, min((self.mood), (len(self.mood_list) - 1) * self.mood_interval) // self.mood_interval)]
        self.set_mood(mood)

    def render(self, surf) -> None:
        surf.blit(self.animation.img(), self.rect())
        self.animation.update()
        