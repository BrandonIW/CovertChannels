## What is CovertChannels?
Program running in Python 3.9 that utilizes the Scapy library to forge IP packets with false source IP Addresses. The final octet of the false source IP is used as the covert channel, and is replaced by the base 10 representation of ASCII Characters

The program is split into client and server components. The client will first take in -m/--message plaintext and create forged packets with Scapy for each element of the plaintext. The client will first create a random IP address and then replace the final octet with that element’s base 10 equivalent. When the message is finished being sent, the client will send a final packet with “END” inserted as Raw data. 

The server component simply listens for incoming packets on the designated interface:port. Received packets are processed by pulling out the final octet of the source IP Address and converting that value into its ASCII equivalent. 

Once the server finds a packet with the raw data “END,” it will concatenate all received covert elements of the message into a single final message that is then returned to the user. 



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


