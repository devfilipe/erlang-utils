import requests
import os
import time
import json
import uuid
import subprocess

STATUS_OK = 'ok'
STATUS_NOT_FOUND = 'service_not_found'
STATUS_ALREADY_EXISTS = 'service_already_exists'

CONF_PATH = 'priv/cloudi'

# list of modules name
modules_code_path = []

# dictionary service_name : update params
# 'myservice':        '",[{module, myservice}, {modules_load, [myservice, mod1, mod2]}]}]'
services_init = {}

### cloudi API
CLOUDI_IP = 'localhost'
CLOUDI_PORT = '6464'
CLOUDI_API_RPC = 'cloudi/api/rpc'

CODE_PATH_ADD_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/code_path_add.erl'
CODE_PATH_REMOVE_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/code_path_remove.erl'
SERVICES_JSON_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/services.json'
SERVICES_ADD_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/services_add.erl'
SERVICES_UPDATE_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/services_update.erl'
SERVICES_REMOVE_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/services_remove.erl'
SERVICE_SUBSCRIPTIONS_URL = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{CLOUDI_API_RPC}/service_subscriptions.erl'

###
# TODO load services, code path and update params from a file (json, yaml)

###
cwd = os.path.normpath(os.getcwdb().decode('utf-8'))

def set_cwd(c:str):
  global cwd
  cwd = c

def get_cwd():
  return cwd

def compile_all():
  for m in modules_code_path:
    ret = rebar3(m)
    print(f'{m}:{ret}')

def rebar3(app:str):
  command = 'rm _build/ -rf; rm rebar.lock; rebar3 compile'
  c = os.path.expanduser(get_cwd()+"/"+app)
  ret = subprocess.run(command, capture_output=True, shell=True, cwd=c)
  return ret.returncode

def init():
  code_path_add_all()
  services_add()
  return STATUS_OK

def clear():
  services_remove()
  code_path_remove_all()
  return STATUS_OK

def code_path_add_all():
  for m in modules_code_path:
    code_path_add(m)
  return STATUS_OK

def code_path_remove_all():
  for m in modules_code_path:
    code_path_remove(m)
  return STATUS_OK

def code_path_add(module:str):
  if "/" not in module:
    bin_path = f'_build/default/lib/{module}/ebin'
    service_path = f"\'{get_cwd()}/{module}/{bin_path}\'"
  else:
    service_path = f"\'{module}\'"
  print(service_path)
  r = requests.post(CODE_PATH_ADD_URL, data=service_path)
  return r.text

def code_path_remove(module:str):
  if "/" not in module:
    bin_path = f'_build/default/lib/{module}/ebin'
    service_path = f"\'{get_cwd()}/{module}/{bin_path}\'"
  else:
    service_path = f"\'{module}\'"
  r = requests.post(CODE_PATH_REMOVE_URL, data=service_path)
  return r.text

def services_add():
  services = services_init.keys()
  res = {}
  for s in services:
    res[s] = service_add(s)
  print(res)
  return STATUS_OK

def services_remove():
  services = services_init.keys()
  service_ids = []

  # data format: '["<UUID", ...]'
  for s in services:
    s_id = service_id(s)
    if type(s_id) == str:
      service_ids.append('\"'+s_id+'\"')
    else:
      continue
  data = '['+', '.join(['%s']*len(service_ids)) % tuple(service_ids)+']'
  r = requests.post(SERVICES_REMOVE_URL, data=data)
  print(data)
  return STATUS_OK

def service_add(service:str):
  """
    The .conf file is expected to be found at '{SERVICE}/priv/cloudi' directory
  """
  id = service_id(service)
  if id == []:
    conf_file = f'{get_cwd()}/{service}/{CONF_PATH}/{service}.conf'
    file = {'upload_file': open(conf_file,'rb')}
    r = requests.post(SERVICES_ADD_URL, files=file)
    return r.text
  return STATUS_ALREADY_EXISTS

def service_remove(service:str):
  if is_valid_uuid(service) == False:
    id = service_id(service)
    if id == []:
      return STATUS_NOT_FOUND
  else:
    id = service
  data = f"""["{id}"]"""
  r = requests.post(SERVICES_REMOVE_URL, data=data)
  return {data, r.text}

def service_update(service:str):
  if is_valid_uuid(service) == False:
    id = service_id(service)
    if id == []:
      return STATUS_NOT_FOUND
  else:
    id = service
  data = '[{"' + id + services_init[service]
  r = requests.post(SERVICES_UPDATE_URL, data=data)
  return r.text

def service_id(service:str):
  r = requests.get(SERVICES_JSON_URL)
  for s in r.json().get('services'):
    if s['type'] == 'internal':
      if s['module'] == service:
        return s['id']
    else:
      if s['file_path'] == service:
        return s['id']
  return []

def service_ids(service:str):
  list = []
  r = requests.get(SERVICES_JSON_URL)
  for s in r.json().get('services'):
    if s['type'] == 'internal':
      if s['module'] == service:
        list.append(s['id'])
    else:
      if s['file_path'] == service:
        list.append(s['id'])
  return list

def service_list():
  dict = {}
  list = []
  r = requests.get(SERVICES_JSON_URL)
  for s in r.json().get('services'):
    if 'module' in s:
      dict[s['id']] = s['module']
    else:
      dict[s['id']] = s['file_path']
  list.append(dict.copy())
  output = json.JSONEncoder().encode({"services": list})
  print(json.dumps(json.loads(output), indent=2, sort_keys=True))
  return output

def is_valid_uuid(value):
  try:
    uuid.UUID(value)
    return True
  except ValueError:
    return False

def service_subscriptions(service:str):
  if is_valid_uuid(service) == False:
    id = service_id(service)
    if id == []:
      return STATUS_NOT_FOUND
  else:
    id = service
  data = f'"{id}"'
  r = requests.post(SERVICE_SUBSCRIPTIONS_URL, data=data)
  return r.text

def service_subscriptions2(service:str):
  list = []
  dict = {}
  ids = service_ids(service)
  if ids == []:
    return STATUS_NOT_FOUND
  for id in ids:
    data = f'"{id}"'
    r = requests.post(SERVICE_SUBSCRIPTIONS_URL, data=data)
    dict[id] = r.text
  list.append(dict.copy())
  return list

def post(path:str, data:str = "{}"):
  Url = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{path}'
  r = requests.post(Url, data)
  print(r)
  return r.text

def get(path:str):
  Url = f'http://{CLOUDI_IP}:{CLOUDI_PORT}/{path}'
  r = requests.get(Url)
  print(r)
  return r.text
