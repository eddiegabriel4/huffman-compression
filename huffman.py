from __future__ import annotations
from typing import List, Optional
import sys
sys.setrecursionlimit(5000)

class HuffmanNode:
    def __init__(self, char_ascii: int, freq: int, left: Optional[HuffmanNode] = None, right: Optional[HuffmanNode] = None):
        self.char_ascii = char_ascii    # stored as an integer - the ASCII character code value
        self.freq = freq                # the frequency associated with the node
        self.left = left                # Huffman tree (node) to the left!
        self.right = right              # Huffman tree (node) to the right

    def __lt__(self, other: HuffmanNode) -> bool:
        return comes_before(self, other)
"""
    def __repr__(self) -> str:
        return ("HuffmanNode({!r}, {!r}, {!r}, {!r})".format(chr(self.char_ascii), self.freq, self.left, self.right)) 
"""

def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    if a.freq == b.freq:
        if a.char_ascii < b.char_ascii:
            return True
        else:
            return False
    else:
        return False



def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""
    HuffmanNode1 = HuffmanNode(0, 0)
    HuffmanNode1.char_ascii = min(a.char_ascii, b.char_ascii)
    HuffmanNode1.freq = (a.freq) + (b.freq)
    if comes_before(a, b) == True:
        HuffmanNode1.left = a
        HuffmanNode1.right = b
    else:
        HuffmanNode1.left = b
        HuffmanNode1.right = a
    return HuffmanNode1
        


def cnt_freq(filename: str) -> List:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    try:
        with open(filename, 'r') as dataf:
            data_lines = dataf.readlines()
    except:
        raise FileNotFoundError
    final = ''.join(data_lines)
    final_list = [0]*256
    for j in final:
        if ord(j) <= 256:
            freq = final.count(j)
            final_list[ord(j)] = freq
    return final_list


        
    

def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    sorted_list = []
    None_counter = []
    for i in range(0, len(char_freq)):
        if char_freq[i] > 0:
            HuffmanNode1 = HuffmanNode(0, 0)
            HuffmanNode1.char_ascii = i
            HuffmanNode1.freq = char_freq[i]
            sorted_list.append(HuffmanNode1)
        else:
            None_counter.append(1)
    if len(None_counter) == 256:
        return None
    else:
        sorted_listy = sorted(sorted_list, key = lambda x: (x.freq, x.char_ascii))
        while len(sorted_listy) >= 2:
            a = sorted_listy[0]
            b = sorted_listy[1]
            new_huff = combine(a, b)
            sorted_listy.remove(a)
            sorted_listy.remove(b)
            sorted_listy.append(new_huff)
            sorted_listy = sorted(sorted_listy, key = lambda x: (x.freq, x.char_ascii))
        return sorted_listy[0]


def create_code(node: Optional[HuffmanNode]) -> List:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    huff_codes = ['']*256
    if node.left == None and node.right == None:
        create_help(node, '', huff_codes)
    if node.left:
        create_help(node.left, '0', huff_codes)
    if node.right:
        create_help(node.right, '1', huff_codes)
    return huff_codes

    

def create_help(node: Optional[HuffmanNode], temp_str:str, huff_codes:list) -> List:
    if node.left == None and node.right == None:
        huff_codes[node.char_ascii] = temp_str
        return huff_codes
    if node.left:
        yes = temp_str + '0'
        create_help(node.left, yes, huff_codes)
    if node.right:
        yes = temp_str + '1'
        create_help(node.right, yes, huff_codes)
    return huff_codes


def create_header(freqs: List) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    final = []
    for i in range(0, len(freqs)):
        if freqs[i] != 0:
            final.append(str(i))
            final.append(str(freqs[i]))
    a = ' '.join(final)
    return a



def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    freq_cnt = cnt_freq(in_file)
    root = create_huff_tree(freq_cnt)
    huff_codes_lst = create_code(root)
    header = create_header(freq_cnt)
    try:
        with open(in_file, 'r') as dataf:
            data_lines = dataf.readlines()
    except:
        raise FileNotFoundError
    final = ''.join(data_lines)
    all_codes = []
    for i in range(0, len(final)):
        index = ord(final[i])
        all_codes.append(huff_codes_lst[index])
    yes = ''.join(all_codes)
    with open(out_file, 'w', newline = '') as outall:
        outall.write(header + '\n')
        outall.write(yes)

def parse_header(header_string: str) -> List:
    """Takes first line of encoded file and uses a helper function to recursivly turn those numbers into a 256 spaced frequency counter
    """
    frequen_list = [0]*256
    header_list = header_string.split()
    return parse_help(header_list, frequen_list)

def parse_help(header_list: List, frequen_list: List) -> List:

    while len(header_list) > 0:
        frequen_list[int(header_list[0])] = int(header_list[1])
        header_list = header_list[2:]
    return frequen_list


def leaf_check(root: Optional[HuffmanNode]) -> bool:
    """checks if a node is a leaf node that has no left and right attributes"""
    if root.right == None and root.left == None:
        return True
    else:
        return False


def huff_tree_verse2(root: Optional[HuffmanNode], codec: str) -> List:
    """Takes the completed huffman tree and all the ones and zeroes in the encoded file. Iterates over the data and adds the leaf nodes' character data to a list"""

    decoded = []
    reset = root
    for num in codec:
        if int(num) == 1:
            reset = reset.right
        if int(num) == 0:
            reset = reset.left
        if leaf_check(reset) == True:
            decoded.append(chr(reset.char_ascii))
            reset = root
    return decoded


def huffman_decode(encoded_file: str, decoded_file: str) -> None:
    """
    reads an encoded file and turns it into readable information which it writes to an output file
    """
    with open(encoded_file, 'r') as dataf:
        data_lines = dataf.readlines()
    freq_lst = parse_header(data_lines[0])
    root = create_huff_tree(freq_lst)
    codec = data_lines[1][:len(data_lines[1]) - 1]
    text = huff_tree_verse2(root, codec)
    texty = ''.join(text)
    with open(decoded_file, 'w', newline = '') as outall:
        outall.write(texty)


