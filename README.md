# FTPApplication
####How to execute program:
1. Optional - copy cli.py and header.py to seperate file or different OS machine
2. Run the server frist by using code:
	Porking server:
```sh
python serv.py <port number>
```
or
Thread server:
```sh
python server-thread.py <port number>
```
3. Go to file contain cli.py and header.py and run the code:
```sh
python client.py <server IP Address> <port number>
```
4. Optional - can open multiple client in terminal
5. Client can enter:
```sh
get <file name> (downloads file <file name> from the server)
put <filename> (uploads file <file name> to the server)
ls (lists files on the server)
lls (lists files on the client)
quit (disconnects from the server and exits)
```