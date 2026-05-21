from django.contrib import admin
from django.urls import path,include
from adminapp import views

urlpatterns = [
     path('indexview/',views.indexview,name="indexview"),
     path('elementsview/',views.elementsview,name="elementsview"),
     path('layoutsview/',views.layoutsview,name="layoutsview"),
     path('validationview/',views.validationview,name="validationview"),
     path('editorsview/',views.editorsview,name="editorsview"),
     path('contactview/',views.contactview,name="contactview"),
     path('adminregisterview/',views.adminregisterview,name="adminregisterview"),
     path('adminloginview/',views.adminloginview,name="adminloginview"),
     path('tabledataview/',views.tabledataview,name="tabledataview"),
     path('tblgeneralview/',views.tblgeneralview,name="tblgeneralview"),
     path('adminprofileview/',views.adminprofileview,name="adminprofileview"),
     path('adminlogoutview/',views.adminlogoutview,name="adminlogoutview"),
     path('Admindelete/<int:id>/',views.Admindelete,name="Admindelete"),   
     path('AdminUpdate/<int:id>/',views.AdminUpdate,name="AdminUpdate"),


     path('managecategories/',views.managecategories,name="managecategories"),
     path('addcategory/', views.addcategory, name='addcategory'),
     path('updatecategory/<int:category_id>/', views.updatecategory, name='updatecategory'),
     path('deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory'),  # 🔥 NEW  # 🔥 new

     path('adminapp/activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
     path('adminapp/deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
     path('usermanageview/',views.usermanageview,name="usermanageview"),

     path('updatecategoriesview/',views.updatecategoriesview,name="updatecategoriesview"),
     path('addcategoriesview/',views.addcategoriesview,name="addcategoriesview"),
     path('contactmsg/',views.contactmsg,name="contactmsg"),

     path('artistmanageview/', views.artistmanageview, name='artistmanageview'),
     path('activate_artist/<int:artist_id>/', views.activate_artist, name='activate_artist'),
     path('deactivate_artist/<int:artist_id>/', views.deactivate_artist, name='deactivate_artist'),
]
     