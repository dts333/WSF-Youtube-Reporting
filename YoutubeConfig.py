#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:10:01 2019

@author: DannySwift
"""

API = "AIzaSyD7fMTx7o4NMY5skRRiYylhpPL4xEyJouA"
API2 = "AIzaSyAyyLBdAoBXH0LcEZyEn9HhdMR3mA8YX9s"
VIDSTATS = ["views", "average_percentage_viewed"]
VIDSTATSTITLES = [
    "views",
    "averageViewPercentage",
]
YT_ROWS = [
    "Views",
    "Views from Home",
    "Views from Subscriptions",
    "Suggested Videos",
    "Channel Pages",
    "Notifications",
]
# relativeRetentionPerformance is throwing a 400
CHANNELSTATS = ["traffic_source_type"]
DATA_DIRECTORY = "YoutubeData"
WSFID = "UCShHFwKyhcDo3g7hr4f1R8A"
YDEID = "PLKy-B3Qf_RDVL6Z_CmgKf0tAbpXTua9mV"
CJID = "PLKy-B3Qf_RDVqSnLTf4b0cXeeZaiibRII"

COOL_JOBS = {
    "W8E9_R0EWDs": "The Bird Whisperer",
    "Gib7IFdUnQs": "The Leech Guy",
    "cp7C2AZhceE": "Robot Runner",
    "JurS57yz2Ng": "Exercise Brain Changer",
    "mbvq6-bqgXs": "Hubble Doctor",
    "ryj5d2DjMlI": "Galaxy Explorer",
    "Ldww6EIMAbM": "Cave Explorer",
    "XLF-4c1XTJ4": "Doctor Bugs",
    "YpbLa8BGv6E": "Alien Hunter",
    "lQenUMoIufo": "Fossil Hunters",
    "zZSmo2T_otg": "Da Vinci Detective",
    "CyG3QZlgAgs": "Daredevil",
    "Y1biZo9q4ck": "Human-Robot Investigator",
    "_ePLqrHUhaw": "Nano Examiner",
    "BCH6Iei-xcw": "Robot Senser",
}

BIG_IDEAS_URL = "https://www.worldsciencefestival.com/video/playlists/big-ideas/"


KAVLI_URL = "https://www.worldsciencefestival.com/video/video-library/?topic=&playlist=34438&meta="

BI21 = {
    "xlyYipjw560" : "Until the End of Time",
    "OcWEYDddJ7Q" : "Revealing the Cosmos",
    "cm8OHGvl4Oc" : "The Golden Age of Space Exploration",
    "VzxI8Xjx1iw" : "Memory",
    "1f7jm3T_hao" : "Rewriting the Story of Humankind",
    "5Iy5mt7F_N4" : "Brave New Prehistoric World",
    "RDVgfFzZVsA" : "Rewiring the Brain",
    "MD-O4Gpx74s" : "Visual Illusions",
    "FiyyndtlHdQ" : "The Deep",
    "W8W3w3udEXI" : "Artemis",
    "wvvovktKKa4" : "Dreaming",
    "kxFTWk9lLDU" : "Psychedelics",
    "5sMZw_DM5eA" : "Stunning First Images",
    "UtcBFlWSqGM" : "Black Holes",
    "2HU6Hv3fM0I" : "Riddles of Reality",
    "t9jvIyc4Hfg" : "Lifespan Expanded",
    "K7QBnuF6dHg" : "Decoding the Brain",
    "ntxC5KMC4y0" : "Einstein and the Quantum",
    "WtjkNsnC--A" : "Things We've Never Seen",
    "6LXHtDUXkS0" : "Mind Your Language",
    "VN19VOMHxkk" : "Does Math Reveal Reality?",
    "zyaveVWKniw" : "Steven Weinberg and the Quest to Explain the World"
}

LIVE = {
    "9EBJNvrx60I" : "Ardem Patapoutian and David Julius",
    "zokNLqGd9TQ" : "Saul Perlmutter",
    "aYYhg3yts0c" : "Francis Collins",
    "bHKbIhSWpl4" : "School's Out"
}

BI19 = {
    "no3qLqUYBLo" : "Beyond Higgs",
    "ps0NSRFEAE4" : "Making Room for Machines",
    "oCrnA4bYCag" : "We Will Be Martians",
    "qLMLV_7hMOQ" : "Outsourcing Humanity",
    "tdsVRh9oKiE" : "Rethinking Thinking",
    "1FJWvEbeBps" : "The Richness of Time",
    "w18y4iQtca0" : "Eyes in the Skies",
    "EEhI-n_MgbY" : "The Technology That Transforms Us",
    "RpwW9Lw2Ku4" : "Intelligence Without Brains",
    "1VajnuxMJmU" : "Physics in the Dark",
    "S1jn86eUX0E" : "The Reality of Reality",
    "KHa0X4y3ulw" : "On the Shoulders of Giants: Shep Doeleman",
    "pHCfooCqTrw" : "On the Shoulders of Giants: Andrew Strominger",
    "HPEi_CZIhuA" : "The Science of Extreme Behavior",
    "iI9C0R3_bq0" : "Can We Cure Deafness and Blindness? Should We?",
    "Fi66wFfOC-4" : "Revealing the Mind",
    "YSWd21z2qqE" : "Loose Ends",
    "Hzy7ukTQQ_Y" : "What it Takes to Boldly Go"
}

PHYSICS = {
    "no3qLqUYBLo" : "Beyond Higgs",
    "1FJWvEbeBps" : "The Richness of Time",
    "1VajnuxMJmU" : "Physics in the Dark",
    "S1jn86eUX0E" : "The Reality of Reality",
    "YSWd21z2qqE" : "Loose Ends",
    "ntxC5KMC4y0" : "Einstein and the Quantum"
}

LIVE_WITH_BRIAN = {
    "zokNLqGd9TQ" : "Saul Perlmutter",
    "9EBJNvrx60I" : "Ardem Patapoutian and David Julius",
    "Gu28y7vZmrI" : "Max Tegmark",
    "feds3yY3YrQ" : "Live Q+A",
    "nO1eWxjQqaA" : "Brian Schmidt",
    "4eVzJbxMZao" : "Paul Nurse",
    "v6YEKYIkrzI" : "Frank Wilczek",
    "ZXuelZVLdzM" : "Live Q+A",
    "xk48z8N-sl0" : "Leonard Susskind",
    "7oCQuvhQY6o" : "Roger Penrose",
    "GmXB7IqbM1o" : "Andrea Ghez",
    "pMXSKt9g1TE" : "Barry Barish",
    "lcsLMvNTGeY" : "Harold Varmus",
    "7obuj1OHt2c" : "Priyamvada Natarajan",
    "fnk4dMW7AzY" : "Gabriela Gonzalez",
    "GfRJZbsywPQ" : "Cumrun Vafa",
    "HZhHovgJ680" : "Adam Riess",
    "ntZO0lZiV-4" : "Live Q+A"
}

BI22 = {
   "zokNLqGd9TQ": "Saul Perlmutter",
   "aYYhg3yts0c": "Francis Collins",
   "bHKbIhSWpl4": "School's Out",
   "W8W3w3udEXI": "Artemis",
   "UtcBFlWSqGM": "Black Holes"
}

LIVE22 = {
    "zokNLqGd9TQ": "Saul Perlmutter",
    "aYYhg3yts0c": "Francis Collins",
    "bHKbIhSWpl4": "School's Out",
}

WSU_VIDS_ON_WSF_YT = ['6fzrdEJgSzQ', 'SHPoIrQEKWU', 'KMuz_bTRBGA', 'zMkBAEd7A2s', 'MWORkITfgWA', 'Ja3pwczB4FM', 'QltOI5_Ko_o', '1bGOOXdWgm4', 'ejW87b-FpCU', 'V6oNvSCpiKM', '9hwL5YCwWgc', 'zLUkCgykyI8', 'lQADV6sS8g8', 'x3wq4g6_7wY', 'wTelLHqDbeg', 'NCSYW_sevyc', 'nFbU8hIEzFA', 'eQZCTrJYkYI', 'DKQaXcQHsBM', 'SxmLdJvJ8lc', 't40tlEDwjyg', 'aQNWR9WftHY', 'YcPPGVigvZk', '-NBkgjJhI5U', 'dpqBpY6aGMw', 'xxoqw8nubrc', 'zhVSDP-qDok', 'XFV2feKDK9E', 'HTumBSpjX2c', 'ds1oaReVve4', 'tFOxfjs53u8', 'cqszNrp1EDQ', 'CKJuC5CUMgU', 'vdHbQjVlrfc', 'Fhid7_BhUss', 'wPt3f7yRYUE', 'MQXNSKYCWXw', 'C6-3RjV3GS8']

A_TEST = ['ADiql3FG5is', 'nNtR5da5LIE', '3JE_KMfuEWk', 'CKJuC5CUMgU', 'Fi66wFfOC-4', 'IxRfDtaot5U', 'VN19VOMHxkk', 'p0_-7FmrDq8', 'YdjERhTczAs', 'h9MS9i-CdfY', 'tdsVRh9oKiE', 'TI6sY0kCPpk', 'SObhSqYglvQ', 'BFrBr8oUVXU', 'GdqC2bVLesQ', 'e0vKOYQUmgg', 'PTqLPvBz8xc', 'kT9GqvgipOQ', 'OO4uzgiRHkE', 'KDCJZ81PwVM', 'rU_pfCtSWF4', 'DfY-DRsE86s', 'no3qLqUYBLo', '59ODYOaUbX4', 'iMYJn2-1u2Q', 'SK48AsRIMM8', '3EOpHHjv5g8', '1VajnuxMJmU', 'CoF1Bx-glaw', '9gAcHKraVWE', 'xj6vV3T4ok8', 'n2szWY9xSzU', '7oCQuvhQY6o', 'xk48z8N-sl0', '92A5iDjxgOg']
B_TEST = ['WtjkNsnC--A', 'DPPnrDdNoUU', 'S1jn86eUX0E', 'aUW7patpm9s', 'qMMgsjnI1is', '7f9d7XZu8UQ', 'YSWd21z2qqE', 'HnETCBOlzJs', '6LXHtDUXkS0', 'RNRZchHaKgw', 'XFV2feKDK9E']

BI61300 = {
    "5Iy5mt7F_N4" : "Brave New Prehistoric World",
    "RDVgfFzZVsA" : "Rewiring the Brain",
    "MD-O4Gpx74s" : "Visual Illusions",
    "FiyyndtlHdQ" : "The Deep",
    "wvvovktKKa4" : "Dreaming",
    "ovfqJFkuRrg" : "Sacred Nature",
    "kxFTWk9lLDU" : "Psychedelics",
    "5sMZw_DM5eA" : "Stunning First Images",
    "UtcBFlWSqGM" : "Black Holes",
    "2HU6Hv3fM0I" : "Riddles of Reality",
    "t9jvIyc4Hfg" : "Lifespan Expanded",
    "K7QBnuF6dHg" : "Decoding the Brain",
    "ntxC5KMC4y0" : "Einstein and the Quantum",
    "WtjkNsnC--A" : "Things We've Never Seen",
    "6LXHtDUXkS0" : "Mind Your Language",
    "VN19VOMHxkk" : "Does Math Reveal Reality?",
    "zyaveVWKniw" : "Steven Weinberg and the Quest to Explain the World",
    "9EBJNvrx60I" : "Ardem Patapoutian and David Julius",
    "Gu28y7vZmrI" : "Max Tegmark",
    "feds3yY3YrQ" : "Live Q+A",
    "nO1eWxjQqaA" : "Brian Schmidt",
    "4eVzJbxMZao" : "Paul Nurse",
    "v6YEKYIkrzI" : "Frank Wilczek",
    "ZXuelZVLdzM" : "Live Q+A",
    "xk48z8N-sl0" : "Leonard Susskind",
    "7oCQuvhQY6o" : "Roger Penrose",
    "GmXB7IqbM1o" : "Andrea Ghez",
    "pMXSKt9g1TE" : "Barry Barish",
    "lcsLMvNTGeY" : "Harold Varmus",
    "7obuj1OHt2c" : "Priyamvada Natarajan",
    "fnk4dMW7AzY" : "Gabriela Gonzalez",
    "GfRJZbsywPQ" : "Cumrun Vafa",
    "HZhHovgJ680" : "Adam Riess",
    "ntZO0lZiV-4" : "Live Q+A" 
}

BI62375 = {
    "UjDxk9ZnYJQ": "Unifying Nature's Laws",
    "MO3w2D3uDTw": "Was the Big Bang the Beginning?",
    "pdOgsGBw1t8": "Searching for Cosmic Origins",
    "EGDG3hgPNp8" : "AI",
    "YYZnoe4ZNv4": "Mind Over Molecules",
    "ITJ3AF3TK5M" : "Coding the Cosmos",
    "H2guiFmuhgM" : "String Theory, Quantum Gravity, and Black Holes",
    "rRWIcpZqnXQ" : "Shedding Light on the Dark Universe",
    "BYVMulMNZMs" : "The Past and Future of Life and the Cosmos",
    "WGN4Jv5sWQI" : "Quantum to the Cosmos",
    "rcLfAiXuZYU" : "Comets, Planets, and the Origin of Life",
    "jwYHQ6YwwuY" : "Seeing Further",
    "YJuOQWCyMAc" : "Gravitational Waves",
    "xlyYipjw560" : "Until the End of Time",
    "1f7jm3T_hao" : "Rewriting the Story of Humankind",
    "OcWEYDddJ7Q" : "Revealing the Cosmos",
    "cm8OHGvl4Oc" : "The Golden Age of Space Exploration",
    "VzxI8Xjx1iw" : "Memory",
   "zokNLqGd9TQ": "Saul Perlmutter",
   "aYYhg3yts0c": "Francis Collins",
   "bHKbIhSWpl4": "School's Out",
   "W8W3w3udEXI": "Artemis",
   "UtcBFlWSqGM": "Black Holes"
}