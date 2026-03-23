module AST

import Syntax;
import ParseTree;

data Program(loc src = |tmp:///|)
  = component(Component c)
  | sensorp(Sensor s)
  | phrases(Program l, Program r)
  ;

data Sensor(loc src = |tmp:///|)
  = sensor(str id, IO out)
  ;

data Component(loc src = |tmp:///|)
  = model(str id, list[IO] ios)
  | ux(str id, list[IO] ios)
  | aggr(str id, list[IO] ios)
  | dup(str id, list[IO] ios)
  | splitter(str id, list[IO] ios)
  | swit(str id, list[IO] ios, Behaviour b)
  | operation(list[Id] idd, list[IO] ios2, Behaviour b)
  | conn(str id, Def def, Exchange e, Transformation t)
  ;

data Def(loc src = |tmp:///|)
  = def(str org_l, str dst_l, str org_r, str dst_r)
  ;

data Exchange(loc src = |tmp:///|)
  = ex(Method m)
  ;

data Method(loc src = |tmp:///|)
  = fifo()
  | lifo() 
  ;

data Transformation(loc src = |tmp:///|)
  = tr(Behaviour b)
  ;

data Behaviour(loc src = |tmp:///|)
  = behav(list[Behaviour] be)
  | loop(Expression e, Behaviour beha)
  | cond(Expression e, Behaviour b, Behaviour s)
  | assign(Id id, Expression e)
  ;

data Expression(loc src = |tmp:///|)
  = dot(Expression ex, str id, list[Expression] esw)
  | funcCall(str id, ExpressionList params)
  | subscrpt(list[Expression] exps)
  | name(str id, Expression e)
  | ids(str id, str ri)
  | id(str id)
  | nat(int integ)
  | fl(real d)
  | comp(Expression l, Expression r)
  | div(Expression l, Expression r)
  | mul(Expression l, Expression r)
  | add(Expression l, Expression r)
  | min(Expression l, Expression r)
  | lt(Expression l, Expression r)
  | lte(Expression l, Expression r)
  | gt(Expression l, Expression r)
  | gte(Expression l, Expression r)
  ;

data ExpressionList(loc src = |tmp:///|)
  = args(list[Expression] expsq)
  ;

data IO(loc src = |tmp:///|)
  = input(IO io)
  | output(IO io)
  | units(str enum, list[Unit] units, Typ datatype, list[Expression] components)
  | units2(str enum, list[Unit] units, Typ datatype)
  | units3(str enum, list[Unit] units)
  ;

data Typ(loc src = |tmp:///|)
  = float()
  | string()
  | dict()
  | lst()
  ;

data Unit(loc src = |tmp:///|)
  = k()
  | k2()
  | c()
  | c2()
  | f()
  | f2()
  | meter()
  | gl()
  | mol_l()
  | mol_s()
  ;

data Id = name_id(str nam);
// data Natural = natur(int x);
// data Decimal = float(real x);

Program load(Tree t) = implode(#Program, t.top); 
