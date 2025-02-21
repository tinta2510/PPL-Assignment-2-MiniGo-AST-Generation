from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):

    # program  : declList EOF ;
    def visitProgram(self, ctx:MiniGoParser.ProgramContext):
        return self.visit(ctx.declList())

    # declList: decl | declList decl;
    def visitDeclList(self, ctx:MiniGoParser.DeclListContext):
        if ctx.declList():
            return self.visit(ctx.declList()) + [self.visit(ctx.decl())]
        else:
            return [self.visit(ctx.decl())]

    # decl: declBody eos ;
    def visitDecl(self, ctx:MiniGoParser.DeclContext):
        return self.visit(ctx.declBody())

    # declBody: varDecl | constDecl | funcDecl | methodDefine | structDecl | interfaceDecl ;
    def visitDeclBody(self, ctx:MiniGoParser.DeclBodyContext):
        if ctx.varDecl():
            return self.visit(ctx.varDecl())
        elif ctx.constDecl():
            return self.visit(ctx.constDecl())
        elif ctx.funcDecl():
            return self.visit(ctx.funcDecl()) 
        elif ctx.methodDefine():
            return self.visit(ctx.methodDefine())
        elif ctx.structDecl():
            return self.visit(ctx.structDecl())
        elif ctx.interfaceDecl():
            return self.visit(ctx.interfaceDecl())

    # varDecl: varDeclWithInit | VAR IDENTIFIER type_ ;
    def visitVarDecl(self, ctx:MiniGoParser.VarDeclContext):
        if ctx.varDeclWithInit():
            return self.visit(ctx.varDeclWithInit())
        else:
            return VarDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.type_()), None)

    # varDeclWithInit: VAR IDENTIFIER type_ initilization | VAR IDENTIFIER initilization;
    def visitVarDeclWithInit(self, ctx:MiniGoParser.VarDeclWithInitContext):
        if ctx.type_():
            return VarDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.type_()), 
                           self.visit(ctx.initilization()))
        else:
            return VarDecl(ctx.IDENTIFIER().getText(), None, 
                           self.visit(ctx.initilization()))

    # type_: IDENTIFIER | STRING | INT | FLOAT | BOOLEAN | arrayType ;
    def visitType_(self, ctx:MiniGoParser.Type_Context):
        if ctx.IDENTIFIER():
            return StructType(ctx.IDENTIFIER().getText(), [], []) #???
        elif ctx.STRING():
            return StringType()
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.arrayType():
            return self.visit(ctx.arrayType())
        
    # initilization: ASSIGN expression ;
    def visitInitilization(self, ctx:MiniGoParser.InitilizationContext):
        return self.visit(ctx.expression())

    # constDecl: CONST IDENTIFIER initilization ;
    def visitConstDecl(self, ctx:MiniGoParser.ConstDeclContext):
        return ConstDecl(ctx.IDENTIFIER().getText(), None, self.visit(ctx.initilization()))

    # funcDecl: FUNC IDENTIFIER signature block ;
    def visitFuncDecl(self, ctx:MiniGoParser.FuncDeclContext):
        params, returnType = self.visit(ctx.signature())
        return FuncDecl(
            ctx.IDENTIFIER().getText(), 
            params, 
            returnType,
            self.visit(ctx.block())
        )

    # signature: parameterList returnType | parameterList ;
    def visitSignature(self, ctx:MiniGoParser.SignatureContext):
        if ctx.returnType():
            return self.visit(ctx.parameterList()), self.visit(ctx.returnType())
        else:
            return self.visit(ctx.parameterList()), VoidType()

    # parameterList: L_PAREN parameterDeclList R_PAREN ;
    def visitParameterList(self, ctx:MiniGoParser.ParameterListContext):
        return self.visit(ctx.parameterDeclList())

    # returnType: type_;
    def visitReturnType(self, ctx:MiniGoParser.ReturnTypeContext):
        return self.visit(ctx.type_())

    # parameterDeclList: nonNullParameterDeclList | ;
    def visitParameterDeclList(self, ctx:MiniGoParser.ParameterDeclListContext):
        if ctx.nonNullParameterDeclList():
            return self.visit(ctx.nonNullParameterDeclList())
        else:
            return []

    # nonNullParameterDeclList: parameterDecl COMMA nonNullParameterDeclList | typedParameterDecl ;
    def visitNonNullParameterDeclList(self, ctx:MiniGoParser.NonNullParameterDeclListContext):
        if ctx.parameterDecl():
            return [self.visit(ctx.parameterDecl())] + self.visit(ctx.nonNullParameterDeclList())
        else:
            return [self.visit(ctx.typedParameterDecl())]

    # parameterDecl: typedParameterDecl | IDENTIFIER ;
    def visitParameterDecl(self, ctx:MiniGoParser.ParameterDeclContext):
        if ctx.typedParameterDecl():
            return self.visit(ctx.typedParameterDecl())
        else:
            return VarDecl(ctx.IDENTIFIER().getText(), None, None) #???

    # typedParameterDecl: IDENTIFIER type_ ;
    def visitTypedParameterDecl(self, ctx:MiniGoParser.TypedParameterDeclContext):
        return VarDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.type_()), None)

    # block: L_BRACE stmtList R_BRACE ; 
    def visitBlock(self, ctx:MiniGoParser.BlockContext):
        return Block(self.visit(ctx.stmtList())) #???
    
    # stmtList: nonNullStmtList | ;
    def visitStmtList(self, ctx:MiniGoParser.StmtListContext):
        if ctx.nonNullStmtList():
            return self.visit(ctx.nonNullStmtList())
        else:
            return []

    # nonNullStmtList: stmt | nonNullStmtList stmt ;
    def visitNonNullStmtList(self, ctx:MiniGoParser.NonNullStmtListContext):
        if ctx.nonNullStmtList():
            return self.visit(ctx.nonNullStmtList()) + [self.visit(ctx.stmt())]
        else:
            return [self.visit(ctx.stmt())]

    # methodDefine: FUNC receiver IDENTIFIER signature block ;
    def visitMethodDefine(self, ctx:MiniGoParser.MethodDefineContext):
        params, returnType = self.visit(ctx.signature())
        receiverName, receiverType = self.visit(ctx.receiver())
        return MethodDecl(
            receiverName, # receiver
            receiverType, # recType
            FuncDecl(
                ctx.IDENTIFIER().getText(), 
                params, 
                returnType,
                self.visit(ctx.block())
            )
        )

    # receiver: L_PAREN IDENTIFIER receiverType R_PAREN ;
    def visitReceiver(self, ctx:MiniGoParser.ReceiverContext):
        '''Result: (receiverName, receiverType)'''
        return ctx.IDENTIFIER().getText(), self.visit(ctx.receiverType())

    # receiverType: IDENTIFIER ;
    def visitReceiverType(self, ctx:MiniGoParser.ReceiverTypeContext):
        return StructType(ctx.IDENTIFIER, [], []) #???

    # structDecl: TYPE IDENTIFIER STRUCT structBody ;
    def visitStructDecl(self, ctx:MiniGoParser.StructDeclContext):
        return StructType(
            ctx.IDENTIFIER().getText(), 
            self.visit(ctx.structBody()), 
            []
        )

    # structBody: L_BRACE fieldDeclList R_BRACE ;
    def visitStructBody(self, ctx:MiniGoParser.StructBodyContext):
        return self.visit(ctx.fieldDeclList())

    # fieldDeclList: nonNullFieldDeclList | ;
    def visitFieldDeclList(self, ctx:MiniGoParser.FieldDeclListContext):
        if ctx.nonNullFieldDeclList():
            return self.visit(ctx.nonNullFieldDeclList())
        else:
            return []

    # nonNullFieldDeclList: fieldDecl | nonNullFieldDeclList fieldDecl ;
    def visitNonNullFieldDeclList(self, ctx:MiniGoParser.NonNullFieldDeclListContext):
        if ctx.nonNullFieldDeclList():
            return self.visit(ctx.nonNullFieldDeclList()) + [self.visit(ctx.fieldDecl())]
        else:
            return [self.visit(ctx.fieldDecl())]

    # fieldDecl: IDENTIFIER type_ eos ;
    def visitFieldDecl(self, ctx:MiniGoParser.FieldDeclContext):
        return (ctx.IDENTIFIER().getText(), self.visit(ctx.type_()))

    # interfaceDecl: TYPE IDENTIFIER INTERFACE interfaceBody;
    def visitInterfaceDecl(self, ctx:MiniGoParser.InterfaceDeclContext):
        return InterfaceType(ctx.IDENTIFIER().getText(), self.visit(ctx.interfaceBody()))

    # interfaceBody: L_BRACE methodDeclList R_BRACE ;
    def visitInterfaceBody(self, ctx:MiniGoParser.InterfaceBodyContext):
        return self.visit(ctx.methodDeclList())

    # methodDeclList: nonNullMethodDeclList | ;
    def visitMethodDeclList(self, ctx:MiniGoParser.MethodDeclListContext):
        if ctx.nonNullMethodDeclList():
            return self.visit(ctx.nonNullMethodDeclList())
        else:
            return []

    # nonNullMethodDeclList: methodDecl | nonNullMethodDeclList methodDecl ;
    def visitNonNullMethodDeclList(self, ctx:MiniGoParser.NonNullMethodDeclListContext):
        if ctx.nonNullMethodDeclList():
            return self.visit(ctx.nonNullMethodDeclList()) + [self.visit(ctx.methodDecl())]
        else:
            return [self.visit(ctx.methodDecl())]

    # methodDecl: IDENTIFIER signature eos;
    def visitMethodDecl(self, ctx:MiniGoParser.MethodDeclContext):
        params, returnType = self.visit(ctx.signature())
        return Prototype(ctx.IDENTIFIER().getText(), params, returnType)

    # Visit a parse tree produced by MiniGoParser#stmt.
    def visitStmt(self, ctx:MiniGoParser.StmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#stmtBody.
    def visitStmtBody(self, ctx:MiniGoParser.StmtBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#assignStmt.
    def visitAssignStmt(self, ctx:MiniGoParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#lhs.
    def visitLhs(self, ctx:MiniGoParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#assignOp.
    def visitAssignOp(self, ctx:MiniGoParser.AssignOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#rhs.
    def visitRhs(self, ctx:MiniGoParser.RhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#ifStmt.
    def visitIfStmt(self, ctx:MiniGoParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#ifCondition.
    def visitIfCondition(self, ctx:MiniGoParser.IfConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elseStmt.
    def visitElseStmt(self, ctx:MiniGoParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forStmt.
    def visitForStmt(self, ctx:MiniGoParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forClause.
    def visitForClause(self, ctx:MiniGoParser.ForClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forCondition.
    def visitForCondition(self, ctx:MiniGoParser.ForConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forLoop.
    def visitForLoop(self, ctx:MiniGoParser.ForLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forLoopInit.
    def visitForLoopInit(self, ctx:MiniGoParser.ForLoopInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forLoopUpdate.
    def visitForLoopUpdate(self, ctx:MiniGoParser.ForLoopUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forRange.
    def visitForRange(self, ctx:MiniGoParser.ForRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forIndex.
    def visitForIndex(self, ctx:MiniGoParser.ForIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forValue.
    def visitForValue(self, ctx:MiniGoParser.ForValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#rangeExpr.
    def visitRangeExpr(self, ctx:MiniGoParser.RangeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#breakStmt.
    def visitBreakStmt(self, ctx:MiniGoParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#continueStmt.
    def visitContinueStmt(self, ctx:MiniGoParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#callStmt.
    def visitCallStmt(self, ctx:MiniGoParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#returnStmt.
    def visitReturnStmt(self, ctx:MiniGoParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#literal.
    def visitLiteral(self, ctx:MiniGoParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#basicLit.
    def visitBasicLit(self, ctx:MiniGoParser.BasicLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#integerLit.
    def visitIntegerLit(self, ctx:MiniGoParser.IntegerLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#compositeLit.
    def visitCompositeLit(self, ctx:MiniGoParser.CompositeLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayLit.
    def visitArrayLit(self, ctx:MiniGoParser.ArrayLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayType.
    def visitArrayType(self, ctx:MiniGoParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayTypeIndex.
    def visitArrayTypeIndex(self, ctx:MiniGoParser.ArrayTypeIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayElementType.
    def visitArrayElementType(self, ctx:MiniGoParser.ArrayElementTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayValue.
    def visitArrayValue(self, ctx:MiniGoParser.ArrayValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayList.
    def visitArrayList(self, ctx:MiniGoParser.ArrayListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nonNullArrayList.
    def visitNonNullArrayList(self, ctx:MiniGoParser.NonNullArrayListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayElement.
    def visitArrayElement(self, ctx:MiniGoParser.ArrayElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structLit.
    def visitStructLit(self, ctx:MiniGoParser.StructLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structType.
    def visitStructType(self, ctx:MiniGoParser.StructTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structValue.
    def visitStructValue(self, ctx:MiniGoParser.StructValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#keyedElementList.
    def visitKeyedElementList(self, ctx:MiniGoParser.KeyedElementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nonNullKeyedElementList.
    def visitNonNullKeyedElementList(self, ctx:MiniGoParser.NonNullKeyedElementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#keyedElement.
    def visitKeyedElement(self, ctx:MiniGoParser.KeyedElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#key.
    def visitKey(self, ctx:MiniGoParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#element.
    def visitElement(self, ctx:MiniGoParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expression.
    def visitExpression(self, ctx:MiniGoParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#logAndExpr.
    def visitLogAndExpr(self, ctx:MiniGoParser.LogAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#relExpr.
    def visitRelExpr(self, ctx:MiniGoParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#addExpr.
    def visitAddExpr(self, ctx:MiniGoParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#mulExpr.
    def visitMulExpr(self, ctx:MiniGoParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#unaryExpr.
    def visitUnaryExpr(self, ctx:MiniGoParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:MiniGoParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#fieldAccess.
    def visitFieldAccess(self, ctx:MiniGoParser.FieldAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrayAccess.
    def visitArrayAccess(self, ctx:MiniGoParser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arguments.
    def visitArguments(self, ctx:MiniGoParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#argumentList.
    def visitArgumentList(self, ctx:MiniGoParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nonNullArgumentList.
    def visitNonNullArgumentList(self, ctx:MiniGoParser.NonNullArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#operand.
    def visitOperand(self, ctx:MiniGoParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#eos.
    def visitEos(self, ctx:MiniGoParser.EosContext):
        return self.visitChildren(ctx)