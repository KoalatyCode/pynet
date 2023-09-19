import telnetlib


def get_arp_table(host, username, password, command="show arp"):
    try:
        print(f"Trying to connect to: {host} ")
        # Connect using Telnet(hostname, port, timeout)
        tn = telnetlib.Telnet(host, 23, 5)

        print(f"Waiting for login prompt ...")
        tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")

        print(f"Waiting for password prompt...")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        # Wait for a prompt or adjust as needed
        print(f"Waiting for command prompt...")
        tn.read_until(b"$")

        # Send the command to fetch ARP table
        print(f"Sending command...")
        tn.write(command.encode('ascii') + b"\n")

        print(f"Reading response...")
        arp_data = b""
        while True:
            chunk = tn.read_some()
            if not chunk:
                break  # End of data

            arp_data += chunk

            if b"$" in chunk:  # Adjust this as needed
                break  # We found the command prompt, so break out of the loop

            tn.write(b"\n")  # Press 'Enter' to get more data

        tn.close()

        return arp_data.decode('ascii')
    except Exception as e:
        print(f"Error connecting to {host}: {e}")
        return None


hosts = ["host1", "host2", "host3"]
username = "username"
password = "password"

for host in hosts:
    arp_table = get_arp_table(host, username, password)
    if arp_table:
        # Save the ARP table to a file named by the host's IP or hostname
        with open(f"{host}_arp_table.txt", "w") as file:
            file.write(arp_table)
        print(f"ARP table for {host} saved.")
    else:
        print(f"Trying next host.")
