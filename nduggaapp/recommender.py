import redis
from django.conf import settings
from .models import Product

#connection
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB
)

class Recommender(object):
    
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'
    
    #get the product bought and give it a score each time its bought
    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id),
                    1,
                    with_id)

    #get products bought together and give a suggestion each time one buys one
    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products] #get the ids
        if len(products) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True)[:max_results]
        else:
            #generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)

        #get the new suggested ids
        suggested_products_ids = [int(id) for id in suggestions]
        #get the suggesteds in a list
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        #sort the new products
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    #clear the recommendations
    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
