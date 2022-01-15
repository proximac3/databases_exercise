"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Playlist(db.Model):
    """Playlist."""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    song = db.relationship('PlaylistSong')

    def __repr__(self):
        p = self
        return f"<Playlist Name= {p.name} description={p.description}>"
    # ADD THE NECESSARY CODE HERE


class Song(db.Model):
    """Song."""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    artist = db.Column(db.String(), nullable=False)

    pl = db.relationship('PlaylistSong')
    # ADD THE NECESSARY CODE HERE


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "playlists_songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))

    song = db.relationship('Song', backref='playlists_songs')
    plist = db.relationship('Playlist', backref='playlists_songs')

    # ADD THE NECESSARY CODE HERE


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
