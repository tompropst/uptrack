# uptrack - Remote Uptime Tracker

Simple web server that records connection attempts by:

* Client IP - Identifier for clients being tracked.
* Timestamp - Time of each check-in for the client.

## Usage

Each client should have a scheduled task to issue an HTTP GET request to the server. The server will record the client IP and time of the request. A unique and obscure URL should be created for the service to avoid tracking entries of web crawlers and other random clients that happen upon the server. One method might be to use the MD5 digest of your server name.

For example:

````
$ echo -n example.com | md5sum
5ababd603b22780302dd8d83498e5172  -
````

Use the produced hash as the PATH value in the script.

The client request would then be:

````
$ wget http://example.com/5ababd603b22780302dd8d83498e5172 >/dev/null
````

The above command could be used in a cron entry set to run every minute, hour, etc. as needed.

The server will record a simple, flat file in CSV format. To avoid disk usage issues, it is recommended to use a tool such as `logrotate` to manage the file growth, especially if you are tracking many clients over long periods of time.
