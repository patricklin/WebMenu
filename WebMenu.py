#WebMenu v.0.4
#Andrea Franco 12/08/2012
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject, RB, Peas, Gtk
import os
import urllib2

web_menu_item = '''
  <ui>
    <menubar name="MenuBar">
      	<menu name="WebMenu" action="WebMenuAction">
        	<menuitem name="YTitem" action="search_on_youtube_action"/>
		<menu name="AlbumMenu" action="album_menu_action">
			<menuitem name="ALWPitem" action="album_wikipedia"/>
			<menuitem name="ALALitem" action="album_allmusic"/>
			<menuitem name="ALGSitem" action="album_discogs"/>
			<menuitem name="ALFBitem" action="album_facebook"/>
			<separator/>
			<menuitem name="AL00item" action="album_all"/>
			<separator/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
			<menuitem name="ARWPitem" action="artist_wikipedia"/>
			<menuitem name="ARALitem" action="artist_allmusic"/>
			<menuitem name="ARGSitem" action="artist_discogs"/>
			<menuitem name="ARFBitem" action="artist_facebook"/>
			<menuitem name="ARMSitem" action="artist_myspace"/>
			<separator/>
			<menuitem name="AR00item" action="artist_all"/>
		</menu>
      	</menu>
    </menubar>
  </ui>
'''

class WebMenuPlugin(GObject.Object, Peas.Activatable):
  __gtype_name__ = 'WebMenuPlugin'
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(WebMenuPlugin, self).__init__()

##########
#The "draw_menu" function creates the 'Web' menu and associates every entry to its specific function
#0.
#  1
#  2.
#    1
#    ...
#    4
#  3.
#    1
#    ...
#    5
##########

  def draw_menu(self, shell): 
    #0. Web Menu
    action_group = Gtk.ActionGroup(name='WebMenuActionGroup')
    web_menu_action = Gtk.Action("WebMenuAction", _("Web"), None, None)
    action_group.add_action(web_menu_action)
    #0.1 Song on Youtube
    youtube_action = Gtk.Action ('search_on_youtube_action', _('Song on Youtube'), _('Look for the current playing song on Youtube'), "")
    youtube_action.connect ('activate', self.search_on_youtube, shell)
    action_group.add_action_with_accel (youtube_action, "<alt>Y")
    action_group.add_action(youtube_action)
    #0.2 Album Menu
    album_menu_action = Gtk.Action("album_menu_action", _("Album"), None, None)
    action_group.add_action(album_menu_action)
    #0.2.1 Album -> Wikipedia
    album_wikipedia_action = Gtk.Action ('album_wikipedia', _('Wikipedia'), _('Look for the current album on Wikipedia'), "")
    album_wikipedia_action.connect ('activate', self.search_on_wikipedia, shell, 1)  #The last argument "1" stands for "Album"
    action_group.add_action(album_wikipedia_action)
    #0.2.2 Album -> AllMusic
    album_allmusic_action = Gtk.Action ('album_allmusic', _('AllMusic'), _('Look for the current album on AllMusic'), "")
    album_allmusic_action.connect ('activate', self.search_on_allmusic, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_allmusic_action)
    #0.2.3 Album -> DiscoGS
    album_discogs_action = Gtk.Action ('album_discogs', _('DiscoGS'), _('Look for the current album on DiscoGS'), "")
    album_discogs_action.connect ('activate', self.search_on_discogs, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_discogs_action)
    #0.2.3 Album -> Facebook
    album_facebook_action = Gtk.Action ('album_facebook', _('Facebook'), _('Look for the current album on Facebook'), "")
    album_facebook_action.connect ('activate', self.search_on_facebook, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_facebook_action)
    #0.2.4 Album -> Every Service
    album_all_action = Gtk.Action ('album_all', _('All'), _('Look for the current album on every service'), "")
    album_all_action.connect ('activate', self.search_on_all, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_all_action)
    #0.3 Artist Menu
    artist_menu_action = Gtk.Action("artist_menu_action", _("Artist"), None, None)
    action_group.add_action(artist_menu_action)
    #0.3.1 Artist -> Wikipedia
    artist_wikipedia_action = Gtk.Action ('artist_wikipedia', _('Wikipedia'), _('Look for the current artist on Wikipedia'), "")
    artist_wikipedia_action.connect ('activate', self.search_on_wikipedia, shell, 2)  #The last argument "2" stands for "Artist"
    action_group.add_action(artist_wikipedia_action)
    #0.3.2 Artist -> AllMusic
    artist_allmusic_action = Gtk.Action ('artist_allmusic', _('AllMusic'), _('Look for the current artist on AllMusic'), "")
    artist_allmusic_action.connect ('activate', self.search_on_allmusic, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_allmusic_action)
    #0.3.3 Artist -> DiscoGS
    artist_discogs_action = Gtk.Action ('artist_discogs', _('DiscoGS'), _('Look for the current artist on DiscoGS'), "")
    artist_discogs_action.connect ('activate', self.search_on_discogs, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_discogs_action)
    #0.3.4 Artist -> Facebook
    artist_facebook_action = Gtk.Action ('artist_facebook', _('Facebook'), _('Look for the current artist on Facebook'), "")
    artist_facebook_action.connect ('activate', self.search_on_facebook, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_facebook_action)
    #0.3.4 Artist -> Myspace
    artist_myspace_action = Gtk.Action ('artist_myspace', _('Myspace'), _('Look for the current artist on Myspace'), "")
    artist_myspace_action.connect ('activate', self.search_on_myspace, shell) #No need to specify what to search
    action_group.add_action(artist_myspace_action)
    #0.3.5 Artist -> Every Service
    artist_all_action = Gtk.Action ('artist_all', _('All'), _('Look for the current artist on every service'), "")
    artist_all_action.connect ('activate', self.search_on_all, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_all_action)
    ui_manager = shell.props.ui_manager
    ui_manager.insert_action_group(action_group)
    self.ui_id = ui_manager.add_ui_from_string(web_menu_item)

##########
#The "do_activate" function is called when Rhythmbox is loaded
##########
  def do_activate(self):
    shell = self.object
    self.draw_menu(shell) #Calls "draw_menu"

    sp=shell.props.shell_player #Connects variuos events to "song_changed"
    sp.connect ('playing-song-changed', self.song_changed)
    sp.connect ('playing-changed', self.song_changed)
    sp.connect ('playing-source-changed', self.song_changed)

##########
#The "do_deactivate" function removes the 'Web' Menu
##########
  def do_deactivate(self):
    shell = self.object
    ui_manager = shell.props.ui_manager
    ui_manager.remove_ui(self.ui_id)

##########
#The "get_metadata" function gets and returns, in order, TITLE, ALBUM and ARTIST of the current playing song as elements of an array (0,1,2)
##########
  def get_metadata(self, shell):
    self.playing_entry = shell.props.shell_player.get_playing_entry()
    playing_title = self.playing_entry.get_string(RB.RhythmDBPropType.TITLE)
    playing_album = self.playing_entry.get_string(RB.RhythmDBPropType.ALBUM)
    playing_artist = self.playing_entry.get_string(RB.RhythmDBPropType.ARTIST)

    result=[playing_title, playing_album, playing_artist]
    return result

##########
#The "search_on_youtube" function search TITLE + ARTIST on youtube
##########
  def search_on_youtube(self, event, shell):
    metadata=self.get_metadata(shell) #Calls "get_metadata"
    command="gnome-open http://www.youtube.com/results?search_query=\"" + urllib2.quote(metadata[0]) + "\"+\"" + urllib2.quote(metadata[2]) + "\""
    os.system(command)

##########
#The "search_on_wikipedia" function search the artist OR the album on wikipedia; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_wikipedia(self, event, shell, what):
    metadata=self.get_metadata(shell) #Calls "get_metadata"
    command="gnome-open http://en.wikipedia.org/w/index.php?search=\"" + urllib2.quote(metadata[what]) + "\""
    os.system(command)

##########
#The "search_on_allmusic" function search the artist OR the album on allmusic; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_allmusic(self, event, shell, what):
    metadata=self.get_metadata(shell) #Calls "get_metadata"
    what_text=['songs', 'albums', 'artists'] #Allmusic uses differt search engines for Songs, Albums and Artists
    command="gnome-open http://www.allmusic.com/search/"+what_text[what]+"/\"" + urllib2.quote(metadata[what]) + "\""
    if what==1: command=command + "+\"" + urllib2.quote(metadata[2]) + "\"" #If you're looking for the album, the artist is added to get better results
    os.system(command)

##########
#The "search_on_discogs" function search the artist OR the album on facebook; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_discogs(self, event, shell, what):
    metadata=self.get_metadata(shell) #Calls "get_metadata"
    what_text=['track', 'release_title', 'artist'] #Allmusic uses differt search engines for Songs, Albums and Artists
    command="gnome-open \"http://www.discogs.com/advanced_search?" + what_text[what] + "=" + urllib2.quote(metadata[what]) + "\""
    if what==1: command=command + "\"&artist=" + urllib2.quote(metadata[2]) + "\"" #If you're looking for the album, the artist is added to get better results
    os.system(command)

##########
#The "search_on_facebook" function search the artist OR the album on facebook; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_facebook(self, event, shell, what):
    metadata=self.get_metadata(shell) #Calls "get_metadata"
    command="gnome-open \"https://www.facebook.com/search/results.php?type=pages&q=" + urllib2.quote(metadata[what]) + "\""
    os.system(command)

##########
#The "search_on_myspace" function search ARTIST on myspace
##########
  def search_on_myspace(self, event, shell):
    metadata=self.get_metadata(shell) #Calls "get_metadata"
    command="gnome-open http://www.myspace.com/search/Music?q=\"" + urllib2.quote(metadata[2]) + "\""
    os.system(command)

##########
#The "search_on_all" function search the artist OR the album on every service; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_all(self, event, shell, what):
    self.search_on_wikipedia('activate', shell, what)
    self.search_on_allmusic('activate', shell, what)
    self.search_on_discogs('activate', shell, what)
    self.search_on_facebook('activate', shell, what)
    if what==2: self.search_on_myspace('activate', shell)

##########
#The "song_changed" function controls if no song is playing. If it is so, the 'Web' menu is hidden.
##########
  def song_changed(self, event, shell):
    shell = self.object
    self.playing_entry = shell.props.shell_player.get_playing_entry()
    
    if self.playing_entry is None:
	shell.props.ui_manager.get_widget("/MenuBar/WebMenu").hide()
    else:
	shell.props.ui_manager.get_widget("/MenuBar/WebMenu").show()
