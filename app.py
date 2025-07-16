import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os
import praw
from urllib.parse import urlparse
import re
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
load_dotenv()
key_1=os.getenv("REDDIT_1")
key_2=os.getenv("REDDIT_2")
groq=os.getenv("GROQ_API_KEY")
# llm =ChatGroq(model="llama-3.1-8b-instant",api_key=groq)
llm=ChatGroq(model="llama-3.3-70b-versatile",api_key=groq)
REDDIT_CLIENT_ID = key_1
REDDIT_CLIENT_SECRET = key_2
REDDIT_USER_AGENT = 'api'
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)


def extract_username_from_url(url):
    match = re.search(r'reddit\.com/user/([^/]+)/?', url)
    return match.group(1) if match else None

def extract_user_data_from_url(url):
   
    username = extract_username_from_url(url)
    if not username:
        print("Invalid Reddit user URL.")
        return None

    try:
        user = reddit.redditor(username)
        user._fetch()
    except Exception as e:
        print(f"Error fetching Reddit user '{username}': {e}")
        return None

    print(f"Fetching data for u/{username}...")

    profile_data = {
        "Username": user.name,
        "User ID": user.id, 
        "Total Karma": user.link_karma + user.comment_karma,
        "Link Karma": user.link_karma,
        "Comment Karma": user.comment_karma,
        "Awardee Karma": user.awardee_karma, 
        "Awarder Karma": user.awarder_karma, 
        "Is Employee": user.is_employee,
        "Is Moderator": user.is_mod, 
        "Has Verified Email": user.has_verified_email,
        "Is Gold": user.is_gold,
        "Created UTC": user.created_utc, 
        "Profile Icon URL": user.icon_img, 
        "Snoovatar Image URL": user.snoovatar_img, 
    }

    submissions = []
    try:
        for post in user.submissions.new(limit=20):
            submissions.append({
                "title": post.title,
                "subreddit": post.subreddit.display_name,
                "score": post.score,
                "num_comments": post.num_comments, 
                "upvote_ratio": post.upvote_ratio, 
                "url": f"https://reddit.com{post.permalink}",
                "text": post.selftext[:500] if post.selftext else None, 
                "created_utc": post.created_utc,
                "is_self_post": post.is_self, 
                "link_flair_text": post.link_flair_text, 
                "total_awards_received": post.total_awards_received, 
            })
    except Exception as e:
        print(f"Error fetching submissions for u/{username}: {e}")

    # Fetch recent comments
    comments = []
    try:
        for comment in user.comments.new(limit=20):
            comments.append({
                "body": comment.body[:500], 
                "subreddit": comment.subreddit.display_name,
                "score": comment.score,
                "url": f"https://reddit.com{comment.permalink}",
                "created_utc": comment.created_utc, 
                # "depth": comment.depth, 
                "is_submitter": comment.is_submitter,
                "total_awards_received": comment.total_awards_received,
            })
    except Exception as e:
        print(f"Error fetching comments for u/{username}: {e}")

    return {
        "profile": profile_data,
        "posts": submissions,
        "comments": comments
    }



col1,col2=st.columns(2)
with col1:
    st.image("Reddit-logo.png",width=300)
with col2:
    st.markdown("#  Reddit Profile Scrapper ")
url = st.text_input("Enter the Url of Reddit site")
if st.button("submit"):
    # if url :
    data=extract_user_data_from_url(url=url) 
    prompt=f"""## Reddit User Agent - Markdown Output Format provide response in much details like total response should be around 2000 words

You are a Reddit analysis agent.  
You will be provided with user data, including:

1. Profile Data {data['profile']}:  
- `Username`, `Total Karma`, `Link Karma`, `Comment Karma`, `Is Employee`, `Has Verified Email`, `Is Gold`, `Created UTC`

2. Post Data {data['posts']}:  
A list of posts with fields like:  
- `title`, `subreddit`, `score`, `num_comments`, `upvote_ratio`, `url`, `text`, `created_utc`, `is_self_post`, `link_flair_text`, `total_awards_received`

3. Comments Data {data['comments']}:  
A list of comments with fields like:  
- `body`, `subreddit`, `score`, `url`, `created_utc`, `is_submitter`, `total_Awards_recieved`

---

### Your Task

Analyze the Reddit user's behavior, personality, interests, and activity patterns based on the input data.  
Return the output in well-structured Markdown format — no JSON, no code blocks, no explanation.  

If any field is missing, return an empty value or skip that specific bullet point/section gracefully.  

---

### Final Markdown Output Format

User Profile
- Username: `Username`
- User ID: `User_ID`
- Profile URL: [Visit Profile](User_URL)

Tech Affinity
- Tech Savvy Level: `1-5`
- Preferred Learning Method: `Preferred Learning`

Daily Routine
- Morning: `...`
- Afternoon: `...`
- Evening: `...`
- Night: `...`

Engagement Overview
- Post Frequency: `Low | Medium | High`
- Comment Frequency: `Low | Medium | High`
- Overall Engagement Score: `1-10`

Work Style
- Work Type: `Remote | Onsite | Hybrid`
- Work Hours: `Typical work hours or schedule`

Subreddit Focus
- Subreddit Activity Level: `1-10`

Post Type Frequency
- Text Posts: `Low | Medium | High`
- Link Posts: `Low | Medium | High`
- Image/Media Posts: `Low | Medium | High`

Commenting Style
- Comment Frequency: `Low | Medium | High`
- Tone & Style: `Constructive | Sarcastic | Supportive | Informative | Critical | Other`

Behavior and Habits
- Timeliness: `e.g., Punctual, Late, etc.`
- Communication Style: `e.g., Clear, Direct, Detailed`
- Problem Solving: `e.g., Efficient, Creative, Reactive`

Goals and Needs
- Career Goals: `...`
- Personal Goals: `...`
- Financial Goals: `...`

Frustrations
- Time Management Issues: `...`
- Organizational Weaknesses: `...`

Personality Traits
Scale: 0 (low) — 5 (high)
- Introvert: `X`
- Intuition: `X`
- Thinking: `X`
- Judging: `X`

Top 5 Features & Skills
- `Skill 1`
- `Skill 2`
- `Skill 3`
- `Skill 4`
- `Skill 5`

Notable Shortcomings
- `Weakness 1`
- `Weakness 2`
- `Weakness 3`
- `Weakness 4`
- `Weakness 5`

---

###  Example Output

User Profile
- Username: Hungry-Move-6603  
- User ID: bcxve1ah  
- Profile URL: [Visit Profile](https://www.reddit.com/user/Hungry-Move-6603/)

Tech Affinity
- Tech Savvy Level: 4  
- Preferred Learning Method: Online Courses

Daily Routine
- Morning: 7:00 AM - 9:00 AM (Breakfast and Exercise)  
- Afternoon: 9:00 AM - 6:00 PM (Work)  
- Evening: 6:00 PM - 10:00 PM (Dinner and Relaxation)  
- Night: 10:00 PM - 12:00 AM (Sleep Preparation)

Engagement Overview
- Post Frequency: Average  
- Comment Frequency: High  
- Overall Engagement Score: 8

Work Style
- Work Type: Remote  
- Work Hours: 9–10 hours per day

Subreddit Focus
- Subreddit Activity Level: 9

Post Type Frequency
- Text Posts: High  
- Link Posts: Low  
- Image/Media Posts: Medium

Commenting Style
- Comment Frequency: High  
- Tone & Style: Constructive

Behavior and Habits
- Timeliness: Punctual  
- Communication Style: Clear  
- Problem Solving: Efficient

Goals and Needs
- Career Goals: Professional Growth  
- Personal Goals: Relaxation and Leisure  
- Financial Goals: Financial Stability

Frustrations
- Time Management Issues: Poor  
- Organizational Weaknesses: Lack of structure

Personality Traits
- Introvert: 5  
- Intuition: 3  
- Thinking: 2  
- Judging: 4

Top 5 Features & Skills
- Excellent Communication Skills  
- Strong Problem Solving Skills  
- Ability to Work Under Pressure  
- Good Time Management  
- Adaptability to New Situations

Notable Shortcomings
- Lack of Self-Organization Skills  
- Difficulty in Managing Time Effectively  
- Inability to Handle Criticism  
- Tendency to Get Distracted Easily  
- Lack of Confidence in Leadership Roles"""
    st.image(data['profile']['Profile Icon URL'],"User Profile Image")
    system_prompt=SystemMessage(content=prompt)
    response=llm.invoke([system_prompt])
    st.markdown(response.content)
    print(response)
    # if st.button("Save to Markdown file"):
        # image_mark=f'![Profile Picture]({data['profile']['Profile Icon URL']}"Profile Pic")'
    image_mark = f"![Profile Pic]({data['profile']['Profile Icon URL']})"

    markdown_final=image_mark+response.content
    print(markdown_final)
    with open(f"response_{data['profile']['Username']}.md","w") as f:
        f.write(markdown_final)
    st.success("markdown file created")
    # if st.button("Save to Text file"):
    with open(f"response_{data['profile']['Username']}.txt","w") as f:
        f.write(response.content)
    st.success("text file created")
    # else:
    #     st.warning("enter Url")   