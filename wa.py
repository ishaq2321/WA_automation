import tkinter as tk
import cv2
import os
from tkinter import messagebox, filedialog
from googletrans import Translator, LANGUAGES
import threading
import time
import random
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import schedule
from functools import partial
from geopy.geocoders import Nominatim
import tempfile
import pygame
import uuid
import soundfile as sf
import numpy as np
from pyttsx3 import init as tts_init
from pygame import mixer
import wave
import struct


def open_whatsapp_web():
    def launch_driver():
        try:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Add user data directory for persistent session
            user_data_dir = os.path.join(os.path.expanduser("~"), "whatsapp_automation_data")
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            
            global driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get("https://web.whatsapp.com")
            
            # Check if already logged in
            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                logged_in()  # Auto-trigger logged in if session exists
            except TimeoutException:
                btn_start.config(state=tk.DISABLED)
                btn_login.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    threading.Thread(target=launch_driver).start()  

def exit_tool():
    root.destroy()

def logged_in():
    btn_login.config(state=tk.DISABLED) 
    display_menu()  

def display_menu():
    for widget in root.winfo_children():
        widget.destroy()

    lbl_menu = tk.Label(root, text="Menu of Available Options", font=("Helvetica", 16))
    lbl_menu.pack(pady=20)

    buttons = [
        ("Send Message", send_message_gui),
        ("Check Online Status", check_online_status_gui),
        ("Share Mock Location", share_mock_location_gui),
        ("Video Profile Change", upload_pictures_gui),
        ("Exit the tool", exit_tool)
    ]

    for text, command in buttons:
        btn = create_button(text, command)
        btn.pack(pady=10, padx=20, fill='x')

def create_button(text, command):
    btn = tk.Button(root, text=text, command=command, font=("Helvetica", 14), bg="#2196F3", fg="white", relief="flat")
    btn.bind("<Enter>", lambda event, button=btn: button.config(bg="#66b3ff"))  
    btn.bind("<Leave>", lambda event, button=btn: button.config(bg="#2196F3"))  
    return btn

def send_message(contact_name, message, is_audio=False, audio_file=None):
    try:
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        if is_audio and audio_file:
            try:
                print(f"Sending audio file: {audio_file}")
                
                # Click attach button
                attach_xpath = "//div[@title='Attach']"
                attach_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, attach_xpath))
                )
                driver.execute_script("arguments[0].click();", attach_btn)
                time.sleep(1)
                
                # Find the audio input element
                audio_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@accept='*']"))
                )
                
                # Send absolute file path
                abs_path = os.path.abspath(audio_file)
                audio_input.send_keys(abs_path)
                time.sleep(3)
                
                # Wait for and click the send button
                send_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
                )
                driver.execute_script("arguments[0].click();", send_btn)
                time.sleep(2)
                
            except Exception as e:
                print(f"Error sending audio: {str(e)}")
                # Fallback to text
                message_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                fallback_message = f"Sorry, couldn't send audio. Here's the text: {message}"
                message_box.send_keys(fallback_message)
                message_box.send_keys(Keys.RETURN)
        else:
            # Regular text message
            message_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
            )
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            print(f"Message sent to {contact_name}: {message}")
            
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        raise

def text_to_audio(text, lang='en'):
    try:
        # Generate unique filename with .ogg extension (WhatsApp's preferred format)
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f'whatsapp_audio_{uuid.uuid4()}.ogg')
        
        # Initialize text-to-speech engine
        engine = tts_init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Save to temp wav first
        wav_path = os.path.join(temp_dir, 'temp_audio.wav')
        engine.save_to_file(text, wav_path)
        engine.runAndWait()
        
        # Convert to ogg using ffmpeg if available
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-i', wav_path, '-c:a', 'libvorbis', temp_file], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.remove(wav_path)  # Clean up temp wav
        except Exception:
            # If ffmpeg fails, just use the wav file
            temp_file = wav_path
            
        if not os.path.exists(temp_file):
            raise Exception("Failed to create audio file")
            
        print(f"Created audio file: {temp_file}")
        return temp_file
    except Exception as e:
        print(f"Error converting text to audio: {e}")
        return None

def send_message_gui():
    for widget in root.winfo_children():
        widget.destroy()

    # Initialize pygame mixer for audio playback
    pygame.mixer.init()
    current_audio_file = [None]  # Use list to modify in nested functions

    lbl_send_message = tk.Label(root, text="Send a Message", font=("Helvetica", 18))
    lbl_send_message.pack(pady=20)

    # Contact input
    lbl_receiver = tk.Label(root, text="Enter contact names (comma separated):", font=("Helvetica", 12))
    lbl_receiver.pack(pady=5)
    receiver_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
    receiver_entry.pack(pady=10)

    # Message input
    message_frame = ttk.LabelFrame(root, text="Message")
    message_frame.pack(pady=10, padx=20, fill='x')

    message_text = tk.Text(message_frame, font=("Helvetica", 14), height=5, width=30)
    message_text.pack(pady=10)

    # Audio preview frame
    audio_frame = ttk.Frame(message_frame)
    audio_frame.pack(fill='x', pady=5)

    def preview_audio():
        text = message_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Text", "Please enter some text first!")
            return

        # Stop any playing audio
        pygame.mixer.music.stop()
        
        # Get language code if translation is enabled
        lang = 'en'
        if translate_var.get():
            lang = next(lang[1] for lang in languages if lang[0] == language_combobox.get())

        # Convert and play
        audio_file = text_to_audio(text, lang)
        if (audio_file):
            # Store current audio file
            if current_audio_file[0]:
                try:
                    pygame.mixer.music.stop()
                    os.remove(current_audio_file[0])
                except:
                    pass
            current_audio_file[0] = audio_file

            try:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play audio: {e}")

    def stop_audio():
        pygame.mixer.music.stop()

    # Audio controls
    btn_preview = ttk.Button(audio_frame, text="Preview Audio", command=preview_audio)
    btn_preview.pack(side='left', padx=5)
    
    btn_stop = ttk.Button(audio_frame, text="Stop Audio", command=stop_audio)
    btn_stop.pack(side='left', padx=5)

    # Add send as audio option
    send_audio_var = tk.BooleanVar()
    send_audio_check = ttk.Checkbutton(
        audio_frame, 
        text="Send as audio message", 
        variable=send_audio_var,
        command=lambda: audio_selected_label.config(
            text="✓ Audio will be sent" if send_audio_var.get() else "✗ Text will be sent"
        )
    )
    send_audio_check.pack(side='left', padx=5)
    
    audio_selected_label = ttk.Label(audio_frame, text="✗ Text will be sent")
    audio_selected_label.pack(side='left', padx=5)

    # Advanced options frame
    advanced_frame = ttk.LabelFrame(root, text="Advanced Options")
    advanced_frame.pack(pady=10, padx=20, fill='x')

    # Translation options
    translate_var = tk.BooleanVar()
    translate_check = ttk.Checkbutton(advanced_frame, text="Translate message", variable=translate_var)
    translate_check.pack(pady=5)
    
    language_combobox = ttk.Combobox(advanced_frame, values=[lang[0] for lang in languages], width=25)
    language_combobox.set("English")
    language_combobox.pack(pady=5)
    language_combobox.config(state='disabled')

    # Schedule options with better validation
    schedule_frame = ttk.Frame(advanced_frame)
    schedule_frame.pack(fill='x', pady=5)
    
    schedule_var = tk.BooleanVar()
    schedule_check = ttk.Checkbutton(schedule_frame, text="Schedule message", variable=schedule_var)
    schedule_check.pack(side='left', padx=5)
    
    time_frame = ttk.Frame(advanced_frame)
    time_frame.pack(fill='x', pady=5)
    
    time_label = ttk.Label(time_frame, text="Time (HH:MM):")
    time_label.pack(side='left', padx=5)
    
    time_entry = ttk.Entry(time_frame, width=10)
    time_entry.pack(side='left', padx=5)
    time_entry.config(state='disabled')

    # Repeat options
    lbl_times = tk.Label(advanced_frame, text="Repeat count:", font=("Helvetica", 12))
    lbl_times.pack(pady=5)
    times_entry = tk.Entry(advanced_frame, font=("Helvetica", 14), width=25)
    times_entry.insert(0, "1")
    times_entry.pack(pady=5)

    def on_translate_toggle():
        language_combobox.config(state='normal' if translate_var.get() else 'disabled')

    def on_schedule_toggle():
        time_entry.config(state='normal' if schedule_var.get() else 'disabled')
        if not schedule_var.get():
            time_entry.delete(0, tk.END)

    translate_check.config(command=on_translate_toggle)
    schedule_check.config(command=on_schedule_toggle)

    def validate_schedule_time():
        if schedule_var.get():
            time_str = time_entry.get().strip()
            try:
                hours, minutes = map(int, time_str.split(':'))
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    raise ValueError
                return True
            except (ValueError, AttributeError):
                messagebox.showwarning("Invalid Time", "Please enter time in HH:MM format (24-hour)")
                return False
        return True

    def send_msg():
        # Stop any playing audio
        pygame.mixer.music.stop()

        if schedule_var.get() and not validate_schedule_time():
            return

        receivers = receiver_entry.get().split(",")
        message = message_text.get("1.0", tk.END).strip()
        times_to_send = times_entry.get().strip() or "1"

        try:
            times_to_send = int(times_to_send)
            if times_to_send <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number of times.")
            return

        # Process message based on options
        if translate_var.get():
            dest_lang = next(lang[1] for lang in languages if lang[0] == language_combobox.get())
            message = translate_message(message, dest_lang)

        # Generate audio if needed
        audio_file = None
        if send_audio_var.get():
            lang = 'en'
            if translate_var.get():
                lang = next(lang[1] for lang in languages if lang[0] == language_combobox.get())
            audio_file = text_to_audio(message, lang)
            if not audio_file:
                messagebox.showerror("Error", "Failed to create audio file")
                return

        for receiver in receivers:
            receiver = receiver.strip()
            if receiver:
                if schedule_var.get():
                    schedule_time = time_entry.get().strip()
                    if schedule_time:
                        schedule_message(receiver, message, schedule_time, send_audio_var.get(), audio_file)
                        messagebox.showinfo("Scheduled", f"Message scheduled for {receiver} at {schedule_time}")
                else:
                    for _ in range(times_to_send):
                        send_message(receiver, message, send_audio_var.get(), audio_file)
                    messagebox.showinfo("Sent", f"Message sent {times_to_send} times to {receiver}")

        # Clean up audio file
        if audio_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except:
                pass

        back_to_menu()

    btn_send = create_button("Send", send_msg)
    btn_send.pack(pady=10, padx=20, fill='x')

    def back_to_menu():
        # Clean up audio
        pygame.mixer.music.stop()
        if current_audio_file[0] and os.path.exists(current_audio_file[0]):
            try:
                os.remove(current_audio_file[0])
            except:
                pass
        pygame.mixer.quit()
        
        for widget in root.winfo_children():
            widget.destroy()
        display_menu()

    btn_back = create_button("Back to Menu", back_to_menu)
    btn_back.pack(pady=10, padx=20, fill='x')

def check_online_status(driver, contact_name):
    try:
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(2) 
        search_box.send_keys(Keys.RETURN)

        status_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[@title='online' or @title='offline']"))
        )
        status = status_element.get_attribute("title")
        return status  
    except TimeoutException:
        return "offline"  
    except Exception as e:
        print(f"Error checking online status: {e}")
        return "unknown" 

def check_online_status_gui():
    for widget in root.winfo_children():
        widget.destroy()

    lbl_check_status = tk.Label(root, text="Check Online Status", font=("Helvetica", 18))
    lbl_check_status.pack(pady=20)

    lbl_contact = tk.Label(root, text="Enter contact name:", font=("Helvetica", 12))
    lbl_contact.pack(pady=5)
    contact_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
    contact_entry.pack(pady=10)

    def check_status():
        contact_name = contact_entry.get().strip()
        if contact_name:
            status = check_online_status(driver, contact_name)  
            if status == "online":
                messagebox.showinfo("Online Status", f"{contact_name} is awake, I mean online!")
            else:
                messagebox.showinfo("Online Status", f"{contact_name} is probably sleeping, I mean  offline.")
        else:
            messagebox.showwarning("Input Error", "Please enter a contact name.")

        back_to_menu()

    btn_check = create_button("Check Status", check_status)
    btn_check.pack(pady=10, padx=20, fill='x')

    def back_to_menu():
        for widget in root.winfo_children():
            widget.destroy()
        display_menu()

    btn_back = create_button("Back to Menu", back_to_menu)
    btn_back.pack(pady=10, padx=20, fill='x')

def schedule_message(contact_name, message, time_to_send, is_audio=False, audio_file=None):
    try:
        schedule.every().day.at(time_to_send).do(
            send_message, contact_name, message, is_audio, audio_file
        )
        print(f"Scheduled message to {contact_name} at {time_to_send}")
    except Exception as e:
        print(f"Failed to schedule message: {e}")

def generate_mock_location_link(mock_location):
    try:
        geolocator = Nominatim(user_agent="Mozilla/5.0")  # Using a standard user agent
        location = geolocator.geocode(mock_location, timeout=10)  # Added timeout
        if location:
            latitude, longitude = location.latitude, location.longitude
            # Use a more reliable Google Maps link format
            maps_link = f"https://maps.google.com/?q={latitude},{longitude}"
            print(f"Generated location coordinates: {latitude}, {longitude}")
            return maps_link
        print(f"Could not find location: {mock_location}")
        return None
    except Exception as e:
        print(f"Error in generate_mock_location_link: {str(e)}")
        return None

def send_live_location_via_whatsapp(contact_name, location_link=None):
    try:
        # Click attach button
        attach_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach"]'))
        )
        driver.execute_script("arguments[0].click();", attach_button)
        time.sleep(2)

        # Click location option
        location_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]'))
        )
        # Find the location button by its text content
        for button in location_buttons:
            if "Location" in button.get_attribute("innerHTML"):
                button.click()
                break
        time.sleep(2)

        # Click "Share live location" button
        share_live_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]'))
        )
        for button in share_live_buttons:
            if "Share live location" in button.get_attribute("innerHTML"):
                button.click()
                break
        time.sleep(2)

        # Send button
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
        )
        send_button.click()
        print("Live location shared successfully")

    except Exception as e:
        print(f"Error sharing live location: {str(e)}")
        if location_link:
            # Fallback to sending location as a message
            send_message(contact_name, f"📍 My location: {location_link}")

def send_mock_location_via_whatsapp(contact_name, mock_location):
    try:
        # First generate the location link
        location_link = generate_mock_location_link(mock_location)
        if not location_link:
            raise Exception("Could not generate location coordinates")

        # Click attach button
        attach_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach"]'))
        )
        driver.execute_script("arguments[0].click();", attach_button)
        time.sleep(2)

        # Click location option
        location_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]'))
        )
        for button in location_buttons:
            if "Location" in button.get_attribute("innerHTML"):
                button.click()
                break
        time.sleep(2)

        # Enter location in search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
        )
        search_box.clear()
        search_box.send_keys(mock_location)
        time.sleep(3)  # Wait for search results

        # Select first result
        try:
            first_result = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="listitem"]'))
            )
            first_result.click()
            time.sleep(1)

            # Click send button
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
            )
            send_button.click()
            print(f"Mock location sent successfully to {contact_name}")

        except TimeoutException:
            # If no results found, send as a message
            print("No location results found, sending as message")
            send_message(contact_name, f"📍 My location: {location_link}")

    except Exception as e:
        print(f"Error sending mock location: {str(e)}")
        # Final fallback
        if location_link:
            send_message(contact_name, f"📍 My location: {location_link}")

def share_mock_location_gui():
    for widget in root.winfo_children():
        widget.destroy()

    lbl_location = tk.Label(root, text="Share Location", font=("Helvetica", 18))
    lbl_location.pack(pady=20)

    def back_to_menu():
        for widget in root.winfo_children():
            widget.destroy()
        display_menu()

    # Contact input
    lbl_receiver = tk.Label(root, text="Enter contact names (comma separated):", font=("Helvetica", 12))
    lbl_receiver.pack(pady=5)
    receiver_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
    receiver_entry.pack(pady=10)

    # Location type selection
    location_type_frame = ttk.LabelFrame(root, text="Location Type")
    location_type_frame.pack(pady=10, padx=20, fill='x')
    
    location_type = tk.StringVar(value="mock")
    mock_radio = ttk.Radiobutton(location_type_frame, text="Mock Location", variable=location_type, value="mock")
    live_radio = ttk.Radiobutton(location_type_frame, text="Real Live Location", variable=location_type, value="live")
    mock_radio.pack(side='left', padx=10)
    live_radio.pack(side='left', padx=10)

    # Mock location input
    mock_frame = ttk.LabelFrame(root, text="Mock Location")
    mock_frame.pack(pady=10, padx=20, fill='x')
    
    lbl_mock_location = tk.Label(mock_frame, text="Enter location (e.g., 'Liaqat Bazar, Quetta'):", font=("Helvetica", 12))
    lbl_mock_location.pack(pady=5)
    location_entry = tk.Entry(mock_frame, font=("Helvetica", 14), width=30)
    location_entry.pack(pady=10)

    # Duration selection
    duration_frame = ttk.LabelFrame(root, text="Share Duration")
    duration_frame.pack(pady=10, padx=20, fill='x')
    
    duration_var = tk.IntVar(value=15)
    ttk.Radiobutton(duration_frame, text="15 minutes", variable=duration_var, value=15).pack(side='left', padx=5)
    ttk.Radiobutton(duration_frame, text="1 hour", variable=duration_var, value=60).pack(side='left', padx=5)
    ttk.Radiobutton(duration_frame, text="8 hours", variable=duration_var, value=480).pack(side='left', padx=5)

    def send_location():
        try:
            receivers = receiver_entry.get().split(",")
            if not receivers or not receivers[0].strip():
                messagebox.showwarning("Input Error", "Please enter at least one contact name")
                return

            is_mock = location_type.get() == "mock"
            if is_mock and not location_entry.get().strip():
                messagebox.showwarning("Input Error", "Please enter a mock location")
                return

            for receiver in receivers:
                receiver = receiver.strip()
                if not receiver:
                    continue

                try:
                    if is_mock:
                        mock_location = location_entry.get().strip()
                        location_link = generate_mock_location_link(mock_location)
                        if location_link:
                            # Regular location link message
                            send_message(receiver, f"My current location: {location_link}")
                            messagebox.showinfo("Success", f"Mock location sent to {receiver}")
                        else:
                            messagebox.showerror("Error", "Could not generate location link")
                    else:
                        # Send actual live location
                        click_location_button(receiver, duration_var.get())
                        messagebox.showinfo("Success", f"Live location shared with {receiver}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to send location to {receiver}: {str(e)}")

            back_to_menu()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def click_location_button(contact_name, duration_minutes):
        try:
            # Click attach button
            attach_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach"]'))
            )
            driver.execute_script("arguments[0].click();", attach_button)
            time.sleep(2)

            # Click location option
            location_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]'))
            )
            for button in location_buttons:
                if "Location" in button.get_attribute("innerHTML"):
                    button.click()
                    break
            time.sleep(2)

            # Click live location option
            live_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]'))
            )
            for button in live_buttons:
                if "Share live location" in button.get_attribute("innerHTML"):
                    button.click()
                    break
            time.sleep(2)

            # Duration selection buttons might be in a different format
            duration_map = {
                15: ["15", "minutes"],
                60: ["1", "hour"],
                480: ["8", "hours"]
            }
            
            # Look for duration button
            duration_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]'))
            )
            duration_text = duration_map.get(duration_minutes, ["15", "minutes"])
            for button in duration_buttons:
                if all(text in button.get_attribute("innerHTML") for text in duration_text):
                    button.click()
                    break
            time.sleep(1)

            # Click send
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
            )
            send_button.click()
            print(f"Live location sent to {contact_name}")

        except Exception as e:
            print(f"Error in click_location_button: {str(e)}")
            raise

    btn_send = create_button("Share Location", send_location)
    btn_send.pack(pady=10, padx=20, fill='x')

    btn_back = create_button("Back to Menu", back_to_menu)
    btn_back.pack(pady=10, padx=20, fill='x')

languages = [
    ("English", "en"), ("Pashto", "ps"), ("Urdu", "ur"), ("Spanish", "es"), ("French", "fr"),
    ("German", "de"), ("Chinese (Simplified)", "zh-CN"), ("Chinese (Traditional)", "zh-TW"),
    ("Arabic", "ar"), ("Russian", "ru"), ("Portuguese", "pt"), ("Hindi", "hi"), ("Bengali", "bn"),
    ("Japanese", "ja"), ("Italian", "it"), ("Korean", "ko"), ("Turkish", "tr"), ("Dutch", "nl"),
    ("Polish", "pl"), ("Romanian", "ro"), ("Greek", "el"), ("Swedish", "sv"), ("Czech", "cs"),
    ("Thai", "th"), ("Vietnamese", "vi"), ("Hungarian", "hu"), ("Indonesian", "id"), ("Finnish", "fi"),
    ("Danish", "da"), ("Norwegian", "no"), ("Hebrew", "he"), ("Hindi", "hi"), ("Tamil", "ta"),
    ("Telugu", "te"), ("Gujarati", "gu"), ("Marathi", "mr"), ("Malayalam", "ml"), ("Punjabi", "pa"),
    ("Ukrainian", "uk"), ("Kazakh", "kk"), ("Serbian", "sr"), ("Croatian", "hr"), ("Bulgarian", "bg"),
    ("Slovak", "sk"), ("Slovenian", "sl"), ("Lithuanian", "lt"), ("Latvian", "lv"), ("Estonian", "et")
]

def translate_message(text, dest_lang="en"):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text


def send_translated_message(driver, contact_name, message, dest_lang):
    translated_message = translate_message(message, dest_lang)
    send_message(contact_name, translated_message)
    print(f"Sent translated message to {contact_name}: {translated_message}")

stop_flag = False

def change_profile_picture_superfast(frames_folder):
    frame_files = sorted(os.listdir(frames_folder))

    try:
        print("Starting rapid profile picture change...")

        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')

        for frame in frame_files:
            if stop_flag:  
                print("Profile change process stopped.")
                return 
            frame_path = os.path.join(frames_folder, frame)
            if os.path.isfile(frame_path):
                file_input.send_keys(frame_path)
                print(f"Uploaded profile picture: {frame}")

                try:
                    done_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div/div[2]/span/div/div/span')
                    done_button.click()
                except:
                    pass

                time.sleep(0.05)

    except Exception as e:
        print(f"Error during profile picture update: {e}")

def upload_pictures_gui():
    for widget in root.winfo_children():
        widget.destroy()

    lbl_warning = tk.Label(
        root,
        text="WARNING: Use this on your own risk!",
        fg="red",
        font=("Helvetica", 16, "bold")
    )
    lbl_warning.pack(pady=20)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=20)

    def back_to_menu():
        global stop_flag
        stop_flag = True
        for widget in root.winfo_children():
            widget.destroy()
        display_menu()

    btn_back = create_button("Back to Menu", back_to_menu)
    btn_back.pack(pady=10, padx=20, fill='x')

    def take_risk():
        global stop_flag
        for widget in root.winfo_children():
            widget.destroy()

        lbl_risk = tk.Label(root, text="Choose an option:", font=("Helvetica", 16))
        lbl_risk.pack(pady=20)

        def already_converted():
            frames_folder = filedialog.askdirectory(title="Select Folder with Frames")
            if not frames_folder:
                messagebox.showwarning("No Selection", "No folder selected.")
                return

            for widget in root.winfo_children():
                widget.destroy()

            text_frame = tk.Frame(root)
            text_frame.pack(pady=20, fill="both", expand=True)

            instruction_text = (
                "It was really hard to find the XPATH to change profile picture. "
                "Please go and select manually from the WhatsApp running in ChromeDriver right now. "
                "When done, press Enter here, and I will change the profile pictures super fast as if the video is played.\n\n"
                "We say 'Take Risk' because if you try to change your profile like this, WhatsApp may ban your account, "
                "or may limit your profile change per second. We are not responsible for any issues caused by this process."
            )

            text_box = tk.Text(text_frame, wrap=tk.WORD, font=("Helvetica", 12), height=10)
            text_box.insert(tk.END, instruction_text)
            text_box.config(state=tk.DISABLED) 
            text_box.pack(side=tk.LEFT, fill="both", expand=True)

            scrollbar = tk.Scrollbar(text_frame, command=text_box.yview)
            scrollbar.pack(side=tk.RIGHT, fill='y')
            text_box.config(yscrollcommand=scrollbar.set)

            def done():
                global stop_flag
                stop_flag = False 
                threading.Thread(target=change_profile_picture_superfast, args=(frames_folder,)).start()

            btn_done = create_button("Done", done)
            btn_done.pack(pady=10, padx=20, fill='x')

            def stop():
                global stop_flag
                stop_flag = True 
                messagebox.showinfo("Stopped", "Profile change process has been stopped.")
                for widget in root.winfo_children():
                    widget.destroy()
                display_menu() 

            btn_stop = create_button("Stop Changing Profile", stop)
            btn_stop.pack(pady=10, padx=20, fill='x')

        btn_already = create_button("I have already converted Video to Frames", already_converted)
        btn_already.pack(pady=10, padx=20, fill='x')

        def not_converted():
            video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4 *.avi *.mov")])
            if not video_path:
                messagebox.showwarning("No Selection", "No video file selected.")
                return

            output_folder = filedialog.askdirectory(title="Select Frame Output Folder")
            if not output_folder:
                messagebox.showwarning("No Selection", "No output folder selected.")
                return

            try:
                extract_frames(video_path, output_folder)
                messagebox.showinfo("Success", f"Frames extracted successfully to {output_folder}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        btn_not_converted = create_button("I have not converted Video to Frames", not_converted)
        btn_not_converted.pack(pady=10, padx=20, fill='x')

        btn_back = create_button("Back to Menu", back_to_menu)
        btn_back.pack(pady=10, padx=20, fill='x')

    btn_risk = create_button("Take Risk", take_risk)
    btn_risk.pack(pady=10, padx=20, fill='x')

def extract_frames(video_path, output_folder, every_n_frame=1):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frame_id = 0
    os.makedirs(output_folder, exist_ok=True) 
    
    while success:
        if frame_id % every_n_frame == 0:  
            cv2.imwrite(os.path.join(output_folder, f"frame{count}.jpg"), image)
            count += 1
        success, image = vidcap.read()
        frame_id += 1

def change_profile_picture_task(frames_folder):
    global stop_flag
    try:
        while not stop_flag:
            change_profile_picture_superfast(frames_folder)
            if stop_flag:
                break
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

stop_flag = False
root = tk.Tk()
root.title("WhatsApp Automation Tool")
root.geometry("400x500")
root.resizable(True, True)  

lbl_welcome = tk.Label(root, text="Welcome to my automation tool", font=("Helvetica", 16))
lbl_welcome.pack(pady=20)

btn_start = tk.Button(root, text="Start the tool", command=open_whatsapp_web, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat")
btn_start.bind("<Enter>", lambda event, button=btn_start: button.config(bg="#66b3ff")) 
btn_start.bind("<Leave>", lambda event, button=btn_start: button.config(bg="#4CAF50"))  
btn_start.pack(pady=10)

btn_exit = tk.Button(root, text="Exit the tool", command=exit_tool, font=("Helvetica", 14), bg="#f44336", fg="white", relief="flat")
btn_exit.bind("<Enter>", lambda event, button=btn_exit: button.config(bg="#ff6666")) 
btn_exit.bind("<Leave>", lambda event, button=btn_exit: button.config(bg="#f44336"))  
btn_exit.pack(pady=10)

btn_login = tk.Button(root, text="I am now logged in", command=logged_in, font=("Helvetica", 14), bg="#2196F3", fg="white", relief="flat")
btn_login.bind("<Enter>", lambda event, button=btn_login: button.config(bg="#66b3ff"))  
btn_login.bind("<Leave>", lambda event, button=btn_login: button.config(bg="#2196F3"))  

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)  

schedule_thread = threading.Thread(target=run_schedule, daemon=True)
schedule_thread.start()
root.mainloop()
