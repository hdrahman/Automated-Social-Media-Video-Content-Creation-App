# Automated Social Media Video Content Creation App

This project automates the creation of mobile-friendly social media videos using content from top daily posts on subreddits. It leverages a combination of **Reddit API**, **AWS Polly**, and **MoviePy** to generate AI voiceovers, attach visually optimized backgrounds, and overlay synchronized text subtitles. The resulting videos are well-optimized for mobile viewing with a 9:16 aspect ratio.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Development Blog](#development-blog)

## Overview

This app automates the following tasks:
1. Fetching daily top posts from the **cscareerquestions** subreddit using **Reddit API**.
2. Applying **AWS Polly** to generate natural-sounding voiceovers from the post titles, body, and top comments.
3. Utilizing **MoviePy** to overlay the voiceovers on top of **Minecraft** gameplay footage cropped to mobile resolution.
4. Adding text subtitles that are split into manageable lines and timed precisely with the audio narration.

## Technologies Used
- **Python**
- **PRAW**: To interact with the Reddit API and retrieve top posts.
- **AWS Polly**: To convert text content into high-quality, natural-sounding AI voiceovers using SSML.
- **MoviePy**: For video editing, including adding subtitles and syncing the voiceover with background footage.
- **TQDM**: For displaying a progress bar when processing multiple posts.
- **Better Profanity**: For detecting and censoring inappropriate language in the Reddit post content.
- **NLTK**: For sentence tokenization, helping to split post text into manageable subtitle lines.

## Features
- **Automated Video Generation**: Automatically generates videos with synced subtitles and voiceovers from subreddit content.
- **Censored Profanity**: Detects and censors profanity using the **Better Profanity** library, replacing it with strategic pauses.
- **SSML Integration**: Incorporates pauses and breaks in the voiceover narration using **SSML** to improve the natural flow of the AI voice.
- **Subtitle Management**: Dynamically splits text into lines that fit within the mobile screen, adjusting based on the audio's duration.
- **Mobile-Optimized Video**: The videos are optimized for social media platforms like Instagram with a 9:16 aspect ratio.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/social-media-video-generator.git
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   **Note**: You will need to have **AWS** credentials set up for **Polly** and **Reddit API** keys for fetching subreddit content.

3. Ensure that **FFmpeg** and **ImageMagick** are installed on your system.

## Usage

1. Set up your **Reddit API** credentials:
   ```python
   reddit = praw.Reddit(
       client_id="your_client_id",
       client_secret="your_client_secret",
       user_agent="your_user_agent"
   )
   ```

2. Set up **AWS Polly**:
   ```python
   polly = boto3.client(
       'polly',
       aws_access_key_id='your_access_key',
       aws_secret_access_key='your_secret_key',
       region_name='your_region'
   )
   ```

3. Run the script:
   ```bash
   python main.py
   ```

4. The generated video files will be saved in the root directory with the names `video1.mp4`, `video2.mp4`, etc.

## Future Enhancements

This project is a **work in progress**. Planned features include:
1. **FastAPI Integration**: I plan to integrate **FastAPI** to enhance efficiency and offer an API service for video generation.
2. **Executable Program**: I aim to convert this script into an executable file for broader distribution and ease of use.
3. **Zap Cap API**: Implementing the **Zap Cap API** to enhance subtitle accuracy, improving the timing and quality of the subtitle-to-audio synchronization.

## Development Blog

You can follow the detailed development process of this project in my [Development Blog](https://docs.google.com/document/d/1SKYHHvXURDxt2aZI7NvKn2Gcnnu5U1JpBUy2LekZ7o4/edit?usp=sharing).
