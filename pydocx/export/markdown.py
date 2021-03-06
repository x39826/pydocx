from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from pydocx.export.base import PyDocXExporter
from pydocx.openxml import wordprocessing

def convertStringWithFont(s, fontTable, vowel):
    R = ''
    V = ['', 'ུ', 'ཱ', 'ཱུ']
    if fontTable == None:
        return s
    
    if vowel == None:
        vowel = ''
    else:
        if vowel < 4 and vowel >= 0:
            vowel = V[vowel]
        else:
            vowel = ''
    
    for i in range(len(s)):
        idx = ord(s[i]) - 33
        if idx < len(fontTable) and idx >= 0:
            C = fontTable[idx]
            R += C + vowel    
        else:
            R += s[i]
    R = R.replace('་ ', '་')
    return R
 

def is_tibetan(a):
    return a.startswith('ededris-') or a.startswith('dedris-')

def dedrisIdFromName(a):
    if a == None:
        return None, None
    a = a.lower()
    if is_tibetan(a):
        a = a.split('-')[1]
        name = ''
        num = ''
        for i in range(len(a)):
            if a[i] >= '0' and a[i] <= '9':
                num += a[i]
            else:
                name += a[i]

        if '' == num:
            num = '0'
    
        return name, num
    else:
        return None, None

class PyDocXMarkdownExporter(PyDocXExporter):
    def __init__(self, path):
        self.dedris = {
            'a':['ཀ', '\'', 'ཁ', 'ག', 'ང', 'ཅ', '�', 'ཆ', 'ཇ', 'ཉ', 'ཏ', 'ཐ', '་', 'ད', 'ན', 'པ', 'ཕ', 'བ', 'མ', 'ཙ', 'ཚ', 'ཛ', 'ཝ', 'ཞ', 'ཟ', 'འ', 'ཡ', 'ར', 'ལ', 'ཤ', 'ས', 'ཧ', 'ཨ', 'ཊ', 'ཋ', 'ཌ', 'ཎ', 'ཥ', 'ཀྱ', 'ཁྱ', 'གྱ', 'པྱ', 'ཕྱ', 'བྱ', 'མྱ', 'ཀྲ', 'ཁྲ', 'གྲ', 'ཏྲ', 'ཐྲ', 'དྲ', 'པྲ', 'ཕྲ', 'བྲ', 'མྲ', 'ཤྲ', 'སྲ', 'ཧྲ', 'ཀླ', 'གླ', 'བླ', 'ཟླ', 'རླ', '`', 'སླ', 'རྐ', 'རྒ', 'རྔ', 'རྗ', 'རྙ', 'རྟ', 'རྡ', 'རྣ', 'རྦ', 'རྨ', 'རྩ', 'རྫ', 'རྐྱ', 'རྒྱ', 'རྨྱ', 'ལྐ', 'ལྒ', 'ལྔ', 'ལྕ', 'ལྗ', 'ལྟ', 'ལྡ', 'ལྤ', 'ལྦ', 'ལྷ', 'སྐ', 'སྒ', 'སྔ', 'སྙ'], 
            'b':['སྟ', '\'', 'སྡ', 'སྣ', 'སྤ', 'སྦ', "'", 'སྨ', 'སྩ', 'སྐྱ', 'སྒྱ', 'སྤྱ', '-', 'སྦྱ', 'སྨྱ', 'སྐྲ', 'སྒྲ', 'སྣྲ', 'སྤྲ', 'སྦྲ', 'སྨྲ', 'ཀྭ', 'ཁྭ', 'གྭ', 'གྲྭ', 'རྒྭ', 'ཉྭ', 'ཏྭ', 'སྟྭ', 'ཊྭ', 'དྭ', 'དྲྭ', 'ཕྱྭ', 'ཙྭ', 'རྩྭ', 'ཚྭ', 'ཞྭ', 'ཟྭ', 'རྭ', 'ལྭ', 'ཤྭ', 'སྭ', 'ཧྭ', 'ཀྐ', 'ཀྐྲ', 'ཀྑ', 'ཀྒ', 'ཀྒྷ', 'ཀྔ', 'ཀྟ', 'ཀྟྭ', 'ཀྟྱ', 'ཀྟྲ', 'ཀྚ', 'ཀྠ', 'ཀྛ', 'ཀྡ', 'ཀྡྲ', 'ཀྞ', 'ཀྤ', 'ཀྤྲ', 'ཀྦ', 'ཀྨ', '`', 'ཀྩ', 'ཀྫྙ', 'ཀྴ', 'ཀྴྱ', 'ཀྵ', 'ཀྵྐྵ', 'ཀྵྜ', 'ཀྵྞ', 'ཀྵྨ', 'ཀྵྭ', 'ཀྵྱ', 'ཀྵྲ', 'ཀྵླ', 'ཀྶ', 'ཀྷ', 'ཁྑ', 'ཁྣ', 'ཁླ', 'ཁྷ', 'གྒ', 'གྔ', 'གྔྷ', 'གྟ', 'གྟྱ', 'གྡ', 'གྡྷ', 'གྣ', 'གྣྱ', 'གྞ', 'གྦ'], 
            'c':['གྦྱ', '\'', 'གྦྷ', 'གྨ', 'གྩ', 'གྫ', "'", 'གྻ', 'གྲྱ', 'གྴ', 'གྴྭ', 'གྷ', '-', 'གྷྒྷ', 'གྷྣ', 'གྷྣྱ', 'གྷྭ', 'གྷྱ', 'གྷྲ', 'གྷླ', 'ངྐ', 'ངྐྟ', 'ངྐྟྲ', 'ངྐྱ', 'ངྐྲ', 'ངྑ', 'ངྒ', 'ངྒྱ', 'ངྒླ', 'ངྒྷ', 'ངྒྷྲ', 'ངྔྷ', 'ངྔྷྱ', 'ངྟ', 'ངྻ', 'ངྴ', 'ངྵ', 'ངྶ', 'ངྷ', 'ངྷྣ', 'ངྷྣྱ', 'ངྷྭ', 'ངྷྱ', 'ངྷྲ', 'ཅྭ', 'ཉྠ', 'ཉྩ', 'ཉྪ', 'ཉྫ', 'ཉྫྙ', 'ཏྐ', 'ཏྐྲ', 'ཏྑ', 'ཏྒ', 'ཏྒྲ', 'ཏྟ', 'ཏྟྭ', 'ཏྟྱ', 'ཏྟྲ', 'ཏྠ', 'ཏྠྱ', 'ཏྡྷ', 'ཏྣ', '`', 'ཏྤ', 'ཏྤྠ', 'ཏྤྣ', 'ཏྤྲ', 'ཏྤྷ', 'ཏྥ', 'ཏྦྷ', 'ཏྨ', 'ཏྨྱ', 'ཏྨྲ', 'ཏྪ', 'ཏྫ', 'ཏྱ', 'ཏྻ', 'ཏྲྟྲ', 'ཏྲྱ', 'ཏྵ', 'ཏྶ', 'ཏྶྣ', 'ཏྶྭ', 'ཏྷ', 'ཊྐ', 'ཊྒ', 'ཊྒྲ', 'ཊྚ', 'ཊྚྱ', 'ཊྠ', 'ཊྡ', 'ཊྣ', 'ཊྤ'], 
            'd':['ཊྥ', '\'', 'ཊྦྷ', 'ཊྨ', 'ཊྱ', 'ཊྲ', "'", 'ཊྵ', 'ཊྶ', 'ཐྭ', 'ཐྱ', 'ཐླྷ', '-', 'ཋྐ', 'ཋྱ', 'ཋྲ', 'དྑ', 'དྒ', 'དྒྷ', 'དྒྷྲ', 'དྔ', 'དྟ', 'དྠ', 'དྡ', 'དྡྲ', 'དྡྷ', 'དྡྷྭ', 'དྡྷྱ', 'དྡྷྲ', 'དྤ', 'དྤྲ', 'དྦ', 'དྦྲ', 'དྦྷ', 'དྦྷྱ', 'དྦྷྲ', 'དྨ', 'དྭྱ', 'དྺ', 'དྱ', 'དྲྱ', 'དྶ', 'དྷ', 'དྷྣ', 'དྷྣྱ', 'དྷྨ', 'དྷྭ', 'དྷྱ', 'དྷྲ', 'ཌྒ', 'ཌྒྷ', 'ཌྒྲ', 'ཌྡྷ', 'ཌྜ', 'ཌྜྷ', 'ཌྦྷ', 'ཌྨ', 'ཌྱ', 'ཌྷ', 'ཌྷྱ', 'ཌྷྲ', 'ནྐ', 'ནྟ', '`', 'ནྟྭ', 'ནྟྱ', 'ནྟྲ', 'ནྚ', 'ནྠ', 'ནྡ', 'ནྡྟ', 'ནྡྭ', 'ནྡྱ', 'ནྡྲ', 'ནྡྷ', 'ནྡྷྱ', 'ནྡྷྲ', 'ནྜ', 'ནྣ', 'ནྤ', 'ནྥ', 'ནྦྷ', 'ནྨ', 'ནྩ', 'ནྫ', 'ནྭ', 'ནྱ', 'ནྻ', 'ནྲ', 'ནླ', 'ནྴ', 'ནྶ', 'ནྷ', 'ཎྔ'], 
            'e':['ཎྔྟ', '\'', 'ཎྟ', 'ཎྟྲ', 'ཎྚ', 'ཎྛ', "'", 'ཎྡ', 'ཎྡྟ', 'ཎྡྡྷ', 'ཎྡྭ', 'ཎྡྱ', '-', 'ཎྡྲ', 'ཎྡྷ', 'ཎྜ', 'ཎྞ', 'ཎྨ', 'ཎྱ', 'ཎྻ', 'ཎྲ', 'ཎྵ', 'པྐྲ', 'པྔྷ', 'པྟ', 'པྠ', 'པྡ', 'པྡྷ', 'པྣ', 'པྤ', 'པྥ', 'པྨ', 'པྫ', 'པྻ', 'པླ', 'པྴ', 'པྶ', 'པྷ', 'ཕྥ', 'བྐ', 'བྟ', 'བྠ', 'བྡ', 'བྡྷ', 'བྥ', 'བྦྷ', 'བྦྷྱ', 'བྨ', 'བྫ', 'བྻ', 'བྷ', 'བྷྨ', 'བྷྱ', 'བྷྻ', 'བྷྲ', 'མྒྷ', 'མྟ', 'མྣ', 'མྞ', 'མྤ', 'མྤྱ', 'མྤྲ', 'མྥ', '`', 'མྦ', 'མྦྲ', 'མྦླ', 'མྦྷ', 'མྦྷྱ', 'མྦྷྲ', 'མྨ', 'མྨྲ', 'མྺ', 'མླ', 'མྴ', 'མྶ', 'ཙྐ', 'ཙྩ', 'ཙྪ', 'ཙྪྭ', 'ཙྪྱ', 'ཙྪྲ', 'ཙྱ', 'ཙྻ', 'ཙྲ', 'ཙྴ', 'ཚྪ', 'ཛྙ', 'ཛྙྱ', 'ཛྨ', 'ཛྫ', 'ཛྫྙ', 'ཛྫྷ', 'ཛྭ'], 
            'f':['ཛྱ', '\'', 'ཛྲ', 'ཛྷ', 'ཛྷྱ', 'ཝྱ', "'", 'ཝྲ', 'འྭ', 'ཡྦ', 'ཡྻ', 'ཡྶ', '-', 'རྐྐ', 'རྐྟ', 'རྐྲ', 'རྐྴ', 'རྐྴྱ', 'རྐྵ', 'རྐྵྱ', 'རྑ', 'རྒྒ', 'རྒྦྷ', 'རྒྵ', 'རྒྱྭ', 'རྒྲ', 'རྒྷ', 'རྒྷྱ', 'རྔྷ', 'རྔྷྱ', 'རྟྟ', 'རྟྤྣྱ', 'རྟྨ', 'རྟྱ', 'རྟྲ', 'རྟྶྣྱ', 'རྚ', 'རྠ', 'རྠྱ', 'རྡྭ', 'རྡྡ', 'རྡྡྷ', 'རྡྨ', 'རྡྱ', 'རྡྲ', 'རྡྷ', 'རྡྷྭ', 'རྡྷྲ', 'རྜ', 'རྜྷྲ', 'རྣྡྲ', 'རྣྭ', 'རྞ', 'རྞྞ', 'རྞྱ', 'རྤྱ', 'རྥ', 'རྦྟ', 'རྦྤ', 'རྦྦ', 'རྦྦྷ', 'རྦྦྷྱ', 'རྦྱ', '`', 'རྦྲ', 'རྦྷ', 'རྦྷྱ', 'རྦྷྲ', 'རྨྨ', 'རྩྩ', 'རྩྪ', 'རྫྙ', 'རྫྫ', 'རྫྭ', 'རྫྲ', 'རྫྷ', 'རྵྱ', 'རྷ', 'ཪྟ', 'ཪྠ', 'ཪྡ', 'ཪྣྲ', 'ཪྞ', 'ཪྞྜ', 'ཪྞྞ', 'ཪྤ', 'ཪྤྤ', 'ཪྤྲ', 'ཪྥ', 'ཪྦ', 'ཪྦྟ', 'ཪྦྷ', 'ཪྨ', 'ཪྪ'], 
            'g':['ཪྺ', '\'', 'ཪྱ', 'ཪྻ', 'ཪྻྻ', 'ཪྴ', "'", 'ཪྴྣ', 'ཪྴྞ', 'ཪྴྨ', 'ཪྴྭ', 'ཪྴྱ', '-', 'ཪྵ', 'ཪྵྨ', 'ཪྶ', 'ལྤྱ', 'ལྥ', 'ལྦྷ', 'ལྨ', 'ལྱ', 'ལྱྭ', 'ལྻ', 'ལླ', 'ལྷྭ', 'ཤྟ', 'ཤྚ', 'ཤྣ', 'ཤྞ', 'ཤྨ', 'ཤྩ', 'ཤྩྱ', 'ཤྪ', 'ཤྱ', 'ཤྻ', 'ཤླ', 'ཤྴ', 'ཥྐ', 'ཥྐྲ', 'ཥྟ', 'ཥྚ', 'ཥྚྭ', 'ཥྚྱ', 'ཥྚྲ', 'ཥྠ', 'ཥྛ', 'ཥྞ', 'ཥྤ', 'ཥྤྱ', 'ཥྤྲ', 'ཥྦ', 'ཥྨ', 'ཥྩ', 'ཥྩྱ', 'ཥྭ', 'ཥྱ', 'ཥླ', 'ཥྵ', 'ཥྶ', 'སྑ', 'སྗ', 'སྟྱ', 'སྟྲ', '`', 'སྟྲྱ', 'སྠ', 'སྥ', 'སྦྷ', 'སྫ', 'སྱ', 'སྻ', 'སྴ', 'སྵ', 'སྶ', 'ཧྟ', 'ཧྣ', 'ཧྞ', 'ཧྥ', 'ཧྨ', 'ཧྨྱ', 'ཧྱ', 'ཧྱྭ', 'ཧྻ', 'ཧླ', 'ཧྶ', 'ཨྱ', 'ཨྸ', 'x', 'y', 'z', '{', '|', '}', '~'], 
            'vowa':['༄༅', '\'', '༄༅༅', '༅', 'ྃ', 'ྃ', "'", 'ཾ', 'ཾ', '༁ྃ', 'ྂ', '།', '་', '༑', '༴', '༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩', 'ཿ', '༔', 'ཨོཾ', 'ཨཱཿ', 'ཧཱུྃ', '༈', '྅', 'ི', 'ི', 'ི', 'ིཾ', 'ིཾ', 'ྀ', 'ྀ', 'ྀཾ', 'ྀཾ', 'ེ', 'ེ', 'ེཾ', 'ེཾ', 'ཻ', 'ཻ', 'ཻཾ', 'ཻཾ', 'ོ', 'ོ', 'ོཾ', 'ོཾ', 'ོྃ', 'ཽ', 'ཽ', 'ཽཾ', 'ཽཾ', 'ཀ྄', 'ག྄', 'ཏ྄', 'ད྄', 'ཌ྄', '`', 'བ྄', 'མ྄', 'ཙ྄', 'ཛ྄', 'ར྄', 'ས྄', 'ཆྒཻ', '྄', '྄', 'ྈ', 'ྉ', 'ྈྐ', 'ྈྑ', 'ྉྤ', 'ྉྥ', '�', 'འུྃ', 'ཧཱུྂ', 'ཨྠ', 'ཨྠྀི', 'ྊྃ', 'ལྙྃ', '༵', '༵', '༷', '༷', '', '༧', '}', '~'], 
            'syma':['*', '\'', '�', '�', '%', '&', "'", '༼', '༽', 'ངྔ', 'ངླ', 'ངྼ', '-', 'ཀྒླཱ', '/', 'ཋྚ', 'ཊྛ', 'ཌྛ', 'རྟྟྨ', 'མླྭ', 'ཀྐླཱ', 'ཀྐཱུ', '_', '_', '_', '{', '}', '(', '=', ')', '?', '', 'ལྼ', 'ལྼཱ', 'ཨྭ', 'ཐྐ', 'མྷ', 'ལྲ', 'ཀྼ', 'ཁྼ', 'གྼ', '«', '»', '༏', '[', ']', '©', '', '', '', '', 'གྷྒྟ', '', '', 'ཉྐ', 'ཤྦ', 'Y', 'Z', '༼', '\\', '༽', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '༼', '|', '༽', '']
            }

        super(PyDocXMarkdownExporter, self).__init__(path=path)
    
    # Perform specific pre-processing
    def export(self):
        self.modify_text_encoding()
        return ''.join(
            result for result in super(PyDocXMarkdownExporter, self).export()
        )

    def modify_text_encoding(self):
        # Delete all text nodes that match 'FOO' exactly
        document = self.main_document_part.document
        styles = self.style_definitions_part.styles
        #print(styles)
        
        for body_child in document.body.children:
            if isinstance(body_child, wordprocessing.Paragraph):
                paragraph = body_child
                ascii = None
                for style in paragraph.get_style_chain_stack():
                    if style.run_properties is not None:
                        if style.run_properties.r_fonts is not None:
                            if style.run_properties.r_fonts.ascii is not None:
                                ascii = style.run_properties.r_fonts.ascii
                                break
                for paragraph_child in paragraph.children:
                    if isinstance(paragraph_child, wordprocessing.Run):
                        run = paragraph_child
                        pop = paragraph_child.properties
                        ascii_n = ascii
                        if pop is not None:
                            if pop.r_fonts is not None:
                                if pop.r_fonts.ascii is not None:
                                    ascii_n = pop.r_fonts.ascii
                        #print(ascii, ascii_n)
                        name, id = dedrisIdFromName(ascii_n)
                        if name is not None:
                            i = 0
                            #print(run.children[:])
                            for run_child in run.children[:]:
                                if isinstance(run_child, wordprocessing.Text):
                                    text = run_child
                                    #print(run_child)
                                    c = convertStringWithFont(run_child.text, self.dedris[name], int(id))
                                    #print(run.children[i].text)
                                    run.children[i].text = c
                                i+=1

    def escape(self, text):
        return text

    def linebreak(self):
        return '\n'

    def paragraph(self, text):
        return text + '\n'

    def insertion(self, text, author, date):
        pass

    def bold(self, text):
        return '**' + text + '**'

    def italics(self, text):
        # TODO do we need a "pre" variable, so I can check for
        # *italics**italics* and turn it into *italicsitatlics*?
        return '*' + text + '*'

    def underline(self, text):
        return '***' + text + '***'
