import os.path

class FileHandler:

    def __init__(self) -> None:
        self.path = './files/favorites.csv'
        check_file = os.path.isfile(self.path)

        if check_file:
            pass
        else:
            open(self.path, 'w').close()

    def get_favorites(self):   

        with open(self.path) as favorites_file:

            new_list = []
            for fav in favorites_file:
                fav = fav.strip()
                fav = fav.upper()
                new_list.append(fav)
            favorites_file.close()
        
        new_list.sort()
        
        return new_list

        #Adds new location in the favorites file
    def add_favorites(self, location: str):

        with open(self.path, 'a') as favorites_file:
            favorites_file.write(location + "\n")
        favorites_file.close()

        #Removes selected favorite by overwriting original file without chosen location
    def remove_favorite(self, location):

            new_list = [item for item in self.get_favorites() if item != location.upper()]

            with open(self.path, 'w') as favorites_file:

                for item in new_list:
                    favorites_file.write(item + '\n')
            
            favorites_file.close()