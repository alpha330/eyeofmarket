from shop.models import ProductModel



class ProductCountsManagement:
        
    def stock_updates(product_id,quantity):
        product = ProductModel.objects.get(id=product_id)
        if product.stock != 0 :
            product.decrease_stock(quantity=quantity)
            return "approved"
        else:
            return "not approved"
        
    def return_to_stock(product_id,quantity):
        product = ProductModel.objects.get(id=product_id)
        product.back_to_stock(quantity=quantity)