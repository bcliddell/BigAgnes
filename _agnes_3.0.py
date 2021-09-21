"""
Agnes v3.0 This is a rewrite with nextcord, a discord.py fork.
discord.py was discontinued on 29 Aug 2021.

Private tokens and keys are contained in config.py.

Requires Python 3.8 or higher.

py -3.x -m pip install -U nextcord

TODO:
"""

# Agnes modules
from Agnes import Agnes
from AgnesCommands import AgnesCommands
from VoiceCommands import VoiceCommands
import config    # pylint: disable=unused-variable


def main():
    agnes = Agnes()
    agnes.add_cog(AgnesCommands(agnes))
    agnes.add_cog(VoiceCommands(agnes))
    agnes.run(config.DISCORD_TOKEN)

if __name__ == '__main__':
    main()
