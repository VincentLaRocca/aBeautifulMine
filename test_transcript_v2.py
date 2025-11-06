"""
Test YouTube Transcript API - Version 2
Testing actual available methods
"""

from youtube_transcript_api import YouTubeTranscriptApi

video_id = "dQw4w9WgXcQ"

print("Testing YouTube Transcript API - Correct Usage")
print(f"Video ID: {video_id}\n")

try:
    # Try using list method (class method, not instance method)
    print("Method 1: Using YouTubeTranscriptApi.list(video_id)")
    result = YouTubeTranscriptApi.list(video_id)
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")

except Exception as e:
    print(f"Method 1 error: {type(e).__name__}: {e}")

try:
    # Try using fetch method
    print("\nMethod 2: Using YouTubeTranscriptApi.fetch(video_id)")
    result = YouTubeTranscriptApi.fetch(video_id)
    print(f"Result type: {type(result)}")
    print(f"Result length: {len(result) if hasattr(result, '__len__') else 'N/A'}")
    if result:
        print(f"First item: {result[0] if hasattr(result, '__getitem__') else result}")

except Exception as e:
    print(f"Method 2 error: {type(e).__name__}: {e}")

try:
    # Try instantiating the class first
    print("\nMethod 3: Instantiate then use methods")
    api = YouTubeTranscriptApi()
    result = api.list(video_id)
    print(f"Result: {result}")

except Exception as e:
    print(f"Method 3 error: {type(e).__name__}: {e}")

print("\nInvestigating library structure...")
import youtube_transcript_api
print(f"Package contents: {dir(youtube_transcript_api)}")
