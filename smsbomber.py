import smtplib
import getpass
import time
import random
import sys 

EMAIL_PROVIDERS = {
    1: {'name': 'Gmail', 'smtp_server': 'smtp.gmail.com', 'port': 587},
    2: {'name': 'Yahoo', 'smtp_server': 'smtp.mail.yahoo.com', 'port': 587},
    3: {'name': 'Hotmail', 'smtp_server': 'smtp.live.com', 'port': 587},
    4: {'name': 'Outlook', 'smtp_server': 'smtp.office365.com', 'port': 587},
    5: {'name': 'Zoho Mail', 'smtp_server': 'smtp.zoho.com', 'port': 587},
    6: {'name': 'Mail.com', 'smtp_server': 'smtp.mail.com', 'port': 587},
    7: {'name': 'GMX', 'smtp_server': 'mail.gmx.com', 'port': 587},
    8: {'name': 'AOL Mail', 'smtp_server': 'smtp.aol.com', 'port': 587},
}

def get_user_input():
    print()
    print("\033[91m")  
    print("WARNING: It is recommended to use a VPN when sending emails using this program.")
    print("This can help protect your privacy and prevent your IP address from being blocked.")
    print("\033[0m")  
    print()

    print("Select email service provider:")
    for key, provider in EMAIL_PROVIDERS.items():
        print(f"{key}. {provider['name']}")
    provider_choice = int(input("Enter number: "))
    email_provider = EMAIL_PROVIDERS.get(provider_choice, EMAIL_PROVIDERS[1])
    
    email_address = input("Enter your email address: ")
    password = getpass.getpass("Enter your password: ")

    print("\nTo find the target SMS email address, visit the following URL and enter the phone number:")
    print("http://freecarrierlookup.com\n")
    target_email = input("Enter target SMS email address: ")

    text_amount = int(input("Enter the number of emails to send: "))
    wait = int(input("Enter the number of seconds to wait between emails: "))

    return email_provider, email_address, password, target_email, text_amount, wait

def create_smtp_server(email_provider, email_address, password):
    try:
        server = smtplib.SMTP(email_provider['smtp_server'], email_provider['port'])
        server.starttls()
        server.login(email_address, password)
        return server
    except smtplib.SMTPAuthenticationError:
        print("Failed to login.")
        return None

def send_emails(server, email_address, target_email, text_amount, wait, messages):
    for i in range(text_amount):
        msg = random.choice(messages)
        try:
            server.sendmail(email_address, target_email, msg)
            print("sent")
            time.sleep(wait)
        except smtplib.SMTPRecipientsRefused:
            print("Recipient refused.")
            break
        except Exception as e:
            print("Error:", str(e))
            break

    print(f"{i+1} texts sent.")

def main():
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

    try:
        email_provider, email_address, password, target_email, text_amount, wait = get_user_input()
        server = create_smtp_server(email_provider, email_address, password)
        if server is not None:
            send_emails(server, email_address, target_email, text_amount, wait, messages)
            server.quit()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Exiting...")
        try:
            if 'server' in locals():  
                server.quit()
        finally:
            sys.exit(0)

if __name__ == "__main__":
    main()