from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes

@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:id>")
def show_playlist(id):
    """Show detail on specific playlist."""
    
    #Query playlists
    playlist = Playlist.query.get(id)

    return render_template('playlist.html', playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    #create playlist forms
    form = PlaylistForm()

    #validate submitted form
    if form.validate_on_submit():
        """If submitted form is valid, execute code below"""
        #form data
        name = form.name.data
        description = form.description.data

        #Create new Playlist
        newPlayList = Playlist(name=name, description=description)

        #add new Playlist to database and commit
        db.session.add(newPlayList)
        db.session.commit()

        return redirect('/playlists')
    else:
        return render_template('new_playlist.html', form=form)



##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    
    #query song
    song = Song.query.get(song_id)

    return render_template('song.html', song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:
    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    #songform
    form = SongForm()

    #validate submitted forms
    if form.validate_on_submit():

        # Get data from form 
        title = form.title.data
        artist = form.atrist.data

        #create new song
        newSong = Song(title=title, artist=artist)

        #add song to database and commit
        db.session.add(newSong)
        db.session.commit()

        return redirect('/songs')
    else:
        return render_template('new_song.html', form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    #get existing songs in playlists
    existing_songs = [song.song.title for song in playlist.song]

    # Restrict form to songs not already on this playlist
    songs = [(s.id, s.title) for s in Song.query.all() if s.title not in existing_songs]

    #dynamically set song choices on form
    form.song.choices = songs

    if form.validate_on_submit():
          #Form Data
          song = form.song.data

          #create new song
          newSong = PlaylistSong(playlist_id=playlist.id, song_id=song)

          #add and commit to database
          db.session.add(newSong)
          db.session.commit()

          return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)