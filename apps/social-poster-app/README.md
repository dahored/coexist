# 🐦 Social Poster App

An automated Python script to post tweets and threads (with or without images) on **X (formerly Twitter)** using the X API v2.

---

## 📦 Requirements

- Python 3.9+
- pip
- Twitter Developer Account ([Get credentials](https://developer.x.com/en/portal/))

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/coexist-apps.git
cd coexist-apps/apps/social-poster-app
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Configuration

### 4. Create the .env file

```bash
cp .env.example .env
```

### 5. Add your X (Twitter) credentials
Go to the [X Developer Portal](https://developer.x.com/en/portal/) and create an app to get the credentials. Add them to your .env file:

```bash
X_CONSUMER_KEY=your_consumer_key
X_CONSUMER_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

Other variables
```bash
X_JSON_FILE=../data/twitter_posts.json
X_ALLOW_POSTING=true
```


💡 Set X_ALLOW_POSTING=false to test without publishing.


## 🏁 Running the Script

After setting everything up, run:

```bash
python index.py
```

This will:

	• Load pending posts from the JSON file
	• Generate images from prompts (if defined)
	• Post single tweets or threads
	• Update the JSON file with the tweet status


## 📂 JSON File Structure
The script uses a JSON file to manage queued tweets. Here’s an example structure:
```json
{
    "name": "Twitter List",
    "description": "A list of Twitter posts to be shared",
    "topic": "Social Media",
    "posts": [
        {
            "id": 1,
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \n\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "prompt_to_media": "",
            "media_path": "",
            "hashtags": ["#hashtag1", "#hashtag2"],
            "status": "posted",
            "is_thread": false,
            "threads": []
        },
        {
            "id": 2,
            "content": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \n\nExcepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "prompt_to_media": "",
            "media_path": null,
            "hashtags": [],
            "status": "not_posted",
            "is_thread": false,
            "threads": []
        },
        {
            "id": 3,
            "content": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.",
            "prompt_to_media": "generar imagen con fondo azul",
            "media_path": "/Users/daho/Documents/Projects/coexist-apps/apps/social-poster-app/modules/../public/uploads/images/image_file_tweet_3.png",
            "hashtags": [],
            "status": "not_posted",
            "is_thread": false,
            "threads": []
        },
        {
            "id": 4,
            "content": "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin.",
            "prompt_to_media": "",
            "media_path": "",
            "hashtags": [],
            "status": "not_posted",
            "is_thread": true,
            "threads": [
                {
                    "content": "In hac habitasse platea dictumst. Maecenas adipiscing faucibus.",
                    "prompt_to_media": "",
                    "media_path": "",
                    "hashtags": [],
                    "id": 400001
                },
                {
                    "content": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "prompt_to_media": "generar imagen con fondo rojo",
                    "media_path": "/Users/daho/Documents/Projects/coexist-apps/apps/social-poster-app/utils/../public/uploads/images/image_file_tweet_400002.png",
                    "hashtags": [],
                    "id": 400002
                }
            ]
        }
    ]
}
```



## ✨ Features
    • ✅ Single tweets and threaded tweets
    • 🖼️ Optional image generation from prompts
    • 🔁 JSON-based post queue
    • 🧠 Smart preprocessing for media and status updates
    • ⚙️ Fully async with Tweepy v2 support



## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📝 License

This project is licensed under the MIT License.
