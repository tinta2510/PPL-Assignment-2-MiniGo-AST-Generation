import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_201(self):
        """Literal int"""
        input = "const max int = 0xA; var min float = 0.5;"
        expect = "Error on line 1 col 11: int"
        self.assertTrue(TestParser.checkParser(input, expect, 201))

    def test_202(self):
        """Literal boolean true"""
        input = "var ABC = [1+1]int{2};"
        expect = "Error on line 1 col 13: +"
        self.assertTrue(TestParser.checkParser(input, expect, 202))
    
    def test_203(self):
        """Literal boolean false"""
        input = "var ABC [1-1][a]int;"
        expect = "Error on line 1 col 11: -"
        self.assertTrue(TestParser.checkParser(input, expect, 203))
        
    def test_204(self):
        """Literal nil"""
        input = "var flag bool = a || b && c;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 204))
        
    def test_205(self):
        """Literal float"""
        input = "const ABC = ca.foo(132) + b.c[2];"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 205))
        
    def test_206(self):
        """Literal array"""
        input = "const ABC = [5][0]string{1, \"string\"};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input , expect, 206))

    def test_207(self):
        """Literal array with nested element"""
        input = "const ABC = [5][5]string{1, \"string\", {1.21, \"content\"}, {3}};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input , expect, 207))
        
    def test_208(self):
        """Literal array with index as constant"""
        input = """const ABC = [ID1][ID2]int{{1, \"string\", {21}}, {1.21, \"content\"}};"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input , expect, 208))
        
    def test_209(self):
        """Literal array with composite element type"""
        input = "const ABC = [ID1][ID2]ID3{1, \"string\", {1.21, \"content\"}};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input , expect, 209))
        
    def test_210(self):
        """Literal array with non-integer index"""
        input = "const ABC = [10.]ID{2, 3};"
        expect = "Error on line 1 col 14: 10."
        self.assertTrue(TestParser.checkParser(input, expect, 210))

    def test_211(self):
        """Literal array with boolean index"""
        input = "const ABC = [true]ID{2, 3};"
        expect = "Error on line 1 col 14: true"
        self.assertTrue(TestParser.checkParser(input, expect, 211))

    def test_212(self):
        """Literal array with invalid index expression"""
        input = """const a = [1]int{1+1}"""
        expect = "Error on line 1 col 19: +"
        self.assertTrue(TestParser.checkParser(input , expect, 212))

    def test_213(self):
        """Literal array with index as expression"""
        input = "const ABC = [1+2+3]ID3{1, \"string\", {1.21, \"content\"}};"
        expect = "Error on line 1 col 15: +"
        self.assertTrue(TestParser.checkParser(input , expect, 213))

    def test_214(self):
        """Literal struct"""
        input = "const ABC = Person{name: \"Alice\", age: 30};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 214))
    
    def test_215(self):
        """Literal struct missing comma separator"""
        input = "const ABC = ABC{name: \"content\" age: 21};"
        expect = "Error on line 1 col 33: age"
        self.assertTrue(TestParser.checkParser(input, expect, 215))

    def test_216(self):
        """Literal struct with trailing comma"""
        input = "const ABC = ABC{name: \"content\", age: 21, school: \"XYZ\",};"
        expect = "Error on line 1 col 57: }"
        self.assertTrue(TestParser.checkParser(input, expect, 216))

    def test_217(self):
        input = "const ABC = funn().field;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 217))

    def test_218(self):
        """Literal struct with missing closing brace"""
        input = "const ABC = ABC{name: \"content\";"
        expect = "Error on line 1 col 32: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 218))

    def test_219(self):
        """Literal struct with empty fields"""
        input = "const ABC = ABC{};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 219))

    def test_220(self):
        """Function declaration"""
        input = """
            func ABC(x int, y int) int {return 10;}
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 220))

    def test_221(self):
        """Method declaration"""
        input = """
            func (c Calculator) ABC(x int) int {return;}
            func (c Calculator) ABC() ID {return;};
            func (c Calculator) ABC(x int, y [2]ABC) {return;}
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 221))

    def test_222(self):
        """If-else statement"""
        input = """    
            func ABC() {
                if (x > 10) {return;} 
                if (x > 10) {
                  return;
                } else if (x == 10) {
                    var z str;
                } else {
                    var z ID;
                }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 222))

    def test_223(self):
        """For-loop statement"""
        input = """    
            func ABC() {
                for i < 10 {return;}
                for i := 0; i < 10; i += 1 {return;}
                for index, value := range array {return;}
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input ,expect, 223))

    def test_224(self):
        """invalid function decl"""
        input = """func main() {
                    func foo() {};
                };"""
        expect = "Error on line 2 col 21: func"
        self.assertTrue(TestParser.checkParser(input, expect, 224))

    def test_225(self):
        """Literal struct with missing field expression"""
        input = "const ABC = ABC{name: \"tin\"};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 225))
        
    def test_226(self):
        """Literal struct with missing field name"""
        input = "const ABC = [1]arr{\"content\"};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 226))
        
    def test_227(self):
        self.assertTrue(TestParser.checkParser("""
        type Name interface {
            func (p Person) Greet() string {
                return "Tin, " + p.name
            }                                        
        }      
        ""","Error on line 3 col 13: func", 227))
            
    def test_228(self):
        """For range statement with non-scalar index"""
        input = """func loop() {
            for arr[1], value := range arr {
                arr := value;
            }
        };"""
        expect = "Error on line 2 col 23: ,"
        self.assertTrue(TestParser.checkParser(input, expect, 228))
        
    def test_229(self):
        """unsupported operators"""
        input = "const ABC = 2 + 2 - 2 ** 2 // 2 % 2;"
        expect = "Error on line 1 col 24: *"
        self.assertTrue(TestParser.checkParser(input, expect, 229))
        
    def test_230(self):
        """Relational operators"""
        input = "const ABC = 2 == 2 != 2 > 2 < 2 >= 2 <= 2;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 230))
        
    def test_231(self):
        """Boolean expressions"""
        input = "const ABC = !3 && 3 || 3 && !!3 ;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 231))
        
    def test_232(self):
        """Access array element"""
        input = "const ABC = a[3];"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 232))
        
    def test_233(self):
        input = """
                func (a Function) DoSomething() {
                    s.fun() += 2;
                }"""
        expect = "Error on line 3 col 29: +="
        self.assertTrue(TestParser.checkParser(input,expect, 233))
        
    def test_234(self):
        """Access array with expression index"""
        input = "var z ABC = a[2][3][a + 2 / d && true];"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 234))
        
    def test_235(self):
        """Invalid array access using comma instead of brackets"""
        input = "var z ABC = a[2, 3];"
        expect = "Error on line 1 col 16: ,"
        self.assertTrue(TestParser.checkParser(input, expect, 235))
        
    def test_236(self):
        """Access struct field"""
        input = "var z ABC = content.name;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 236))
        
    def test_237(self):
        """Access nested struct fields"""
        input = "var z ABC = content.name.first_name;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 237))
        
    def test_238(self):
        """Invalid struct field access with double dot"""
        input = "var z ABC = content.name;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 238))
        
    def test_239(self):
        """Invalid struct field access with numeric field name"""
        input = "var z ABC = recv.meth();"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 239))
           
    def test_240(self):
        """Function call without arguments"""
        input = "var z ABC = add();"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 240))
        
    def test_241(self):
        """Function call with expression arguments"""
        input = "var z ABC = add(1+3, 2/4, a[3][2]);"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 241))
        
    def test_242(self):
        """Invalid function call missing comma separator"""
        input = "var z ABC = add(3, a);"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 242))
        
    def test_243(self):
        """Function call with arguments"""
        input = "var z variable_name = doSt(a, c, 2);"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 243))
        
    def test_244(self):
        """Method call"""
        input = "var z ABC = add(3, a);"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 244))
    
    def test_245(self):
        """Method call without arguments"""
        input = "var z ABC = add();"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 245))
         
    def test_246(self):
        """Complex expression with logical and arithmetic operators"""
        input = "const ABC = 1 || 2 && c + 3 / 2 - -1;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 246))

    def test_247(self):
        """Expression involving array indexing and function calls"""
        input = "const ABC = 1[2] + foo()[2] + ID[2].b.b;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test_248(self):
        """Function call inside expression"""
        input = "const ABC = content.foo(132) + b.c[2];"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test_249(self):
        """Method call in nested struct"""
        input = "const ABC = a.a.foo();"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 249))
        
    def test_250(self):
        """Expression involving nested struct initialization"""
        input = "var z ABC = ID {a: 2, b: 2 + 2 + ID {a: 2}};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test_251(self):
        """Expression with multiple relational comparisons"""
        input = "var z ABC = a >= 2 <= \"string\" > a[2][3] < ID{A: 2} >= [2]S{2};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 251))
        
    def test_252(self):
        """Method call with nested struct and array access"""
        input = "var z ABC = a.a.a[2].foo();"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 252))
    
    def test_253(self):
        """Function call with trailing comma"""
        input = "var z ABC = a.a.a[2].c[2].foo(1);"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 253))
        
    def test_254(self):
        """Function call with nested struct initialization"""
        input = "var z ABC = !a.a.a[2].c[2].foo(1, ID{A: 2});"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 254))
        
    def test_255(self):
        """Complex struct initialization"""
        input = "var z ABC = ABC {name: NAME{first_name: \"abc\", last_name: \"content\"}, age: a[2][3]};"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 255))
    
    def test_256(self):
        """Variable declaration"""
        input = """
            var x int = foo() + 3 / 4;
            var y = "Hello" / 4;
            var z str;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 256))

    def test_257(self):
        """Constant declaration"""
        input = "const ABC = a.b() + 2;"
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 257))
        
    def test_258(self):
        """Function declaration with return statement"""
        input = """
            func (c c) Add(x, c int) { return; }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 258))
    
    def test_259(self):
        """Constant declaration missing semicolon"""
        input = "const ABC = a.b() + 2"
        expect = "Error on line 1 col 22: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 259))
        
    def test_260(self):
        """Invalid variable declaration missing type"""
        input = "var y;"
        expect = "Error on line 1 col 6: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 260))
    
    def test_261(self):
        """Invalid variable declaration using reserved keyword"""
        input = "var float;"
        expect = "Error on line 1 col 5: float"
        self.assertTrue(TestParser.checkParser(input, expect, 261))

    def test_262(self):
        input = """func foo () {
            continue;
        };"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 262))
    
    def test_263(self):
        """Invalid function declaration missing closing parenthesis"""
        input = """func main({};"""
        expect = "Error on line 1 col 11: {"
        self.assertTrue(TestParser.checkParser(input, expect, 263))
        
    def test_264(self):
        """Function declaration with parameters and return type"""
        input = """
            func ABC(x, y int) {return 10;}                           
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 264))

    def test_265(self):
        """Method declaration inside struct"""
        input = """
            func (c Calculator) ABC(x int) int {return;}  
            func (c Calculator) ABC() ID {return;};
            func (c Calculator) ABC(x int, y [2]ABC) {return;}                                                      
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 265))

    def test_266(self):
        """Struct declaration"""
        input = """
            type ABC struct {
                field1 string;
                field2 [1][3]ABC
            }                                                                     
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 266))

    def test_267(self):
        """Variable assignment inside function"""
        input = """    
            func ABC() {
                x  := foo() + 3 / 4;
                x.c[2][4] := 1 + 2;                       
            }                                       
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 267))
        
    def test_268(self):
        """Interface declaration"""
        input = """
            type Calculator interface {
                /* This is a comment */
                Add(x, y int) int;
                Subtract(a, b float, c int) [3]ID;
                Reset();
                SayHello(name string);
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 268))

    def test_269(self):
        """If statement"""
        input = """    
            func ABC() {
                if (x > 10) {return;} 
                if (x > 10) {
                  return;
                } else if (x == 10) {
                    var z str;
                } else {
                    var z ID;
                }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 269))

    def test_270(self):
        """For loops with different variations"""
        input = """    
            func ABC() {
                for i < 10 {return;}
                for i := 0; i < 10; i += 1 {return;}
                for index, value := range array {return;}
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 270))

    def test_271(self):
        """Break, continue, return, and function calls in loops"""
        input = """    
            func ABC() {                           
                for i < 10 {break;}
                break;
                continue;
                return 1;
                return;
                foo(2 + x, 4 / y); m.goo();                        
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 271))

    def test_272(self):
        """Invalid function declaration with missing parameter type"""
        input = """    
            func Add(a) [2]id {diem := 10;}
        """
        expect = "Error on line 2 col 23: )"
        self.assertTrue(TestParser.checkParser(input, expect, 272))     

    def test_273(self):
        """Valid interface declaration with method signatures"""
        input = """
            type Calculator interface {
                Add(x, y [2]ID) [2]int;
                Subtract(a, b float, c, e int);
                Reset();
                SayHello(name string);
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 273))
        
    def test_274(self):
        """Valid struct and interface declarations"""
        input = """
            type Calculator interface { Subtract(a int); }
            type Person struct { a int; }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 274))
        
    def test_275(self):
        """Valid function declaration with struct and variable declarations"""
        input = """
            func Add(x      , y int) int  {return;};
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 275))

    def test_276(self):
        """Method declaration with invalid receiver type"""
        input = """
            func (c C) Add(x int) {/*cmt*/diem := 10;}
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 276))
    
    def test_277(self):
        """Function with missing return type"""
        input = """    
            func (c c) Add(x, c int) {
                if (x > 10) {break;}
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 277))
        
    def test_278(self):
        """Constant declaration followed by function"""
        input = """    
            const a = 2 func (c c) Add(x int) {continue;}
        """
        expect = "Error on line 2 col 25: func"
        self.assertTrue(TestParser.checkParser(input, expect, 278))
        
    def test_279(self):
        """Variable and constant declarations inside function"""
        input = """
            func Add() {
                const a = a[2].b;
                var a = a[2].b; 
                var a = "s";           
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 279))
        
    def test_280(self):
        """Assignment statements with arithmetic operations"""
        input ="""
            func Add() {
                a += 2;
                a -= a[2].b();
                a /= 2;
                a *= 2;
                a %= 2;         
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 280))
        
    def test_281(self):
        """Invalid assignment to function call"""
        input = """
            func Add() {
                a.foo() += 2;
            }
        """
        expect = "Error on line 3 col 25: +="
        self.assertTrue(TestParser.checkParser(input, expect, 281))
    
    def test_282(self):
        """Invalid assignment to expression"""
        input = """
            func Add() {
                a += 2;     
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 282))
    
    def test_283(self):
        """Assignment with complex expression"""
        input = """
            func Add() {
               a[2+3&&2] += foo().b[2];       
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 283))
        
    def test_284(self):
        """Invalid if statement with missing condition"""
        input = """
            func Add() {
                if (x.foo().b[2]) {
                    if (){}
                }
            }
        """
        expect = "Error on line 4 col 25: )"
        self.assertTrue(TestParser.checkParser(input, expect, 284))
        
    def test_285(self):
        """Valid for loop"""
        input = """
            func Add() {
                for var i = 0; i < 10; i += 1 {
                    break;
                }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 285))
        
    def test_286(self):
        """Invalid for loop declaration"""
        input = """
            func Add() {
                for var i [2]int = 0; foo().a.b(); i[3] := 1 {
                    break;
                }
            }
        """
        expect = "Error on line 3 col 53: ["
        self.assertTrue(TestParser.checkParser(input, expect, 286))
        
    def test_287(self):
        """For loop iterating over array"""
        input = """
            func Add() {
                for index, value := range arr[2] {
                    break;
                }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 287))
    
    def test_288(self):
        """For loop iterating over integer"""
        input = """
            func Add() {
                for index, value := range 23 {
                    break;
                }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 288))
    
    def test_289(self):
        """Invalid function with unsuitable newline"""
        input ="""
            func (p Person) Greet() string {
                for i := 0
                    i < 10
                    i += 1 {
                    return
                }
                for i := 0
                    i < 10
                    i += 1 
                {
                    return
                }
            }
        """
        expect = "Error on line 10 col 29: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 289)) 
    
    def test_290(self):
        """Function call within array and struct access"""
        input = """
            func Add() {
                a[2][3].foo(2 + 3, a {a:2});
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 290))
    
    def test_291(self):
        """Invalid return statement with expression access"""
        input = """
            func Add() {
                return -A.c;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 291))
    
    def test_292(self):
        """Function with return type but missing return value"""
        input = """
            func Add(x int, y int) int {
                return;
            };"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 292))

    def test_293(self):
        """Valid function return"""
        input = """
            func Add(x int, y int) int {
                return x + y;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 293))

    def test_294(self):
        """Valid struct with method"""
        input = """
            type Calculator struct {
                value int;
            }
            func (c Calculator) Add(x int) int {
                return c.value + x;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 294))

    def test_295(self):
        """Struct initialization with missing field name"""
        input = """
            var p ABC = ABC{name: "content", age: 21 };
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 295))

    def test_296(self):
        """Struct initialization with correct field names"""
        input = """
            var p ABC = ABC{name: "content", age: 21};
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 296))

    def test_297(self):
        """Multiple function declarations"""
        input = """
            func Func1() {
                a := 10
            }
            func Func2() {
                b := 9.5e0
            }
            func Func3() {
                c := 10;}
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 297))

    def test_298(self):
        """Method call with missing parentheses"""
        input = """
            func Add() {
                obj.method;
            }
        """
        expect = "Error on line 3 col 27: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 298))

    def test_299(self):
        """Correct function call"""
        input = """
            func Add() {
                obj.method();
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 299))

    def test_300(self):
        """Struct with duplicate field name"""
        input = """
            type ABC struct {
                field1 int;
                field1 string;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 300))