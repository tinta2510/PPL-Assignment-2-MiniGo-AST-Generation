import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase): 
    # Test CHARACTER SET
    def test_101(self):
        self.assertTrue(TestLexer.checkLexeme(""" // /* 
                                       */""", "*,/,<EOF>", 101))
        
    def test_102(self):
        self.assertTrue(TestLexer.checkLexeme(
"""abc
""","abc,;,<EOF>", 102))
    
    def test_103(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme("""/* abc */ var""","""var,<EOF>""",103))
        
    def test_104(self):
        """test multi comment"""
        self.assertTrue(TestLexer.checkLexeme("""/* comment */ func ()""","""func,(,),<EOF>""",104))
        
    def test_105(self):
        """test nested comment"""
        self.assertTrue(TestLexer.checkLexeme("""/* /* comment */ */ abc""","""abc,<EOF>""",105))
        
    def test_106(self):
        """test nested comment"""
        self.assertTrue(TestLexer.checkLexeme("""/* /* comment */ */ abc /* comment2 */""","""abc,<EOF>""",106))
        
    def test_107(self):
        """test nested comment"""
        self.assertTrue(TestLexer.checkLexeme("""/* /* comment */ comment_content /* comment2 */ */ abc""","""abc,<EOF>""",107))
        
    def test_108(self):
        """test nested comment"""
        self.assertTrue(TestLexer.checkLexeme(
            """/* comment \n
                  comment2 \n
                  comment3 \n
                */  abc // comment3""","""abc,<EOF>""",108))
    
    def test_109(self):
        """test nested comment"""
        self.assertTrue(TestLexer.checkLexeme(
            """/* a /* b /* c */ b */ a */\t""","""<EOF>""",109))
        
    def test_110(self):
        """test nested comment"""
        self.assertTrue(TestLexer.checkLexeme(
            """/* a //////* b /* c */ b */ a */\t""","""<EOF>""",110))
    
    def test_111(self):
        self.assertTrue(TestLexer.checkLexeme("""if /* */ /* */""", "if,<EOF>", 111))
        
    def test_112(self):
        self.assertTrue(TestLexer.checkLexeme("// TaTrungTin","<EOF>", 112))   
        
    def test_113(self):
        self.assertTrue(TestLexer.checkLexeme("/* cmt */ content","content,<EOF>", 113))
    
    def test_114(self):
        """Test nested comment and newline"""
        self.assertTrue(TestLexer.checkLexeme("""
        /* test
        */ a /* */
""","a,;,<EOF>", 114))
    
    def test_115(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("abc","abc,<EOF>",115))
        
    def test_116(self):
        self.assertTrue(TestLexer.checkLexeme("_TaTrungTin","_TaTrungTin,<EOF>", 116))
        
    def test_117(self):
        """test keyword var"""
        self.assertTrue(TestLexer.checkLexeme("var abc int ;","var,abc,int,;,<EOF>",117))
        
    def test_118(self):
        """test keyword func"""
        self.assertTrue(TestLexer.checkLexeme("""func abc ( ) ""","""func,abc,(,),<EOF>""",118))
        
    def test_119(self):
        self.assertTrue(TestLexer.checkLexeme("if then else", "if,then,else,<EOF>", 119))
        
    def test_120(self):
        self.assertTrue(TestLexer.checkLexeme("+","+,<EOF>", 120))
    
    def test_121(self):
        self.assertTrue(TestLexer.checkLexeme("[]","[,],<EOF>", 121))
        
    def test_122(self):
        self.assertTrue(TestLexer.checkLexeme("12","12,<EOF>", 122))
        
    def test_123(self):
        self.assertTrue(TestLexer.checkLexeme("0x11","0x11,<EOF>", 123))
    
    def test_124(self):
        self.assertTrue(TestLexer.checkLexeme("0452.", "0452.,<EOF>", 124))
        
    def test_125(self):
        self.assertTrue(TestLexer.checkLexeme("0X1234", "0X1234,<EOF>", 125))
    
    def test_126(self):
        self.assertTrue(TestLexer.checkLexeme("0b1010", "0b1010,<EOF>", 126))
    
    def test_127(self):
        self.assertTrue(TestLexer.checkLexeme("0o1234", "0o1234,<EOF>", 127))
    
    def test_128(self):
        self.assertTrue(TestLexer.checkLexeme("0O1234", "0O1234,<EOF>", 128))
    
    def test_129(self):  
        self.assertTrue(TestLexer.checkLexeme("0B1001", "0B1001,<EOF>", 129))
        
    def test_130(self):
        """INT_LIT"""
        self.assertTrue(TestLexer.checkLexeme("-12", "-,12,<EOF>", 130))
        
    ## Test FLOAT LITERALS
    def test_131(self):
        self.assertTrue(TestLexer.checkLexeme("12.e-8","12.e-8,<EOF>", 131))
    
    def test_132(self):
        self.assertTrue(TestLexer.checkLexeme("09.e-002","09.e-002,<EOF>", 132))

    def test_133(self):
        """FLOAT_LIT"""
        self.assertTrue(TestLexer.checkLexeme("010.010e-020", "010.010e-020,<EOF>", 133))
        
    ## Test STRING LITERALS
    def test_134(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "abc" """,""""abc",<EOF>""",134))
    
    def test_135(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "abc\\ndef" """,""""abc\\ndef",<EOF>""",135))
        
    def test_136(self):
        self.assertTrue(TestLexer.checkLexeme(""" "TaTrungTin \\r" ""","\"TaTrungTin \\r\",<EOF>", 136))  
        
    ## Test BOOLEAN LITERALS
    
    ## Test NIL LITERALS
    
    # Test ERROR
    ## Test ERROR TOKEN
    def test_137(self):
        self.assertTrue(TestLexer.checkLexeme("ab?sVN","ab,ErrorToken ?",137))
        
    def test_138(self):
        self.assertTrue(TestLexer.checkLexeme("abc?xyz","abc,ErrorToken ?", 138))
        
    def test_139(self):
        self.assertTrue(TestLexer.checkLexeme("^","ErrorToken ^", 139))
        
    def test_140(self):
        self.assertTrue(TestLexer.checkLexeme("0b1234", "0b1,234,<EOF>", 140))
        
    ## Test UNCLOSED STRING
    def test_141(self):
        self.assertTrue(TestLexer.checkLexeme(""" "abc\ndef" ""","Unclosed string: \"abc", 141))
        
    def test_142(self):
        self.assertTrue(TestLexer.checkLexeme(
""""abc
""","Unclosed string: \"abc", 142))
        
    def test_143(self):
        self.assertTrue(TestLexer.checkLexeme(""" "TaTrungTin\n" ""","Unclosed string: \"TaTrungTin", 143))
        
    ## Test ILLEGAL ESCAPE
    def test_144(self):
        self.assertTrue(TestLexer.checkLexeme(""" "TaTrungTin\\f" ""","Illegal escape in string: \"TaTrungTin\\f", 144))
        
    def test_145(self):
        """ILLEGAL_ESCAPE"""
        self.assertTrue(TestLexer.checkLexeme(""" "abcd\ysafda" ""","Illegal escape in string: \"abcd\\y", 145))
        
    # Additional random test cases
    def test_146(self):
        """Test hexadecimal integer literals"""
        self.assertTrue(TestLexer.checkLexeme("0x1A 0XFFTIN 0x0", "0x1A,0XFF,TIN,0x0,<EOF>", 146))

    def test_147(self):
        """Test binary integer literals"""
        self.assertTrue(TestLexer.checkLexeme("0b101 0B1101 0b0", "0b101,0B1101,0b0,<EOF>", 147))

    def test_148(self):
        """Test octal integer literals"""
        self.assertTrue(TestLexer.checkLexeme("0o12 0O77 0o0", "0o12,0O77,0o0,<EOF>", 148))

    def test_149(self):
        """Test valid floating-point literals"""
        self.assertTrue(TestLexer.checkLexeme("3.14 0. 2.0e10 1.5E-3", "3.14,0.,2.0e10,1.5E-3,<EOF>", 149))

    def test_150(self):
        """Test edge cases for floating-point literals"""
        self.assertTrue(TestLexer.checkLexeme("10.0.5", "10.0,.,5,<EOF>", 150))

    def test_151(self):
        """Test floating literals missing integer part"""
        self.assertTrue(TestLexer.checkLexeme(".5e3", ".,5,e3,<EOF>", 151))

    def test_152(self):
        """Test valid string literals"""
        self.assertTrue(TestLexer.checkLexeme('"hello" "world" "MiniGo"', '"hello","world","MiniGo",<EOF>', 152))

    def test_153(self):
        """Test valid string escape sequences"""
        self.assertTrue(TestLexer.checkLexeme('"Hello\\nWorld" "Tab\\tTest" "Quote\\\"Example"', '"Hello\\nWorld","Tab\\tTest","Quote\\\"Example",<EOF>', 153))

    def test_154(self):
        """Test unclosed string"""
        self.assertTrue(TestLexer.checkLexeme('"Hello', 'Unclosed string: "Hello', 154))

    def test_155(self):
        """Test illegal escape sequences in strings"""
        self.assertTrue(TestLexer.checkLexeme('"Illegal\\qEscape"', 'Illegal escape in string: "Illegal\\q', 155))

    def test_156(self):
        """Test boolean literals"""
        self.assertTrue(TestLexer.checkLexeme("true false", "true,false,<EOF>", 156))

    def test_157(self):
        """Test nil literal"""
        self.assertTrue(TestLexer.checkLexeme("nil", "nil,<EOF>", 157))

    def test_158(self):
        """Test single-line comment"""
        self.assertTrue(TestLexer.checkLexeme("// This is a comment\nx := 10;", "x,:=,10,;,<EOF>", 158))

    def test_159(self):
        """Test multi-line comments"""
        self.assertTrue(TestLexer.checkLexeme("/* This is a\n multi-line\n comment */ x := 10;", "x,:=,10,;,<EOF>", 159))

    def test_160(self):
        """Test nested multi-line comments"""
        self.assertTrue(TestLexer.checkLexeme("/* Outer /* Inner */ Comment */ x := 5;", "x,:=,5,;,<EOF>", 160))

    def test_161(self):
        """Test valid identifiers"""
        self.assertTrue(TestLexer.checkLexeme("myVar _myVar x123 my_variable", "myVar,_myVar,x123,my_variable,<EOF>", 161))

    def test_162(self):
        """Test invalid identifiers starting with numbers"""
        self.assertTrue(TestLexer.checkLexeme("123var", "123,var,<EOF>", 162))

    def test_163(self):
        """Test identifier containing a keyword"""
        self.assertTrue(TestLexer.checkLexeme("returnValue", "returnValue,<EOF>", 163))
        
    def test_164(self):
        """Test arithmetic operators"""
        self.assertTrue(TestLexer.checkLexeme("+ - * / %", "+,-,*,/,%,<EOF>", 164))

    def test_165(self):
        """Test relational operators"""
        self.assertTrue(TestLexer.checkLexeme("== != < <= > >=", "==,!=,<,<=,>,>=,<EOF>", 165))

    def test_166(self):
        """Test logical operators"""
        self.assertTrue(TestLexer.checkLexeme("&& || !", "&&,||,!,<EOF>", 166))

    def test_167(self):
        """Test assignment operators"""
        self.assertTrue(TestLexer.checkLexeme(":= += -= *= /= %=", ":=,+=,-=,*=,/=,%=,<EOF>", 167))

    def test_168(self):
        """Test separators"""
        self.assertTrue(TestLexer.checkLexeme("( ) { } [ ] , ;", "(,),{,},[,],,,;,<EOF>", 168))


    def test_169(self):
        """Test identifier with illegal characters"""
        self.assertTrue(TestLexer.checkLexeme("var x$ = 5;", "var,x,ErrorToken $", 169))

    def test_170(self):
        """Test identifier containing only underscores"""
        self.assertTrue(TestLexer.checkLexeme("_ _var __main__", "_,_var,__main__,<EOF>", 170))

    def test_171(self):
        """Test unterminated multi-line comment"""
        self.assertTrue(TestLexer.checkLexeme("/* This is a comment", "/,*,This,is,a,comment,<EOF>", 171))

    def test_172(self):
        """Test nested multi-line comment with unclosed part"""
        self.assertTrue(TestLexer.checkLexeme("/* Nested comment */", "<EOF>", 172))

    def test_173(self):
        """Test floating-point number with multiple dots"""
        self.assertTrue(TestLexer.checkLexeme("10.5", "10.5,<EOF>", 173))

    def test_174(self):
        """Test floating-point number with invalid exponent"""
        self.assertTrue(TestLexer.checkLexeme("1.2e", "1.2,e,<EOF>", 174))

    def test_175(self):
        """Test binary number with invalid digits"""
        self.assertTrue(TestLexer.checkLexeme("0b102", "0b10,2,<EOF>", 175))

    def test_176(self):
        """Test octal number with invalid digits"""
        self.assertTrue(TestLexer.checkLexeme("0o787", "0o7,87,<EOF>", 176))
        
    def test_177(self):
        """Test hexadecimal number with invalid characters"""
        self.assertTrue(TestLexer.checkLexeme("0xG1", "0,xG1,<EOF>", 177))

    def test_178(self):
        """Test unterminated string"""
        self.assertTrue(TestLexer.checkLexeme('"This is an unterminated string', 'Unclosed string: "This is an unterminated string', 178))

    def test_179(self):
        """Test illegal escape sequence in string"""
        self.assertTrue(TestLexer.checkLexeme('"Illegal\\yEscape"', 'Illegal escape in string: "Illegal\\y', 179))

    def test_180(self):
        """Test empty character literal"""
        self.assertTrue(TestLexer.checkLexeme("''", "ErrorToken '", 180))

    def test_181(self):
        """Test nested escape sequences in strings"""
        self.assertTrue(TestLexer.checkLexeme('"Nested \\\\ escape"', '"Nested \\\\ escape",<EOF>', 181))

    def test_182(self):
        """Test large integer"""
        self.assertTrue(TestLexer.checkLexeme("999999999999999999999999999999999", "999999999999999999999999999999999,<EOF>", 182))

    def test_183(self):
        self.assertTrue(TestLexer.checkLexeme("abc_d1","abc_d1,<EOF>", 183))

    def test_184(self):
        """Test multiple unclosed strings"""
        self.assertTrue(TestLexer.checkLexeme('"string1 "string2', '"string1 ",string2,<EOF>', 184))

    def test_185(self):
        """Test mixed valid and invalid tokens"""
        self.assertTrue(TestLexer.checkLexeme("@", "ErrorToken @", 185))
        
    def test_186(self):
        """Test identifier starting with a keyword"""
        self.assertTrue(TestLexer.checkLexeme("ifCondition elseStatement", "ifCondition,elseStatement,<EOF>", 186))

    def test_187(self):
        """Test mixed valid and invalid identifiers"""
        self.assertTrue(TestLexer.checkLexeme("_validIdentifier 123invalid", "_validIdentifier,123,invalid,<EOF>", 187))

    def test_188(self):
        """Test a valid function declaration"""
        self.assertTrue(TestLexer.checkLexeme("func foo() { return 10; }", "func,foo,(,),{,return,10,;,},<EOF>", 188))

    def test_189(self):
        """Test a function call with arguments"""
        self.assertTrue(TestLexer.checkLexeme("print(42, 'hello')", "print,(,42,,,ErrorToken '", 189))

    def test_190(self):
        """Test invalid escape sequence in string"""
        self.assertTrue(TestLexer.checkLexeme('"Hello\\zWorld"', 'Illegal escape in string: "Hello\\z', 190))

    def test_191(self):
        """Test unterminated string with an escape sequence"""
        self.assertTrue(TestLexer.checkLexeme('"Hello\\n', 'Unclosed string: "Hello\\n', 191))

    def test_192(self):
        """Test string containing valid escape sequences"""
        self.assertTrue(TestLexer.checkLexeme('"Line1\\nLine2\\tTab"', '"Line1\\nLine2\\tTab",<EOF>', 192))

    def test_193(self):
        """Test large floating-point number"""
        self.assertTrue(TestLexer.checkLexeme("1.23456789e+308", "1.23456789e+308,<EOF>", 193))

    def test_194(self):
        """Test mixed arithmetic and relational operators"""
        self.assertTrue(TestLexer.checkLexeme("a + b * c / d == e", "a,+,b,*,c,/,d,==,e,<EOF>", 194))

    def test_195(self):
        """Test unexpected character"""
        self.assertTrue(TestLexer.checkLexeme("var x = 5 #", "var,x,=,5,ErrorToken #", 195))

    def test_196(self):
        """Test valid struct declaration"""
        self.assertTrue(TestLexer.checkLexeme("type Person struct { name string; age int; }", 
                                            "type,Person,struct,{,name,string,;,age,int,;,},<EOF>", 196))

    def test_197(self):
        """Test invalid number format"""
        self.assertTrue(TestLexer.checkLexeme("0b120", "0b1,20,<EOF>", 197))

    def test_198(self):
        """Test deeply nested parentheses"""
        self.assertTrue(TestLexer.checkLexeme("((a + b)", "(,(,a,+,b,),<EOF>", 198))

    def test_199(self):
        """Test valid boolean expressions"""
        self.assertTrue(TestLexer.checkLexeme("true && false || !true", "true,&&,false,||,!,true,<EOF>", 199))

    def test_200(self):
        """Test valid array declaration"""
        self.assertTrue(TestLexer.checkLexeme("var arr [5]int;", "var,arr,[,5,],int,;,<EOF>", 200))
