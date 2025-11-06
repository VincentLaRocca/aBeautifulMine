"""
Test YouTube Transcript API
"""

from youtube_transcript_api import YouTubeTranscriptApi

# Test video ID
video_id = "dQw4w9WgXcQ"

print("Testing YouTube Transcript API...")
print(f"Video ID: {video_id}")

try:
    # Method 1: Direct get_transcript
    print("\nMethod 1: get_transcript()")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(f"Success! Got {len(transcript)} transcript segments")
    print(f"First segment: {transcript[0]}")

except Exception as e:
    print(f"Method 1 failed: {e}")

try:
    # Method 2: list_transcripts then fetch
    print("\nMethod 2: list_transcripts().find_transcript().fetch()")
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Try to get English transcript
    transcript = transcript_list.find_transcript(['en'])
    transcript_data = transcript.fetch()
    print(f"Success! Got {len(transcript_data)} transcript segments")
    print(f"First segment: {transcript_data[0]}")

except Exception as e:
    print(f"Method 2 failed: {e}")

print("\nTest complete!")
