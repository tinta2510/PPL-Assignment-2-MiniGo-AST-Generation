import unittest
from TestUtils import TestAST
from AST import *
        
class ASTGenSuite(unittest.TestCase):
    def test_300(self):
        """Simple program: int main() {} """
        input = """var a int;"""
        expect = str(Program([VarDecl("a",IntType(),None)]))
        # expect = str(Program([FuncDecl("main",[],VoidType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def test_301(self):
        """More complex program"""
        input = """var x int ;"""
        expect = str(Program([VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
    def test_302(self):
        """More complex program"""
        input = """func main () {}; var x int ;"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([])),VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,302))
   
    def test_303(self):
        input = """
            func main(){
                a["s"][foo()] := a[2][2][3];
                a[2] := a[3][4];
                b.c.a[2] := b.c.a[2];
            } 
"""
        expect = Program([FuncDecl("main",[],VoidType(),Block([
            Assign(ArrayCell(Id("a"),[StringLiteral("\"s\""),FuncCall("foo",[])]),ArrayCell(Id("a"),[IntLiteral(2),IntLiteral(2),IntLiteral(3)])),
            Assign(ArrayCell(Id("a"),[IntLiteral(2)]),ArrayCell(Id("a"),[IntLiteral(3),IntLiteral(4)])),
            Assign(ArrayCell(FieldAccess(FieldAccess(Id("b"),"c"),"a"),[IntLiteral(2)]),ArrayCell(FieldAccess(FieldAccess(Id("b"),"c"),"a"),[IntLiteral(2)]))]))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 303))
        
    def test_304(self):
        """Test Nested ArrayCell"""
        input = """
            func main(){
                b.c.a[2][3] := b.c.a[9+1][3];
            }
""" 
        expect = Program([FuncDecl("main",[],VoidType(),Block([
            Assign(ArrayCell(FieldAccess(FieldAccess(Id("b"),"c"),"a"),[IntLiteral(2),IntLiteral(3)]),ArrayCell(FieldAccess(FieldAccess(Id("b"),"c"),"a"),[BinaryOp('+',IntLiteral(9),IntLiteral(1)),IntLiteral(3)]))
            ])
        )])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 304))
        
    def test_305(self):
        input = """var TaTrungTin = info(a[10][10], b.c.d);"""
        expect = Program([
            VarDecl(
                "TaTrungTin",
                None,
                FuncCall(
                    "info",
                    [ArrayCell(Id("a"),[IntLiteral(10),IntLiteral(10)]),
                     FieldAccess(FieldAccess(Id("b"),"c"),"d")]
                )
            )
        ])
        self.assertTrue(TestAST.checkASTGen(input,str(expect),305))

    def test_306(self):
        input = """const x = 42;"""
        expect = Program([ConstDecl("x", None, IntLiteral(42))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 306))

    def test_307(self):
        input = """var y float = 3.14;"""
        expect = Program([VarDecl("y", FloatType(), FloatLiteral(3.14))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 307))

    def test_308(self):
        input = """const flag = true;"""
        expect = Program([ConstDecl("flag", None, BooleanLiteral(True))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 308))

    def test_309(self):
        input = """const text = "hello";"""
        expect = Program([ConstDecl("text", None, StringLiteral("\"hello\""))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 309))

    def test_310(self):
        input = """const arr = [2]int {1, 2};"""
        expect = Program([ConstDecl("arr", None, ArrayLiteral([IntLiteral(2)], IntType(), [IntLiteral(1), IntLiteral(2)]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 310))

    def test_311(self):
        input = """var p Person = Person{name: "tin", age: 18};"""
        expect = Program([VarDecl("p", Id("Person"), StructLiteral("Person",[("name",StringLiteral("\"tin\"")), ("age",IntLiteral(18))])) ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 311))

    def test_312(self):
        input = """const sum = 10 + 20 * 3;"""
        expect = Program([ConstDecl("sum", None, BinaryOp("+", IntLiteral(10), BinaryOp("*", IntLiteral(20), IntLiteral(3))))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 312))

    def test_313(self):
        input = """func foo() { return 0; }
        """
        expect = Program([FuncDecl("foo", [], VoidType(), Block([Return(IntLiteral(0))]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 313))

    def test_314(self):
        input = """func add(a int, b int) int { return a + b; }
        """
        expect = Program([FuncDecl("add", [ParamDecl("a", IntType()), ParamDecl("b", IntType())], IntType(), Block([Return(BinaryOp("+", Id("a"), Id("b")))]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 314))

    def test_315(self):
        input = """const expr = (1 + 2) * (3 - 4);"""
        expect = Program([ConstDecl("expr", None, BinaryOp("*", BinaryOp("+", IntLiteral(1), IntLiteral(2)), BinaryOp("-", IntLiteral(3), IntLiteral(4))))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 315))

    def test_316(self):
        input = """func call() { foo(1, 2, 3); };"""
        expect = Program([FuncDecl("call", [], VoidType(), Block([FuncCall("foo", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 316))

    def test_317(self):
        input = """var flag boolean = a || b && c;"""
        expect = Program([VarDecl("flag", BoolType(), BinaryOp("||",Id("a"), BinaryOp("&&", Id("b"), Id("c"))))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 317))

    def test_318(self):
        input = """func foo() { 
            if (x > 0) { return x; } else { return -x; }
        };"""
        expect = Program([FuncDecl("foo", [], VoidType(), Block([If(BinaryOp(">", Id("x"), IntLiteral(0)), Block([Return(Id("x"))]), Block([Return(UnaryOp("-", Id("x")))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 318))

    def test_319(self):
        input = """const complex = a[2].b().c[1];"""
        expect = Program([ConstDecl("complex", None, ArrayCell(FieldAccess(MethCall(ArrayCell(Id("a"), [IntLiteral(2)]), "b", []), "c"), [IntLiteral(1)]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 319))

    def test_320(self):
        input = """func loop() { for i := 0; i < 10; i += 1 { print(i); }; };"""
        expect = Program([FuncDecl("loop", [], VoidType(), Block([ForStep(Assign(Id("i"), IntLiteral(0)), BinaryOp("<", Id("i"), IntLiteral(10)), Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))), Block([FuncCall("print", [Id("i")])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 320))

    def test_321(self):
        input = """var test = [1][2]float{1.5, 2.3};"""
        expect = Program([VarDecl("test", None, ArrayLiteral([IntLiteral(1), IntLiteral(2)], FloatType(), [FloatLiteral(1.5), FloatLiteral(2.3)]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 321))

    def test_322(self):
        input = """func assign() { x := 1; x += 2; x *= 3; };"""
        expect = Program([FuncDecl("assign", [], VoidType(), Block([Assign(Id("x"), IntLiteral(1)), Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral(2))), Assign(Id("x"), BinaryOp("*", Id("x"), IntLiteral(3)))]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 322))

    def test_323(self):
        input = """const logic = true && false || !true;"""
        expect = Program([ConstDecl("logic", None, BinaryOp("||", BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False)), UnaryOp("!", BooleanLiteral(True))))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 323))

    def test_324(self):
        input = """func nested() { 
            if (x) { 
                if (y) { return z; } 
            } 
            }
        """
        expect = Program([FuncDecl("nested", [], VoidType(), Block([If(Id("x"), Block([If(Id("y"), Block([Return(Id("z"))]), None)]), None)]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 324))

    def test_325(self):
        input = """func multiReturn() { return c; }
        """
        expect = Program([FuncDecl("multiReturn", [], VoidType(), Block([Return(Id("c"))]))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 325))

    def test_326(self):
        """Test continue statement inside a loop"""
        input = """func loopTest() { 
            for i := 0; i < 10; i += 1 { 
                if (i % 2 == 0) { continue; };
            }; 
        };"""
        expect = Program([
            FuncDecl("loopTest", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(10)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([
                        If(
                            BinaryOp("==", BinaryOp("%", Id("i"), IntLiteral(2)), IntLiteral(0)),
                            Block([Continue()]),
                            None
                        )
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 326))

    def test_327(self):
        """Test break statement inside a loop"""
        input = '''func loopBreak() { 
            for i := 0; i < 10; i += 1 { 
                if (i == 5) { break; };
            }; 
        };'''
        expect = Program([
            FuncDecl("loopBreak", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(10)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([
                        If(
                            BinaryOp("==", Id("i"), IntLiteral(5)),
                            Block([Break()]),
                            None
                        )
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 327))

    def test_328(self):
        """Test unary operation with negative number"""
        input = """const neg = -10;"""
        expect = Program([ConstDecl("neg", None, UnaryOp("-", IntLiteral(10)))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 328))

    def test_329(self):
        """Test unary operation with logical not"""
        input = """const logicNeg = !true;"""
        expect = Program([ConstDecl("logicNeg", None, UnaryOp("!", BooleanLiteral(True)))])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 329))

    def test_330(self):
        """Test for loop without step"""
        input = """func simpleLoop() int { 
            for i := 5; i > 0; i -= 1 { 
                print(i); 
            }; 
            return;
        };"""
        expect = Program([
            FuncDecl("simpleLoop", [], IntType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(5)),
                    BinaryOp(">", Id("i"), IntLiteral(0)),
                    Assign(Id("i"), BinaryOp("-", Id("i"), IntLiteral(1))),
                    Block([
                        FuncCall("print", [Id("i")])
                    ])
                ),
                Return(None)
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 330))

    def test_331(self):
        """Test return expression inside loop"""
        input = """func findNumber() { 
            for i := 0; i < 100; i += 1 { 
                if (i == 42) { return i; };
            }; 
        };"""
        expect = Program([
            FuncDecl("findNumber", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(100)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([
                        If(
                            BinaryOp("==", Id("i"), IntLiteral(42)),
                            Block([Return(Id("i"))]),
                            None
                        )
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 331))

    def test_332(self):
        """Test nested loop with break"""
        input = """func nestedLoop() { 
            for i := 0; i < 10; i += 1 { 
                for j := 0; j < 5; j += 1 { 
                    if (i + j == 7) { break; };
                };
            }; 
        };"""
        expect = Program([
            FuncDecl("nestedLoop", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(10)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([
                        ForStep(
                            Assign(Id("j"), IntLiteral(0)),
                            BinaryOp("<", Id("j"), IntLiteral(5)),
                            Assign(Id("j"), BinaryOp("+", Id("j"), IntLiteral(1))),
                            Block([
                                If(
                                    BinaryOp("==", BinaryOp("+", Id("i"), Id("j")), IntLiteral(7)),
                                    Block([Break()]),
                                    None
                                )
                            ])
                        )
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 332))

    def test_333(self):
        """Test complex nested conditionals"""
        input = """func complexIf() { 
            if (a > 0) { 
                if (b > 0) { 
                    return 1; 
                } else if (c > 0) { 
                    return 2; 
                } else { 
                    return 3; 
                };
            } else { 
                return 4; 
            };
        };"""
        expect = Program([
            FuncDecl("complexIf", [], VoidType(), Block([
                If(
                    BinaryOp(">", Id("a"), IntLiteral(0)),
                    Block([
                        If(
                            BinaryOp(">", Id("b"), IntLiteral(0)),
                            Block([Return(IntLiteral(1))]),
                            If(
                                BinaryOp(">", Id("c"), IntLiteral(0)),
                                Block([Return(IntLiteral(2))]),
                                Block([Return(IntLiteral(3))])
                            )
                        )
                    ]),
                    Block([Return(IntLiteral(4))])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 333))

    def test_334(self):
        """Test complex binary operation"""
        input = """const calc = (a + b) * (c - d) / e;"""
        expect = Program([
            ConstDecl("calc", None, BinaryOp("/",
                BinaryOp("*",
                    BinaryOp("+", Id("a"), Id("b")),
                    BinaryOp("-", Id("c"), Id("d"))
                ),
                Id("e")
            ))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 334))

    def test_335(self):
        """Test array declaration and access"""
        input = """var arr = [5]int{1, 2, 3, 4, 5}; var x = arr[2];"""
        expect = Program([
            VarDecl("arr", None, ArrayLiteral([IntLiteral(5)], IntType(), [
                IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4), IntLiteral(5)
            ])),
            VarDecl("x", None, ArrayCell(Id("arr"), [IntLiteral(2)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 335))

    def test_336(self):
        """Test struct type declaration"""
        input = """type Person struct { name string; age int; };"""
        expect = Program([
            StructType("Person", [
                ("name", StringType()),
                ("age", IntType())
            ], [])
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 336))

    def test_337(self):
        """Test interface type with method prototype"""
        input = """type Animal interface { makeSound(a string) string; };"""
        expect = Program([
            InterfaceType("Animal", [
                Prototype("makeSound", [StringType()], StringType())
            ])
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 337))

    def test_338(self):
        """Test method declaration inside struct"""
        input = """
        type Person struct {
            name string;
        };"""
        expect = Program([
            StructType("Person", [
                ("name", StringType())
            ], [])
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 338))

    def test_339(self):
        """Test calling a method from a struct instance"""
        input = """var p Person; var name = p.getName();"""
        expect = Program([
            VarDecl("p", Id("Person"), None),
            VarDecl("name", None, MethCall(Id("p"), "getName", []))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 339))

    def test_340(self):
        """Test explicit array type declaration"""
        input = """var nums [5]int;"""
        expect = Program([
            VarDecl("nums", ArrayType([IntLiteral(5)], IntType()), None)
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 340))

    def test_341(self):
        """Test accessing a struct field"""
        input = """var p Person; var age = p.age;"""
        expect = Program([
            VarDecl("p", Id("Person"), None),
            VarDecl("age", None, FieldAccess(Id("p"), "age"))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 341))

    def test_342(self):
        """Test for-each loop"""
        input = """
        func printArray(arr [5]int) {
            for i, value := range arr {
                print(value);
            };
        };"""
        expect = Program([
            FuncDecl("printArray", [
                ParamDecl("arr", ArrayType([IntLiteral(5)], IntType()))
            ], VoidType(), Block([
                ForEach(Id("i"), Id("value"), Id("arr"), Block([
                    FuncCall("print", [Id("value")])
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 342))

    def test_343(self):
        """Test bitwise NOT operator"""
        input = """const bitwiseNot = !false;"""
        expect = Program([
            ConstDecl("bitwiseNot", None, UnaryOp("!", BooleanLiteral(False)))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 343))

    def test_344(self):
        """Test nested struct and method call"""
        input = """
        type Company struct{
            name string;
            c Company;
        };
        var d Department;
        var deptId = d.getId();
        """
        expect = Program([
            StructType("Company", [
                ("name", StringType()), ("c", Id("Company"))
            ], []),
            VarDecl("d", Id("Department"), None),
            VarDecl("deptId", None, MethCall(Id("d"), "getId", []))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 344))

    def test_345(self):
        """Test array literal assignment and nested access"""
        input = """var arr = [3]int{10, 20, 30}; var x = arr[1];"""
        expect = Program([
            VarDecl("arr", None, ArrayLiteral([IntLiteral(3)], IntType(), [
                IntLiteral(10), IntLiteral(20), IntLiteral(30)
            ])),
            VarDecl("x", None, ArrayCell(Id("arr"), [IntLiteral(1)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 345))

    def test_346(self):
        """Test built-in functions getInt() and putIntLn()"""
        input = """func main() { var x = getInt(); putIntLn(x); };"""
        expect = Program([
            FuncDecl("main", [], VoidType(), Block([
                VarDecl("x", None, FuncCall("getInt", [])),
                FuncCall("putIntLn", [Id("x")])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 346))

    def test_347(self):
        """Test array iteration using range"""
        input = """
        func iterateArray() { 
            var arr = [5]int {1, 2, 3, 4, 5}; 
            for index, value := range arr { 
                putIntLn(value);
            }; 
        };"""
        expect = Program([
            FuncDecl("iterateArray", [], VoidType(), Block([
                VarDecl("arr", None, ArrayLiteral([IntLiteral(5)], IntType(), [
                    IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4), IntLiteral(5)
                ])),
                ForEach(Id("index"), Id("value"), Id("arr"), Block([
                    FuncCall("putIntLn", [Id("value")])
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 347))

    def test_348(self):
        """Test struct method call with parameters"""
        input = """var p Person; var result = p.setAge(25);"""
        expect = Program([
            VarDecl("p", Id("Person"), None),
            VarDecl("result", None, MethCall(Id("p"), "setAge", [IntLiteral(25)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 348))

    def test_349(self):
        """Test interface implementation with method override"""
        input = """
        type Animal interface { makeSound() string; };
        type Dog struct {};
        func (d Dog) makeSound() string { return "Woof"; };"""
        expect = Program([
            InterfaceType("Animal", [
                Prototype("makeSound", [], StringType())
            ]),
            StructType("Dog", [], []),
            MethodDecl("d", Id("Dog"),
                FuncDecl("makeSound", [], StringType(),
                    Block([Return(StringLiteral("\"Woof\""))])
                )
            )
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 349))

    def test_350(self):
        """Test boolean operations with precedence"""
        input = """var flag boolean = true || false && !true;"""
        expect = Program([
            VarDecl("flag", BoolType(), 
                BinaryOp("||", 
                    BooleanLiteral(True), 
                    BinaryOp("&&", 
                        BooleanLiteral(False), 
                        UnaryOp("!", BooleanLiteral(True))
                    )
                )
            )
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 350))

    def test_351(self):
        """Test nested array indexing and arithmetic operations"""
        input = """var x = arr[2][3] + arr[1][1] * 2;"""
        expect = Program([
            VarDecl("x", None, 
                BinaryOp("+", 
                    ArrayCell(Id("arr"), [IntLiteral(2), IntLiteral(3)]),
                    BinaryOp("*", 
                        ArrayCell(Id("arr"), [IntLiteral(1), IntLiteral(1)]),
                        IntLiteral(2)
                    )
                )
            )
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 351))

    def test_352(self):
        """Test function prototype inside an interface"""
        input = """type Calculator interface { add(a int, b int) int; };"""
        expect = Program([
            InterfaceType("Calculator", [
                Prototype("add", [IntType(), IntType()], IntType())
            ])
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 352))

    def test_353(self):
        """Test assignment expressions inside loops"""
        input = """func loopTest() { for i := 0; i < 10; i += 2 { x := x + i; }; };"""
        expect = Program([
            FuncDecl("loopTest", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(10)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(2))),
                    Block([
                        Assign(Id("x"), BinaryOp("+", Id("x"), Id("i")))
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 353))

    def test_354(self):
        """Test break and continue in a loop"""
        input = """
        func loopControl() {
            for i := 0; i < 5; i += 1 {
                if (i == 2) { continue; };
                if (i == 4) { break; };
                putIntLn(i);
            };
        };"""
        expect = Program([
            FuncDecl("loopControl", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(5)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([
                        If(BinaryOp("==", Id("i"), IntLiteral(2)), Block([Continue()]), None),
                        If(BinaryOp("==", Id("i"), IntLiteral(4)), Block([Break()]), None),
                        FuncCall("putIntLn", [Id("i")])
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 354))

    def test_355(self):
        """Test function returning a struct"""
        input = """func createPerson() Person { return Person{name: "John", age: 25}; };"""
        expect = Program([
            FuncDecl("createPerson", [], Id("Person"), Block([
                Return(StructLiteral("Person", [
                    ("name", StringLiteral("\"John\"")),
                    ("age", IntLiteral(25))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 355))

    def test_356(self):
        """Test variable and constant declarations"""
        input = """var x int = 10; const pi = 3.14;"""
        expect = Program([
            VarDecl("x", IntType(), IntLiteral(10)),
            ConstDecl("pi", None, FloatLiteral(3.14))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 356))

    def test_357(self):
        """Test function definition and return"""
        input = """func getNumber() int { return 42; };"""
        expect = Program([
            FuncDecl("getNumber", [], IntType(), Block([Return(IntLiteral(42))]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 357))

    def test_358(self):
        """Test simple for loop"""
        input = """func loopExample() { for i := 0; i < 5; i += 1 { putInt(i); }; };"""
        expect = Program([
            FuncDecl("loopExample", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(5)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([FuncCall("putInt", [Id("i")])])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 358))

    def test_359(self):
        """Test function call with arguments"""
        input = """var result = add(5, 10);"""
        expect = Program([
            VarDecl("result", None, FuncCall("add", [IntLiteral(5), IntLiteral(10)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 359))

    def test_360(self):
        """Test struct definition and field access"""
        input = """type Person struct { name string; age int; }; var p Person; var n = p.name;"""
        expect = Program([
            StructType("Person", [("name", StringType()), ("age", IntType())], []),
            VarDecl("p", Id("Person"), None),
            VarDecl("n", None, FieldAccess(Id("p"), "name"))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 360))

    def test_361(self):
        """Test array declaration and indexing"""
        input = """var arr [3]int = [3]int{1, 2, 3}; var x = arr[2];"""
        expect = Program([
            VarDecl("arr", ArrayType([IntLiteral(3)], IntType()), ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])),
            VarDecl("x", None, ArrayCell(Id("arr"), [IntLiteral(2)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 361))

    def test_362(self):
        """Test method call on struct instance"""
        input = """var p Person; var age = p.getAge();"""
        expect = Program([
            VarDecl("p", Id("Person"), None),
            VarDecl("age", None, MethCall(Id("p"), "getAge", []))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 362))

    def test_363(self):
        input = """
            type Expr interface {
                Add(a, b int, c float) [2]string;
                Minus() ID;
            }
"""
        expect = Program([InterfaceType("Expr",[Prototype("Add",[IntType(), IntType(), FloatType()],ArrayType([IntLiteral(2)],StringType())),Prototype("Minus",[],Id("ID"))])
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 363))

    def test_364(self):
        input = """
            func main(){
                a += 1;
                a -= 1;
                a *= 1;
                a /= 1;
                a %= 1;
                return 10;
            } 
"""
        expect = Program([FuncDecl("main",[],VoidType(),Block([
            Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),
            Assign(Id("a"),BinaryOp("-", Id("a"), IntLiteral(1))),
            Assign(Id("a"),BinaryOp("*", Id("a"), IntLiteral(1))),
            Assign(Id("a"),BinaryOp("/", Id("a"), IntLiteral(1))),
            Assign(Id("a"),BinaryOp("%", Id("a"), IntLiteral(1))),
            Return(IntLiteral(10))
            ]))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 364))
    def test_365(self):
        """Test unary minus operation"""
        input = """var neg int = -10;"""
        expect = Program([
            VarDecl("neg", IntType(), UnaryOp("-", IntLiteral(10)))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 365))

    def test_366(self):
        """Test constant and variable declarations"""
        input = """const max = 0xA; var min float = 0.5;"""
        expect = Program([
            ConstDecl("max", None, IntLiteral("0xA")),
            VarDecl("min", FloatType(), FloatLiteral(0.5))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 366))

    def test_367(self):
        """Test function with return statement"""
        input = """func square(n int) int { return n * n; };"""
        expect = Program([
            FuncDecl("square", [ParamDecl("n", IntType())], IntType(), Block([
                Return(BinaryOp("*", Id("n"), Id("n")))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 367))

    def test_368(self):
        """Test for loop with decrement"""
        input = """func countdown() { for i := 10; i > 0; i -= 1 { putInt(i); }; };"""
        expect = Program([
            FuncDecl("countdown", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(10)),
                    BinaryOp(">", Id("i"), IntLiteral(0)),
                    Assign(Id("i"), BinaryOp("-", Id("i"), IntLiteral(1))),
                    Block([FuncCall("putInt", [Id("i")])])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 368))

    def test_369(self):
        """Test struct definition with multiple fields"""
        input = """type Rectangle struct { width int; height int; };"""
        expect = Program([
            StructType("Rectangle", [
                ("width", IntType()), 
                ("height", IntType())
            ], [])
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 369))

    def test_370(self):
        """Test struct instantiation and field access"""
        input = """var r Rectangle = Rectangle{width: 5, height: 10}; var area = r.width * r.height;"""
        expect = Program([
            VarDecl("r", Id("Rectangle"), StructLiteral("Rectangle", [
                ("width", IntLiteral(5)), 
                ("height", IntLiteral(10))
            ])),
            VarDecl("area", None, BinaryOp("*", FieldAccess(Id("r"), "width"), FieldAccess(Id("r"), "height")))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 370))

    def test_371(self):
        """Test array declaration and indexing"""
        input = """var data [4]float = [4]float{1.1, 2.2, 3.3, 4.4}; var value = data[2];"""
        expect = Program([
            VarDecl("data", ArrayType([IntLiteral(4)], FloatType()), ArrayLiteral([IntLiteral(4)], FloatType(), [
                FloatLiteral(1.1), FloatLiteral(2.2), FloatLiteral(3.3), FloatLiteral(4.4)
            ])),
            VarDecl("value", None, ArrayCell(Id("data"), [IntLiteral(2)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 371))

    def test_372(self):
        """Test method call on struct"""
        input = """var rect Rectangle; var w = rect.getWidth();"""
        expect = Program([
            VarDecl("rect", Id("Rectangle"), None),
            VarDecl("w", None, MethCall(Id("rect"), "getWidth", []))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 372))

    def test_373(self):
        """Test function call with expressions as arguments"""
        input = """var result = add(2 * 3, 4 + 5);"""
        expect = Program([
            VarDecl("result", None, FuncCall("add", [
                BinaryOp("*", IntLiteral(2), IntLiteral(3)),
                BinaryOp("+", IntLiteral(4), IntLiteral(5))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 373))

    def test_374(self):
        """Test boolean expressions with precedence"""
        input = """var flag boolean = (a && b) || c;"""
        expect = Program([
            VarDecl("flag", BoolType(), BinaryOp("||",
                BinaryOp("&&", Id("a"), Id("b")),
                Id("c")
            ))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 374))

    def test_375(self):
        input = """
            func foo(a,b,c,d [ID][2][c] ID ) int {return a;}
"""
        expect = Program([FuncDecl("foo",[ParamDecl("a",ArrayType([Id("ID"),IntLiteral(2),Id("c")],Id("ID"))),ParamDecl("b",ArrayType([Id("ID"),IntLiteral(2),Id("c")],Id("ID"))),ParamDecl("c",ArrayType([Id("ID"),IntLiteral(2),Id("c")],Id("ID"))),ParamDecl("d",ArrayType([Id("ID"),IntLiteral(2),Id("c")],Id("ID")))],IntType(),Block([Return(Id("a"))]))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 375))

    def test_376(self):
        """Test function call with multiple arguments and expression"""
        input = """var result = add(3 * 2, subtract(10, 5));"""
        expect = Program([
            VarDecl("result", None, FuncCall("add", [
                BinaryOp("*", IntLiteral(3), IntLiteral(2)),
                FuncCall("subtract", [IntLiteral(10), IntLiteral(5)])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 376))

    def test_377(self):
        """Test using struct methods with parameters"""
        input = """type Car struct { model string; year int; };
                func (c Car) displayInfo() string { return c.model + " " + c.year; };"""
        expect = Program([
            StructType("Car", [("model", StringType()), ("year", IntType())], []),
            MethodDecl(
                "c", 
                Id("Car"),
                FuncDecl(
                    "displayInfo", 
                    [], 
                    StringType(),
                    Block([Return(
                            BinaryOp("+", 
                                    BinaryOp("+", 
                                              FieldAccess(Id("c"), "model"),
                                              StringLiteral("\" \"")
                                              ),
                                    FieldAccess(Id("c"), "year")
                                    )
                            )
                           ])
            ))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 377))


    def test_378(self):
        input = """
            func foo(){
                a[2].b.c[2] := 1;
            } 
"""
        expect = Program([FuncDecl("foo",[],VoidType(),Block([Assign(ArrayCell(FieldAccess(FieldAccess(ArrayCell(Id("a"),[IntLiteral(2)]),"b"),"c"),[IntLiteral(2)]),IntLiteral(1))]))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 378))

    def test_379(self):
        """Test method chaining"""
        input = """var result = obj.method1().method2(42).method3();"""
        expect = Program([
            VarDecl("result", None, MethCall(
                MethCall(
                    MethCall(Id("obj"), "method1", []),
                    "method2", [IntLiteral(42)]
                ),
                "method3", []
            ))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 379))

    def test_380(self):
        """Test complex boolean expression with precedence"""
        input = """var isValid = (a && b || c) && (d || e);"""
        expect = Program([
            VarDecl("isValid", None,
                BinaryOp("&&",
                    BinaryOp("||", BinaryOp("&&", Id("a"), Id("b")), Id("c")),
                    BinaryOp("||", Id("d"), Id("e"))
                )
            )
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 380))

    def test_381(self):
        """Test multi-level function calls"""
        input = """var result = outer(inner(5));"""
        expect = Program([
            VarDecl("result", None, FuncCall("outer", [
                FuncCall("inner", [IntLiteral(5)])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 381))

    def test_382(self):
        """Test for-each loop with nested arrays"""
        input = """
        func printNestedArray(arr [2][3]int) { 
            for i, value := range arr { 
                for j, v := range value { putInt(v); } 
            } 
        };"""
        expect = Program([
            FuncDecl("printNestedArray", [ParamDecl("arr", ArrayType([IntLiteral(2), IntLiteral(3)], IntType()))], VoidType(), Block([
                ForEach(Id("i"), Id("value"), Id("arr"), Block([
                    ForEach(Id("j"), Id("v"), Id("value"), Block([
                        FuncCall("putInt", [Id("v")])
                    ]))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 382))

    def test_383(self):
        input = """
            func foo(){
                continue;
                return foo() + 2;
            } 
"""
        expect = Program([FuncDecl("foo",[],VoidType(),Block([Continue(),Return(BinaryOp("+", FuncCall("foo",[]), IntLiteral(2)))]))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 383))

    def test_384(self):
        """Test recursive function with base case"""
        input = """
        func factorial(n int) int {
            if (n <= 1) { return 1; }
            return n * factorial(n - 1);
        };"""
        expect = Program([
            FuncDecl("factorial", [ParamDecl("n", IntType())], IntType(), Block([
                If(BinaryOp("<=", Id("n"), IntLiteral(1)), Block([Return(IntLiteral(1))]), None),
                Return(BinaryOp("*", Id("n"), FuncCall("factorial", [BinaryOp("-", Id("n"), IntLiteral(1))])))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 384))

    def test_385(self):
        """Test nested loops with break and continue"""
        input = """
        func nestedLoop() {
            for i := 0; i < 5; i += 1 {
                if (i == 2) { continue; };
                if (i == 4) { break; };
                putInt(i);
            };
        };"""
        expect = Program([
            FuncDecl("nestedLoop", [], VoidType(), Block([
                ForStep(
                    Assign(Id("i"), IntLiteral(0)),
                    BinaryOp("<", Id("i"), IntLiteral(5)),
                    Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral(1))),
                    Block([
                        If(BinaryOp("==", Id("i"), IntLiteral(2)), Block([Continue()]), None),
                        If(BinaryOp("==", Id("i"), IntLiteral(4)), Block([Break()]), None),
                        FuncCall("putInt", [Id("i")])
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 385))

    def test_386(self):
        """Test method chaining with nested methods"""
        input = """var result = obj.method1().method2(10).method3().method4();"""
        expect = Program([
            VarDecl("result", None, MethCall(
                MethCall(
                    MethCall(
                        MethCall(Id("obj"), "method1", []),
                        "method2", [IntLiteral(10)]
                    ),
                    "method3", []
                ),
                "method4", []
            ))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 386))

    def test_387(self):
        """Test array literal assignment and sum operation"""
        input = """var arr = [3]int{1, 2, 3}; var sum = arr[0] + arr[1] + arr[2];"""
        expect = Program([
            VarDecl("arr", None, ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)])),
            VarDecl("sum", None, BinaryOp("+", BinaryOp("+", ArrayCell(Id("arr"), [IntLiteral(0)]), ArrayCell(Id("arr"), [IntLiteral(1)])), ArrayCell(Id("arr"), [IntLiteral(2)])))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 387))

    def test_388(self):
        """Test field access on nested structs"""
        input = """
        type Department struct { name string; };
        type Company struct { dept Department; };
        var c Company;
        var deptName = c.dept.name;"""
        expect = Program([
            StructType("Department", [("name", StringType())], []),
            StructType("Company", [("dept", Id("Department"))], []),
            VarDecl("c", Id("Company"), None),
            VarDecl("deptName", None, FieldAccess(FieldAccess(Id("c"), "dept"), "name"))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 388))

    def test_389(self):
        input = """
            func main(){
                a.b[2].c := 1;
            } 
"""
        expect = Program([FuncDecl("main",[],VoidType(),Block([Assign(FieldAccess(ArrayCell(FieldAccess(Id("a"),"b"),[IntLiteral(2)]),"c"),IntLiteral(1))]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 389))
        
    def test_390(self):
        """Test complex expression with multiple operations"""
        input = """var result = (a + b) * (c - d) / e;"""
        expect = Program([
            VarDecl("result", None, BinaryOp("/",
                BinaryOp("*", BinaryOp("+", Id("a"), Id("b")), BinaryOp("-", Id("c"), Id("d"))),
                Id("e")
            ))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 390))
    
    def test_391(self):
        """Test variable declaration with simple operation"""
        input = """var y int = 5 + 3;"""
        expect = Program([
            VarDecl("y", IntType(), BinaryOp("+", IntLiteral(5), IntLiteral(3)))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 391))


    def test_392(self):
        """Test a simple function declaration"""
        input = """func add(a float, b, d int) int { return a + b; }
        """
        expect = Program([
            FuncDecl("add", [ParamDecl("a", FloatType()), ParamDecl("b", IntType()), ParamDecl("d", IntType())], 
                    IntType(), Block([Return(BinaryOp("+", Id("a"), Id("b")))]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 392))
    
    def test_393(self):
        input = """
            type a struct{a float;}
            type b interface {foo();} 
            func  (Cat c) foo() [2]int {return;}
"""
        expect = Program([
			StructType("a",[("a",FloatType())],[]),
			InterfaceType("b",[Prototype("foo",[],VoidType())]),
			MethodDecl("Cat",Id("c"),FuncDecl("foo",[],ArrayType([IntLiteral(2)],IntType()),Block([Return(None)])))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 393))

    def test_394(self):
        input = """
            func f(a int, b [1]int) {return;}
"""
        expect = Program([FuncDecl("f",[ParamDecl("a",IntType()),ParamDecl("b",ArrayType([IntLiteral(1)],IntType()))],VoidType(),Block([Return(None)]))
		])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 394))

    def test_395(self):
        """Test return statement with expression"""
        input = """func add(a int, b int) int { return a + b; }
        """
        expect = Program([
            FuncDecl("add", [ParamDecl("a", IntType()), ParamDecl("b", IntType())], 
                    IntType(), Block([Return(BinaryOp("+", Id("a"), Id("b")))]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 395))

    def test_396(self):
        """Test simple array declaration"""
        input = """var arr [3]int;"""
        expect = Program([
            VarDecl("arr", ArrayType([IntLiteral(3)], IntType()), None)
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 396))

    def test_397(self):
        """Test simple array initialization"""
        input = """var arr = [3]int{1, 2, 3};"""
        expect = Program([
            VarDecl("arr", None, 
                    ArrayLiteral([IntLiteral(3)], IntType(), [IntLiteral(1), IntLiteral(2), IntLiteral(3)]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 397))

    def test_398(self):
        """Test simple subtraction in assignment"""
        input = """var difference int = 30 - 15;"""
        expect = Program([
            VarDecl("difference", IntType(), BinaryOp("-", IntLiteral(30), IntLiteral(15)))
        ])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 398))

    def test_399(self):
        input = """func main() { print("Hello, world!"); };"""
        expect = Program([
    FuncDecl(
        "main", 
        [], 
        VoidType(), 
        Block([
            FuncCall("print", [StringLiteral("\"Hello, world!\"")])
        ])
    )
])
        self.assertTrue(TestAST.checkASTGen(input, str(expect), 399))