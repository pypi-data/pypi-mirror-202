# proxy decorator

## usage

1. create a `ini` file or add to exist `ini` file

2. put this in your `ini` file

   ```ini
   [http]
   http = http://your_proxy_server:your_proxy_port
   https = https://your_proxy_server:your_proxy_port
   username = your_username
   password = your_password
   ```

3. use it in your program

   ```python
   from proxy_decorator.proxy_decorator import proxy_http
   
   config_file = "path/to/proxy_config.ini"
   
   @proxy_http(config_file)
   def your_function():
       # 您的函数实现
       pass
   