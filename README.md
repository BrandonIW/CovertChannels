## What is CovertChannels?
Program running in Python 3.9 that utilizes the Scapy library to forge IP packets with false source IP Addresses. The final ocetet of the false source IP is used as the covert channel, and is replaced by the base 10 represetnation of ASCII Characters

The program is split into a client and server component. The server componment simply listens for incoming packets on the designated interface:port. Recieved packets are processed by pulling out the final octet of the source IP Address and converting that value into its ASCII equivlent. 

## Compatability
Runs on Python 3.9
Tested on:
•	Windows 10 Version10.0.19042 Build 19042
●	Kali GNU/Linux Rolling Release 2021.3
●	RHEL 7.8 (Maipo)

Do note firewall rules may need to be edited depending on the port that you are listening on, on the svr 

## Options
# Server:
* No options needed for the server

# Client:
* -h      Displays Help Regarding how to run the cmd

* -m / --message      Required (Client script only): Plaintext input that will covertly be transferred from the Client to the Server


## Quickstart
1) Download .ZIP File and extract to a directory of your choice
2) The "client" folder will be run on a separate client machine than the server. Move the folders to whichever machines will be acting as the client and server
3) ```sudo python3 server.py```   <- run on server machine
4) ```sudo python3 client.py -m "Hello There World"``` <- run on client machine


### Example Output

![image](https://user-images.githubusercontent.com/77559638/158628225-66ef8bb6-848f-4d2e-8140-b300c0226e32.png)

![image](https://user-images.githubusercontent.com/77559638/158628318-6faf4940-f972-4ada-a904-acb00fcbc558.png)


