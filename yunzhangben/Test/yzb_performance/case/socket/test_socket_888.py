from locust import Locust, events, task, TaskSet
import websocket
import time,random,json
 
class WebSocketClient():
    def __init__(self, host):
        self.host = host
        # self.port = port
 
class WebSocketLocust(Locust):
    def __init__(self, *args, **kwargs):
        self.client = WebSocketClient("ws://172.20.100.111:12345/ws")
 
class UserBehavior(TaskSet):
 
    @task(1)
    def buy(self):
        try:
            self.ws = websocket.WebSocket()
            number = random.randint(111,999)
            socket_url = "ws://172.20.100.111:12345/ws?passport=2&orderid={}&ruid=12&type=buy&num=123123".format(number)
            # print("socket_url",socket_url)
            self.ws.connect(socket_url)
            start_time = time.time()
            obj = {
                "url": "/buy",
                "data":{
                    "id":"123",
                    "date":time.strftime('%Y%m%d',time.localtime(time.time())),
                    "orderid":number
                }
            }

            self.ws.send(json.dumps(obj))
            while True:
                resultStr = self.ws.recv()
                result = json.loads(resultStr)
                if 'msg_type' in result:
                    print("接收到了数据{}".format(result))
                    time.sleep(random.randint(10,30))
                    self.ws.send(json.dumps(obj))
                    print("发送了数据===={}".format(json.dumps(obj)))
                else:
                    print("没有接收到数据！！！")
        except Exception as e:
        # except xmlrpclib.Fault as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="tcp", name="buy", response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="tcp", name="buy", response_time=total_time,
                                        response_length=0)
 
class ApiUser(WebSocketLocust):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
    host = ""