from .serializers import BaseSerializer, ProductSerializer, OrderSerializer
from .models import Product, Base

class EventHandler:
    def __init__ (self, request):
        self.data = request.data
        self.request = request
        self.request_return = {
            "request_event": None,
            "data": None,
            "message": None,
            "error": None
        }
        self.base_event_handler = self.BaseEventHandler(request, self.request_return)
        self.product_event_handler = self.ProductEventHandler(request, self.request_return)
        # self.order_event_handler = self.OrderEventHandler(request, self.request_return)
    

    class BaseEventHandler:   
        def __init__(self, request, request_return):
            self.query = Base.objects
            self.data = request.data
            self.request = request
            self.request_return = request_return
            self.base_serializer = BaseSerializer
        
        def add_base (self):
            # set request_event
            self.request_return["request_event"] = self.request.data.get("request_event", None)
            
            # print({**self.data}.get("base_price"))
            # print(self.data.get("base_group"))
            print(self.data)
            
            # store data
            serializer = self.base_serializer(data=self.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                self.request_return["data"] = serializer.data
                self.request_return["message"] = "Data went through."
            else:
                print(serializer.errors)
                
        
            return self.request_return
            
        
        def delete_base(self):
            item_code = self.request.data.get("item_code", None)
            item = self.query.filter(base_code=item_code)
            self.request_return["request_event"] = "delete_single"
            if item.exists():
                item.delete()
                self.request_return["message"] = "The item has been deleted."
            else:
                self.request_return["message"] = "The item does not exist."
                self.request_return["error"] = "Not Found"
            return self.request_return
      
        def delete_bases(self):
            self.request_return["request_event"] = self.request.data.get("request_event", None)
            item_codes = self.request.data.get("item_codes", None)
            items = self.query.filter(base_code__in=item_codes)
            if items.exists():
                items.delete()
                self.request_return["message"] = "The items have been deleted."
            else: 
                self.request_return["message"] = "The items do not exist."
                self.request_return["error"] = "Not Found"
            return self.request_return
        
        def delete_all_bases(self):
            self.request_return["request_event"] = self.request.data.get("request_event", None)
            item_codes = self.request.data.get("item_codes", None)
            items = self.query.all()
            if items.exists():
                items.delete()
                self.request_return["message"] = "The items have been deleted."
            else: 
                self.request_return["message"] = "The items do not exist."
                self.request_return["error"] = "Not Found"
            return self.request_return
       
        
        def edit_base(self):
            # set request_event
            self.request_return["request_event"] = self.request.data.get("request_event", None)
            
            # print({**self.data}.get("base_price"))
            # print(self.data.get("base_group"))
            print(self.data)
            
            # store data
            serializer = self.base_serializer(data=self.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.update()
                self.request_return["data"] = serializer.data
                self.request_return["message"] = "Data went through."
            else:
                self.request_return["message"] = "The items do not exist."
                self.request_return["error"] = "Not Found"
                
        
            return self.request_return
            
        
        def get_bases(self, key):
            pass
        
        def get_all_bases(self):
            # set request_event
            self.request_return["request_event"] = "get_all_bases"
            self.request_return["data"] = self.base_serializer(self.query.all(), many=True).data 
            self.request_return["message"] = "Collected all bases"
            
            return self.request_return
        
        
        
    class ProductEventHandler:
        def __init__(self, request, request_return):
            self.request = request
            self.data = request.data
            self.request_return = request_return
            self.product_serializer = ProductSerializer
        
        def add_product(self):
            self.request_return["request_event"] = "add_product"
            
            # print({**self.data}.get("base_price"))
            # print(self.data.get("base_group"))
            print(self.data)
            
            # store data
            serializer = self.product_serializer(data=self.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                # serializer.save()
                self.request_return["data"] = serializer.data
                self.request_return["message"] = "Data went through."
            else:
                print(serializer.errors)
                self.request_return["message"] = "Data didn't go through."
                self.request_return["error"] = "Check Dev Log for more information"
        
            return self.request_return
        
        def add_products(self):
            pass
        
        def delete_product(self):
            pass
        
        def edit_product(self):
            pass
        
        def get_product(self):
            pass
        
        def get_products(self):
            pass
        
        def get_all_products(self):
            pass
        
    class OrderEventHandler:
        def __init__(self, request):
            self.request = request
        
        def add_order(self):
            pass
        
        def delete_order(self):
            pass
        
        def delete_orders(self):
            pass
        
        def edit_order(self):
            pass
        
        def get_orders(self):
            pass
        
        def get_all_orders(self):
            pass
        
    