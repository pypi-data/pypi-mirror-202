"""
Copyright 2019-2022 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.


* NOTICE:  All information contained herein is, and remains
* the property of Knowledge Investment Group SRL.  
* The intellectual and technical concepts contained
* herein are proprietary to Knowledge Investment Group SRL
* and may be covered by Romanian and Foreign Patents,
* patents in process, and are protected by trade secret or copyright law.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Knowledge Investment Group SRL.


@copyright: Lummetry.AI
@author: Lummetry\.AI - Stefan Saraev
@project: 
@description:
"""
from time import time
from ..utils.code_exec import code_to_base64


WAIT_FOR_WORKER = 15


class Pipeline(object):
  def __init__(self, session, log, *, e2id, name, data_source, config={}, plugins, on_data, silent=True, on_notification=None, **kwargs) -> None:
    self.log = log
    self.session = session
    self.e2id = e2id
    self.name = name
    self.data_source = data_source
    self.config = config
    self.plugins = plugins
    self.on_data = on_data
    self.on_notification = on_notification

    self.payload = {}

    self.silent = silent

    self._create_new_pipeline_on_box(**kwargs)
    return

  def _create_new_pipeline_on_box(self, *, create_pipeline=True, **kwargs):
    # beautify the fields that enter in the config file
    kwargs = {k.upper(): v for k, v in kwargs.items()}

    self.payload = {
        'NAME': self.name,
        'SESSION_ID': self.name,
        'DEFAULT_PLUGIN': False,
        'PLUGINS': [] if self.plugins is None else self.plugins,
        'TYPE': self.data_source,
        **self.config,
        **kwargs
    }

    if create_pipeline:
      self.session.send_command_update_pipeline(
          worker=self.e2id,
          stream_config=self.payload
      )

    if self.on_data is not None:
      self._add_payload_pipeline_callback_to_session(self.on_data)
    if self.on_notification is not None:
      self._add_notification_pipeline_callback_to_session(self.on_notification)
    return

  def _add_payload_instance_callback_to_session(self, signature, instance, callback):
    self.session.payload_instance_callbacks.append(
        (self, signature, instance, callback))

  def _add_notification_instance_callback_to_session(self, signature, instance, callback):
    self.session.notification_instance_callbacks.append(
        (self, signature, instance, callback))

  def _add_payload_pipeline_callback_to_session(self, callback):
    self.session.payload_pipeline_callbacks.append((self, callback))

  def _add_notification_pipeline_callback_to_session(self, callback):
    self.session.notification_pipeline_callbacks.append((self, callback))

  # TODO: maybe wait for a confirmation?
  def start_plugin_instance(self, *, signature, instance_id, params, on_data, on_notification=None, **kwargs):
    """Create a new instance of a desired plugin, with a given configuration. This instance is attached to this pipeline, 
    meaning it processes data from this pipelines data source. Parameters can be passed either in the params dict, or as kwargs.

    Args:
        signature (str): name of the plugin signature. This is the name of the desired overall functionality.
        instance_id (str): name of the instance. There can be multiple instances of the same plugin, mostly with different prameters
        params (dict): parameters used to customize the functionality. One can change the AI engine used for object detection, or finetune alerter parameters to better fit a camera located in a low light environment.
        on_data (Callable[[Pipeline, str, str, dict], None]): Callback that handles messages received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself.
        on_notification (Callable[[Pipeline, dict], None], optional): Callback that handles notifications received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself. Defaults to None.

    Raises:
        Exception: Plugin instance already exists. 

    Returns:
        str: An identifier for this instance, useful for stopping an instance.
    """
    plugins = self.payload['PLUGINS']
    found_plugin_signature = False
    to_update_plugin = {
        'INSTANCES': [],
        'SIGNATURE': signature
    }
    # beautify the fields that enter in the config file
    kwargs = {k.upper(): v for k, v in kwargs.items()}

    to_add_instance = {
        'INSTANCE_ID': instance_id,
        **params,
        **kwargs
    }

    for plugin in plugins:
      if plugin['SIGNATURE'] == signature:
        found_plugin_signature = True
        to_update_plugin = plugin
        break

    if not found_plugin_signature:
      plugins.append(to_update_plugin)

    for instance in to_update_plugin['INSTANCES']:
      if instance['INSTANCE_ID'] == instance_id:
        raise Exception(
            "plugin {} with instance {} already exists".format(signature, instance_id))

    to_update_plugin['INSTANCES'].append(to_add_instance)

    self.session.send_command_update_pipeline(
        worker=self.e2id,
        stream_config=self.payload
    )

    self._add_payload_instance_callback_to_session(
        signature, instance_id, on_data)
    if on_notification is not None:
      self._add_notification_instance_callback_to_session(
          signature, instance_id, on_notification)
    self.P("Starting plugin {}:{}".format(
        signature, instance_id))
    self.D("with params {}".format(params))
    return "##".join([self.e2id, self.name, signature, instance_id])

  def stop_plugin_instance(self, signature, instance_id=None, /):
    """Stop a plugin instance from this pipeline. The function can accept either the signature and the instance_id of the desired instance,
    or the identifier returned from `start_plugin_instance` or `start_custom_instance` or `attach_to_instance` or `attach_to_custom_instance`.

    Args:
        signature (str): Signature of a plugin (name of the plugin type) or instance identifier
        instance_id (str, optional): Name of the instance. Defaults to None.

    """
    if instance_id is None:
      try:
        e2id, pipeline_name, signature, instance_id = tuple(
            signature.split('##'))
      except:
        raise ("Unknown format of instance_id. Please provide the return value of a 'start_plugin_instance' call")

      if self.e2id != e2id:
        raise ("Sending a command for a pipeline that was started by another box")

      if self.name != pipeline_name:
        raise ("Sending a command for a pipeline that was started by another instance")
    plugins = self.payload['PLUGINS']
    to_remove_instance_index = None
    to_update_plugin_index = None

    for i, plugin in enumerate(plugins):
      if plugin['SIGNATURE'] == signature:
        to_update_plugin_index = i
        break

    if to_update_plugin_index is None:
      return

    for i, instance in enumerate(plugins[to_update_plugin_index]['INSTANCES']):
      if instance['INSTANCE_ID'] == instance_id:
        to_remove_instance_index = i
        break

    if to_remove_instance_index is None:
      return

    plugins[to_update_plugin_index]['INSTANCES'].pop(to_remove_instance_index)

    if len(plugins[to_update_plugin_index]['INSTANCES']) == 0:
      self.payload['PLUGINS'].pop(to_update_plugin_index)

    self.session.send_command_update_pipeline(
        worker=self.e2id,
        stream_config=self.payload
    )
    self.session.remove_instance_callback(self, signature, instance_id)

    return

  def start_custom_plugin(self, *, instance_id, plain_code: str = None, plain_code_path: str = None, params, on_data, on_notification=None, **kwargs):
    """Create a new custom execution instance, with a given configuration. This instance is attached to this pipeline, 
    meaning it processes data from this pipelines data source. The code used for the custom instance must be provided either as a string, or as a path to a file. Parameters can be passed either in the params dict, or as kwargs.
    The custom plugin instance will run periodically. If one desires to execute a custom code only once, use `wait_exec`.

    Args:
        instance_id (str): name of the instance. There can be multiple instances of the same plugin, mostly with different prameters
        params (dict): parameters used to customize the functionality.
        on_data (Callable[[Pipeline, str, str, dict], None]): Callback that handles messages received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself.
        plain_code (str, optional): A string containing the entire code that is to be executed remotely on an AiXp node. Defaults to None.
        plain_code_path (str, optional): A string containing the path to the code that is to be executed remotely on an AiXp node. Defaults to None.
        on_notification (Callable[[Pipeline, dict], None], optional): Callback that handles notifications received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself. Defaults to None.

    Raises:
        Exception: The code was not provided.

    Returns:
        str: An identifier for this instance, useful for stopping an instance.
    """

    def custom_exec_on_data(self, data):
      exec_data = None
      if "SB_IMPLEMENTATION" in data or "EE_FORMATTER" in data:
        exec_data = data.get('EXEC_RESULT', data.get('EXEC_INFO'))
        exec_error = data.get('EXEC_ERRORS', 'no keyword error')
      else:
        try:
          exec_data = data['specificValue']['exec_result']
        except Exception as e:
          self.P(e, color='r')
          self.P(data, color='r')
        exec_error = data['specificValue']['exec_errors']

      if exec_error is not None:
        self.P("Error received from <CUSTOM_EXEC_01:{}>: {}".format(
            instance_id, exec_error), color="r")
      if exec_data is not None:
        on_data(self, exec_data)
      return

    if plain_code is None and plain_code_path is None:
      raise Exception(
          "Need to specify at least one of the following: plain_code, plain_code_path")

    if plain_code is not None and plain_code_path is not None:
      raise Exception(
          "Need to specify at most one of the following: plain_code, plain_code_path")

    if plain_code is None:
      with open(plain_code_path, "r") as fd:
        plain_code = "".join(fd.readlines())

    b64code = code_to_base64(plain_code)
    return self.start_plugin_instance(
        signature='CUSTOM_EXEC_01',
        instance_id=instance_id,
        params={
            'CODE': b64code,
            **params
        },
        on_data=custom_exec_on_data,
        on_notification=on_notification,
        **kwargs
    )

  def stop_custom_instance(self, instance_id):
    """Stop a custom execution instance from this pipeline.

    Args:
        instance_id (str, optional): Name of the custom instance. Defaults to None.

    """
    self.stop_plugin_instance('CUSTOM_EXEC_01', instance_id)

  def wait_exec(self, *, plain_code: str = None, plain_code_path: str = None, params={}):
    """Create a new REST-like custom execution instance, with a given configuration. This instance is attached to this pipeline, 
    meaning it processes data from this pipelines data source. The code used for the custom instance must be provided either as a string, or as a path to a file. Parameters can be passed either in the params dict, or as kwargs.
    The REST-like custom plugin instance will execute only once. If one desires to execute a custom code periodically, use `start_custom_plugin`.

    Args:
        params (dict, optional): parameters used to customize the functionality. Defaults to {}.
        plain_code (str, optional): A string containing the entire code that is to be executed remotely on an AiXp node. Defaults to None.
        plain_code_path (str, optional): A string containing the path to the code that is to be executed remotely on an AiXp node. Defaults to None.

    Raises:
        Exception: The code was not provided.

    Returns:
        Tuple[Any, Any]: a tuple containing the result of the execution and the error, if any. 
        If the execution completed succesfully, the `error` is None, and the `result` is the returned value of the custom code.
    """
    if plain_code is None and plain_code_path is None:
      raise Exception(
          "Need to specify at least one of the following: plain_code, plain_code_path")

    if plain_code is None:
      with open(plain_code_path, "r") as fd:
        plain_code = "".join(fd.readlines())

    finished = False
    result = None
    error = None

    def on_data(pipeline, data):
      nonlocal finished
      nonlocal result
      nonlocal error

      if 'rest_execution_result' in data['specificValue'] and 'rest_execution_error' in data['specificValue']:
        result = data['specificValue']['rest_execution_result']
        error = data['specificValue']['rest_execution_error']
        finished = True
      return

    b64code = code_to_base64(plain_code)
    instance_id = self.name + "_rest_custom_exec_synchronous_0"
    params = {
        'REQUEST': {
            'DATA': {
                'CODE': b64code,
            },
            'TIMESTAMP': self.log.time_to_str()
        },
        'RESULT_KEY': 'REST_EXECUTION_RESULT',
        'ERROR_KEY': 'REST_EXECUTION_ERROR',
        **params
    }

    self.start_plugin_instance(
        signature='REST_CUSTOM_EXEC_01',
        instance_id=instance_id,
        params=params,
        on_data=on_data
    )
    while not finished:
      pass

    # stop the stream
    self.stop_plugin_instance('REST_CUSTOM_EXEC_01', instance_id)

    return result, error

  def close(self):
    """Close the pipeline, stopping all the instances associated with it.
    """
    # remove callbacks
    self.session.send_command_delete_pipeline(self.e2id, self.name)
    self.session.remove_pipeline_callbacks(self)
    return

  def P(self, *args, **kwargs):
    """Print info to stdout.
    """
    return self.log.P(*args, **kwargs)

  def D(self, *args, **kwargs):
    """Print debug info to stdout if the session was created with the silent argument set to `False`. 
    The silent argument is passed to the Pipeline object when creating it with `create_pipeline` or `attach_to_pipeline`.
    """
    if not self.silent:
      return self.log.P(*args, **kwargs)

  def attach_to_instance(self, signature, instance_id, on_data, on_notification=None):
    """Attach to an existing instance on this pipeline. 
    This method is useful when one wishes to attach an 
    `on_data` and `on_notification` callbacks to said instance.

    Args:
        signature (str): name of the plugin signature.
        instance_id (str): name of the instance.
        on_data (Callable[[Pipeline, str, str, dict], None]): Callback that handles messages received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself.
        on_notification (Callable[[Pipeline, dict], None], optional): Callback that handles notifications received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself. Defaults to None.

    Raises:
        Exception: the pipeline does not contain plugins with a given signature or it does not contain the desired instance.

    Returns:
        str: An identifier for this instance, useful for stopping an instance.
    """
    plugins = self.payload['PLUGINS']
    found_plugin_signature = False

    for plugin in plugins:
      if plugin['SIGNATURE'] == signature:
        found_plugin_signature = True
        break

    if not found_plugin_signature:
      raise Exception("Unable to attach to instance. Signature does not exist")

    for instance in plugin['INSTANCES']:
      if instance['INSTANCE_ID'] == instance_id:
        self._add_payload_instance_callback_to_session(
            signature, instance_id, on_data)
        if on_notification is not None:
          self._add_notification_instance_callback_to_session(
              signature, instance_id, on_notification)
        return "##".join([self.e2id, self.name, signature, instance_id])

    raise Exception("Unable to attach to instance. Instance does not exist")

  def attach_to_custom_instance(self, instance_id, on_data, on_notification=None):
    """Attach to an existing custom execution instance on this pipeline. 
    This method is useful when one wishes to attach an 
    `on_data` and `on_notification` callbacks to said instance.

    Args:
        instance_id (str): name of the instance.
        on_data (Callable[[Pipeline, str, str, dict], None]): Callback that handles messages received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself.
        on_notification (Callable[[Pipeline, dict], None], optional): Callback that handles notifications received from this instance. As arguments, it has a reference to this Pipeline object, along with the payload itself. Defaults to None.

    Raises:
        Exception: the pipeline does not contain plugins with a given signature or it does not contain the desired instance.

    Returns:
        str: An identifier for this instance, useful for stopping an instance.
    """

    def custom_exec_on_data(self, data):
      exec_data = None
      if "SB_IMPLEMENTATION" in data or "EE_FORMATTER" in data:
        exec_data = data.get('EXEC_RESULT', data.get('EXEC_INFO'))
        exec_error = data.get('EXEC_ERRORS', 'no keyword error')
      else:
        try:
          exec_data = data['specificValue']['exec_result']
        except Exception as e:
          self.P(e, color='r')
          self.P(data, color='r')
        exec_error = data['specificValue']['exec_errors']

      if exec_error is not None:
        self.P("Error received from <CUSTOM_EXEC_01:{}>: {}".format(
            instance_id, exec_error), color="r")
      if exec_data is not None:
        on_data(self, exec_data)
      return

    return self.attach_to_instance("CUSTOM_EXEC_01", instance_id, custom_exec_on_data, on_notification)
