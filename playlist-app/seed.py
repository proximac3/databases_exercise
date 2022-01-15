from models import Playlist, Song, PlaylistSong, db
from app import app

db.drop_all()
db.create_all()

playlist1 = Playlist(name='Bars', description='rap and Hiphop')
playlist2 = Playlist(name='Rock', description='modern day rock and classic rock')

wish = Song(title='Wish you were here', artist='pink Floyd')
nothing = Song(title='Nothing Else Matters', artist='Metallica')
south = Song(title='95.South', artist='J Cole')
mic = Song(title='When I be on the mic', artist='Rakim')

barsList1 = PlaylistSong(playlist_id=1, song_id=3)
barsList2 = PlaylistSong(playlist_id=1, song_id=4)
rocklist1 = PlaylistSong(playlist_id=2, song_id=1)
rocklist2 = PlaylistSong(playlist_id=2, song_id=2)

db.session.add(playlist1)
db.session.add(playlist2)
db.session.commit()

db.session.add(wish)
db.session.add(nothing)
db.session.add(south)
db.session.add(mic)
db.session.commit()

db.session.add(barsList1)
db.session.add(barsList2)
db.session.add(rocklist1)
db.session.add(rocklist2)
db.session.commit()

