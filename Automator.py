import praw, boto3, os
from better_profanity import profanity
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

#Set up Reddit API - PRAW
reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="your_user_agent"
    password="your_password",
    username="your_username",
)

#Set up AWS client
polly = boto3.client(
    'polly',
    aws_access_key_id='your_access_key',
    aws_secret_access_key='your_secret_key',
    region_name='your_region'
)

#pulling daily top posts from the cscareerquestions subreddit
subreddit = reddit.subreddit('cscareerquestions')
top_posts = subreddit.top(time_filter='day', limit=10)

# Function to fetch top posts that are questions
def fetch_top_question_posts(subreddit, limit=10):
    validposts = []
    top_posts = subreddit.top(time_filter='day', limit=limit)
    for post in top_posts:
        if post.title.strip().endswith('?'):
            validposts.append(post)
            if len(validposts) == 2:
                break
    return validposts

# Function to apply censoring and SSML formatting
def censor_and_format_text(title, body, topcomment):
    def censor(text):
        censored_text = profanity.censor(text)
        return censored_text.replace("****", '<break time="1s"/>')

    censored_title = censor(title)
    censored_body = censor(body)
    censored_comment = censor(topcomment)

    # Use SSML to add pauses
    return f"""
    <speak>
        {censored_title}
        <break time="0.5s"/>
        {censored_body}
        <break time="0.5s"/>
        {censored_comment}
        <break time="0.2s"/>
    </speak>
    """

# Function to generate audio using Polly
def generate_audio(text, filename="redditaudio.mp3"):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Matthew',
        TextType='ssml'
    )
    with open(filename, 'wb') as file:
        file.write(response['AudioStream'].read())
    return filename
# Function to prepare and attach video background
def getvideo(start_time, text, audio_file, idx):
    audio = AudioFileClip(audio_file)
    video = VideoFileClip("MC vid.mp4").without_audio()
    endtime = start_time + audio.duration + 0.2
    clip = video.subclip(start_time, endtime)
    
    # Save the end time to a file so that we can access it as a start time later
    with open("time.txt", "w") as file:
        file.write(str(endtime))
    
    # Crop sides of the 16:9 video to fit 9:16 phone screen (center crop)
    new_width = video.h * (9 / 16)
    cropped_video = clip.crop(x_center=video.w / 2, width=new_width, height=video.h)

    # Scale the cropped video to 1080x1920 to match the phone screen size
    scaled_video = cropped_video.resize((1080, 1920))

    # Clean text and remove SSML tags in place
    cleaned_text = text.replace('<speak>', '').replace('</speak>', '').replace('<break time="0.5s"/>', '').replace('<break time="0.2s"/>','')

    # Break the text into sentences
    sentences = sent_tokenize(cleaned_text)

    # Calculate total words across all sentences
    total_words = sum(len(sentence.split()) for sentence in sentences)

    # Calculate sentence durations and generate text clips
    text_clips = []
    sentence_start_time = 0
    max_words_per_line = 8  # Adjust this based on how much text can fit in one line

    for sentence in sentences:
        # Split sentence into lines with a max number of words
        words = sentence.split()
        lines = [' '.join(words[i:i + max_words_per_line]) for i in range(0, len(words), max_words_per_line)]

        # Calculate sentence duration based on word proportion to total words
        sentence_word_count = len(sentence.split())
        sentence_duration = audio.duration * (sentence_word_count / total_words)

        # Split the sentence duration across the lines
        line_duration = sentence_duration / len(lines)

        # Display each line as a text clip
        for line in lines:
            # Create text clip and set its duration and start time
            txt_clip = TextClip(line, fontsize=50, color='white', font="Arial")
            txt_clip = txt_clip.set_position('center').set_duration(line_duration).set_start(sentence_start_time)
            text_clips.append(txt_clip)

            # Update the start time for the next line
            sentence_start_time += line_duration
    
    # Combine the text clips with the video
    final_video = CompositeVideoClip([scaled_video] + text_clips)

    # Add audio to the final video
    final_video = final_video.set_audio(audio)

    # Save the final video
    final_video.write_videofile(f"video{idx + 1}.mp4", codec="libx264")


def get_start_time():
    if os.path.exists("time.txt"):
        with open("time.txt", "r") as file:
            return float(file.read())  # Read and convert to float
    return 0  # Default start time if file doesn't exist


# Main logic
subreddit = reddit.subreddit('cscareerquestions')
posts = fetch_top_question_posts(subreddit)
#use for loop so that two videos can be made with one call, saving resources.
for idx, post in enumerate(tqdm(posts, desc="Processing posts", total=len(posts))):
    title = post.title
    body = post.selftext
    post.comment_sort = "top"
    topcomment = post.comments[0].body

    formatted_text = censor_and_format_text(title, body, topcomment)
    audio_file = generate_audio(formatted_text)
    getvideo(get_start_time(), formatted_text, audio_file, idx)

    
