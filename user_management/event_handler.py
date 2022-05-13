from pizzaordering.event_handler import EventHandler
from .serializers import NewUserSerializer

class EventHandler(EventHandler):
    def __init__ (self, request):
        super().__init__(request)
        self.user_event_handler = self.UserEventHandler(request, self.request_return)
        
    class Handler:
        def __init__(self, request, request_return):
            self.data = request.data
            self.request = request
            self.request_return = request_return

    class UserEventHandler:
        def __init__(self, request, request_return):
            self.data = request.data
            self.request = request
            self.request_return = request_return
            self.user_serializer = NewUserSerializer
            
        def login_handler(self):
            pass
        
        def register_handler(self):
            self.request_return["request_event"] = "register_user"
            
            serializer = self.user_serializer(data=self.data)
            
            if serializer.is_valid():
                serializer.save()
                self.request_return["data"] = None
                self.request_return["message"] = "register user successfully!"
                
            else:
                self.request_return["message"] = "register user successfully!"
                self.request_return["error"] = "register failed!"
                
            return self.request_return
        
        def get_user_info(self):
            self.request_return["request_event"] = "get_user_infor"
            self.request_return["data"] = self.user_serializer(self.data).data
            self.request_return["message"] = "Get data successfully!"
   
            return self.request_return
            

    
    