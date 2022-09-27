from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page_, name="homepage"),
    path("search_page", views.search_page, name ="search-comics"),
    path("registration", views.registration_page, name="registr"),
    path("signin", views.sign_in, name="sign_in"),
    path("logout", views.logout, name="logout"),
    path("comics<str:comics_title>", views.render_comics, name='comics_render'),
    path("comics<str:comics_title>/author<int:author_id>", views.render_author, name='author_render'),
    path("/author<int:id>/", views.only_author, name='author'),
    path("comics<str:comics_title>/publisher<int:publisher_id>", views.render_publisher, name='publisher_render'),
    path("comics<str:comics_title>/order", views.do_order, name='ordering'),
    path('/order_history/', views.order_history, name="order-history"),
    path('/profile_information/', views.profile, name="profile_information"),
    path('/edit_profile/', views.edit_profile, name="edit_profile"),
    path('/all_comics', views.all_comics_render, name="all_comics"),
    path('/delete_<int:_code_><str:name>/', views.delete_item, name="delete_item"),
    path("/edit_comics/", views.edit_comics, name="edit_comics"),
    path("/all_author/", views.authors, name="authors"),
    path("/search_author/", views.search_author, name="search_author"),
    path("/all_publisher/", views.publishers, name="publishers"),
    path("/publisher<int:id>/", views.only_publisher, name="publisher_page"),
    path("/add_comics", views.add_comics, name="add_comics"),
    path("/add_author/", views.add_author, name="add_author"),
    path("/add_publisher/", views.add_publisher, name="add_publisher"),

    path("edit_comics<int:id>", views.edit_comics, name="edit_comics"),
    path("edit_author<int:id>", views.edit_author, name="edit_author"),
    path("edit_publisher<int:id>", views.edit_publisher, name="edit_publisher"),

    path("manage_order_line<int:id>", views.manage_order_line, name = "manage_order_line"),
    path("order_line", views.see_orderline, name = "see_orderline"),


    ]
