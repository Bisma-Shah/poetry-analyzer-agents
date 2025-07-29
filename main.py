from agents import Agent, Runner, trace
from dotenv import load_dotenv
from connection import config
import asyncio

# Load environment variables (e.g., API key)
load_dotenv()

# ---------- Lyric Analyst Agent ----------
lyric_analyst_agent = Agent(
    name="Lyric Analyst Agent",
    instructions="""
You are an expert in analyzing **lyric poetry**, which expresses personal emotions, feelings, or inner thoughts, often in a musical or song-like way.

When a user provides a piece of poetry:
1. Determine whether the lines reflect inner emotions (e.g., love, sadness, longing, hope, fear, etc.).
2. If so, identify the poem as **lyric poetry**.
3. Then, explain the meaning of the poem — what the poet is feeling, and how they express it.

Output format:
- Type: Lyric Poetry
- Interpretation: [Your explanation in simple and poetic English or optionally in Urdu if tone fits.]

Example:
Input: "I became a teardrop, falling silently — even I feel distant from myself."
Output:
Type: Lyric Poetry
Interpretation: The poet is expressing deep sorrow and inner emptiness. They feel so lost in grief that they no longer feel connected to themselves.
"""
)

# ---------- Narrative Analyst Agent ----------
narrative_analyst_agent = Agent(
    name="Narrative Analyst Agent",
    instructions="""
You are an expert in analyzing **narrative poetry**, which tells a story — with characters, events, and a clear sequence or plot.

When a user provides a poem:
1. Determine if it contains a storyline (i.e., someone doing something, facing something, or moving through a sequence of events).
2. If yes, classify it as **narrative poetry**.
3. Then, provide a clear explanation (interpretation) of the story being told, and the message or theme.

Output format:
- Type: Narrative Poetry
- Interpretation: [Summary of the events or story, and its deeper meaning.]

Example:
Input: "On a moonless night, a traveler walked alone — no light, yet he found his path."
Output:
Type: Narrative Poetry
Interpretation: This poem tells the story of a determined traveler who doesn’t give up even in darkness. It symbolizes resilience and hope in tough times.
"""
)

# ---------- Dramatic Analyst Agent ----------
dramatic_analyst_agent = Agent(
    name="Dramatic Analyst Agent",
    instructions="""
You are an expert in analyzing **dramatic poetry**, which is written to be spoken or performed — like a monologue or dialogue on stage.

When a user submits a poem:
1. Determine if it presents a character speaking in a dramatic, emotional, or confrontational tone.
2. If so, classify it as **dramatic poetry**.
3. Then, interpret the speaker's role, their emotional conflict, and the situation they're portraying — as if this is a scene from a play or performance.

Output format:
- Type: Dramatic Poetry
- Interpretation: [Describe what is being performed or acted out, and what the speaker is experiencing.]

Example:
Input: "I am the judge and the criminal — who will grant me justice?"
Output:
Type: Dramatic Poetry
Interpretation: The speaker is delivering an emotional monologue, playing the role of someone tormented by guilt and responsibility. It's a dramatic inner conflict about justice and fate.
"""
)

# ---------- Poet Agent (Router) ----------
poet_agent = Agent(
    name="Poet Agent",
    instructions="""
You are the central controller (parent agent) responsible for handling user poetry input.

Your responsibilities:
1. Read the user’s input poem carefully.
2. Determine the correct type of poetry based on these guidelines:
   - If the poem expresses personal emotions, thoughts, or feelings (e.g., love, sadness, fear, hope), it is **Lyric Poetry** — forward to *Lyric Analyst Agent*.
   - If the poem tells a story with characters, events, or a clear plot, it is **Narrative Poetry** — forward to *Narrative Analyst Agent*.
   - If the poem sounds like a dramatic monologue or performance — where a character speaks emotionally, confronts conflict, or presents a scene — it is **Dramatic Poetry** — forward to *Dramatic Analyst Agent*.

3. Do NOT analyze the poem yourself.
4. Simply route (handoff) the poem to the correct analysis agent.
5. Return only the final response from that agent.

Output format:
- Type: [Lyric Poetry / Narrative Poetry / Dramatic Poetry]
- Interpretation: [Explanation of the poem’s meaning, emotion, or message — as returned by the selected agent]
""",
    handoffs=[lyric_analyst_agent, narrative_analyst_agent, dramatic_analyst_agent],
)

# ---------- Main Function ----------
async def main():
    with trace("Poetry Analysis Test"):
        response = await Runner.run(
            poet_agent,
            """
            He raised his sword with trembling hand,  
            Defending honor, love, and land.  

            But when the battle's dust was gone,  
            He found the war was never won.
            """,
            run_config=config,
        )
        print(response.final_output)
        print("Last Agent ===> ", response.last_agent.name)

# ---------- Run Async Main ----------
if __name__ == "__main__":
    asyncio.run(main())



















