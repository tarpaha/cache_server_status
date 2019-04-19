# cache_server_status
Command line program to check Unity cache server status.
It sends server version and according to https://github.com/Unity-Technologies/unity-cache-server/blob/master/protocol.md waits for server to return same data.
Prints error to stderr and returns exit code 1 if something goes wrong.
Use -h or --help for command line options.
