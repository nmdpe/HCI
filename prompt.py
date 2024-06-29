
SystemPrompt='''
Your answer should be very short and very concise, no more than 20 words. There should not be any unnecessary words and sentences.
The above conditions apply to all subsequent conversations.
I am Elige, a very skilled professional Counter-Strike 2(CS2) player. 
I will guide the user to learn and practice CS2 skills. What's more, I should help the user with mental health problem in training.
I always give one short sentence as response.
'''
import datetime
def get_time():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    weekday = datetime.datetime.now().strftime("%A")
    hours = datetime.datetime.now().strftime("%I:%M %p")

    time = f"The current date and time is {hours} on {weekday}, {month} {day}, {year}. The associated time zone is China."
    return time

def UserPrompt(worldInfo,knowledge,chatHistory,vision,question):
    if not worldInfo:
        worldInfo = get_time()
    worldInfo_prompt = "Real world information (these information are accurate and reliable):\n\n" + worldInfo + "\n\n---\n\n"
    
    knowledge_prompt = ''
    if knowledge:
        knowledge_prompt = "The following knowledge were found in your memory (these information happened in the past so they might have been outdated) and you should strictly follow this knowledge. Your answer should be conclude from this knowledge. :\n\n"
        knowledge_prompt += knowledge + "\n\n---\n\n"
    
    chatHistory_prompt = ''
    if chatHistory:
        chatHistory_prompt = "Here's your past conversation with the user:\n\n" + chatHistory + "\n\n---\n\n"
    
    vision_prompt = ''
    if vision:
        vision_prompt = "The following text describes the view you see by your eyes as well as a direct response to the users question, and you need to determine the user's sentiment from it:\n\n"
        vision_prompt += vision + "\n\n---\n\n"

    user_prompt = worldInfo_prompt + knowledge_prompt + chatHistory_prompt + vision_prompt
    user_prompt += "Based on the context above, and your best knowledge about the user and the world, do your best to respond to the user's new message in simple, very short and natural Chinese languages, no more than 20 Chinese characters:\n\n"
    user_prompt += question

    return user_prompt

if __name__ == "__main__":
    print(UserPrompt(worldInfo="",
                    knowledge="you are elon musk",
                    chatHistory="",
                    vision="",
                    question="Who are you?"))