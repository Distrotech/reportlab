#Copyright ReportLab Europe Ltd. 2000-2004
#see license.txt for license details
# tests some paragraph styles
__version__='''$Id$'''
from reportlab.lib.testutils import setOutDir,makeSuiteForClasses, outputfile, printLocation
setOutDir(__name__)
import unittest
from reportlab.platypus import Paragraph, SimpleDocTemplate, XBox, Indenter, XPreformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import red, black, navy, white, green
from reportlab.lib.randomtext import randomText
from reportlab.rl_config import defaultPageSize

(PAGE_WIDTH, PAGE_HEIGHT) = defaultPageSize

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(red)
    canvas.setLineWidth(5)
    canvas.line(66,72,66,PAGE_HEIGHT-72)
    canvas.setFont('Times-Bold',24)
    canvas.drawString(108, PAGE_HEIGHT-54, "TESTING PARAGRAPH STYLES")
    canvas.setFont('Times-Roman',12)
    canvas.drawString(4 * inch, 0.75 * inch, "First Page")
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(red)
    canvas.setLineWidth(5)
    canvas.line(66,72,66,PAGE_HEIGHT-72)
    canvas.setFont('Times-Roman',12)
    canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


class ParagraphTestCase(unittest.TestCase):
    "Test Paragraph class (eyeball-test)."

    def test0(self):
        """Test...

        The story should contain...

        Features to be visually confirmed by a human being are:

            1. ...
            2. ...
            3. ...
        """

        story = []

        #need a style
        styNormal = ParagraphStyle('normal')
        styGreen = ParagraphStyle('green',parent=styNormal,textColor=green)

        # some to test
        stySpaced = ParagraphStyle('spaced',
                                   parent=styNormal,
                                   spaceBefore=12,
                                   spaceAfter=12)


        story.append(
            Paragraph("This is a normal paragraph. "
                      + randomText(), styNormal))
        story.append(
            Paragraph("There follows a paragraph with only \"&lt;br/&gt\"", styNormal))
        story.append(Paragraph("<br/>", styNormal))
        story.append(
            Paragraph("This has 12 points space before and after, set in the style. "
                      + randomText(), stySpaced))
        story.append(
            Paragraph("This is normal. " +
                      randomText(), styNormal))

        story.append(
            Paragraph("""<para spacebefore="12" spaceafter="12">
            This has 12 points space before and after, set inline with
            XML tag.  It works too.""" + randomText() + "</para",
                      styNormal))

        story.append(
            Paragraph("This is normal. " +
                      randomText(), styNormal))

        styBackground = ParagraphStyle('MyTitle',
                                       fontName='Helvetica-Bold',
                                       fontSize=24,
                                       leading=28,
                                       textColor=white,
                                       backColor=navy)
        story.append(
            Paragraph("This is a title with a background. ", styBackground))

        story.append(
            Paragraph("""<para backcolor="pink">This got a background from the para tag</para>""", styNormal))


        story.append(
            Paragraph("""<para>\n\tThis has newlines and tabs on the front but inside the para tag</para>""", styNormal))
        story.append(
            Paragraph("""<para>  This has spaces on the front but inside the para tag</para>""", styNormal))

        story.append(
            Paragraph("""\n\tThis has newlines and tabs on the front but no para tag""", styNormal))
        story.append(
            Paragraph("""  This has spaces on the front but no para tag""", styNormal))

        story.append(Paragraph("""This has <font color=blue>blue text</font> here.""", styNormal))
        story.append(Paragraph("""This has <i>italic text</i> here.""", styNormal))
        story.append(Paragraph("""This has <b>bold text</b> here.""", styNormal))
        story.append(Paragraph("""This has <u>underlined text</u> here.""", styNormal))
        story.append(Paragraph("""This has <font color=blue><u>blue and <font color=red>red</font> underlined text</u></font> here.""", styNormal))
        story.append(Paragraph("""<u>green underlining</u>""", styGreen))
        story.append(Paragraph("""<u>green <font size=+4><i>underlining</font></i></u>""", styGreen))
        story.append(Paragraph("""This has m<super>2</super> a superscript.""", styNormal))
        story.append(Paragraph("""This has m<sub>2</sub> a subscript. Like H<sub>2</sub>O!""", styNormal))
        story.append(Paragraph("""This has a font change to <font name=Helvetica>Helvetica</font>.""", styNormal))
        #This one fails:
        #story.append(Paragraph("""This has a font change to <font name=Helvetica-Oblique>Helvetica-Oblique</font>.""", styNormal))
        story.append(Paragraph("""This has a font change to <font name=Helvetica><i>Helvetica in italics</i></font>.""", styNormal))

        story.append(Paragraph('''This one uses upper case tags and has set caseSensitive=0: Here comes <FONT FACE="Helvetica" SIZE="14pt">Helvetica 14</FONT> with <STRONG>strong</STRONG> <EM>emphasis</EM>.''', styNormal, caseSensitive=0))
        story.append(Paragraph('''The same as before, but has set not set caseSensitive, thus the tags are ignored: Here comes <FONT FACE="Helvetica" SIZE="14pt">Helvetica 14</FONT> with <STRONG>strong</STRONG> <EM>emphasis</EM>.''', styNormal))
        story.append(Paragraph('''This one uses fonts with size "14pt" and also uses the em and strong tags: Here comes <font face="Helvetica" size="14pt">Helvetica 14</font> with <Strong>strong</Strong> <em>emphasis</em>.''', styNormal, caseSensitive=0))
        story.append(Paragraph('''This uses a font size of 3cm: Here comes <font face="Courier" size="3cm">Courier 3cm</font> and normal again.''', styNormal, caseSensitive=0))
        story.append(Paragraph('''This is just a very long silly text to see if the <FONT face="Courier">caseSensitive</FONT> flag also works if the paragraph is <EM>very</EM> long. '''*20, styNormal, caseSensitive=0))
        story.append(Indenter("1cm"))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm' bulletOffsetY='2'><seq id='s0'/>)</bullet>Indented list bulletOffsetY=2. %s</para>" % randomText(), styNormal))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Indenter("1cm"))
        story.append(XPreformatted("<para leftIndent='0.5cm' backcolor=pink><bullet bulletIndent='-1cm'><seq id='s1'/>)</bullet>Indented list.</para>", styNormal))
        story.append(XPreformatted("<para leftIndent='0.5cm' backcolor=palegreen><bullet bulletIndent='-1cm'><seq id='s1'/>)</bullet>Indented list.</para>", styNormal))
        story.append(Indenter("-1cm"))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Indenter("-1cm"))
        story.append(Paragraph("<para>Indented list using seqChain/Format<seqChain order='s0 s1 s2 s3 s4'/><seqReset id='s0'/><seqFormat id='s0' value='1'/><seqFormat id='s1' value='a'/><seqFormat id='s2' value='i'/><seqFormat id='s3' value='A'/><seqFormat id='s4' value='I'/></para>", stySpaced))
        story.append(Indenter("1cm"))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Indenter("1cm"))
        story.append(XPreformatted("<para backcolor=pink boffsety='-3'><bullet bulletIndent='-1cm'><seq id='s1'/>)</bullet>Indented list bulletOffsetY=-3.</para>", styNormal))
        story.append(XPreformatted("<para backcolor=pink><bullet bulletIndent='-1cm'><seq id='s1'/>)</bullet>Indented list.</para>", styNormal))
        story.append(Indenter("-1cm"))
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'><seq id='s0'/>)</bullet>Indented list. %s</para>" % randomText(), styNormal))
        story.append(Indenter("1cm"))
        story.append(XPreformatted("<para backcolor=palegreen><bullet bulletIndent='-1cm'><seq id='s1'/>)</bullet>Indented list.</para>", styNormal))
        story.append(Indenter("1cm"))
        story.append(XPreformatted("<para><bullet bulletIndent='-1cm'><seq id='s2'/>)</bullet>Indented list. line1</para>", styNormal))
        story.append(XPreformatted("<para><bullet bulletIndent='-1cm'><seq id='s2'/>)</bullet>Indented list. line2</para>", styNormal))
        story.append(Indenter("-1cm"))
        story.append(XPreformatted("<para backcolor=palegreen><bullet bulletIndent='-1cm'><seq id='s1'/>)</bullet>Indented list.</para>", styNormal))
        story.append(Indenter("-1cm"))
        story.append(Indenter("-1cm"))

        template = SimpleDocTemplate(outputfile('test_paragraphs.pdf'),
                                     showBoundary=1)
        template.build(story,
            onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    
    def testBidi(self):
        from reportlab.pdfbase import ttfonts
        def registerFont(filename):
            from reportlab.pdfbase import pdfmetrics
            from reportlab.lib.fonts import addMapping
        
            face = ttfonts.TTFontFace(filename)
            pdfmetrics.registerFont(ttfonts.TTFont(face.name, filename, asciiReadable=0))
            addMapping(face.familyName, face.bold, face.italic, face.name)

        # register a font that supports most Unicode characters
        import os
        fontDir = 'ttf-dejavu'
        fontName = 'DejaVuSans'
        try:
            registerFont(os.path.join('/usr/share/fonts/truetype/', fontDir, fontName + '.ttf'))
        except ttfonts.TTFError:
            registerFont(os.path.join(fontDir, fontName + '.ttf'))

        # create styles based on the registered font
        from reportlab.lib.enums import TA_LEFT, TA_RIGHT
        styLTR = ParagraphStyle('left', fontName = fontName)
        styRTL = ParagraphStyle('right', parent = styLTR, alignment = TA_RIGHT,
                                wordWrap = 'RTL', spaceAfter = 12)

        # strings for testing LTR.
        ltrStrings = [# English followed by Arabic.
                      'English followed by \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a.',
                      # English with Arabic in the middle
                      'English with \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a in the middle.',
                      # English symbols (!@#$%^&*) Arabic
                      'English symbols (!@#$%^&*) \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a.',
                      # ((testing integers in LTR)) 
                      '123 LTR 123 Integers 123.',
                      # ((testing decimals in LTR))
                      '456.78 LTR 456.78 Decimals 456.78.',
                      # Long English text with RTL script in the middle, splitting over multiple lines
                      'Long \xd8\xb7\xd9\x88\xd9\x8a\xd9\x84 English text'
                          ' \xd9\x86\xd8\xb5 \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a with RTL script'
                          ' \xd9\x83\xd8\xaa\xd8\xa7\xd8\xa8\xd8\xa9 \xd9\x85\xd9\x86'
                          ' \xd8\xa7\xd9\x84\xd9\x8a\xd9\x85\xd9\x8a\xd9\x86 \xd8\xa5\xd9\x84\xd9\x89'
                          ' \xd8\xa7\xd9\x84\xd9\x8a\xd8\xb3\xd8\xa7\xd8\xb1 in the middle,'
                          ' \xd9\x81\xd9\x8a \xd8\xa7\xd9\x84\xd9\x88\xd8\xb3\xd8\xb7\xd8\x8c'
                          ' splitting \xd9\x85\xd9\x82\xd8\xb3\xd9\x85 over \xd8\xb9\xd9\x84\xd9\x89'
                          ' multiple lines \xd8\xb9\xd8\xaf\xd8\xa9 \xd8\xb3\xd8\xb7\xd9\x88\xd8\xb1.',
                      ]

        # strings for testing RTL
        rtlStrings = [# Arabic followed by English
                      '\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a \xd9\x85\xd8\xaa\xd8\xa8\xd9\x88\xd8\xb9'
                          ' \xd8\xa8\xd9\x80 English.',
                      # Arabic with English in the middle
                      '\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a \xd9\x85\xd8\xb9 English \xd9\x81\xd9\x8a'
                          ' \xd8\xa7\xd9\x84\xd9\x85\xd9\x86\xd8\xaa\xd8\xb5\xd9\x81.',
                      # Arabic symbols (!@##$%^&*) English
                      '\xd8\xb1\xd9\x85\xd9\x88\xd8\xb2 \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd8\xa9'
                          ' (!@#$%^&*) English.',
                      # 123 from right to left 123 integer numbers 123. ((testing integers in RTL))
                      '123 \xd9\x85\xd9\x86 \xd8\xa7\xd9\x84\xd9\x8a\xd9\x85\xd9\x8a\xd9\x86'
                          ' \xd8\xa5\xd9\x84\xd9\x89 \xd8\xa7\xd9\x84\xd9\x8a\xd8\xb3\xd8\xa7\xd8\xb1'
                          ' 123 \xd8\xa3\xd8\xb1\xd9\x82\xd8\xa7\xd9\x85'
                          ' \xd8\xb5\xd8\xad\xd9\x8a\xd8\xad\xd8\xa9 123.',
                      # 456.78 from right to left 456.78 decimal numbers 456.78. ((testing decimals in RTL))
                      '456.78 \xd9\x85\xd9\x86 \xd8\xa7\xd9\x84\xd9\x8a\xd9\x85\xd9\x8a\xd9\x86'
                          ' \xd8\xa5\xd9\x84\xd9\x89 \xd8\xa7\xd9\x84\xd9\x8a\xd8\xb3\xd8\xa7\xd8\xb1'
                          ' 456.78 \xd8\xa3\xd8\xb1\xd9\x82\xd8\xa7\xd9\x85'
                          ' \xd8\xb9\xd8\xb4\xd8\xb1\xd9\x8a\xd8\xa9 456.78.',
                      # Long Arabic text with LTR script in the middle, splitting over multiple lines
                      '\xd9\x86\xd8\xb5 \xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a \xd8\xb7\xd9\x88\xd9\x8a\xd9\x84'
                          ' Long Arabic text \xd9\x85\xd8\xb9 with \xd9\x83\xd8\xaa\xd8\xa7\xd8\xa8\xd8\xa9'
                          ' \xd9\x85\xd9\x86 \xd8\xa7\xd9\x84\xd9\x8a\xd8\xb3\xd8\xa7\xd8\xb1'
                          ' \xd8\xa5\xd9\x84\xd9\x89 \xd8\xa7\xd9\x84\xd9\x8a\xd9\x85\xd9\x8a\xd9\x86'
                          ' LTR script \xd9\x81\xd9\x8a \xd8\xa7\xd9\x84\xd9\x88\xd8\xb3\xd8\xb7\xd8\x8c'
                          ' in the middle, \xd9\x85\xd9\x82\xd8\xb3\xd9\x85 splitted'
                          ' \xd8\xb9\xd9\x84\xd9\x89 over \xd8\xb9\xd8\xaf\xd8\xa9'
                          ' \xd8\xb3\xd8\xb7\xd9\x88\xd8\xb1 multiple lines.'
                      ]

        assert len(ltrStrings) == len(rtlStrings)
        n = len(ltrStrings)
        
        # create a store to be printed
        story = []
        
        # write every LTR string and its corresponding RTL string to be matched.
        for i in range(0, n):
            story.append(Paragraph(ltrStrings[i], styLTR))
            story.append(Paragraph(rtlStrings[i], styRTL))

        # a few additional scripts for testing.
        story.append(
            Paragraph('\xd9\x87\xd8\xb0\xd9\x87 \xd9\x81\xd9\x82\xd8\xb1\xd8\xa9'
                          ' \xd8\xb9\xd8\xa7\xd8\xaf\xd9\x8a\xd8\xa9. ', styRTL))
        story.append(
            Paragraph('\xd9\x87\xd8\xb0\xd9\x87 \xd8\xa7\xd9\x84\xd9\x81\xd9\x82\xd8\xb1\xd8\xa9'
                          ' \xd9\x84\xd8\xaf\xd9\x8a\xd9\x87\xd8\xa7 12'
                          ' \xd9\x86\xd9\x82\xd8\xb7\xd8\xa9 \xd9\x82\xd8\xa8\xd9\x84\xd9\x87\xd8\xa7'
                          ' \xd9\x88\xd8\xa8\xd8\xb9\xd8\xaf\xd9\x87\xd8\xa7. ', styRTL))
        story.append(
            Paragraph('<para spacebefore="12" spaceafter="12">'
                          '\xd9\x87\xd8\xb0\xd9\x87 \xd8\xa7\xd9\x84\xd9\x81\xd9\x82\xd8\xb1\xd8\xa9'
                          ' \xd9\x84\xd8\xaf\xd9\x8a\xd9\x87\xd8\xa7 12 \xd9\x86\xd9\x82\xd8\xb7\xd8\xa9'
                          ' \xd9\x82\xd8\xa8\xd9\x84\xd9\x87\xd8\xa7'
                          ' \xd9\x88\xd8\xa8\xd8\xb9\xd8\xaf\xd9\x87\xd8\xa7\xd8\x8c'
                          ' \xd9\x85\xd8\xad\xd8\xaf\xd8\xaf\xd8\xa9 \xd8\xa8\xd9\x80 XML.'
                          ' \xd8\xa5\xd9\x86\xd9\x87\xd8\xa7 \xd8\xaa\xd8\xb9\xd9\x85\xd9\x84'
                          ' \xd8\xa3\xd9\x8a\xd8\xb6\xd8\xa7! \xd9\x80.'
                          '</para',
                      styRTL))

        # TODO: add more RTL scripts to the test (Farsi, Hebrew, etc.)

        template = SimpleDocTemplate(outputfile('test_paragraphs_bidi.pdf'))
        template.build(story)

    def testRTLBullets(self):
        try:
            import mwlib.ext
        except ImportError:
            pass

        import os
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.platypus.paragraph import Paragraph
        from reportlab.platypus.flowables import Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase import ttfonts
        from reportlab.lib.fonts import addMapping
        from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT

        # register a font that supports most Unicode characters
        if 1:
            fontDir = 'ttf-dejavu'
            font_name = 'DejaVuSans'
            font_info = [(font_name, 0, 0, font_name),
                         (font_name, 1, 0, font_name + '-Bold'),
                         (font_name, 0, 1, font_name + '-Oblique'),
                         (font_name, 1, 1, font_name + '-BoldOblique'),
                         ]
            for font in font_info:
                fontName = font[3]
                try:
                    pdfmetrics.registerFont(ttfonts.TTFont(fontName,os.path.join('/usr/share/fonts/truetype/', fontDir, fontName + '.ttf')))
                except ttfonts.TTFError:
                    pdfmetrics.registerFont(ttfonts.TTFont(fontName,os.path.join(fontDir, fontName + '.ttf')))
                addMapping(*font)
        else:
            font_dir = '/usr/share/fonts/truetype/freefont/'
            font_name = 'FreeSerif'
            font_info = [(font_name, 0, 0, font_name),
                         (font_name, 1, 0, font_name + 'Bold'),
                         (font_name, 0, 1, font_name + 'Italic'),
                         (font_name, 1, 1, font_name + 'BoldItalic'),
                         ]
            for font in font_info:
                pdfmetrics.registerFont(ttfonts.TTFont(font[3], os.path.join(font_dir, '%s.ttf' % font[3])))
                addMapping(*font)
        # done registering fonts


        doc = SimpleDocTemplate(outputfile('test_rtl_bullets.pdf'),showBoundary=True)
        p_style = ParagraphStyle('default')
        p_style.leftIndent = 0
        p_style.rightIndent = 0

        list_styles=[ParagraphStyle('list%d' % n) for n in range(3)]
        all_styles = list_styles[:]
        all_styles.append(p_style)

        direction='rtl'

        for s in all_styles:
            s.fontSize = 15
            s.leading = s.fontSize*1.2
            s.fontName = font_name
            if direction=='rtl':
                s.wordWrap = 'RTL'
                s.alignment = TA_RIGHT
            else:
                s.alignment = TA_JUSTIFY

        indent_amount = 20

        for list_lvl, list_style in enumerate(list_styles):
            list_lvl += 1
            list_style.bulletIndent = indent_amount*(list_lvl-1)

            if direction=='rtl':
                list_style.rightIndent = indent_amount*list_lvl
            else:
                list_style.leftIndent = indent_amount*list_lvl


        elements =[]

        TEXTS=[
                '\xd7\xa9\xd7\xa8 \xd7\x94\xd7\x91\xd7\x99\xd7\x98\xd7\x97\xd7\x95\xd7\x9f, \xd7\x94\xd7\x95\xd7\x90 \xd7\x94\xd7\xa9\xd7\xa8 \xd7\x94\xd7\x90\xd7\x97\xd7\xa8\xd7\x90\xd7\x99 \xd7\xa2\xd7\x9c \xd7\x9e\xd7\xa9\xd7\xa8\xd7\x93 \xd7\x96\xd7\x94. \xd7\xaa\xd7\xa4\xd7\xa7\xd7\x99\xd7\x93 \xd7\x96\xd7\x94 \xd7\xa0\xd7\x97\xd7\xa9\xd7\x91 \xd7\x9c\xd7\x90\xd7\x97\xd7\x93 \xd7\x94\xd7\xaa\xd7\xa4\xd7\xa7\xd7\x99\xd7\x93\xd7\x99\xd7\x9d \xd7\x94\xd7\x91\xd7\x9b\xd7\x99\xd7\xa8\xd7\x99\xd7\x9d \xd7\x91\xd7\x9e\xd7\x9e\xd7\xa9\xd7\x9c\xd7\x94. \xd7\x9c\xd7\xa9\xd7\xa8 \xd7\x94\xd7\x91\xd7\x99\xd7\x98\xd7\x97\xd7\x95\xd7\x9f \xd7\x9e\xd7\xaa\xd7\x9e\xd7\xa0\xd7\x94 \xd7\x9c\xd7\xa8\xd7\x95\xd7\x91 \xd7\x92\xd7\x9d \xd7\xa1\xd7\x92\xd7\x9f \xd7\xa9\xd7\xa8.',
                '\xd7\xa9\xd7\xa8 \xd7\x94\xd7\x91\xd7\x99\xd7\x98\xd7\x97\xd7\x95\xd7\x9f, <b>\xd7\x94\xd7\x95\xd7\x90 \xd7\x94\xd7\xa9\xd7\xa8 \xd7\x94\xd7\x90\xd7\x97\xd7\xa8\xd7\x90\xd7\x99 \xd7\xa2\xd7\x9c \xd7\x9e\xd7\xa9\xd7\xa8\xd7\x93 \xd7\x96\xd7\x94.</b> \xd7\xaa\xd7\xa4\xd7\xa7\xd7\x99\xd7\x93 \xd7\x96\xd7\x94 <i>\xd7\xa0\xd7\x97\xd7\xa9\xd7\x91 \xd7\x9c\xd7\x90\xd7\x97\xd7\x93</i> \xd7\x94\xd7\xaa\xd7\xa4\xd7\xa7\xd7\x99\xd7\x93\xd7\x99\xd7\x9d <b><i>\xd7\x94\xd7\x91\xd7\x9b\xd7\x99\xd7\xa8\xd7\x99\xd7\x9d \xd7\x91\xd7\x9e\xd7\x9e\xd7\xa9\xd7\x9c\xd7\x94</b></i>. \xd7\x9c\xd7\xa9\xd7\xa8 \xd7\x94\xd7\x91\xd7\x99\xd7\x98\xd7\x97\xd7\x95\xd7\x9f \xd7\x9e\xd7\xaa\xd7\x9e\xd7\xa0\xd7\x94 \xd7\x9c\xd7\xa8\xd7\x95\xd7\x91 \xd7\x92\xd7\x9d \xd7\xa1\xd7\x92\xd7\x9f \xd7\xa9\xd7\xa8.',
                u'<bullet>\u2022</bullet>\u05e9\u05e8 \u05d4\u05d1\u05d9\u05d8\u05d7\u05d5\u05df, <b>\u05d4\u05d5\u05d0 \u05d4\u05e9\u05e8 \u05d4\u05d0\u05d7\u05e8\u05d0\u05d9 \u05e2\u05dc \u05de\u05e9\u05e8\u05d3 \u05d6\u05d4.</b> \u05ea\u05e4\u05e7\u05d9\u05d3 \u05d6\u05d4 <i>\u05e0\u05d7\u05e9\u05d1 \u05dc\u05d0\u05d7\u05d3</i> \u05d4\u05ea\u05e4\u05e7\u05d9\u05d3\u05d9\u05dd <b><i>\u05d4\u05d1\u05db\u05d9\u05e8\u05d9\u05dd \u05d1\u05de\u05de\u05e9\u05dc\u05d4</b></i>. \u05dc\u05e9\u05e8\u05d4\u05d1\u05d9\u05d8\u05d7\u05d5\u05df \u05de\u05ea\u05de\u05e0\u05d4 \u05dc\u05e8\u05d5\u05d1 \u05d2\u05dd \u05e1\u05d2\u05df \u05e9\u05e8.',
                ]

        # simple text in a paragraph
        # working with patch from Hosam Aly
        p = Paragraph(TEXTS[0], p_style)
        elements.append(p)

        elements.append(Spacer(0, 40))

        # uses intra paragraph markup -> style text
        p = Paragraph(TEXTS[1], p_style)
        elements.append(p)
        elements.append(Spacer(0, 40))

        # list item (just a paragraph with a leading <bullet> element
        for list_style in list_styles:
            p = Paragraph(TEXTS[2], list_style)
            elements.append(p)

        doc.build(elements)

def makeSuite():
    return makeSuiteForClasses(ParagraphTestCase)


#noruntests
if __name__ == "__main__":
    unittest.TextTestRunner().run(makeSuite())
    printLocation()
