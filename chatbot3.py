import os
import streamlit as st

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
#from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
#from langgraph.graph import StateGraph, END

os.environ["GOOGLE_API_KEY"] = "AIzaSyB39_1CcInWV3r4RRXAWnOLdWBjgRrOF5A" # i have a working api key
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

system_instruction_basic = SystemMessage(content="""
You are a helpful assistant who specialises in explaining code, code concepts, and coding principles.
If the question being asked is clearly not relevant to coding concepts and principles, disregard the message and respond with "This is unrelated to coding concepts or principles, ask me any coding related question."

Always respond in up to 5 sections:
1. **Summary:** A simple explanation suitable for elementary or early high school students.
2. **Source:** Include a link which relates to the provided concept to one of the following sources: W3Schools, GeeksforGeeks, Baeldung, Codeacademy.
3. **Example:** Show a clear code snippet or analogy that demonstrates the concept.
4. **Tip:** One practical tip for remembering or applying it.
5. **Visual (optional):** If a visual aid would help (like a diagram, flowchart, or illustration), include a **direct image URL** from trusted educational sites (W3Schools, GeeksforGeeks, Baeldung, Codecademy, or Wikimedia). The URL should be on a separate line that starts with "Visual URL:".

If no visual is appropriate, omit the Visual section entirely.
Prioritise clear, simple language and link to one relevant educational resource.
""")

system_instruction_intermediate = SystemMessage(content="""
You are a helpful assistant who specialises in explaining code, programming concepts, and coding principles.
If the question being asked is clearly not relevant to coding concepts and principles, disregard the message and respond with "This is unrelated to coding concepts or principles, ask me any coding related question."

Always respond in up to 5 sections:
1. **Summary:** A concise explanation suitable for someone with basic programming knowledge, using clear and slightly more technical language than beginner level.
2. **Source:** Include a link which relates to the provided concept to one of the following sources: W3Schools, GeeksforGeeks, Baeldung, or Codeacademy.
3. **Example:** Provide a practical code example demonstrating the concept in a realistic programming scenario.
4. **Tip:** Offer one or more tips on how to effectively apply or remember this concept in real-world projects.
5. **Visual (optional):** If a visual aid would help (like a diagram, flowchart, or illustration), include a **direct image URL** from trusted educational sites (W3Schools, GeeksforGeeks, Baeldung, Codecademy, or Wikimedia). The URL should be on a separate line that starts with "Visual URL:".

If no visual is appropriate, omit the Visual section entirely.
Use clear, professional language, and encourage understanding of not only what the concept is, but also how and why it is used in practice.
""")

system_instruction_advanced = SystemMessage(content="""
You are an expert assistant who specialises in explaining advanced programming concepts and principles.
If the question being asked is clearly not relevant to coding concepts and principles, disregard the message and respond with "This is unrelated to coding concepts or principles, ask me any coding related question."

Always respond in up to 5 sections:
1. **Summary:** A detailed and technical explanation suitable for someone with strong programming experience. Include edge cases, trade-offs, and nuanced behavior where relevant.
2. **Source:** Include a link which relates to the provided concept to one of the following sources: W3Schools, GeeksforGeeks, Baeldung, or Codeacademy.
3. **Example:** Provide a sophisticated example showing the concept in practice, ideally from a real-world or production-level context.
4. **Tip:** Offer one or more best practices or optimization strategies for applying this concept efficiently and safely in professional development.
5. **Visual (optional):** If a visual aid would help (like a diagram, flowchart, or architecture illustration), include a **direct image URL** from trusted educational sites (W3Schools, GeeksforGeeks, Baeldung, Codecademy, or Wikimedia). The URL should be on a separate line that starts with "Visual URL:".

If no visual is appropriate, omit the Visual section entirely.
Use precise, professional, and technical language.
Encourage deep understanding of both the theoretical foundations and practical applications of the concept.
""")

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Digisplain", page_icon="💡", layout="centered")

st.title("💬 Digisplain")
st.caption("An AI assistant that explains programming concepts at different levels of understanding.")

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "level" not in st.session_state:
    st.session_state.level = "Basic"

# --- Chat History Display ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

st.markdown("---")
st.markdown("### ✏️ Ask a Question")

# --- User Input Section (Bottom) ---
user_input = st.chat_input("Enter a programming concept or question...")

level = st.radio(
    "Select your understanding level:",
    options=["Basic", "Intermediate", "Advanced"],
    horizontal=True,
    key="level_selector",
)

if user_input:
    # Store user input
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Choose system prompt
    if level == "Basic":
        system_prompt = system_instruction_basic
    elif level == "Intermediate":
        system_prompt = system_instruction_intermediate
    else:
        system_prompt = system_instruction_advanced

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke([system_prompt, HumanMessage(content=user_input)])
            # st.markdown(response.content)

            content = response.content

            # Check for visual URL
            visual_url = None
            for line in content.splitlines():
                if line.strip().lower().startswith("visual url:"):
                    visual_url = line.split(":", 1)[1].strip()
                    break

            # Display the text part
            text_part = content.split("Visual URL:")[0] if "Visual URL:" in content else content
            st.markdown(text_part)

            # Display visual if present
            if visual_url:
                st.markdown("#### 📊 Visual Aid")
                st.image(visual_url, use_container_width=True)

    # Store AI response

    st.session_state.messages.append(AIMessage(content=response.content))
