from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

#Defining State
class BlogState(TypedDict):
    title:str
    outline:str
    content:str

#Defining Node
def create_outline(state:BlogState)->BlogState:
    # Fetch title
    title=state["title"]

    #Call the llm and get outline
    prompt=f"Generate a detailed outline ,for a blog on the topic,{title}"
    outline=llm.invoke(prompt).content

    #update state
    state["outline"]=outline

    return state

def create_blog(state:BlogState)->BlogState:
    #Fetching title and outline
    title=state["title"]
    outline=state["outline"]

    #writing content form llm
    prompt=f"Write a detailed blog on the {title} using the folloing outline \n{outline}"
    content=llm.invoke(prompt).content

    #updating content
    state["content"]=content

    return state




#Adding Node and Edges
graph=StateGraph(BlogState)

graph.add_node("create_outline",create_outline)
graph.add_node("create_blog",create_blog)


graph.add_edge(START,"create_outline")
graph.add_edge("create_outline","create_blog")
graph.add_edge("create_blog",END)

#Compilation
workflow=graph.compile()

#Initial State
initial_state={
    "title":"Rise of AI int the world"
}

#Execution
result=workflow.invoke(initial_state)
print(result)
print("====="*10)

print(result["content"])



"""
## The AI Revolution: Understanding Its Unstoppable Rise

From predicting your next purchase to powering self-driving cars, Artificial Intelligence is no longer a futuristic fantasy – it's here, now, deeply woven into the fabric of our daily lives. But what exactly is AI? At its core, Artificial Intelligence refers to the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, problem-solving, perception, and even decision-making. While the ultimate goal of Artificial General Intelligence (AGI) – AI that can understand, learn, and apply intelligence to any intellectual task a human can – remains a distant aspiration, and Super AI (AI surpassing human intelligence) is purely theoretical, the narrow AI we interact with today is already profoundly impactful.

This blog post aims to explore the fascinating journey of AI, tracing its path from a conceptual idea to the transformative global force it is today. We'll delve into its intriguing history, the technological breakthroughs fueling its current surge, its widespread applications across virtually every sector, and the critical opportunities and challenges it presents for humanity.

---

### Section 1: A Glimpse into AI's Past – The Genesis

The idea of intelligent machines isn't new; it echoes in ancient myths of automatons and philosophical discussions about the nature of thought. However, the true dawn of AI theory began in the mid-20th century. Visionaries like Alan Turing, with his seminal 1950 paper "Computing Machinery and Intelligence," proposed the "Turing Test" as a benchmark for machine intelligence, laying crucial theoretical groundwork. The term "Artificial Intelligence" itself was coined at the Dartmouth Conference in 1956, marking a pivotal moment where researchers formally gathered to explore the possibility of creating thinking machines.

Initial enthusiasm for AI was immense, fueled by ambitious promises. Early expert systems, designed to mimic human decision-making in specific domains, showed glimpses of potential. However, these early waves soon encountered significant limitations. Computational power was scarce and expensive, and the sheer volume of data needed to train complex systems was simply unavailable. This led to periods of disillusionment, known as "AI Winters," where funding dried up, and public interest waned.

Despite these setbacks, dedicated researchers quietly persisted. They continued to lay the groundwork in areas like machine learning, neural networks, and advanced algorithms, refining theories and developing foundational techniques. This quiet persistence, often out of the spotlight, was crucial, paving the way for the explosive breakthroughs we witness today. The key takeaway here is clear: AI isn't a sudden phenomenon; its current rise is built on decades of foundational work and resilience.

---

### Section 2: The Driving Forces Behind the Surge – Why Now?

If AI has been around for decades, what explains its unprecedented acceleration in recent years? The answer lies in a "perfect storm" of converging technological advancements.

Firstly, we are living in the era of **Big Data**. The explosion of digital information from the internet, social media, e-commerce, IoT devices, and countless sensors provides AI models with the fuel they desperately need. Unlike earlier systems that struggled with limited datasets, today's AI thrives on vast amounts of data for training, enabling it to learn complex patterns and make highly accurate predictions.

Secondly, **unprecedented computational power** has become widely accessible. Moore's Law, which predicted the doubling of transistors on a microchip every two years, has continued to deliver, making processors faster and more affordable. Crucially, the rise of powerful GPUs (Graphics Processing Units), initially designed for gaming, proved perfectly suited for the parallel processing demands of AI, especially deep learning. Coupled with the scalability and accessibility of cloud computing platforms like AWS, Azure, and Google Cloud Platform, high-performance computing is no longer an exclusive domain but a readily available resource.

Thirdly, **algorithmic breakthroughs and the evolution of machine learning** have been transformative. While machine learning techniques (supervised, unsupervised, reinforcement learning) have existed for some time, the "Deep Learning" revolution truly changed the game. Deep learning utilizes multi-layered neural networks (e.g., Convolutional Neural Networks for image recognition, Recurrent Neural Networks for sequence data like text) to process vast amounts of data and learn features automatically. Pioneering work by figures like Geoffrey Hinton, Yann LeCun, and Yoshua Bengio has been instrumental in this advancement.

Finally, the **accessibility and open-source movement** have democratized AI development. The availability of robust open-source frameworks like TensorFlow, PyTorch, and Keras has lowered the barrier to entry, allowing researchers, developers, and even hobbyists worldwide to experiment, innovate, and contribute to AI's rapid progress. This convergence of data, power, sophisticated algorithms, and widespread accessibility has created the ideal environment for AI's current explosion.

---

### Section 3: AI in Action – Transforming Every Sector

AI is no longer confined to research labs; it's a fundamental shift impacting virtually every aspect of human endeavor. Its applications are diverse and pervasive:

**A. Everyday Life & Consumer Tech:** You interact with AI constantly. **Voice assistants** like Siri, Alexa, and Google Assistant leverage natural language processing to understand and respond to your commands. **Recommendation engines** on Netflix, Amazon, and Spotify use predictive analytics to suggest movies, products, or music tailored to your tastes. **Facial recognition** unlocks your smartphone and enhances security, while AI-powered **navigation apps** like Google Maps optimize routes and estimate arrival times, often integrating with **ride-sharing** services like Uber.

**B. Business & Finance:** AI is streamlining operations and enhancing decision-making. **Robotic Process Automation (RPA)** automates mundane, repetitive back-office tasks. In finance, AI excels at **fraud detection**, identifying unusual patterns in transactions far faster than humans. **Algorithmic trading** uses AI to execute high-frequency trades based on real-time market analysis. **Customer service** has been revolutionized by chatbots and virtual agents, providing instant support and freeing up human agents for more complex issues.

**C. Healthcare & Medicine:** The potential for AI in healthcare is immense. It assists in **diagnostics** by analyzing medical images (X-rays, MRIs, CT scans) with remarkable accuracy, often spotting anomalies missed by the human eye. **Drug discovery** is being accelerated, with AI sifting through vast chemical libraries to identify potential compounds and predict their efficacy. **Personalized medicine** is becoming a reality, as AI analyzes individual genetic data and patient histories to tailor treatments for optimal outcomes.

**D. Transportation & Logistics:** The dream of **self-driving cars** is moving closer to reality, with AI handling perception, decision-making, and control. In logistics, AI optimizes **supply chains**, improving route planning, inventory management, and warehouse operations. **Drone delivery** systems are also leveraging AI for autonomous navigation and package handling.

**E. Creative & Content Generation:** Perhaps one of the most surprising areas, AI is now generating original works. **AI art and music** tools (like Midjourney, DALL-E, and various music composition AI) can create unique visual and auditory pieces. **Content creation** tools, such as AI-powered writing assistants and summarizers (like ChatGPT), are assisting writers, marketers, and researchers in generating text, drafting emails, and summarizing complex documents.

**F. Manufacturing & Industry:** AI is enhancing efficiency and safety on factory floors. **Predictive maintenance** systems use AI to analyze sensor data from machinery, anticipating equipment failures before they occur, reducing downtime and costs. Advanced **robotics** perform precision tasks and work in dangerous environments, while **quality control** is improved through automated inspection systems that identify defects with high accuracy.

From the mundane to the miraculous, AI is not a niche technology; it's a fundamental shift impacting virtually every facet of human endeavor, ushering in an era of unprecedented automation, intelligence, and innovation.

---

### Section 4: Navigating the AI Landscape – Opportunities & Challenges

The rise of AI presents humanity with a double-edged sword: immense opportunities for progress alongside significant challenges that demand careful consideration.

**A. Tremendous Opportunities:**
AI offers the potential for **increased efficiency and productivity** across all sectors by automating mundane tasks, optimizing complex processes, and freeing up human workers for more creative and strategic roles. It is a powerful engine for **innovation and the creation of new industries**, leading to entirely new products, services, and job roles that we can barely imagine today. Critically, AI holds the key to **solving complex global problems**, from accelerating scientific discovery in fields like climate change and disease research to addressing poverty and resource management. Furthermore, AI enhances **decision-making** by providing data-driven insights, allowing individuals and organizations to make more informed and effective choices.

**B. Significant Challenges & Concerns:**
However, the path forward is fraught with challenges. One of the most pressing concerns is **job displacement and the need for reskilling**. As AI automates various tasks, many existing job roles will change or disappear, necessitating a massive workforce adaptation and investment in education and training.

**Ethical dilemmas** are at the forefront of the AI discussion:
*   **Bias:** AI systems learn from data, and if that data reflects societal biases (e.g., racial, gender), the AI will inherit and even amplify those biases, leading to unfair or discriminatory outcomes.
*   **Accountability:** When an AI system makes a mistake, especially in critical applications like autonomous vehicles or medical diagnostics, determining who is responsible (the developer, the deployer, the AI itself?) becomes a complex legal and ethical question.
*   **Privacy:** AI thrives on data, leading to extensive data collection that raises significant concerns about individual privacy and how personal information is used and protected.
*   **Transparency/Explainability (The "Black Box Problem"):** Many advanced AI models, particularly deep learning networks, operate as "black boxes," making decisions in ways that are difficult for humans to understand or explain. This lack of transparency can hinder trust and make auditing difficult.

Beyond ethics, **security risks** are escalating. AI can be misused for sophisticated cyberattacks, generating convincing deepfakes, or developing autonomous weapons systems. This necessitates robust cybersecurity measures and international cooperation. Finally, the rapid pace of AI development outstrips existing frameworks, highlighting the urgent need for comprehensive **regulation and governance** to guide its ethical and safe deployment. Brief mention is also given to **existential risks**, the long-term concerns about the potential for highly advanced Artificial General Intelligence (AGI) or Super AI to pose unforeseen threats to humanity.

The key takeaway here is that AI is a powerful tool with immense potential for good, but its responsible development and deployment, guided by strong ethical principles and thoughtful regulation, are paramount to harnessing its benefits while mitigating its risks.

---

### Conclusion

The journey of Artificial Intelligence, from its theoretical beginnings and early "winters" to its current omnipresence, is a testament to human ingenuity and persistent scientific endeavor. Driven by a confluence of readily available Big Data, unprecedented computational power, revolutionary algorithmic breakthroughs like Deep Learning, and the democratization of open-source tools, AI has transcended its niche origins to become a transformative global force.

The rise of AI is far from over; it's an ongoing process. We are on a clear trajectory towards more sophisticated AI, with increasing integration into even more facets of life and a growing emphasis on human-AI collaboration. The discussions around Artificial General Intelligence (AGI) and the future of human-machine interaction will only intensify.

As we stand at this pivotal moment, it's crucial for all of us to engage with AI responsibly. This isn't just a technological story; it's a human one, demanding our collective wisdom, foresight, and ethical commitment. We must prioritize continuous learning, adaptation, and critical thinking to navigate this evolving landscape. By doing so, we can ensure that the rise of AI truly serves humanity's best interests, shaping a future that is not only intelligent but also equitable, prosperous, and secure for all.

---

**Additional Considerations:**
*   **Tone:** The blog post maintains an informative, engaging, and balanced tone, acknowledging both the immense potential and the significant challenges.
*   **Target Audience:** It's written to be accessible to a general public, tech enthusiasts, and professionals without being overly technical.
*   **Visuals:** For a live blog, incorporating visuals would be highly beneficial:
    *   A timeline infographic of AI milestones (Turing Test, Dartmouth, Deep Learning breakthroughs).
    *   Graphics illustrating Big Data growth or computational power increases.
    *   Images showcasing AI applications (self-driving car, medical imaging, AI-generated art).
    *   An infographic on AI opportunities vs. challenges.
*   **Keywords:** The blog naturally incorporates keywords like AI, Artificial Intelligence, Machine Learning, Deep Learning, AI revolution, future of AI, AI impact, AI ethics, Big Data, autonomous systems.
*   **Internal/External Links:** In a live blog, specific phrases could be linked to reputable sources for definitions, statistics, or further reading on specific topics (e.g., "Turing Test," "Deep Learning," "TensorFlow," "AI bias studies").
"""
