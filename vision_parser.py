import base64
import requests
import json
import os
import time
from tenacity import retry, stop_after_attempt, wait_fixed


api_key = "sk-proj-rS5ndvzPPzz99BHBI1YdT3BlbkFJA79RvpuzIweYlBei3MC6"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_paths(directory):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and 
            os.path.splitext(f)[1].lower() in image_extensions]
'''
def process_images(image_paths, batch_size=5):
    all_ads = []
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        base64_images = [encode_image(path) for path in batch]
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """Analyze these images and extract information about all of the advertisements shown, there are likely  multiple advertisments per image. For each ad, provide every piece of information listed on the information card: the company name, the 16-digit library id (at the top of the card), if the ad is active or not, when the ad started running, what specific social media platforms the ad runs on (their icons will be shown), all of the ad text, that is, the text associated with the ad, a description of the photo associated with the ad, and any specific discounts or offers mentioned. If you can't extract something, write "n/a" for that field. Take extra care, being extremely careful to make sure the library id is correct. Be absolutely sure that you process all advertisements in the images. Strictly format the response as a JSON object with an 'ads' array containing objects for each ad (and no text outside of this) as shown in this example:
                    {
  "ads": [
    {
      "company": "Gaia Health",
      "library_id": "1146296186451945",
      "active": True,
      "started": "Jul 19, 2024",
      "platforms": ["Facebook", "Instagram", "Audience Network", "Messenger"],
      "text": "Enhance your journey with herbal supplements designed to nurture your body at all stages of motherhood. Discover natural support for fertility, pregnancy & healthy lactation.*

*This statement has not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
      "photo_description": "A bottle of herbal supplement.",
      "discount": "n/a"
    },
    ...
    ]
    } """},
                        *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}} for image in base64_images]
                    ]
                }
            ],
            "max_tokens": 16384
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", 
                                 headers={"Authorization": f"Bearer {api_key}"}, 
                                 json=payload)
        
        # Parse the JSON response
        response_data = response.json()
        print(response_data)

# Extract the content from the response
        if 'choices' in response_data and len(response_data['choices']) > 0:
            content = response_data['choices'][0]['message']['content']
            json_string = content.strip().removeprefix('```json').removesuffix('```')
            print(json_string)
            print(240*"=")
    
    # Parse the content as JSON
            try:
                ads_data = json.loads(json_string)
                for ad in ads_data['ads']:
                    print(f"Company: {ad['company']}")
                    print(f"Library ID: {ad['library_id']}")
                    print(f"Description: {ad['text']}")
                    print(f"Photo: {ad['photo_description']}")
                    print(f"Active: {ad['active']}")
                    print(f"Launch Date/Run time: {ad['started']}")
                    print(f"Discounts/Offers: {ad['discount']}")
                    print("-" * 40)
                    all_ads.append(ad)
                print(len(ads_data['ads']))
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for batch {i//batch_size + 1}")
            except KeyError:
                print(f"Unexpected response structure for batch {i//batch_size + 1}")
        else:
            print(f"API request failed for batch {i//batch_size + 1}: {response.status_code}")
        
        time.sleep(2)  # Rate limiting
    
    return all_ads

output_photo_dir = "output_photo"
image_paths = get_image_paths(output_photo_dir)
all_ads = process_images(image_paths)

print(f"Total advertisements processed: {len(all_ads)}")
'''
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def make_api_call(payload):
    response = requests.post("https://api.openai.com/v1/chat/completions", 
                             headers={"Authorization": f"Bearer {api_key}"}, 
                             json=payload)
    response.raise_for_status()
    return response.json()

def process_images(image_paths, batch_size=3):
    all_ads = []
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        base64_images = [encode_image(path) for path in batch]
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """Analyze these images and extract information about all of the advertisements shown, there are likely  multiple advertisments per image. For each ad, provide every piece of information listed on the information card: the company name, the 16-digit library id (at the top of the card), if the ad is active or not, when the ad started running, what specific social media platforms the ad runs on (their icons will be shown), all of the ad text, that is, the text associated with the ad, a description of the photo associated with the ad, and any specific discounts or offers mentioned. If you can't extract something, write "n/a" for that field. Take extra care, being extremely careful to make sure the library id is correct-- the library id being correct is absolutely crucial. Make sure you grab all of the description text associated with the ad, not just the first sentence. Be absolutely sure that you process all advertisements in the images. Lastly, come up with anywhere between 3-5 tags describing the advertisement. Strictly format the response as a JSON object with an 'ads' array containing objects for each ad (and no text outside of this) as shown in this example:
                    {
  "ads": [
    {
      "company": "Gaia Health",
      "library_id": "1146296186451945",
      "active": true,
      "started": "Jul 19, 2024",
      "platforms": ["Facebook", "Instagram", "Audience Network", "Messenger"],
      "text": "Enhance your journey with herbal supplements designed to nurture your body at all stages of motherhood. Discover natural support for fertility, pregnancy & healthy lactation.*

*This statement has not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
      "photo_description": "A bottle of herbal supplement.",
      "discount": "n/a"
       "tags": ["maternity", "supplements", "pregnancy", "motherhood" ]
    },
    ...
    ]
    } """},
                        *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}} for image in base64_images]
                    ]
                }
            ],
            "max_tokens": 4096
        }

        try:
            response_data = make_api_call(payload)
            
            if 'choices' in response_data and len(response_data['choices']) > 0:
                content = response_data['choices'][0]['message']['content']
                json_string = content.strip().removeprefix('```json').removesuffix('```')
                
                ads_data = json.loads(json_string)
                for ad in ads_data['ads']:
                    print(f"Company: {ad['company']}")
                    print(f"Library ID: {ad['library_id']}")
                    print(f"Description: {ad['text']}")
                    print(f"Photo: {ad['photo_description']}")
                    print(f"Active: {ad['active']}")
                    print(f"Launch Date/Run time: {ad['started']}")
                    print(f"Discounts/Offers: {ad['discount']}")
                    print(f"Tags: {ad['tags']}")
                    print("-" * 40)
                all_ads.extend(ads_data['ads'])
                print(f"Processed {len(ads_data['ads'])} ads from batch {i//batch_size + 1}")
            else:
                print(f"Unexpected response structure for batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
        
        time.sleep(2)  # Rate limiting
    
    return all_ads

output_photo_dir = "output_photo"
image_paths = get_image_paths(output_photo_dir)
all_ads = process_images(image_paths)

print(f"Total advertisements processed: {len(all_ads)}")

# Save JSON output
output_file = "processed_ads.json"
with open(output_file, 'w') as f:
    json.dump({"ads": all_ads}, f, indent=2)

print(f"Processed ads saved to {output_file}")
  