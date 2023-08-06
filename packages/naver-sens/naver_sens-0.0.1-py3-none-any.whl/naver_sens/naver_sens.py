# security protocol
import hashlib
import hmac
import base64
import requests
import time
import json
# path control
from pathlib import Path
import os
# reserveTime
import datetime

class SensClient:
  """
  Naver Cloud Platform SENS(Simple & Easy Notification Service) python wrapper\n
  Reference : https://api.ncloud-docs.com/docs/ai-application-service-sens-smsv2\n
  Guide : https://codedbyjst.tistory.com/10\n
  To use this class, 3 parameters must be provided.\n
  [service_id] : service id of project. Can be found in https://console.ncloud.com/sens/project\n
  [access_key] : access key for Naver Cloud Platform. Can be found in https://www.ncloud.com/mypage/manage/authkey\n
  [secret_key] : secret key for Naver Cloud Platform(provided together with accesss key)
  """
  def __init__(self, 
    service_id: str,
    access_key: str,
    secret_key: str
    ):
    self.service_id = service_id
    self.access_key = access_key
    self.secret_key = secret_key
    self.from_num = None

  def generate_timestamp(self):
    """
    According to NCloud API V2, x-ncp-apigw-timestamp header must be set to use API.
    This function generates the timestamp(type string) for that.
    """
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    return timestamp
    
  def genereate_signature(self, method: str, timestamp: str, uri: str):
    """
    Reference : https://api.ncloud-docs.com/docs/common-ncpapi\n
    According to NCloud API V2, x-ncp-apigw-signature-v2 header must be set to use API.
    This function generates the signature(sign_key) for that.
    """
    access_key = self.access_key
    secret_key = bytes(self.secret_key, 'UTF-8') # str -> bytes

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')

    sign_key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
    return sign_key

  def set_from_num(self, from_num: str):
    """
    set [from_num] in advance.
    """
    self.from_num = from_num

  def send_message(self, 
    to_num: str,
    content: str,
    from_num: str = None,
    msgType: str = "SMS",
    contentType: str = "COMM",
    subject: str = None,
    messages: list = None,
    files: list = None,
    reserveTime: str = None,
    reserveTimeZone: str = None,
    scheduleCode: str = None
    ) -> requests.Response :
    """
    Reference : https://api.ncloud-docs.com/docs/ai-application-service-sens-smsv2\n
    Send message from [from_num] to [to_num].\n
    [content] is the content of the message.\n
    If [from_num] is already set by set_from_num(), [from_num] is not required.\n
    Return : <class 'requests.Response'>
    """

    # If the [from_num] is not given as a parameter
    if from_num == None:
      if self.from_num == None: # If [from_num] is never given, raise Exception
        raise Exception("[from_num] is never given. Set [from_num] by calling set_from_num() or give as a parameter.")
      else: # If [from_num] is already set, use the value.
        from_num = self.from_num

    # There is limit in each msgType.
    # SMS <= 80 bytes, LMS <= 2000 bytes
    if msgType == "SMS":
      if 80 < len(content) and len(content) <= 2000:
        msgType = "LMS"
      elif 2000 < len(content):
        raise Exception("Exceeds maximum message length(2000 bytes). : %sbytes" % len(content))

    # There is limit in reserveTime.
    # Reservation cannot be requested within 10 minutes.
    if reserveTime != None:
      cur_datetime = datetime.datetime.now()
      try:
        reserveTime_datetime = datetime.datetime.strptime(reserveTime, '%Y-%m-%d %H:%M')
      except ValueError as e:
        raise Exception("reserveTime follows the format of \"yyyy-MM-dd HH:mm\".\n[ValueError]%s" % e)
      time_interval = reserveTime_datetime - cur_datetime
      seconds = time_interval.total_seconds()
      if seconds < 600:
        raise Exception("Reservation cannot be requested within 10 minutes.")

    timestamp = self.generate_timestamp()

    access_key = self.access_key
    service_id = self.service_id
    base_url = "https://sens.apigw.ntruss.com" # SENS API default URL
    uri_1 = "/sms/v2/services/"
    uri_2 = "/messages"
    uri = uri_1 + service_id + uri_2
    req_url = base_url + uri
    sign_key = self.genereate_signature(method="POST", timestamp=timestamp, uri=uri)

    headers = {
    'Content-Type' : "application/json; charset=utf-8",
    'x-ncp-apigw-timestamp' : timestamp,
    'x-ncp-iam-access-key' : access_key,
    'x-ncp-apigw-signature-v2' : sign_key
    }

    body = {
      "type": msgType,
      "contentType": contentType,
      "from": from_num,
      "content": content,
      "messages": [{"to" : to_num}]
    }
    if subject != None:
      body["subject"] = subject
    if reserveTime != None:
      body["reserveTime"] = reserveTime
    if reserveTimeZone != None:
      body["reserveTimeZone"] = reserveTimeZone
    if scheduleCode != None:
      body["scheduleCode"] = scheduleCode
    if messages != None:
      body["messages"] = messages
    if files != None:
      body["files"] = files

    body_json = json.dumps(body)
    resp = requests.post(req_url, headers=headers, data=body_json)

    return resp

  def send_message_with_image(self, 
    to_num: str,
    content: str,
    img_dir: str,
    from_num: str = None,
    contentType: str = "COMM",
    subject: str = None,
    reserveTime: str = None,
    reserveTimeZone: str = None,
    scheduleCode: str = None
    ) -> requests.Response:
    """
    Send message from [from_num] to [to_num].\n
    [content] is the text content of the message.\n
    [img_dir] is the directory to the image, which will be sent with the text message. There are limits to image.\n
    1. Image's format must be .jpg or .jpeg\n
    2. Image's max resolution is 1500*1440\n
    If [from_num] is already set by set_from_num(), [from_num] is not required.\n
    Return : <class 'requests.Response'>
    """

    # If from_num is already set, use the value.
    if from_num == None:
      from_num = self.from_num

    # Image file type check
    extension = Path(img_dir).suffix.lower()
    if extension not in ['.jpg', '.jpeg']:
      raise Exception("img_dir must have suffix of .jpg or .jpeg")
    # Image file size check
    file_size = os.path.getsize(img_dir)
    if file_size > 300000:
      raise Exception("filesize must be 300Kbyte or less.")
    # Image file(.jpg) -> Base64 String
    with open(img_dir,'rb') as img:
      body = base64.b64encode(img.read()).decode('utf-8')
    
    files = [{"name": "img.jpg", "body": body}]

    resp = self.send_message(
      to_num=to_num, content=content, from_num=from_num, msgType="MMS",
      contentType=contentType, subject=subject, files=files, 
      reserveTime=reserveTime, reserveTimeZone=reserveTimeZone,
      scheduleCode=scheduleCode)
    
    return resp