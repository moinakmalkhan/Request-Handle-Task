- Use python logging to log user IPs+time in a file whenever request come to server, this should he done in a custom middleware.
- Use redis to cache users IPs and block them (server should return proper exception) if they request the server more than x number of times in a minute. You can assume x to be 5 for instance.
- Create user groups and based on user’s group allow them to access endpoints of our app, say Gold user can access 10 times a minute, Silver 5 times and Bronze 2 times. Unauthenticated users shouldn’t be able to access more than once a minute.
  PS: Once user is blocked they should get unblocked after 1 minute automatically. Tasks should he done in custom django middlewares.
  Edited
