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
            pass
        
        def delete_bases(self):
            pass
        
        def delete_all_bases(self):
            pass
        
        def edit_base(self):
            pass
        
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
        
    