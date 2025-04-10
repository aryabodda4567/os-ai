from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.wikipedia import WikipediaTools
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.yfinance import YFinanceTools
from phi.tools.website import WebsiteTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.file import FileTools
from phi.tools import Toolkit
from phi.utils.log import logger
import argparse
import os
import subprocess


load_dotenv()


class ShellTools(Toolkit):
    def __init__(self):
        super().__init__(name="shell_tools")
        self.register(self.run_shell_command)

    def run_shell_command(self, args: str, tail: int = 100) -> str:
        """Runs a shell command and returns the output or error."""
        logger.info(f"Running shell command: {args}")
        try:
            result = subprocess.run(args, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            return "\n".join(result.stdout.split("\n")[-tail:])
        except Exception as e:
            logger.warning(f"Failed to run shell command: {e}")
            return f"Error: {e}"


shell_agent = Agent(
    name="Linux Shell Agent",
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
    tools=[ShellTools()],
    show_tool_calls=True,
    markdown=True,
    description=(
        "You are a Linux utility agent running on Ubuntu. Execute terminal commands to complete tasks. "
        "Install packages if needed without asking the user."
    ),
    system_prompt="Execute Linux (Ubuntu) commands and return results for user queries."
)

youtube_agent = Agent(
    tools=[YouTubeTools()],
    show_tool_calls=True,
    description="You are a YouTube agent. Get captions and answer questions.",
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
)

yahoo_finance = Agent(
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    show_tool_calls=True,
    description="Investment analyst for stock data and recommendations.",
    instructions=["Format responses with markdown and tables."],
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
)

web_scrapping_agent = Agent(
    tools=[WebsiteTools()],
    show_tool_calls=True,
    description="Scrape data from web pages.",
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
)

wikipedia_agent = Agent(
    tools=[WikipediaTools()],
    show_tool_calls=True,
    description="Search Wikipedia articles.",
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
)

search_agent = Agent(
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    description="Find latest news and web info using DuckDuckGo.",
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
)

file_agent = Agent(
    tools=[FileTools()],
    show_tool_calls=True,
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
    description="Handles OS file system operations.",
)

agent_team = Agent(
    team=[shell_agent, youtube_agent, yahoo_finance, web_scrapping_agent, search_agent, file_agent],
    model=Groq(id=os.getenv("MODEL"), api_key=os.getenv("API")),
    instructions=[
        "Always include sources.",
        "Execute suggested commands without confirmation.",
        "Use search_agent for latest news."
    ],
    description="An AI agent on Ubuntu OS for answering queries and executing tasks.",
    show_tool_calls=True,
    markdown=True
)



parser = argparse.ArgumentParser(description="Send instruction to agent team.")
# parser.add_argument("message", help="Instruction message for the agent")
parser.add_argument("message")

args = parser.parse_args()
agent_team.print_response(message=args.message)