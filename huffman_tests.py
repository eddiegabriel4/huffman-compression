import unittest
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self) -> None:
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

    def test_combine(self) -> None:
        a = HuffmanNode(65, 1)
        b = HuffmanNode(66, 2)
        c = combine(a, b)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii,65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:   # pragma: no cover
            self.fail()
        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii,65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:   # pragma: no cover
            self.fail()

    def test_create_huff_tree(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        if hufftree is not None:
            self.assertEqual(hufftree.freq, 33)
            self.assertEqual(hufftree.char_ascii, 10)
            left = hufftree.left
            right = hufftree.right
            if (left is not None) and (right is not None):
                self.assertEqual(left.freq, 16)
                self.assertEqual(left.char_ascii, 100)
                self.assertEqual(right.freq, 17)
                self.assertEqual(right.char_ascii, 10)
            else: # pragma: no cover
                self.fail()
        else: # pragma: no cover
            self.fail()
    
    def test_create_header(self) -> None:
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "10 1 97 2 98 4 99 8 100 16 102 2")

    def test_before_false(self) -> None:
        a = HuffmanNode(71, 8)
        b = HuffmanNode(70, 8)
        self.assertEqual(comes_before(a, b), False)

    def test_all_none(self) -> None:
        char_freq = [0]*256
        self.assertEqual(create_huff_tree(char_freq), None)

    def test_both_none(self) -> None:
        a = HuffmanNode(80, 8, None, None)
        huff_codes = ['']*256
        huff_codes[a.char_ascii] = ''
        self.assertEqual(create_code(a), huff_codes)

    def test_lt(self) -> None:
        no = HuffmanNode(100, 20)
        other = HuffmanNode(130, 40)
        yes = no.__lt__(other)
        self.assertTrue(yes)


    
    def test_create_code(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '0')
        self.assertEqual(codes[ord('a')], '11111')
        self.assertEqual(codes[ord('f')], '1110')
    
    def test_01_textfile(self) -> None:
        huffman_encode("declaration.txt", "file1_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1_out.txt", "declaration_soln.txt"))

    def test_parse_header(self) -> None:
        header = "97 2 98 4 99 8 100 16 102 2"
        freqlist = parse_header(header)
        anslist = [0]*256
        anslist[97:104] = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist[97:104])

    def test_decode_01(self) -> None:
        huffman_decode("file1_soln.txt", "file1_decode.txt")
        # detect errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1.txt", "file1_decode.txt"))

    def test_decode_02(self) -> None:
        huffman_decode("declaration_soln.txt", "declaration_decode.txt")
        # detect errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("declaration.txt", "declaration_decode.txt"))

    def test_errors_01(self) -> None:
        with self.assertRaises(FileNotFoundError):
            cnt_freq('sdjhfsjhf.txt')

    def test_errors_02(self) -> None:
        with self.assertRaises(FileNotFoundError):
            huffman_encode('fsljdfhsjfh.txt', 'fasoudhf.txt')

    def test_errors_03(self) -> None:
        with self.assertRaises(FileNotFoundError):
            huffman_decode('faskdjfhasiudhfiasdhf.txt', 'tashdfiu.txt')



# Compare files - takes care of CR/LF, LF issues
def compare_files(file1: str, file2: str) -> bool: # pragma: no cover
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:
                    done = True
                    match = False
    return match
    
if __name__ == '__main__':
    unittest.main()
