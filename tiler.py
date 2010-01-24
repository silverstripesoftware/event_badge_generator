# AUTHOR: Yuvi Panda <me@yuvi.in>
import os
import Image
import sys

DPMM = 11.8 # That's 300 DPI

PAPER = (int(297 * DPMM), int(420 * DPMM))

CARD = (int(140 * DPMM), int(100 * DPMM))

PADDING = (int(4 * DPMM), int(4 * DPMM))

COLS = int(PAPER[0] / CARD[0])
ROWS = int(PAPER[1] / CARD[1])

paper_index = 0
card_index = 0

if len(sys.argv) < 3:
    print "USAGE: %s <cards_folder> <output_folder>" % __file__
    sys.exit()

card_folder = sys.argv[1]
tiled_folder = sys.argv[2]

if not os.path.exists(tiled_folder):
    os.mkdir(tiled_folder)

card_files = os.listdir(card_folder)

def create_paper():
    return Image.new("CMYK", PAPER)

def save_paper(paper, name):
    paper.save(os.path.join(tiled_folder, name + '.jpeg'))

paper = create_paper()

for card_file in card_files:
    card = Image.open(os.path.join(card_folder, card_file))
    card = card.resize(CARD)
    # UGLY HACK
    # I HAVE NO IDEA WHY THE PADDING WORKS THE WAY IT DOES
    # FIX THIS WHEN YOU WANT TO HAVE CORRECT CODE AND NOT JUST WORKING CODE
    x = ((CARD[0] + PADDING[0]) * (card_index % COLS)) + PADDING[0]
    y = ((CARD[1] + PADDING[1]) * (card_index / COLS)) + PADDING[1]
    paper.paste(card, (x, y))
    print "Paper %d, Card %d" % (paper_index, card_index)

    # Paper rotation
    if card_index == (ROWS * COLS) - 1: 
        save_paper(paper, str(paper_index))
        print "Saved Paper %d" % paper_index
        paper = create_paper()
        paper_index += 1
        card_index = 0
    else:
        card_index += 1
    
save_paper(paper, str(paper_index)) # Save the last paper
