#WebMenu v.1.0
#Andrea Franco 19/08/2012
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

import webbrowser, os
import urllib2

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import PeasGtk
from gi.repository import Gtk

DCONF_DIR = 'org.gnome.rhythmbox.plugins.webmenu'
CURRENT_VERSION = '1.0'

class WMConfig(object):
    def __init__(self):
	global services, services_order
        self.settings = Gio.Settings(DCONF_DIR)
	services = self.settings['services'] #'services' is a global variable with all the settings in it
	services_order=self.settings['services-order']

    def get_settings(self):
        return self.settings

    def check_services_order(self):
	global services, services_order
	changed=False #The services order is rewritten only if it is changed by this function
	for service, data in services.items():
		if service not in services_order: 
			services_order.append(service) #If a service is missing from the "service-order" key, it is added at the end
			changed=True
	for service in services_order:
		if service not in services: 
			services_order.remove(service) #If a service is missing from the "services" key, it is also deleted from the "service-order" key
			changed=True
	if changed: self.settings['services-order']=services_order
         
class WMConfigDialog(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'WebMenuConfigDialog'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings(DCONF_DIR)

    def do_create_configure_widget(self):
        dialog = Gtk.VBox()
    	
	vbox=Gtk.VBox(False, 0)
	vbox.set_margin_left(15)
	vbox.set_margin_right(15)
	hbox=Gtk.HBox()

	albumvbox = Gtk.VBox()
	albumlabel = Gtk.Label("<b>Album Submenu:</b>", use_markup=True) #Frome here: 'Album' vertical box    
	albumvbox.pack_start(albumlabel, False, False, 5)
	albumvbox.set_margin_right(15)
        for service in services_order:
	    if services[service][1] is not '': #If the album URL is empty does not display the option
		    check = Gtk.CheckButton(service)
		    check.set_active(services[service][3])
		    check.connect("toggled", self.website_toggled, service, 1)#The last argument, 1, stands for "Album"   
		    albumvbox.pack_start(check, False, False, 0)
	
	albumhseparator = Gtk.HSeparator()
	albumvbox.pack_start(albumhseparator, False, False, 0)
	check = Gtk.CheckButton("All") #The 'All'-album checkbox
        check.set_active(self.settings['other-settings'][1])
	check.connect("toggled", self.other_settings_toggled, 1) #The last argument, 1, stands for "Album"   
	albumvbox.pack_start(check, False, False, 0)
	
        hbox.pack_start(albumvbox, False, False, 0)

	artistlabel = Gtk.Label("<b>Artist Submenu:</b>", use_markup=True) #Frome here: 'Artist' vertical box      
	artistvbox = Gtk.VBox()
	artistvbox.pack_start(artistlabel, False, False, 5)
        artistvbox.set_margin_left(15)
        for service in services_order:
	    if services[service][2] is not '': #If the artist URL is empty does not display the option
		    check = Gtk.CheckButton(service)
		    check.set_active(services[service][4])
	 	    check.connect("toggled", self.website_toggled, service, 2) #The last argument, 2, stands for "Artist"  
		    artistvbox.pack_start(check, False, False, 0)

	artisthseparator = Gtk.HSeparator()
	artistvbox.pack_start(artisthseparator, False, False, 0)
	check = Gtk.CheckButton("All") #The 'All'-artist checkbox
        check.set_active(self.settings['other-settings'][2])
	check.connect("toggled", self.other_settings_toggled, 2) #The last argument, 2, stands for "Album"   
	artistvbox.pack_start(check, False, False, 0)
       
        hbox.pack_start(artistvbox, False, False, 0)
	vbox.pack_start(hbox, False, False, 0)

	check = Gtk.CheckButton("Show the 'Options' item in the Web Menu") #The 'Options' checkbox
        check.set_active(self.settings['other-settings'][0])
	check.connect("toggled", self.other_settings_toggled, 0) #The last argument, 2, stands for the "Options" item
	vbox.pack_start(check, False, False, 10)
	
	manage_button = Gtk.Button("Manage services") #crea il pulsante
	manage_button.connect("clicked", self.manage_window)
	vbox.pack_start(manage_button, False, False, 0)

	update_button = Gtk.Button("Look for updates (Current Version: "+CURRENT_VERSION+")") #crea il pulsante
	update_button.connect("clicked", self.update_search)
	vbox.pack_start(update_button, False, False, 0)

        dialog.pack_start(vbox, True, False, 0)
        dialog.show_all()
        
        return dialog
     
    def website_toggled(self, checkbutton, service, what):
	global services
	data = list(services[service])
	data[what+2] = checkbutton.get_active()
	services[service]= tuple(data)
	#after asigning the new data, you should persist the services
	self.settings['services'] = services

    def website_toggled_from_list(self, checkbutton, path, treeview, what):
	global services
	(model, tree_iter) =  treeview.get_selection().get_selected()
        service = model.get_value(tree_iter,0)
	
	data = list(services[service])
	data[what+2] = not data[what+2]
	model[path][what+2] = data[what+2]
	services[service]= tuple(data)
	#after asigning the new data, you should persist the services
	self.settings['services'] = services

    def other_settings_toggled(self, checkbutton, what):
	options_list=self.settings['other-settings']
	options_list[what] = checkbutton.get_active()
	self.settings['other-settings']=options_list

    def update_search(self, widget, data=None):
    	webbrowser.open("https://github.com/afrancoto/WebMenu/downloads")

    def manage_window(self, widget, data=None):
	self.window = Gtk.Window()
	self.window.set_default_size(1000,300)
	liststore = Gtk.ListStore(str, str, str, bool, bool)
	for service in services_order: liststore.append([service, services[service][1], services[service][2], services[service][3], services[service][4]])
	
	vbox=Gtk.VBox()
	treeview = Gtk.TreeView(liststore)
	treeview.set_cursor(0)
	#treeview.set_mode(Gtk.SELECTION_SINGLE)

	rendererText = Gtk.CellRendererText()
        column_0 = Gtk.TreeViewColumn("Service", rendererText, text=0)
	column_0.set_resizable(True)
	column_0.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_0.set_fixed_width(100)
        treeview.append_column(column_0)

	rendererAlbumCheck = Gtk.CellRendererToggle()
	rendererAlbumCheck.set_property('activatable', True)
	rendererAlbumCheck.connect("toggled", self.website_toggled_from_list, treeview, 1)
	column_1 = Gtk.TreeViewColumn("Album", rendererAlbumCheck, active=3)
	column_1.set_resizable(True)
	column_1.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_1.set_fixed_width(50)
        treeview.append_column(column_1)

	rendererArtistCheck = Gtk.CellRendererToggle()
	rendererArtistCheck.set_property('activatable', True)
	rendererArtistCheck.connect("toggled", self.website_toggled_from_list, treeview, 2)
	column_2 = Gtk.TreeViewColumn("Artist", rendererArtistCheck, active=4)
	column_2.set_resizable(True)
	column_2.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_2.set_fixed_width(50)
        treeview.append_column(column_2)


        column_3 = Gtk.TreeViewColumn("Album URL", rendererText, text=1)
	column_3.set_resizable(True)
	column_3.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_3.set_fixed_width(450)
        treeview.append_column(column_3)
        column_4 = Gtk.TreeViewColumn("Artist URL", rendererText, text=2) 
	column_4.set_resizable(True)
	column_4.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_4.set_fixed_width(450)
        treeview.append_column(column_4)
	

	scroll = Gtk.ScrolledWindow()
    	scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    	scroll.add(treeview)
	
	vbox.pack_start(scroll, True, True, 5)
           
	hbox=Gtk.HBox()
        button_up = Gtk.Button(u'\u2191')
        button_up.connect("clicked", self.change_order, treeview, liststore, 'up')
        hbox.pack_start(button_up, False, False, 0)
            
        button_down = Gtk.Button(u'\u2193')
        button_down.connect("clicked", self.change_order, treeview, liststore, 'down')
        hbox.pack_start(button_down, False, False, 0)

	new_button = Gtk.Button("Add a service")
	new_button.connect("clicked", self.new_service_window, treeview, liststore)
	hbox.pack_start(new_button, False, False, 0)

        delete_button = Gtk.Button('Delete service')
        delete_button.connect("clicked", self.delete_service, treeview, liststore)
        hbox.pack_start(delete_button, False, False, 0)

	done_button = Gtk.Button(stock=Gtk.STOCK_OK)
	hbox.pack_end(done_button, False, False, 0)
	done_button.connect_object("clicked", Gtk.Widget.destroy, self.window)

	vbox.pack_start(hbox, False, True, 5)
	self.window.add(vbox)
	self.window.show_all()
	return
 
    def change_order(self, widget, treeview, liststore, direction):
	#TODO: Need to update the menus
	global services, services_order
	(model, tree_iter) =  treeview.get_selection().get_selected()
        service = model.get_value(tree_iter,0)

	moved_one_index=services_order.index(service)
	if direction is 'down': moved_two_index=moved_one_index + 1
	if direction is 'up': moved_two_index=moved_one_index - 1
	
	services_order[moved_one_index]=services_order[moved_two_index]
	services_order[moved_two_index]=service
	self.settings['services-order']=services_order

	liststore.clear()
	for service in services_order: liststore.append([service, services[service][1], services[service][2], services[service][3], services[service][4]])
	treeview.set_cursor(moved_two_index)
	return

    def new_service_window(self, widget, treeview, liststore):
	self.window = Gtk.Window()

	vbox=Gtk.VBox(False, 0)
	vbox.set_margin_left(15)
	vbox.set_margin_right(15)
	main_label = Gtk.Label("<b>Add a new service:</b>", use_markup=True) #Main label 
	vbox.pack_start(main_label, False, False, 10)
	description_label = Gtk.Label("Make a search on the website you want to add, copy here the URL and replace your query\n"
				      "with the keywords: <b>[ALBUM]</b> and/or <b>[ARTIST]</b>\n"
				      "<i>(If you want the service to show up in only one menu, simply leave the other URL empty.)</i>", use_markup=True) #Description label  
	vbox.pack_start(description_label, False, False, 10)	

	hbox=Gtk.HBox(False, 5)
	
	vbox_labels=Gtk.VBox(False, 7)
 	name_label = Gtk.Label("<b>Service Name:</b>", use_markup=True)
	vbox_labels.pack_start(name_label, True, True, 0)

 	album_url_label = Gtk.Label("<b>Album URL:</b>", use_markup=True)
	vbox_labels.pack_start(album_url_label, True, True, 0)

 	artist_url_label = Gtk.Label("<b>Artist URL</b>", use_markup=True)
	vbox_labels.pack_start(artist_url_label, True, True, 0)
	hbox.pack_start(vbox_labels, False, False, 0)	

	vbox_entries=Gtk.VBox(False, 7)
 	name_entry = Gtk.Entry()
	name_entry.set_width_chars(52)
	name_entry.set_max_length(30)
	name_entry.set_text('')
	vbox_entries.pack_start(name_entry, True, True, 0)

 	album_url_entry = Gtk.Entry()
	album_url_entry.set_max_length(300)
	album_url_entry.set_text('')
	vbox_entries.pack_start(album_url_entry, True, True, 0)

 	artist_url_entry = Gtk.Entry()
	artist_url_entry.set_max_length(300)
	artist_url_entry.set_text('')
	vbox_entries.pack_start(artist_url_entry, True, True, 0)
	hbox.pack_start(vbox_entries, False, False, 0)	
	vbox.pack_start(hbox, False, False, 10)

	bbox = Gtk.HButtonBox()
	bbox.set_border_width(5)
	#bbox.set_layout(gtk.BUTTONBOX_END) <---------------------------------------------- I can't find BUTTONBOX_END in gi.repository! Help! :S
	bbox.set_spacing(10)
	create_button = Gtk.Button(stock=Gtk.STOCK_OK)
	create_button.connect("clicked", self.new_service_add, name_entry, 
	                                                       album_url_entry, 
	                                                       artist_url_entry,
							       treeview, liststore)
	bbox.add(create_button)

	cancel_button = Gtk.Button(stock=Gtk.STOCK_CANCEL)
	bbox.add(cancel_button)
	cancel_button.connect_object("clicked", Gtk.Widget.destroy, self.window)

	#button = Gtk.Button(stock=Gtk.STOCK_HELP) #Future development
	#bbox.add(button)
	vbox.pack_start(bbox, False, False, 0)
        self.window.add(vbox)
	self.window.show_all()
	return

    def new_service_add(self, widget, name, album, artist, treeview, liststore):
        #TODO: dinamically add the checkboxs on the active configuration dialog
	global services, services_order
        service=name.get_text()
	album_URL=album.get_text()
	if (album_URL[:7] != "http://") and (album_URL[:8] != "https://"): album_URL="http://"+album_URL #Adds the http:// if it's not in the URL
	artist_URL=artist.get_text()
	if (artist_URL[:7] != "http://") and (artist_URL[:8] != "https://"): artist_URL="http://"+artist_URL #Adds the http:// if it's not in the URL
	
	if service is not '':
        	services[service] = ('', album_URL, artist_URL , True, True) #Gets the new service
		services_order.append(service)
	
	        self.settings['services'] = services #Writes the new service in dconf
        	self.settings['services-order']=services_order

	liststore.clear()
	for service in services_order: liststore.append([service, services[service][1], services[service][2], services[service][3], services[service][4]])
	treeview.set_cursor(len(services_order)-1)
        self.window.destroy()

    def delete_service(self, widget, treeview, liststore):
	global services, services_order
	(model, tree_iter) =  treeview.get_selection().get_selected()
        service = model.get_value(tree_iter,0)

	question = _("Are you sure you want to delete '"+service+"' from WebMenu?")
    	dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, question) 
    	response = dialog.run()
	os.system("echo "+str(response))
	dialog.destroy()

	if response == Gtk.ResponseType.YES:
	    del services[service]
	    services_order.remove(service)
	    self.settings['services-order']=services_order
	    self.settings['services'] = services
	    
	    liststore.clear()
	    for service in services_order: liststore.append([service, services[service][1], services[service][2], services[service][3], services[service][4]])
	    #treeview.set_cursor(deleted_one_index)
