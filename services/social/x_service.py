import tweepy
import os
from fastapi import HTTPException
from dotenv import load_dotenv

from services.post.post_service import PostService
from utils.file_utils import FileHandler

KEY_CONTENT = "x_content"

class XAPI:
    def __init__(self):
        load_dotenv()
        consumer_key = os.getenv("X_CONSUMER_KEY")
        consumer_secret = os.getenv("X_CONSUMER_SECRET")
        access_token = os.getenv("X_ACCESS_TOKEN")
        access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

        self.allow_posting = os.getenv("ALLOW_POSTING", "false").lower() == "true"

        self.client = tweepy.Client(
            consumer_key=consumer_key, 
            consumer_secret=consumer_secret,
            access_token=access_token, 
            access_token_secret=access_token_secret
        )

        self.auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        self.file_handler = FileHandler()
        self.post_service = PostService()

    def combine_caption(self, caption, links=None, hashtags=None):
        """Combines the caption with links and hashtags, avoiding duplicate hashtags that already appear in the caption."""
        parts = [caption.strip()] if caption else []
        existing_caption = caption.lower() if caption else ""
        
        # Añadir links si existen
        if links:
            links_block = "\n".join(f"{link['description']}: {link['url']}" for link in links)
            parts.append(links_block)

        # Añadir hashtags solo si el hashtag exacto (#tag) no está ya en el caption
        if hashtags:
            unique_hashtags = []
            for tag in hashtags:
                clean_tag = tag.lstrip('#').lower()
                hashtag_with_hash = f"#{clean_tag}"
                if hashtag_with_hash not in existing_caption:
                    unique_hashtags.append(hashtag_with_hash)
            
            if unique_hashtags:
                hashtags_block = " ".join(unique_hashtags)
                parts.append(hashtags_block)

        return "\n".join(parts)


    def get_thread_list(self, threads):
        """Builds list of (caption, media) tuples for each thread tweet."""
        return [
            (
                self.combine_caption(thread[KEY_CONTENT], thread.get("x_links", [])),
                thread.get("media_path_remote") or thread.get("media_path")
            )
            for thread in threads
        ]

    def upload_media_tweet(self, media_path):
        if not media_path:
            raise ValueError("media_path cannot be empty")

        if media_path.startswith("http://") or media_path.startswith("https://"):
            media_path = self.file_handler.download_media_to_temp(media_path)

        if not os.path.isfile(media_path):
            raise FileNotFoundError(f"Media file not found at path: {media_path}")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4']
        ext = os.path.splitext(media_path)[1].lower()
        if ext not in valid_extensions:
            raise ValueError(f"Unsupported media extension '{ext}'. Supported: {valid_extensions}")

        try:
            media = self.api.media_upload(media_path)
            return media.media_id
        except Exception as e:
            raise RuntimeError(f"Failed to upload media to Twitter: {e}")

    async def post_tweet(self, message, media_path=None, in_reply_to_tweet_id=None):
        if not self.allow_posting:
            raise HTTPException(status_code=403, detail="Posting is disabled by config.")

        try:
            print(f"Posting tweet: {message} with media: {media_path}")
            media_id = self.upload_media_tweet(media_path) if media_path else None
            result = self.client.create_tweet(
                text=message, 
                media_ids=[media_id] if media_id else None, 
                in_reply_to_tweet_id=in_reply_to_tweet_id
            )
            print(f"✅ X: Tweet posted successfully: {result.data['id']}")
            return {"message": "Tweet posted successfully", "tweet_id": result.data["id"]}
        finally:
            if media_path and media_path.startswith("/tmp/"):
                try:
                    os.remove(media_path)
                    print(f"Deleted temp file: {media_path}")
                except Exception as e:
                    print(f"Warning: Failed to delete {media_path}: {e}")

    async def post_thread(self, tweets):
        if not tweets:
            raise HTTPException(status_code=400, detail="The thread is empty.")

        if not self.allow_posting:
            raise HTTPException(status_code=403, detail="Thread posting is disabled by config.")

        first_text, first_media = tweets[0]
        first_response = await self.post_tweet(first_text, first_media)
        tweet_id = first_response["tweet_id"]

        for text, media in tweets[1:]:
            response = await self.post_tweet(text, media, in_reply_to_tweet_id=tweet_id)
            tweet_id = response["tweet_id"]

        print(f"✅ X: Thread posted successfully {tweet_id}")
        return {"message": "X Thread posted successfully", "thread_root_id": first_response["tweet_id"]}

    async def run_posts(self):
        if not self.allow_posting:
            raise HTTPException(status_code=403, detail="Posting is disabled by configuration.")
        
        tweet_data = await self.post_service.get_next_post('x_status', 'not_posted', extra_filters={'is_processed': True})

        if not tweet_data:
            raise HTTPException(status_code=404, detail="No tweets to post.")

        tweet_text = tweet_data.get(KEY_CONTENT)
        media_path = tweet_data.get("media_path_remote") or tweet_data.get("media_path")
        is_thread = tweet_data.get("is_thread")
        threads = tweet_data.get("threads")
        links = tweet_data.get("x_links", [])
        hashtags = tweet_data.get("hashtags_x", [])

        if is_thread:
            first_caption = self.combine_caption(tweet_text, links, hashtags)
            first_tweet = (first_caption, media_path)
            thread_list = self.get_thread_list(threads)
            tweets = [first_tweet] + thread_list
            result = await self.post_thread(tweets)
        else:
            combined_caption = self.combine_caption(tweet_text, links, hashtags)
            result = await self.post_tweet(combined_caption, media_path)

        await self.post_service.update_post_status(tweet_data["id"], status_key="x_status")
        return result
