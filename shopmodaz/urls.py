from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("search/", views.search, name="search"),
    path("search1/", views.search1, name="search1"),
    path('contact/', views.contact, name='contact'),
    # path("shop", views.shop, name="shop"),

    path("loadWishlist", views.loadWishlist, name="loadWishlist"),
    path("inserWishlist", views.inserWishlist, name="inserWishlist"),
    path("deleteWishlist", views.deleteWishlist, name="deleteWishlist"),

    path("loadProductdesc", views.loadProductdesc, name="loadProductdesc"),
    # path("insertProductdesc", views.insertProductdesc, name="insertProductdesc"),


    # path("men", views.men, name="men"),
    # path("topwear", views.topwear, name="topwear"),
    path("filterProductType", views.filterProductType, name="filterProductType"),
    # path("filterProductSubCat", views.filterProductSubCat, name="filterProductSubCat"),
    # path("filterProductCat", views.filterProductCat, name="filterProductCat"),

    path("admin/loadDashbord", views.adminLoadDashbord, name="adminLoadDashbord"),
    path("admin/loadValidation", views.adminLoadValidation, name="loadValidation"),
    path("admin/loadDatabase", views.adminLoadDatabase, name="adminLoadDatabase"),
    path("admin/viewUser", views.adminViewUser, name="adminViewUser"),

    path("changeStatus/<str:foo>", views.changeStatus, name="changeStatus"),

    path("admin/viewAdmin", views.adminViewAdmin, name="adminViewAdmin"),
    path("admin/editAdmin", views.adminEditAdmin, name="adminEditAdmin"),
    path("admin/updateAdmin", views.adminUpdateAdmin, name="adminUpdateAdmin"),
    path("admin/insertAdmin", views.adminInsertAdmin, name="adminInsertAdmin"),
    path("admin/loadAdmin", views.adminLoadAdmin, name="adminLoadAdmin"),
    path("admin/deleteAdmin", views.adminDeleteAdmin, name="adminDeleteAdmin"),

    path("admin/viewCategory", views.adminViewCategory, name="adminViewCategory"),
    path("admin/insertCategory", views.adminInsertCategory, name="adminInsertCategory"),
    path("admin/deleteCategory", views.adminDeleteCategory, name="adminDeleteCategory"),
    path("admin/editCategory", views.adminEditCategory, name="adminEditCategory"),
    path("admin/updateCategory", views.adminUpdateCategory, name="adminUpdateCategory"),

    path("admin/viewSubcategory", views.adminViewSubcategory, name="adminViewSubcategory"),
    path("admin/insertSubcategory", views.adminInsertSubCategory, name="adminInsertSubCategory"),
    path("admin/deleteSubcategory", views.adminDeleteSubcategory, name="adminDeleteSubcategory"),
    path("admin/editSubcategory", views.adminEditSubcategory, name="adminEditSubcategory"),
    path("admin/updateSubcategory", views.adminUpdateSubcategory, name="adminUpdateSubcategory"),

    path("admin/viewType", views.adminViewType, name="adminViewType"),
    path("admin/insertType", views.adminInsertType, name="adminInsertType"),
    path("admin/deleteType", views.adminDeleteType, name="adminDeleteType"),
    path("admin/editType", views.adminEditType, name="adminEditType"),
    path("admin/updateType", views.adminUpdateType, name="adminUpdateType"),
    path("admin/ajaxSubcategory", views.adminAjaxSubcategory, name="adminAjaxSubcategory"),

    path("admin/loadProduct", views.adminLoadProduct, name="adminLoadProduct"),
    path("admin/viewProduct", views.adminViewProduct, name="adminViewProduct"),
    path("admin/deleteProduct/<str:foo>", views.adminDeleteProduct, name="adminDeleteProduct"),
    path("admin/insertProduct", views.adminInsertProduct, name="adminInsertProduct"),
    path("admin/editProduct/<str:foo>", views.adminEditProduct, name="adminEditProduct"),
    path("admin/updateProduct", views.adminUpdateProduct, name="adminUpdateProduct"),
    path("admin/deleteImage", views.adminDeleteImage, name="adminDeleteImage"),

    path("admin/loadDataset", views.adminLoadDataset, name="adminLoadDataset"),
    path("admin/insertDataset", views.adminInsertDataset, name="adminInsertDataset"),

    path("admin/loadBenner", views.adminLoadBenner, name="adminLoadBenner"),
    path("admin/insertBenner", views.adminInsertBenner, name="adminInsertBenner"),
    path("admin/viewBenner", views.adminViewBenner, name="adminViewBenner"),
    path("admin/deleteBenner", views.adminDeleteBenner, name="adminDeleteBenner"),
    path("admin/editBenner", views.adminEditBenner, name="adminEditBenner"),
    path("admin/updateBenner", views.adminUpdateBenner, name="adminUpdateBenner"),

    path("admin/viewOrder", views.adminViewOrder, name="adminViewOrder"),
    path("admin/orderStatus/<str:foo>", views.adminOrderStatus, name="adminOrderStatus"),

]
