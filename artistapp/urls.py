from django.contrib import admin
from django.urls import path,include
from artistapp import views

urlpatterns = [
     path('artistindexview/',views.artistindexview,name="artistindexview"),
     # path('artistindex2view/',views.artistindex2view,name="artistindex2view"),
     path('formbasicview/',views.formbasicview,name="formbasicview"),
     path('basictableview/',views.basictableview,name="basictableview"),
     path('datatableview/',views.datatableview,name="datatableview"),
     path('update/<int:id>/', views.artist_update_view, name='artistupdate'),
     path('delete/<int:id>/', views.artist_delete_view, name='artistdelete'), 
     path('artistprofileview/',views.artistprofileview,name="artistprofile"),
     path('artistloginview/',views.artistloginview,name="artistloginview"),
     path('artistlogoutview/',views.artistlogoutview,name="artistlogoutview"),
     path('artistregisterview/',views.artistregisterview,name="artistregisterview"),
     path('artmanagecategories/',views.artmanagecategories,name="artmanagecategories"),
     path('artupdatecategory/<int:category_id>/', views.artupdatecategory, name='artupdatecategory'),
     path('artdeletecategory/<int:category_id>/', views.artdeletecategory, name='artdeletecategory'),
     path('artaddcategory/',views.artaddcategory,name="artaddcategory"),
      
]