from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

handler500 = "pmdunity.views.error500"

urlpatterns = patterns('',
    url(r'^$', 'pmdunity.views.index'),
    
    # Account Functions
    url(r'^login$', 'pmdunity.views.login'),
    url(r'^logout$', 'pmdunity.views.logout'),
    url(r'^account/manage$', 'pmdunity.views.account_manage'),
    
    # Team Functions
    url(r'^pokemon/delete$', 'pmdunity.views.pokemon_delete'),
    url(r'^team/actions/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.team_actions'),
    url(r'^team/delete$', 'pmdunity.views.team_delete'),
    url(r'^team/manage$', 'pmdunity.views.team_manage'),
    url(r'^team/set/(?P<id>[0-9]+)$', 'pmdunity.views.team_set'),
    url(r'^team/inventory/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.team_inventory'),
    url(r'^team$', 'pmdunity.views.team'),
    url(r'^team/view/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.team', {"read_only":True}),
    url(r'^team/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.team'),
    
    # Deprecated Functions
    #url(r'^team/view/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.team_view'),
    #url(r'^pokemon/create/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.pokemon_create'),
    #url(r'^pokemon/edit/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.pokemon_edit'),
    #url(r'^team/create$', 'pmdunity.views.team_create'),
    #url(r'^team/edit/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.team_edit'),
    url(r'^pokemon/create/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.team'),
    url(r'^pokemon/edit/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.team'),
    url(r'^team/create$', 'pmdunity.views.team'),
    url(r'^team/edit/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.team'),
    
    # Logbook Functions
    url(r'^logbook/arrange/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.logbook_arrange'),
    url(r'^logbook/bookmarks$', 'pmdunity.views.logbook_bookmarks'),
    url(r'^logbook/browse/(?P<key>[0-9A-Za-z_-]+)$', 'pmdunity.views.logbook_browse'),
    url(r'^logbook/browse$', 'pmdunity.views.logbook_browse'),
    url(r'^logbook/create/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.logbook_create'),
    url(r'^logbook/delete/(?P<id>[0-9]+)$', 'pmdunity.views.logbook_delete'),
    url(r'^logbook/view/(?P<id>[0-9]+)/(.*)$', 'pmdunity.views.logbook_view'),
    
    # Dungeon Functions
    url(r'^dungeon/browse$', 'pmdunity.views.dungeon_browse'),
    #url(r'^dungeon/map/(?P<seed>[A-Za-z0-9-]+)/(.*)$', 'pmdunity.views.dungeon_explore', {"read_only":True}),
    #url(r'^dungeon/explore/(?P<dungeon_id>[0-9]+)/(.*)/(?P<floor>[0-9]+)$', 'pmdunity.views.dungeon_explore'),
    url(r'^dungeon/explore/(?P<dungeon_id>[0-9]+)/(.*)$', 'pmdunity.views.dungeon_explore'),
    url(r'^dungeon/faq$', 'pmdunity.views.generic', {"template":"dungeons/faq.html"}),
    url(r'^dungeon/reroll$', 'pmdunity.views.dungeon_reroll'),
    url(r'^dungeon/view/(?P<dungeon_id>[0-9]+)/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.dungeon_view'),
    url(r'^dungeon/view/map/(?P<map_id>[0-9]+)/(.*)$', 'pmdunity.views.dungeon_view'), # Admin specific map
    url(r'^dungeon/view/map/(?P<map_id>[0-9]+)$', 'pmdunity.views.dungeon_view'), # Admin specific map
    
    # Actions
    #url(r'^equip/(?P<team_id>[0-9]+)/(.*)$', 'pmdunity.views.equip'),
    url(r'^ability/(?P<inv_id>[0-9]+)$', 'pmdunity.views.ability'),
    url(r'^evolve/(?P<inv_id>[0-9]+)$', 'pmdunity.views.evolve'),
    url(r'^open/(?P<inv_id>[0-9]+)$', 'pmdunity.views.open_item'),
    url(r'^set_stats/(?P<pokemon_id>[0-9]+)/(.*)$', 'pmdunity.views.set_stats'),
    url(r'^tm/(?P<inv_id>[0-9]+)$', 'pmdunity.views.tm'),
    
    # Search
    url(r'^search$', 'pmdunity.views.search'),
    
    # Shop
    url(r'^shop$', 'pmdunity.views.shop'),
    url(r'^shop/buy/customization$', 'pmdunity.views.customization'),
    url(r'^shop/buy/(?P<item_id>[0-9]+)$', 'pmdunity.views.buy'),
    
    # Misc
    url(r'^misc$', 'pmdunity.views.misc'),
    url(r'^changes$', 'pmdunity.views.generic', {"template":"misc/changes.html"}),
    url(r'^credits$', 'pmdunity.views.credits'),
    url(r'^contributors$', 'pmdunity.views.contributors'),
    url(r'^faq$', 'pmdunity.views.generic', {"template":"misc/faq.html"}),
    url(r'^locations$', 'pmdunity.views.generic', {"template":"misc/locations.html"}),
    url(r'^storehouse$', 'pmdunity.views.storehouse'),
    
    #Stats
    url(r'^stats$', 'pmdunity.views.generic', {"template":"stats/stats.html"}),
    url(r'^stats/logbooks$', 'pmdunity.views.logbooks'),
    url(r'^stats/population$', 'pmdunity.views.population'),
    
    # AJAX
    url(r'^ajax/get_item$', 'pmdunity.ajax.get_item'),
    url(r'^ajax/get_resources/(?P<map_id>-?[0-9]+)$', 'pmdunity.ajax.get_resources'),
    url(r'^ajax/get_teams_map/(?P<team_id>-?[0-9]+)/(?P<key_id>-?[0-9A-Za-z-]+)$', 'pmdunity.ajax.get_team_map'),
    url(r'^ajax/get_species/(?P<species_id>-?[0-9]+)$', 'pmdunity.ajax.get_species'),
    url(r'^ajax/submit_approval$', 'pmdunity.ajax.submit_approval'),
    url(r'^ajax/validate_logbook$', 'pmdunity.ajax.validate_logbook'),
    
    # Approvals
    url(r'^approval/resubmit$', 'pmdunity.views.resubmit'),
    url(r'^approval/undo$', 'pmdunity.views.undo'),

    # Administration
    url(r'^admin$', 'pmdunity.views.admin'),
    url(r'^admin/add-event$', 'pmdunity.views.add_event'),
    url(r'^admin/account_transfer$', 'pmdunity.views.account_transfer'),
    url(r'^admin/approvals$', 'pmdunity.views.approvals'),
    url(r'^admin/dungeons$', 'pmdunity.views.dungeons'),
    url(r'^admin/dungeons/design$', 'pmdunity.views.dungeon_design'),
    url(r'^admin/dungeons/entity$', 'pmdunity.views.dungeon_entity'),
    #url(r'^admin/manage-events$', 'pmdunity.views.manage_events'),
    #url(r'^admin/manage-inventory$', 'pmdunity.views.manage_inventory'),
    url(r'^admin/manage-items$', 'pmdunity.views.manage_items'),
    url(r'^admin/manage-items/new$', 'pmdunity.views.manage_items', {'item_id':'-1'}),
    url(r'^admin/manage-items/(?P<item_id>[0-9]+)$', 'pmdunity.views.manage_items'),
    url(r'^admin/manage-merits-strikes$', 'pmdunity.views.manage_merits_strikes'),
    url(r'^admin/manage-star-coins$', 'pmdunity.views.manage_star_coins'),
    url(r'^admin/manage-star-coins/(?P<team>[0-9]+)$', 'pmdunity.views.manage_star_coins'),
    url(r'^admin/powerless$', 'pmdunity.views.powerless'),
    url(r'^admin/reward_teams$', 'pmdunity.views.reward_teams'),
    url(r'^admin/site-log$', 'pmdunity.views.site_log'),
    url(r'^admin/timeline$', 'pmdunity.views.timeline'),
    url(r'^admin/transaction-log$', 'pmdunity.views.transaction_log'),
    #url(r'^admin/twitter$', 'pmdunity.views.twitter'),
    url(r'^admin/verify_logbooks$', 'pmdunity.views.verify_logbooks'),
    
    
    # Errors
    url(r'^error/(?P<type>.*)$', 'pmdunity.views.error'),
    
    # Test
    url(r'^test$', 'pmdunity.views.test'),
)

if settings.ENV == "DEV":
    urlpatterns += patterns('', (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))