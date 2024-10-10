import cv2
import requests
import os
import pygame
import json
import time
import logging

logging.basicConfig(level=logging.INFO)

client_id = '23dbofq5xefmvbhss1q2iphs1tibs41p'
client_secret = '47r0zlxebu9tj5tm6n55050dlk9vwfctcpinjgs63brofo9vzv45ywpy7effb2iv'
token_url = 'https://www.nyckel.com/connect/token'
model_url = 'https://www.nyckel.com/v1/functions/8hvju73hkjyq3x8b/invoke'

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def load_anthem(anthem_path):
    if os.path.exists(anthem_path):
        pygame.mixer.init()
        pygame.mixer.music.load(anthem_path)
        return True
    return False

saudi_anthem_loaded = load_anthem('anthems/saudi_arabia.mp3')

def play_anthem():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.play()

def get_access_token():
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get access token: {e}")
        return None

def send_to_nyckel(image, token):
    headers = {'Authorization': f'Bearer {token}'}
    _, img_encoded = cv2.imencode('.png', image)
    files = {'file': ('image.png', img_encoded.tobytes(), 'image/png')}
    
    try:
        model_response = requests.post(model_url, headers=headers, files=files, timeout=5)
        model_response.raise_for_status()
        response_text = model_response.text
        logging.info(f"Model Response: {response_text}")
        return extract_label_from_response(response_text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in sending to Nyckel: {e}")
        return None

def extract_label_from_response(response_text):
    try:
        response_data = json.loads(response_text)
        return response_data.get('labelName', '').strip()
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response.")
        return ''

def show_country_info(label_name):
    country_info = {
        'egypt': 'National Day: July 23',
        'Saudi Arabia': 'National Day: September 23',
        'kuwait': 'National Day: February 25',
        'UAE': 'National Day: December 2',
        'palestine': 'National Day: November 15',
        'iraq': 'National Day: October 3'
    }
    return country_info.get(label_name, '')

def show_saudi_info():
    saudi_info = [
        "Saudi Arabia Achievements:",
        "1. Largest economy in the Middle East.",
        "2. Member of G20.",
        "3. Leading oil producer globally.",
        "4. Vision 2030: Diversifying the economy.",
        "5. Hosting international events like Formula 1 and Dakar Rally.",
        "6. Major developments like NEOM and Red Sea Project.",
        "7. Ranked top 2 in MENA region for cybersecurity readiness.",
        "8. Heavy investment in AI, aiming to be a global AI hub by 2030."
    ]
    return saudi_info

def draw_text(frame, text, position, font_scale=1, color=(255, 255, 255)):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)

def update_display(frame, label_name):
    if label_name == 'SaudiSymbol':
        draw_text(frame, "Saudi Symbol!", (50, 50), color=(255, 255, 255))  
        saudi_info = show_saudi_info()
        for idx, line in enumerate(saudi_info):
            draw_text(frame, line, (50, 100 + (idx * 30))) 
    elif label_name == 'Not Saudi Symbol':
        draw_text(frame, "It's not Saudi symbol!", (50, 50), color=(0, 0, 255)) 
    elif label_name == 'Cant recognize the flag':
        draw_text(frame, "Can't recognize the flag!", (50, 50), color=(0, 0, 255))  
    elif label_name:
        draw_text(frame, f"{label_name}!", (50, 50), color=(255, 255, 255)) 
        info_text = show_country_info(label_name)
        if info_text:
            draw_text(frame, info_text, (50, 100))
    else:
        draw_text(frame, "Can't recognize this flag!", (50, 50), color=(0, 0, 255)) 


def main():
    token = get_access_token()
    if not token:
        return

    current_label = None
    last_sent_time = time.time()
    send_interval = 0.5

    while True:
        ret, frame = camera.read()
        if not ret:
            logging.error("Failed to capture frame, retrying...")
            time.sleep(0.1)
            continue

        current_time = time.time()
        if current_time - last_sent_time > send_interval:
            label_name = send_to_nyckel(frame, token)
            last_sent_time = current_time

            if label_name and label_name != current_label:
                current_label = label_name

                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                if current_label == 'Saudi Arabia' and saudi_anthem_loaded:
                    play_anthem()

        update_display(frame, current_label)

        cv2.imshow('Live Stream', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
