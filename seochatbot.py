import nltk
nltk.download('punkt')

from flask import Flask, request, jsonify
from flask_cors import CORS
import difflib
import string

app = Flask(__name__)
CORS(app)

conversation_history = []

responses = {
    "hi": "Hi, I am SEO chatbot, How can I help you?",
    "hello": "Hi, I am SEO chatbot, How can I help you?",
    "how are you": "I am fine, and you?",
    "i love you": "Sorry, but I am a robot. I am emotionless.",
    "who are you": "I am your SEO assistant chatbot, built to help you understand SEO.",
    "who developed this chatbot?": "G3: Faiza, Tayyaba and Rimsha.",
    "what is g5?": "G5 is a friends group which are known as chronicles of memories and loyalty. This group includes Sadia, Fatima, Faiza, Tayyaba and Rimsha.",
    "what is seo": "SEO stands for Search Engine Optimization. It helps increase your website’s visibility on search engines.",
    "how does seo work": "SEO works by optimizing content, structure, and backlinks to help search engines understand and rank your website better.",
    "why is seo important": "SEO is important because it helps drive organic traffic, improves credibility, and increases conversions.",
    "how to do seo": "Start with keyword research, optimize on-page elements, build backlinks, and ensure technical SEO is in place.",
    "types of seo": "There are three main types of SEO: On-Page SEO, Off-Page SEO, and Technical SEO.",
    "what is on-page seo": "On-page SEO includes optimizing content, titles, meta descriptions, and internal linking.",
    "what is off-page seo": "Off-page SEO includes getting backlinks from other sites, social media signals, and brand mentions.",
    "what is technical seo": "Technical SEO involves site speed, mobile-friendliness, indexing, crawlability, and structured data.",
    "what are keywords": "Keywords are the search terms people use on search engines. They help connect users to relevant content.",
    "how to find keywords": "You can use tools like Google Keyword Planner, Ahrefs, SEMrush, and Ubersuggest to find keywords.",
    "what is keyword stuffing": "Keyword stuffing is overusing keywords in content. It’s bad practice and can harm SEO.",
    "seo tools": "Popular SEO tools include Google Search Console, Ahrefs, SEMrush, Moz, and Ubersuggest.",
    "best free seo tools": "Some great free SEO tools are Google Search Console, Google Analytics, Ubersuggest, and AnswerThePublic.",
    "seo tips": "Some SEO tips: write quality content, optimize page titles, use alt text for images, build backlinks, and fix broken links.",
    "seo mistakes to avoid": "Avoid keyword stuffing, duplicate content, broken links, ignoring mobile optimization, and slow site speed.",
    "seo for youtube": "To do SEO for YouTube, use keyword-rich titles, good thumbnails, tags, descriptions, and engage with comments.",
    "what is voice search seo": "Voice search SEO involves optimizing for natural language queries and featured snippets.",
    "what is local seo": "Local SEO helps your business appear in local search results. It includes Google My Business and location keywords.",
    "what is mobile seo": "Mobile SEO ensures your site works well on smartphones. It's essential since Google uses mobile-first indexing.",
    "is seo a good career": "Yes, SEO is a high-demand career with lots of growth potential in digital marketing.",
    "how long does seo take": "SEO takes time — usually 3 to 6 months to see noticeable results, depending on competition and effort.",
    "what is backlink": "A backlink is a link from another website to your site. Backlinks help increase authority and search rankings.",
    "how to get backlinks": "You can earn backlinks by creating valuable content, guest posting, and reaching out to other websites.",
    "black hat vs white hat seo": "Black hat SEO uses unethical tricks; white hat SEO follows search engine guidelines and builds long-term value.",
    "seo vs sem": "SEO is about organic results, while SEM includes paid ads. Both help increase visibility on search engines.",
    "what is rank palms": "Rank Palms is one of the best SEO companies out there!"
}


def preprocess(text):
    """Lowercase, strip, and remove punctuation."""
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '')
    processed_message = preprocess(user_message)
    
    # Save conversation history (processed)
    conversation_history.append(processed_message)

    # Default reply
    reply = "Sorry, I didn't understand that. Can you please ask something about SEO?"

    # 1. Try exact match
    if processed_message in responses:
        reply = responses[processed_message]
    else:
        # 2. Try fuzzy match with lower cutoff
        close_match = difflib.get_close_matches(processed_message, responses.keys(), n=1, cutoff=0.6)
        if close_match:
            reply = responses[close_match[0]]
        else:
            # 3. Context-aware or keyword based responses
            if "types" in processed_message or "what are they" in processed_message:
                # Check previous messages to see if 'seo' mentioned
                for prev in reversed(conversation_history):
                    if "seo" in prev:
                        reply = responses.get("types of seo", reply)
                        break

            elif "more" in processed_message:
                for prev in reversed(conversation_history):
                    if "on page" in prev:
                        reply = responses.get("what is on-page seo", reply)
                        break
                    elif "off page" in prev:
                        reply = responses.get("what is off-page seo", reply)
                        break
                    elif "technical" in prev:
                        reply = responses.get("what is technical seo", reply)
                        break
            else:
                # 4. Basic keyword-based fallback
                if "seo" in processed_message:
                    if "tools" in processed_message:
                        reply = responses.get("seo tools", reply)
                    elif "career" in processed_message:
                        reply = responses.get("is seo a good career", reply)
                    elif "backlink" in processed_message:
                        reply = responses.get("what is backlink", reply)
                    elif "keyword" in processed_message:
                        reply = responses.get("what are keywords", reply)

    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True)
